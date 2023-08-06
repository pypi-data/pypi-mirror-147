from based.converters.bigint import BigIntBaseConverter

__ALL__ = ['fuckbase']

# Custom encoding I made for my own devious purposes.
#alphabet = ''.join(sorted(string.ascii_uppercase+string.ascii_lowercase+string.digits+'`!@#$%^&*()-=~_+{}[]:";\',./<>?\\|', key=ord))
fuckbase = BigIntBaseConverter('fuckbase', '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
