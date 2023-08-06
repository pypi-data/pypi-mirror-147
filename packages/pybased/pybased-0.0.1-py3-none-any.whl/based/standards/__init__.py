from typing import List

from based.abcs import IBaseConverter

__ALL__ = [
    'base32',
    'base32hex',
    'crockford32',
    'zbase32', 

    'base62', 

    'base64',
    'base64b64',
    'base64bash',
    'base64bcrypt',
    'base64hqx',
    'base64url',
    'base64uu',
    'base64xx',
    
    'base85',

    'fuckbase',
]

from .base32 import ALL as _ALL_B32
from .base32 import base32, base32hex, zbase32
from .base62 import ALL as _ALL_B62
from .base62 import base62
from .base64 import ALL as _ALL_B64
from .base64 import (base64, base64b64, base64bash, base64bcrypt, base64hqx,
                     base64url, base64uu, base64xx)
from .base85 import ALL as _ALL_B85
from .base85 import base85
from .fuckbase import fuckbase

ALL: List[IBaseConverter] = _ALL_B32 + _ALL_B62 + _ALL_B64 + _ALL_B85 + [fuckbase]
