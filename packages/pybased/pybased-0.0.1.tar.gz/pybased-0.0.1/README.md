# based

Library for creating arbitrary binary encodings.  Includes variations on base32, base64, base85, and more.

## Getting started

```shell
$ pip install pybased
```

## Doing stuff
```python
# Lets's assume we want to use the Crockford32 encoding scheme.
from based.standards.base32 import crockford32

# And let's assume the variable data has what we want to encode.
data: bytes = ...

# Encode to string.
encoded: str = crockford32.encode_bytes(data)

# ...

# Decode the string back to bytes.
data: bytes = crockford32.decode_bytes(encoded)
```

## `based` Command-Line Tool

`based --help`

NOTE: This is generally only useful for testing.