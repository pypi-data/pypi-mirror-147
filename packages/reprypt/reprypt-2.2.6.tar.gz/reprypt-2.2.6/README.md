[![PyPI](https://img.shields.io/pypi/v/reprypt)](https://pypi.org/project/reprypt/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/reprypt) ![PyPI - Downloads](https://img.shields.io/pypi/dm/reprypt) ![PyPI - License](https://img.shields.io/pypi/l/reprypt) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)
# reprypt
A simple encryption library for Python.

## Installation
To install, simply do the following
```terminal
pip install reprypt
```

## Example
```python
import reprypt

# Encryption
encrypted = reprypt.encrypt("Zesu yuge kogiya ga dofu sokieshie", "Kuu Neru Engazer")
print(encrypted)
# p=vZ=znIl1dVB5ItvWZlddWmS5SGBkSYYbBNH2all2c2hZQ2

# Decryption
decrypted = reprypt.decrypt(encrypted, "Kuu Neru Engazer")
print(decrypted)
# Zesu yuge kogiya ga dofu sokieshie
```

## Benchmark
We have benchmarked the encryption of this `README.md`.
```python
"""
Benchmark of reprypt

### Environment
CPU: M1
RAM: 8GB
"""

from timeit import timeit

with open("README.md", "r") as f:
    content = f.read()

print("Result:", timeit(
    lambda : reprypt.encrypt(content, 'a "mutilation of compulsive love"'),
    number=100
))
# Result: 0.20371679199888604
```

## LICENSE
[MIT License](https://github.com/tasuren/reprypt/blob/main/LICENSE)

## Console
Reprypt can also be used from the console once installed.  
You can find instructions on how to use it at `reprypt help`.

## Documentation
You can see the documentation at [here](https://tasuren.github.io/reprypt).