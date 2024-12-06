# Copyright 2024 Giacomo Ferretti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import pathlib
import shutil
import sys
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, TypedDict

import click

from .. import __version__ as deobfuscator_version
from .. import constants, paranoid
from ..encoding import decode_unicode_chunks, encode_smali_string

logger = logging.getLogger(__name__)

REMOVED_COMMENT = (
    f"    # Removed with https://github.com/giacomoferretti/paranoid-deobfuscator - v{deobfuscator_version}"
)


class ParanoidSmaliDeobfuscator:
    class ParanoidSmaliDeobfuscatorError(Exception):
        def __init__(self, message: str, extra: Dict[str, Any] = {}):
            super().__init__(message)

            self.extra = extra

        def __str__(self):
            if not self.extra:
                return super().__str__()

            return f"{super().__str__()}\n{json.dumps(self.extra, indent=4)}"

    class State(TypedDict):
        class_name: str
        registers: Dict[str, paranoid.register.SmaliRegister]
        last_deobfuscated_string: str | None

    def __init__(
        self,
        filepath: pathlib.Path | str,
        target_method: paranoid.SmaliMethod,
        obfuscated_chunks: List[str],
        # edit_in_place: bool = True,
    ):
        # if edit_in_place:
        #     self.file = open(filepath, "r+")
        # else:
        #     self.file = open(filepath, "r")
        self.file = open(filepath, "r")
        self.tmp_file = NamedTemporaryFile(mode="wt", dir=pathlib.Path(filepath).parent.absolute(), delete=False)

        self.target_method = target_method
        self.obfuscated_chunks = obfuscated_chunks
        self._reset_state()

    def _reset_state(self, key_to_reset: str | None = None):
        default_state: ParanoidSmaliDeobfuscator.State = {
            "class_name": "",
            "registers": {},
            "last_deobfuscated_string": None,
        }

        if key_to_reset:
            self.state[key_to_reset] = default_state[key_to_reset]
        else:
            self.state = default_state

    @staticmethod
    def get_fully_qualified_class_name(line: str) -> str:
        if not line.startswith(".class"):
            raise Exception("Line does not start with .class")

        return line.split()[-1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def process(self, line: str) -> str | None:
        # Get fully qualified class name
        if line.startswith(".class"):
            self.state["class_name"] = self.get_fully_qualified_class_name(line)
            return

        # Update registers
        if line.startswith("const"):
            try:
                instr = paranoid.instructions.SmaliInstrConst.parse(line)
            except ValueError:
                return

            self.state["registers"][instr.register] = paranoid.register.SmaliRegisterConst(instr.value)
            return

        # Search for calls to the target method
        if line.startswith("invoke-static"):
            try:
                instr = paranoid.instructions.SmaliInstrInvokeStatic.parse(line)
            except ValueError:
                return

            method_name, method_arguments, method_return_type = paranoid.SmaliMethod.parse_method_signature(
                instr.method
            )

            # Check if the target method is the one we are looking for
            if not (
                self.target_method
                and instr.class_name == self.target_method.class_name
                and method_name == self.target_method.method
                and method_arguments == self.target_method.arguments
                and method_return_type == self.target_method.return_type
                and len(instr.registers) == 2
            ):
                return

            first_register = instr.registers[0]

            # TODO: parameters are not supported
            if first_register.startswith("p"):
                raise ParanoidSmaliDeobfuscator.ParanoidSmaliDeobfuscatorError(
                    "Parameters are not supported",
                    extra={
                        "registers": self.state["registers"],
                        "register": first_register,
                        "line": line,
                    },
                )

            # Get the value of the register
            register_value = self.state["registers"].get(first_register)
            if not register_value:
                raise ParanoidSmaliDeobfuscator.ParanoidSmaliDeobfuscatorError(
                    "Register not found",
                    extra={
                        "registers": self.state["registers"],
                        "register": first_register,
                        "line": line,
                    },
                )

            # Check if the register is a constant
            if not isinstance(register_value, paranoid.register.SmaliRegisterConst):
                raise ParanoidSmaliDeobfuscator.ParanoidSmaliDeobfuscatorError(
                    "Register is not a constant",
                    extra={
                        "registers": self.state["registers"],
                        "register": first_register,
                        "line": line,
                    },
                )

            # Deobfuscate the string
            deobfuscated_string = paranoid.deobfuscate_string(register_value.value, self.obfuscated_chunks, True)
            self.state["last_deobfuscated_string"] = deobfuscated_string

            return REMOVED_COMMENT

        # Move result object
        if line.startswith("move-result-object"):
            try:
                instr = paranoid.instructions.SmaliInstrMoveResult.parse(line)
            except ValueError:
                return

            if self.state["last_deobfuscated_string"] is not None:
                new_line = f'    const-string {instr.register}, "{encode_smali_string(self.state["last_deobfuscated_string"])}"'
                self.state["last_deobfuscated_string"] = None
                return new_line

            return

        return

    def update(self, _line: str):
        line = _line.strip()

        # Skip empty lines
        if not line:
            self.tmp_file.write(_line)
            return

        # Process the line
        updated_line = self.process(line)
        if updated_line is not None:
            self.tmp_file.write(updated_line + "\n")
            return

        # Add the line to the temporary file
        self.tmp_file.write(_line)


@click.command(name="deobfuscate", help="Deobfuscate a paranoid obfuscated APK smali files")
@click.argument("target", type=click.Path(exists=True, file_okay=False))
def cli(target: str):
    target_directory = pathlib.Path(target)

    # First pass: find the get string method and the obfuscated string array
    potential_get_string_methods = []
    potential_obfuscated_string_arrays = []
    for smali_file in target_directory.rglob("*.smali"):
        with open(smali_file, "r") as f:
            smali_parser = paranoid.ParanoidSmaliParser(filename=str(smali_file))

            for line in f:
                smali_parser.update(line)

            # Add potential get string methods
            for method, data in smali_parser.methods.items():
                if (
                    data["consts"] == constants.PARANOID_GET_STRING_CONST_SIGNATURE
                    and method.arguments == constants.PARANOID_GET_STRING_ARGUMENTS
                    and method.return_type == constants.PARANOID_GET_STRING_RETURN_TYPE
                ):
                    potential_get_string_methods.append((method, data["sget_objects"]))

            # Add potential obfuscated string arrays
            for field, data in smali_parser.fields.items():
                if field.type == "[Ljava/lang/String;":
                    potential_obfuscated_string_arrays.append((field, data["value"]))

    # Check if only one method is found
    if len(potential_get_string_methods) != 1:
        logger.error("Found more than one potential get string method")
        logger.error("This is not supported yet")
        sys.exit(1)

    get_string_method, get_string_fields = potential_get_string_methods[0]
    get_string_field: paranoid.SmaliField = get_string_fields[0]

    # Check if only one field is found
    if len(get_string_fields) != 1:
        logger.error("Found more than one potential obfuscated string array")
        logger.error("This is not supported yet")
        sys.exit(1)

    # Extract the string chunks
    chunks = []
    for field, value in potential_obfuscated_string_arrays:
        if field.class_name == get_string_field.class_name and field.name == get_string_field.name:
            chunks = value

    # Check if the chunks are found
    if not chunks:
        logger.error("No chunks found")
        return

    logger.debug(f"Method: {get_string_method}")
    logger.debug(f"Field: {get_string_field}")
    logger.debug("Chunks:")
    logger.debug(chunks)

    # Decode the chunks
    chunks = decode_unicode_chunks(chunks)

    # Second pass: deobfuscate file
    for smali_file in target_directory.rglob("*.smali"):
        with ParanoidSmaliDeobfuscator(smali_file, get_string_method, chunks) as deobfuscator:
            for line in deobfuscator.file:
                deobfuscator.update(line)

        # Replace the original file with the temporary one
        shutil.move(deobfuscator.tmp_file.name, smali_file)
