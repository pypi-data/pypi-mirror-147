
from abc import ABC, abstractmethod
from typing import Dict

from frozendict import frozendict


class IBaseConverter(ABC):
    def __init__(self, id: str, alphabet: str) -> None:
        super().__init__()
        self.id: str = id
        self.alphabet: str = alphabet
        self.length: int = len(alphabet)
        self.zero_char: str = alphabet[0]
        self.c2i: Dict[str, int] = frozendict((c, i) for i, c in enumerate(self.alphabet))

    @abstractmethod
    def decode_bytes(self, input: str) -> bytes:
        pass
    @abstractmethod
    def decode_int(self, input: str) -> int:
        pass
    @abstractmethod
    def encode_bytes(self, data: bytes) -> str:
        pass
    @abstractmethod
    def encode_int(self, integer: int) -> str:
        pass
