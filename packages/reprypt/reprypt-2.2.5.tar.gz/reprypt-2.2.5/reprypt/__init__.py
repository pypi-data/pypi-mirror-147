""".. include:: ../README.md""" # Reprypt by tasuren

from __future__ import annotations

from typing import Callable

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode


__version__ = "2.2.5"
"""Version of reprypt."""
__author__ = "tasuren"
__all__ = (
    "encrypt", "decrypt", "convert_b64", "convert_hex",
    "old_encrypt", "old_decrypt", "__version__", "DecryptError"
)


class DecryptError(Exception):
    """This exception occurs when decryption fails.  
    This exception occurs when the key or converter used for encryption is different.

    Parameters
    ----------
    text : str
        Text which was tried to be decrypted.
    key : str
        Password which was used for decryption.
    exception : Exception
        Errors actually encountered during decryption

    Attributes
    ----------
    text : str
    key : str
    error : Exception"""

    def __init__(self, text: str, key: str, error: Exception, *args, **kwargs):
        self.text, self.key, self.error = text, key, error
        super().__init__(*args, **kwargs)


def _convert_unicode(text: str, length: int = None) -> str:
    # 指定された文字列をユニコードにします。
    if length is None: length = len(text)
    r = ""
    for ti in range(length):
        r += str(ord(text[ti]))
    return r


def convert_b64(text: str, un: bool) -> str:
    """Encode/decode the string in Base64.  
    This is used by default for obfuscation when encrypting with Reprypt.

    Parameters
    ----------
    test : str
        The string to be encoded or decoded.
    un : bool
        If this is `False`, encoding is performed; if `True`, decoding is performed.

    See Also
    --------
    convert_hex : Converts a string to hexadecimal; can be used to obfuscate Reprypt."""
    return convert_hex(text, un, what_isd=(b64decode, b64encode))


def convert_hex(
    text: str, un: bool,
    what_isd: tuple[Callable[[bytes], bytes], Callable[[bytes], bytes]] = (unhexlify, hexlify)
) -> str:
    """Converts a string to hexadecimal.  
    This is something that can be used to obfuscate when encrypting with Reprypt.

    Examples
    --------
    >>> reprypt.encrypt("You are fine.", "what", converter=reprypt.convert_hex)
    '051e292e66f566757206296665'

    Parameters
    ----------
    text : str
        The string to be converted to hexadecimal.
    un : bool
        If this is `False`, it is converted to hexadecimal; if `True`, it is converted back from hexadecimal.
    what_isd : tuple[Callable[[bytes], bytes], Callable[[bytes], bytes]], default (binascii.unhexlify, binascii.hexlify)
        This is used to convert hexadecimal numbers.  
        Normally this is not changed here."""
    will_hexlify = what_isd[0] if un else what_isd[1]
    text = will_hexlify(text.encode()).decode()
    del will_hexlify
    return text


def _replace(text: str, length: int, original: int, target: int) -> str:
    # 文字列の対象の位置にあるものを対象の位置と交換する関数です。
    after = text[target]
    end = target + 1
    end = text[end:] if end < length else "" # type: ignore
    text = text[:target] + text[original] + end # type: ignore
    end = original + 1
    end = text[end:] if end < length else "" # type: ignore
    text = text[:original] + after + end # type: ignore
    del end, after
    return text


def _parse_key(key: str, key_length: int, text_length: int) -> tuple[str, int]:
    # 暗号化/復号化時に最適な状態にパスワードを調整する関数です。
    error = 0
    while key_length < text_length:
        error = text_length - key_length
        if error > key_length:
            error -= error - key_length
        key = key + key[0 - error:]
        key_length += error
    del key_length, error
    return key[:text_length], text_length


def encrypt(
    text: str, key: str, *, convert: bool = True,
    converter: Callable[[str, bool], str] = convert_b64,
    log: bool = False
) -> str:
    """Encrypt the passed string with Reprypt.

    Parameters
    ----------
    text : str
        The string to be encrypted.
    key : str
        Password used for encryption.  
        It is required for decryption.
    convert : bool, default True
        This is whether or not the text before encryption is converted to something else using the function you put in the converter.  
        If disabled, the cipher result will only contain characters from the original text.  
        It is recommended that this be enabled, since the content may be guessed from the included characters.
    converter : Callable[[str, bool], str], default convert_b64
        What to use for conversion when convert is True.  
        The default is `convert_b64` which encodes in Base64.  
        There is another `convert_hex` which converts to hexadecimal.  
        You can also make your own.
    log : bool, default False
        Whether or not to output the encryption progress.

    Returns
    -------
    text : str
        Result of encryption.

    See Also
    --------
    decrypt : Decryption"""
    if convert:
        text = converter(text, False)
    key, text_length = _convert_unicode(key), len(text)
    key_length, key_index = len(key), -1
    key, key_length = _parse_key(key, key_length, text_length)
    if log:
        print("Encrypt target	:", text)
        print("Encrypt key	:", key)
    for index in range(text_length):
        key_index += 1
        target = int(key[key_index])
        if target >= text_length:
            target = int(target / 2)
        text = _replace(text, text_length, index, target)
        if log:
            print("  Replaced", index, "->", str(target) + "\t:", text)
    return text


def decrypt(
    text: str, key: str, convert: bool = True,
    converter: Callable[[str, bool], str] = convert_b64,
    log: bool = False
) -> str:
    """Decrypt the cipher.

    Parameters
    ----------
    text : str
        The cipher string to be decrypted.
    key : str
        The password set for encryption.
    convert : bool, default True
        If you set the `convert` argument of the `encrypt` function to `True`, this argument must also be `True`.  
        Details of what this is are in the description of the `convert` argument to `encrypt`.
    converter : Callable[[str, bool], str], default convert_b64
        This function is used for conversion when `True` is put in convert.  
        It must be the same as for encryption.  
        The default is `convert_b64` which decodes in Base64.  
        There are others that convert to hexadecimal.  
        See `encrypt` converter for details.
    log : bool, default False
        Outputs the progress of decryption.

    Returns
    -------
    text : str
        Result of decryption

    Raises
    ------
    DecryptError
        Occurs when decryption fails.  
        It occurs when the key does not match or the converter does not match the encryption.

    See Also
    --------
    encrypt : Encryption.

    Warnings
    --------
    If the `convert` argument is `False`, no `DecryptError` will be raised even if the `key` is wrong."""
    original_key = key
    key, text_length = _convert_unicode(key), len(text)
    key, key_index = _parse_key(key, len(key), text_length)
    if log:
        print("Decrypt target	:", text)
        print("Decrypt key	:", key)
    for index in reversed(range(text_length)):
        key_index -= 1
        target = int(key[key_index])
        if target >= text_length:
            target = int(target / 2)
        text = _replace(text, text_length, target, index)
        if log:
            print("  Replaced", target, "->", str(index) + "\t:", text)
    if convert:
        try:
            text = converter(text, True)
        except Exception as e:
            raise DecryptError(
                "Decryption failed, please check if the key is correct and the converter is the same as during encryption: %s" % e,
                original_key, e
            )
    return text


def old_encrypt(text: str, pa: str, log: bool = False) -> str:
    """Perform encryption using pre-2.0.0 encryption methods.

    Notes
    -----
    It is recommended to use the latest `encrypt` due to its slow speed.

    Parameters
    ----------
    text : str
        String to encrypt.
    pa : str
        Password to be used for encryption.
    log : bool, default False
        Whether or not to output log during encryption.

    Returns
    -------
    text : str
        The result of encryption.

    See Also
    --------
    old_decrypt : Function to decrypt the cipher created by this function
    encrypt : The latest Reprypt encryption"""
    if log: print("Start encrypt")
    pa = _convert_unicode(pa)
    text = list(b64encode(text.encode()).decode()) # type: ignore
    for i in range(2):
        if i == 1: text.reverse() # type: ignore
        for ti in range(len(text)):
            for pi in range(len(pa)):
                pi = int(pa[pi])
                if len(text) < pi+1:
                    while pi+1 > len(text):
                        pi -= 1
                if pi == 0:
                    pi = len(text)-1
                if log:
                    print(f"  {i} - {ti+1} ... {text[pi]} -> {text[ti]}")
                m = text[ti]
                text[ti] = text[pi] # type: ignore
                text[pi] = m # type: ignore
    if log: print("Done")
    return "".join(text)


def old_decrypt(text: str, pa: str, log: bool = False) -> str:
    """Decrypts items encrypted with Reprypt up to 2.0.0.  

    Notes
    -----
    It is recommended to use the latest `reprypt.decrypt` because it is slow.  
    However, ciphers created with Reprypt versions up to 2.0.0 cannot be decrypted without this function.  
    Please be careful.

    Parameters
    ----------
    text : str
        String to be decrypted.
    pa : str
        Password to be used for decryption.
    log : bool, default False
        Whether or not to output log during decryption.

    Returns
    -------
    text : str
        The result of decryption.

    See Also
    --------
    old_encrypt : Function to encrypt a text which can be decrypted by using this function.
    decrypt : decrypts ciphers made with the latest Reprypt."""
    if log: print("Start Decrypt")
    original_pa = pa
    pa = _convert_unicode(pa)
    text = list(text) # type: ignore
    for i in range(2):
        if i == 1: text.reverse() # type: ignore
        l_ = list(range(len(text)))
        l_.reverse()
        for ti in l_:
            li = list(range(len(pa)))
            li.reverse()
            for pi in li:
                pi = int(pa[pi])
                if len(text) < pi+1:
                    while pi+1 > len(text):
                        pi -= 1
                if pi == 0:
                    pi = len(text)-1
                if log:
                    print(f"  {i} - {ti+1} ... {text[ti]} -> {text[pi]}")
                m = text[pi]
                text[pi] = text[ti] # type: ignore
                text[ti] = m # type: ignore
    if log: print("Done")
    try: text = b64decode("".join(text).encode()).decode()
    except Exception as e:
        code = "".join((
            "Failed to decode Base64. ",
            "Please check if the password is correct",
            ":", str(e))
        )
        raise DecryptError(code, original_pa, e)
    return text


if __name__ == "__main__":
    import __main__