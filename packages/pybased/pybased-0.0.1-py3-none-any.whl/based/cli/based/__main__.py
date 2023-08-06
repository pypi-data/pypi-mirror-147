
import hashlib
from typing import List
import click
import tabulate
import argparse
import sys
from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter
from based.standards import ALL

def print_table() -> None:
    import tabulate
    entries = []
    header = ['ID', 'Bits/Char', 'Chars/Byte', 'Alphabet']
    for base in sorted(ALL, key=lambda x: x.id):
        if isinstance(base, SlidingWindowBaseConverter):
            entries += [[base.id, base.bits_per_char, base.chars_per_byte, base.alphabet]]
        elif isinstance(base, BigIntBaseConverter):
            entries += [[base.id, 'N/A', 'N/A', base.alphabet]]
    print(tabulate.tabulate(entries, headers=header, tablefmt='github'))

def _main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--dump', action='store_true', default=False)
    argp.add_argument('--hash', type=str, default=None, help='Algorithm to use when hashing.  e.g. sha256, md5')
    argp.add_argument('--standard', choices=[x.id for x in ALL], nargs='?')
    edp = argp.add_mutually_exclusive_group()
    edp.add_argument('--encode', '-E', action='store_true', default=False)
    edp.add_argument('--decode', '-D', action='store_true', default=False)
    argp.add_argument('inputstr')

    if '--dump' in sys.argv:
        print_table()
        return

    args = argp.parse_args()

    o = []
    origb: bytes = args.inputstr.encode('utf-8')
    if args.encode and args.hash:
        origb = hashlib.new(args.hash, origb).digest()
        click.secho(f'>>> input as hex:   {origb.hex()}', fg='cyan')
        click.secho(f'>>> input as bytes: {origb!r}', fg='cyan')
    lenorigb = len(origb)
    if args.standard is None:
        hdr = ['Standard', 'Encoded', 'Decoded', 'Passed Test']
        for base in sorted(ALL, key=lambda x: x.id):
            enc: str = base.encode_bytes(origb)
            decb: str = base.decode_bytes(enc)
            row: List[str]
            if args.hash:
                row = [base.id, enc, repr(decb), decb == origb]
            else:
                #assert lenorigb == len(decb), f'lenorigb={lenorigb}, len(decb)={len(decb)}'
                dec: str = decb.decode('utf-8')
                row = [base.id, enc, dec, dec == args.inputstr]
            o.append(row)
        click.echo(tabulate.tabulate(o, headers=hdr))
    else:
        conv: IBaseConverter = next(c for c in ALL if c.id == args.standard)
        if args.encode:
            print(conv.encode_bytes(origb))
        elif args.decode:
            print(conv.decode_bytes(args.inputstr))
        else:
            click.secho('You must specify --encode (-E) or --decode (-D)!', fg='red', err=True)

if __name__ == "__main__":
    _main()