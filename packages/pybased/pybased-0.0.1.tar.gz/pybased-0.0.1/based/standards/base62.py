import string
from typing import List

from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter

__ALL__=['base62']

base62 = BigIntBaseConverter('base62', string.ascii_uppercase + string.ascii_lowercase + string.digits)

ALL: List[IBaseConverter] = [
    base62,
]
