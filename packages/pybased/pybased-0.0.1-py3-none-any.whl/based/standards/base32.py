import string
from typing import List

from based.abcs import IBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter

__ALL__ = [
    'base32',
    'base32hex',
    'crockford32',
    'zbase32',
]

base32      = SlidingWindowBaseConverter('base32',      string.ascii_uppercase + '234567')  # rfc4648
base32hex   = SlidingWindowBaseConverter('base32hex',   string.digits+string.ascii_uppercase[:22])  # rfc2938
crockford32 = SlidingWindowBaseConverter('crockford32', '0123456789ABCDEFGHJKMNPQRSTVWXYZ')
zbase32     = SlidingWindowBaseConverter('zbase32',     'ybndrfg8ejkmcpqxot1uwisza345h769')

ALL: List[IBaseConverter] = [
    base32,
    base32hex,
    crockford32,
    zbase32,
]
