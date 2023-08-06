import math
from typing import Literal

from based.abcs import IBaseConverter

__ALL__ = ['BigIntBaseConverter']

class BigIntBaseConverter(IBaseConverter):
    def __init__(self, id: str, alphabet: str, endianness: Literal['big', 'little']='big') -> None:
        super().__init__(id, alphabet)
        self.endianness: Literal['big', 'little'] = endianness

    def encode_bytes(self, data: bytes) -> str:
        return self.encode_int(int.from_bytes(data, byteorder=self.endianness))

    def encode_int(self, integer: int) -> str:
        if integer == 0:
            return self.zero_char
        ret = ''
        while integer != 0:
            ret = self.alphabet[integer % self.length] + ret
            integer //= self.length
        return ret

    def decode_int(self, input: str) -> int:
        ret: int = 0
        for i, c in enumerate(input[::-1]):
            ret += (self.length ** i) * self.c2i[c]
        return ret

    def decode_bytes(self, input: str) -> bytes:
        i: int = self.decode_int(input)
        return i.to_bytes(math.ceil(i.bit_length()/8.), self.endianness)
