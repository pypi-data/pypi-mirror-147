from typing import Literal, Union

from based.debug import _debugprint
from based.exceptions import InvalidArgumentError


class BitView:
    def __init__(self, data: bytes) -> None:
        self.data = bytearray(data)
        self.last_written: int = -1
        self.size: int = len(data) * 8

    def __getitem__(self, s: Union[int, slice]) -> Union[int, bool]:
        if isinstance(s, slice):
            return self._get_slice(s)
        elif isinstance(s, int):
            return self.get(s)
        else:
            raise InvalidArgumentError('s', s)
                
    def get(self, idx: int) -> int:
        assert idx >= 0
        assert idx < self.size
        byte, bit = divmod(idx, 8)
        return (self.data[byte] & (1 << bit)) >> bit

    def _get_slice(self, s: slice) -> int:
        #print(repr(s))
        start = s.start
        stop = s.stop
        step = s.step
        assert start < stop
        assert start < self.size, f'{start} < {self.size}'
        if stop is None:
            stop = self.size
        if step is None:
            step = 1
        #assert stop <= self.size, f'{stop} <= {self.size}'
        _debugprint(f'BitView._get_slice(slice({start}, {stop}, {step}))')
        o = 0
        for i, idx in enumerate(range(start, stop, step)):
            if idx >= self.size:
                break
            byte, bit = divmod(idx, 8)
            _debugprint(i, idx, byte, bit)
            o |= ((self.data[byte] & (1 << bit)) >> bit) << i
        return o

    def __setitem__(self, s: Union[int, slice], v: int) -> None:
        if isinstance(s, int):
            self.set(s, v)
        elif isinstance(s, slice):
            self._set_slice(s, v)

    def set(self, idx: int, val: Literal[0, 1]) -> None:
        assert idx >= 0
        assert idx < self.size
        assert val in (0, 1)
        byte, bit = divmod(idx, 8)
        mask = 1 << bit
        if val == 1:
            self.data[byte] |= mask
        elif val == 0:
            self.data[byte] &= ~mask
        self.last_written = max(self.last_written, byte)

    def _set_slice(self, s: slice, val: int) -> None:
        #print(repr(s))
        start = s.start
        stop = s.stop
        step = s.step
        assert start < stop
        assert start < self.size, f'{start} < {self.size}'
        if stop is None:
            stop = self.size - 1
        if step is None:
            step = 1
        #assert stop <= self.size, f'{stop} <= {self.size}'
        for i, idx in enumerate(range(start, stop, step)):
            byte, bit = divmod(idx, 8)
            srcmask = (1 << i)
            destmask = (1 << bit)
            if (val & srcmask) == srcmask:
                self.data[byte] |= destmask
            else:
                self.data[byte] &= ~destmask
            self.last_written = max(self.last_written, byte)

    def as_bytes(self) -> bytes:
        return bytes(self.data[0:self.last_written])
