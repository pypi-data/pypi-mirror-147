# Reprypt

from reprypt import *
from sys import argv


HELP = f"""# Reprypt v{__version__}
Python cipher creation module.
GitHub: https://github.com/tasuren/reprypt

## Usage
## Parameters
version\t\tDisplays the version of Reprypt.
help\t\tIt displays this message.
encrypt\t\tIt will encrypt.
decrypt\t\tDecryptDecrypts the file.

## Options
Options can be used by appending them to the end of the command.

dont-conv\tEncrypt without conversion to obfuscate.
\t\tReprypt will replace characters in the string to make them unrecognizable.
\t\tIf you just replace the characters, it is possible that the content of the encrypted string can be guessed from characters in the encrypted string.
\t\tTherefore, it is recommended not to use this option for confidential information.
conv-hex\tThe conversion used for obfuscation uses the hexadecimal conversion.
log\t\tIt outputs a log of the encryption/decryption progress.

## Example usage
Normal: `reprypt encrypt string key`.
Option: `reprypt encrypt string key dont-conv`.

Copyright (c) 2021 tasuren"""


def option_manager(args):
    kwargs = {}
    if "dont-conv" in args:
        kwargs["convert"] = False
    if "conv-hex" in args:
        kwargs["converter"] = convert_hex
    if "log" in args:
        kwargs["log"] = True
    return kwargs


def main():
    varg = argv[1:]
    for word in ("python", "python3", "-m"):
        for arg in varg:
            if arg.startswith(word):
                varg.remove(arg)
    if varg:
        if varg[0] == "help":
            print(HELP)
        elif varg[0] in ("version", "ver", "-V", "--version"):
            print(__version__)
        elif varg[0] in ("encrypt", "en") and len(varg) > 2:
            print("Result :", encrypt(varg[1], varg[2], **option_manager(varg)))
        elif varg[0] in ("decrypt", "de") and len(varg) > 2:
            try:
                result = decrypt(varg[1], varg[2], **option_manager(varg))
            except Exception as e:
                print("Error:", e)
            else:
                print("Result:", result)
                del result
        else:
            print("Error: Usage is different. Check with `reprypt help`.")
    else:
        print(HELP)


if __name__ == "__main__":
    main()