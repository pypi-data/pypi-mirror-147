import math

from based.abcs import IBaseConverter
from based.bitview import BitView
from based.debug import _debugprint

__ALL__ = ['SlidingWindowBaseConverter']

class SlidingWindowBaseConverter(IBaseConverter):
    def __init__(self, id: str, alphabet: str) -> None:
        super().__init__(id, alphabet)
        #print(self.length)
        bits_per_char: float = (self.length-1).bit_length()
        #if not bits_per_char.is_integer():
        #    raise NotWholeNumberError(self.id, 'bits_per_char', bits_per_char)
        self.bits_per_char: int = math.ceil(bits_per_char)
        chars_per_byte: float = 4 * self.bits_per_char / 8
        #if not chars_per_byte.is_integer():
        #    raise NotWholeNumberError(self.id, 'chars_per_byte', chars_per_byte)
        self.chars_per_byte: int = math.ceil(chars_per_byte)

    def decode_bytes(self, input: str) -> bytes:
        data = bytes(math.ceil(len(input)*self.bits_per_char/8))
        bv = BitView(data)
        for i, c in enumerate(input):
            #_debugprint(i, c)
            s = i*self.bits_per_char
            bv[s:s+self.bits_per_char] = self.decode_int(c)
        o = bv.as_bytes()
        _debugprint(repr(o))
        return o
    
    def decode_int(self, input: str) -> int:
        ret: int = 0
        for i, c in enumerate(input[::-1]):
            ret += (self.length ** i) * self.c2i[c]
        return ret


    def encode_bytes(self, data: bytes) -> str:
        o: str = ''
        bv = BitView(data)
        for i in range(0, bv.size, self.bits_per_char):
            _debugprint(f'{bv[i:i+self.bits_per_char]:0{self.bits_per_char}b}')
            o += self.encode_int(bv[i:i+self.bits_per_char])
        
        #for b in data:
        #    o += self.encode_int(b).rjust(self.chars_per_byte)

        _debugprint(f'{data!r} -> {o!r}')
        return o

    def encode_int(self, integer: int) -> str:
        if integer == 0:
            return self.zero_char
        ret = ''
        while integer != 0:
            ret = self.alphabet[integer % self.length] + ret
            integer //= self.length
        return ret
