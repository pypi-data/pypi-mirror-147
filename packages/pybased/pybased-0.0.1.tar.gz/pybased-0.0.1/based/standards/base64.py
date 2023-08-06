import string
from typing import List

from based.abcs import IBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter

__ALL__ = [
    'base64',
    'base64b64',
    'base64bash',
    'base64bcrypt',
    'base64hqx',
    'base64url',
    'base64uu',
    'base64xx',
]

base64       = SlidingWindowBaseConverter('base64', string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/')  # rfc4648
base64b64    = SlidingWindowBaseConverter('base64b64', './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
base64bash   = SlidingWindowBaseConverter('base64bash', '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@_')
base64bcrypt = SlidingWindowBaseConverter('base64bcrypt', './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
base64hqx    = SlidingWindowBaseConverter('base64hqx', '!"#$%&\'()*+,-012345689@ABCDEFGHIJKLMNPQRSTUVXYZ[`abcdefhijklmpqr')
base64url    = SlidingWindowBaseConverter('base64url', string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_')  # rfc4648
base64uu     = SlidingWindowBaseConverter('base64uu', ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_')
base64xx     = SlidingWindowBaseConverter('base64xx', '+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

ALL: List[IBaseConverter] = [
    base64,
    base64b64,
    base64bash,
    base64bcrypt,
    base64hqx,
    base64url,
    base64uu,
    base64xx,
]
