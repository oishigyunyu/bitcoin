from logging import getLogger
from typing import IO, ByteString, Callable

from helper import (
    encode_variant,
    int_to_little_endian,
    little_endian_to_int,
    read_variant,
)
from op import OP_CODE_FUNCTIONS, OP_CODE_NAMES

LOGGER = getLogger(__name__)


class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    @classmethod
    def parse(cls, s: IO) -> "Script":  # type: ignore
        length: int = read_variant(s)
        cmds: list[int] = []
        count: int = 0
        while count < length:
            current = s.read(1)
            count += 1
            current_byte = current[0]

            if current_byte >= 1 and current_byte <= 75:
                n: int = current_byte
                cmds.append(s.read(n))
                count += n
            elif current_byte == 76:
                data_length: int = little_endian_to_int(s.read(1))
                cmds.append(s.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length_: int = little_endian_to_int(s.read(1))
                cmds.append(s.read(data_length_))
                count += data_length_ + 2
            else:
                op_code: int = current_byte
                cmds.append(op_code)
            if count != length:
                raise SyntaxError("parsing script failed")
            return cls(cmds)

    def raw_serialize(self) -> ByteString:
        result = b""
        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError("too long an cmd")
                result += cmd
        return result

    def serialize(self) -> ByteString:
        result: ByteString = self.raw_serialize()
        total: int = len(result)
        return encode_variant(total) + result  # type: ignore

    def __add__(self, other: "Script") -> "Script":
        return Script(self.cmds + other.cmds)

    def evaluate(self, z: ByteString) -> bool:
        cmds = self.cmds[:]
        stack: list = []
        altstack: list = []
        while len(cmds) > 0:
            cmd = cmds.pop()
            if type(cmd) == int:
                operation: Callable = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):
                    if not operation(stack, cmds):
                        LOGGER.info("bad op: {}".format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):
                    if not operation(stack, altstack):
                        LOGGER.info("bad op: {}".format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, 2):
                        LOGGER.info("bad op: {}".format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                stack.append(cmd)
        if len(stack) == 0:
            return False
        if stack.pop() == b"":
            return False
        return True


assert Script.__add__.__annotations__ == {"other": "Script"}
