import string
from typing import List
from based.abcs import IBaseConverter

from based.converters.bigint import BigIntBaseConverter

base85       = BigIntBaseConverter('base85', string.ascii_uppercase+string.ascii_lowercase+string.digits+'!#$%&()*+-;<=>?@^_`{|}~')  # RFC1924

ALL: List[IBaseConverter] = [
    base85,
]