#!/usr/bin/env python
# MIT License
#
# Copyright (c) 2022 Noah McIlraith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module for the creation, parsing and verification of luckyposts.

A luckypost is a compact human-readable text-based data structure
designed for decentralized and trust-less authenticated public
text-based discussion.

The "lucky" prefix is named after the creator's late pet cat of the
same name, the name was chosen to make Lucky posthumously famous.
Because of this it is a name that carries a sentiment that cannot be
replicated by big tech companies no matter how well-resourced.

The following is an example of a short discussion consisting of two
luckyposts:

    ae3mzuya4u57o2nw7 2022-01-05 19:14:12 en.icecream alice
    <Peppermint is the best icecream flavor
    @agmxl5djhznzshm5eaha4co252zf4zqhbb3g2dqvv2enag542qxsq
    !a16+37ctvYjf75E5M1JzGr27D4cbzZ7dPh7qoroRhYVN5Xd4iyNNoV1AnW7qWFTbAe
    mwcY8qcAcYvmU8T5JGDGM1VFin

    ahbb3g2dqvv2ena 2022-01-05 19:14:12 en.icecream bob
    ^ae3mzuya4u57o2nw7
    >Peppermint is the best icecream flavor
    <Nope, it's hokey pokey!
    @agmxl5djhznzshm5eaha4co252zf4zqhbb3g2dqvv2enag542qxsq
    !a16+4Rq3SEd9KSjfLvvwFEWSFowDzPiGXbqcgF5nsxV7RQsonEg8a9FWyj6vNCbMHj
    WQBwCCQEjKbGQiouhouwdFBkaJ
"""
__author__ = "Noah McIlraith"
__license__ = "MIT"

from os.path import basename
import re
import hashlib
from binascii import hexlify, unhexlify
from functools import partial
from io import BytesIO, SEEK_END
import random
import string
from typing import (
    BinaryIO,
    Tuple,
    Iterable,
    List,
    Optional,
    Callable,
    Iterator,
    Union,
    Any,
    Dict)
from datetime import datetime
from base64 import b32encode, b32decode, urlsafe_b64encode

import nacl.signing
import nacl.exceptions
import ecdsa
from base58 import b58encode, b58decode


MIN_CHANNEL_LEN = 4
MAX_CHANNEL_LEN = 32
MIN_HASH_DIGEST_LEN = 16
MAX_HASH_DIGEST_LEN = 64
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_REGEX = re.compile(r'^(\d\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d)')
CHANNEL_REGEX = re.compile(r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d ([a-z0-9.]*) ')
BODY_REGEX = re.compile(
    r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d .*? ([<>^].*) @[abcdefghijklmnopqrstu'
    r'vwxyz234567]* ![0-9a-zA-Z+]+[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijk'
    r'mnopqrstuvwxyz]*$')
AUTHOR_NAME_REGEX = re.compile(
    r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d .*? ([a-zA-Z\d\-_]*)')
ATTACHMENTS_REGEX = re.compile(
    r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d .*? (\".*) [<>^]')
ATTACHMENT_NO_METADATA_REGEX = re.compile(
    r'"([^><^\n\r\t]*)?" ([\d,]*) ([abcdefghijklmnopqrstuvwxyz234567]*)')
ATTACHMENT_WITH_METADATA_REGEX = re.compile(
    r'"([^><^\n\r\t]*)?" \(([a-zA-Z0-9.,\-_*+]*?)\) ([\d,]*) ([abcdefghijklmnop'
    r'qrstuvwxyz234567]*)')
ATTACHMENT_OPTIONAL_METADATA_REGEX = re.compile(
    r'^("[^><^\n\r\t]*?" (?:\([a-zA-Z0-9.,\-_*+]*?\) )?[\d,]* [abcdefghijklmnop'
    r'qrstuvwxyz234567]*)')
AUTHOR_NAME_VALIDATE_REGEX = re.compile(r'^[a-zA-Z\d\-_]*$')

SALT_1 = unhexlify(
    'e2eef4e13a4041b2a5f3361f250017024f5ac015568823b399ca0d3ffad04111')
SALT_2 = unhexlify(
    '5d9077cba4a844ca88a2bdace699baceb9dc846827bd45b00aaface75e4d9fb3')

HASH_TYPE_NAMES = {
    'a': "SHA256",
    'b': "SHA3-256",
    '1a': "MD5",
    '1b': "SHA1",
}


class UnsupportedSignatureTypeError(Exception):
    pass


class InvalidSignatureError(Exception):
    pass


class UnsupportedHashFunctionCodeError(Exception):
    pass


class InvalidHashDigestLengthError(Exception):
    pass


class InvalidAttachmentNameError(Exception):
    pass


class InvalidBodyError(Exception):
    pass


class InvalidAuthorNameError(Exception):
    pass


class DuplicateAttachmentNameError(Exception):
    pass


def create_luckypost_footer(
        header_and_body: str,
        extensions: List[str],
        hash_type_chrp: str,
        hash_digest_length: int,
        signature_type_chrp: str,
        passphrase: str) -> str:
    """Create the footer for a luckypost.

    Args:
        header_and_body: String containing the header and body sections.
        extensions: List of strings containing extensions (can be empty).
        hash_type_chrp: Type of hashing algorithm to use for the luckypost's ID.
        hash_digest_length: Length of the hash digest in the luckypost's ID.
        signature_type_chrp: CHRP of the type of signature generator to use.
        passphrase: Passphrase to feed to the signature generator.

    Returns:
        Footer to be appended to a partially-created luckypost.
    """
    pk = lb32encode(derive_public_key(signature_type_chrp, passphrase))
    s = f'{header_and_body} @{signature_type_chrp}{pk} ' \
        f'!{hash_type_chrp}{hash_digest_length}+'
    if extensions:
        s += '+'.join(extensions) + '+'
    signature_bytes = sign_bytes(
        signature_type_chrp, passphrase, s.encode('utf-8'))
    return f"{s}{b58encode(signature_bytes).decode('ascii')}"


def verify_post(luckypost_str: str) -> str:
    """Verify a luckypost's signature.

    Args:
        luckypost_str: Luckypost in raw text form.

    Raises:
        InvalidSignatureError: If the luckypost is not valid.

    Returns:
        CHRPed public key of the account that created the luckypost.
    """
    # get public key
    header_and_body, footer = luckypost_str.rsplit(' @', 1)
    full_public_key = footer.split(' ', 1)[0]
    signature_type_chrp, public_key_lb32 = \
        split_chrp(full_public_key.encode('utf-8'))
    signature_type_chrp = signature_type_chrp.decode('utf-8')
    public_key_lb32 = public_key_lb32.decode('utf-8')
    public_key_bytes = lb32decode(public_key_lb32)
    del full_public_key
    # get signature
    partial_footer, signature_b58 = footer.rsplit('+', 1)
    signature_bytes = b58decode(signature_b58)
    del signature_b58, footer
    # verify signature
    verify_bytes(  # returns None or raises exception
        signature_type_chrp,
        public_key_bytes,
        signature_bytes,
        f"{header_and_body} @{partial_footer}+".encode('utf-8'))
    return f"{signature_type_chrp}{public_key_lb32}"


def get_body_from_luckypost(luckypost_str: str) -> str:
    return BODY_REGEX.match(luckypost_str).group(1)


def get_author_name_from_luckypost(luckypost_str: str) -> str:
    """Get the author name from a given luckypost.

    Args:
        luckypost_str: Luckypost in raw text form.

    Returns:
        Name of the given luckypost's author.
    """
    return AUTHOR_NAME_REGEX.match(luckypost_str).group(1)


def split_attachments_str(attachments_str: str) -> List[str]:
    """Split a string containing concatenated attachments.

    Args:
        attachments_str: String containing zero or more attachments and no
          extraneous data.

    Returns:
        List of strings, each of an individual attachment, can be empty.

    >>> split_attachments_str(
    ...     '"a.jpg" (640x480) 1,024 a222 "b.png" 1,048,576 a333')
    ['"a.jpg" (640x480) 1,024 a222', '"b.png" 1,048,576 a333']
    """
    result = []
    while True:
        if not attachments_str:
            break
        match = ATTACHMENT_OPTIONAL_METADATA_REGEX.match(attachments_str)
        if not match:
            raise Exception('attachments parsing error')
        attachment = match.group(1)
        result.append(attachment)
        attachments_str = attachments_str[len(attachment):]
        if attachments_str:
            attachments_str = attachments_str[1:]
    return result


def get_attachments_from_luckypost(
        luckypost_str: str) -> List[Tuple[str, List[str], int, str]]:
    """Get attachments from a given luckypost.

    Args:
        luckypost_str: Luckypost in raw text form.

    Returns:
        Name of the given luckypost's author.
    """
    match = ATTACHMENTS_REGEX.match(luckypost_str)
    if not match:
        return []
    attachments_str = match.group(1)
    attachment_strs = split_attachments_str(attachments_str)
    return list(map(untextify_attachment, attachment_strs))


def get_signature_from_luckypost(luckypost_str: str) -> str:
    return '@' + luckypost_str.rsplit('@', 1)[1].split(None, 1)[0]


def get_extensions_from_luckypost(luckypost_str: str) -> List[str]:
    extensions_str = '!' + luckypost_str.rsplit('!', 1)[1]
    return extensions_str.split('+')[1:-1]


def get_footer_from_luckypost(luckypost_str: str) -> str:
    return '@' + luckypost_str.rsplit('@', 1)[1]


def split_body_iter(body_str: str) -> Iterable[str]:
    # TODO: make less shit
    for line in body_str.replace('>', '\n>').replace('<', '\n<')\
            .replace('^', '\n^').strip().split('\n'):
        yield line.strip()


def split_body(body_str: str) -> str:
    return '\n'.join(split_body_iter(body_str))


def get_references_from_body(body_str: str) -> Iterable[str]:
    for line in split_body_iter(body_str):
        if line.startswith('^'):
            yield line[1:]


def get_hash_config_from_post(luckypost_str: str) -> Tuple[str, int]:
    """Get the post hashing configuration used by a given post.

    Args:
        luckypost_str: Luckypost in raw text form.

    Returns: A tuple containing a CHRP indicating the hashing algorithm used
      and a number indicating the length of the hash digest.
    """
    hash_config = luckypost_str.rsplit('!', 1)[-1].split('+', 1)[0]
    hash_type_chrp = read_chrp(hash_config.encode('utf-8')).decode('utf-8')
    hash_spec = hash_config[len(hash_type_chrp):]
    hash_digest_length = int(hash_spec)
    return hash_type_chrp, hash_digest_length


def get_hasher_from_chrp(hash_type_chrp: str):
    if hash_type_chrp == 'a':
        hasher = hashlib.sha256
    elif hash_type_chrp == 'b':
        hasher = hashlib.sha3_256
    elif hash_type_chrp == '1a':
        hasher = hashlib.md5
    elif hash_type_chrp == '1b':
        hasher = hashlib.sha1
    else:
        raise UnsupportedHashFunctionCodeError(
            f"unsupported hash function code {hash_type_chrp}")
    return hasher


def get_luckypost_id(luckypost_str: str) -> str:
    """Get the post ID of a given luckypost.

    Args:
        luckypost_str: Luckypost in raw text form.

    Raises:
        UnsupportedHashFunctionCodeError: If the luckypost uses a type of
          hashing that is not supported.

    Returns:
        ID of the luckypost (including CHRP).
    """
    hash_type_chrp, hash_digest_length = \
        get_hash_config_from_post(luckypost_str)
    if hash_digest_length > MAX_HASH_DIGEST_LEN:
        raise InvalidHashDigestLengthError("hash digest too long")
    if hash_digest_length < MIN_HASH_DIGEST_LEN:
        raise InvalidHashDigestLengthError("hash digest too short")
    hasher = get_hasher_from_chrp(hash_type_chrp)
    hash_digest = hasher(luckypost_str.encode('utf-8')).digest()
    while len(hash_digest) < hash_digest_length:  # TODO: optimize
        hash_digest += hash_digest
    return hash_type_chrp + lb32encode(hash_digest)[:hash_digest_length]


def generate_private_key(signature_type_chrp: str) -> bytes:
    """Generate a private key.

    Args:
        signature_type_chrp: CHRP indicating the type of encryption to
          generate a private key for.

    Raises:
        UnsupportedSignatureTypeError: If the given signature type CHRP doesn't
           correspond to a supported signature type.

    Returns:
        Generated private key in bytes form, no CHRP is prefixed.
    """
    if signature_type_chrp == 'a':
        return bytes(nacl.signing.SigningKey.generate())
    elif signature_type_chrp == 'b':
        return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string()
    else:
        raise UnsupportedSignatureTypeError(
            "not a supported signature type: %r" % signature_type_chrp)


def derive_private_key(signature_type_chrp: str, passphrase: str) -> bytes:
    if signature_type_chrp == 'a':
        return hashlib.scrypt(
            password=passphrase.encode('utf-8'),
            salt=SALT_1,
            n=65_536,
            r=8,
            p=1,
            maxmem=65_536 * 2 * 8 * 65,
            dklen=32)
    elif signature_type_chrp == 'b':
        return hashlib.scrypt(
            password=passphrase.encode('utf-8'),
            salt=SALT_2,
            n=65_536,
            r=8,
            p=1,
            maxmem=65_536 * 2 * 8 * 65,
            dklen=32)
    else:
        raise UnsupportedSignatureTypeError(
            "not a supported signature type: %r" % signature_type_chrp)


def derive_public_key(
        signature_type_chrp: str,
        passphrase: str) -> bytes:
    """Get a public key from a given private key.

    Args:
        signature_type_chrp: CHRP indicating the type of encryption used.
        passphrase: Passphrase to get the public key from.

    Raises:
        UnsupportedSignatureTypeError: If the given signature type CHRP doesn't
           correspond to a supported signature type.

    Returns:
        Public key in bytes form, no CHRP prefixed.

    >>> hexlify(derive_public_key('a', 'p4ssphr4s3'))
    b'd7b8b8c07e8299b3f67a719e2c17c4b1c33e1da6021cf43a87478266e25ba8d0'
    """
    if not isinstance(passphrase, str):
        raise ValueError("passphrase must be a string")
    private_key_bytes = derive_private_key(signature_type_chrp, passphrase)
    if signature_type_chrp == 'a':
        return bytes(nacl.signing.SigningKey(private_key_bytes).verify_key)
    elif signature_type_chrp == 'b':
        vk = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        return vk.to_string('compressed')
    else:
        raise UnsupportedSignatureTypeError(
            "not a supported signature type: %r" % signature_type_chrp)


def verify_bytes(
        signature_type_chrp: str,
        public_key_bytes: bytes,
        signature_bytes: bytes,
        bytes_to_verify: bytes) -> None:
    """Verify a signature created using `sign_bytes()`.

    Args:
        signature_type_chrp: CHRP indicating the type of encryption used.
        public_key_bytes: Encryption key to feed to the signature validator.
        signature_bytes: Bytes containing the signature.
        bytes_to_verify: Bytes that the signature was created to verify.

    Raises:
        InvalidSignatureError: If the signature isn't valid.

    Returns:
        Nothing.

    >>> type_chrp = 'a'
    >>> passphrase = 'p4ssphr4se'
    >>> data = b"hello"
    >>> signature = sign_bytes(type_chrp, passphrase, data)
    >>> public_key = derive_public_key(type_chrp, passphrase)
    >>> verify_bytes(type_chrp, public_key, signature, data)
    """
    if signature_type_chrp == 'a':
        try:
            vk = nacl.signing.VerifyKey(public_key_bytes)
        except nacl.exceptions.ValueError as e:
            raise InvalidSignatureError(
                "signature appears to be corrupt or forged") from e
        try:
            vk.verify(bytes_to_verify, signature_bytes)
        except nacl.exceptions.BadSignatureError as e:
            raise InvalidSignatureError(
                "signature appears to be corrupt or forged") from e
        if bytes(vk) != public_key_bytes:
            raise InvalidSignatureError(
                "signature appears to be corrupt or forged")
    elif signature_type_chrp == 'b':
        vk = ecdsa.VerifyingKey.from_string(
            public_key_bytes, curve=ecdsa.SECP256k1)
        vk.verify(signature_bytes, bytes_to_verify, hashfunc=hashlib.sha256)
        if vk.to_string('compressed') != public_key_bytes:
            raise InvalidSignatureError(
                "signature appears to be corrupt or forged")
    else:
        raise UnsupportedSignatureTypeError(
            "not a supported signature type: %r" % signature_type_chrp)


def sign_bytes(
        signature_type_chrp: str,
        passphrase: str,
        bytes_to_sign: bytes) -> bytes:
    """Sign bytes with CHRP-selected encryption.

    Args:
        signature_type_chrp: CHRP indicating the type of encryption to use.
        passphrase: Passphrase to feed to the signature generator.
        bytes_to_sign: Bytes to generate the signature for.

    Raises:
        UnsupportedSignatureTypeError: If the given signature type CHRP doesn't
           correspond to a supported signature type.

    Returns:
        Raw signature in bytes-form, the CHRP is not prefixed.

    >>> hexlify(sign_bytes('a', 'p4ssphr4s3', b"hello"))  # doctest: +ELLIPSIS
    b'28fceb7f33ee98daf6d918b6c26c633e...e380aec2e508053aec96dec51566a2f9e55c00'
    """
    if not isinstance(passphrase, str):
        raise ValueError("passphrase must be a string")
    if signature_type_chrp == 'a':
        private_key_bytes = derive_private_key(signature_type_chrp, passphrase)
        signing_key = nacl.signing.SigningKey(private_key_bytes)
        return bytes(signing_key.sign(bytes_to_sign).signature)
    elif signature_type_chrp == 'b':
        private_key_bytes = derive_private_key(signature_type_chrp, passphrase)
        signing_key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1)
        return signing_key.sign(bytes_to_sign, hashfunc=hashlib.sha256)
    else:
        raise UnsupportedSignatureTypeError(
            "not a supported signature type: %r" % signature_type_chrp)


def get_channel_from_luckypost(luckypost_str: str) -> str:
    """Get the channel from a given luckypost.

    Args:
        luckypost_str: Luckypost in raw string format.

    Returns:
        Channel extracted from the given luckypost.

    >>> get_channel_from_luckypost(
    ... "2022-04-08 02:50:17 en.test bob >Hello world! @axjbeldudxj4snoulr47jv"
    ... "ookv4hrysiy3wumkuiij55owedfw5fq !a24+4FGH3neGquhsN376ckjYVjqYBM6Wrkgd"
    ... "3jvnXBQLPcX23w1Uo8i9phNS8PSSWVAz9acRLxtotu7BApbWtbG2FWL1")
    'en.test'
    """
    channel = CHANNEL_REGEX.match(luckypost_str).group(1)
    if not channel:
        raise ValueError("Luckypost does not contain a valid channel")
    return channel


def get_timestamp_from_luckypost(luckypost_str: str) -> str:
    """Get the timestamp from a given luckypost.

    Args:
        luckypost_str: Luckypost in raw string format.

    Returns:
        Timestamp string extracted from the given luckypost.

    >>> get_timestamp_from_luckypost(
    ... "2022-04-08 02:50:17 en.test bob >Hello world! @axjbeldudxj4snoulr47jv"
    ... "ookv4hrysiy3wumkuiij55owedfw5fq !a24+4FGH3neGquhsN376ckjYVjqYBM6Wrkgd"
    ... "3jvnXBQLPcX23w1Uo8i9phNS8PSSWVAz9acRLxtotu7BApbWtbG2FWL1")
    '2022-04-08 02:50:17'
    """
    return TIMESTAMP_REGEX.match(luckypost_str).group(0)


def lb32encode(raw_bytes: bytes, encoding: str = 'utf-8') -> str:
    """Encodes bytes using Base32 with padding stripped and in lowercase.

    Args:
        raw_bytes: Bytes to LB32 encode.
        encoding: Encoding to use to encode LB32-encoded string.

    Returns:
        LB32-encoded bytes as a string.

    >>> lb32encode(b"hello")
    'nbswy3dp'
    """
    return b32encode(raw_bytes).rstrip(b'=').lower().decode(encoding)


def lb32decode(lb32_str: str) -> bytes:
    """Decodes text string that was encoded using `lb32encode()`.

    Args:
        lb32_str: LB32-encoded string to decode.

    Returns:
        Bytes decoded from LB32-encoded string.

    >>> lb32decode('nbswy3dp')
    b'hello'
    """
    if lb32_str.endswith('='):
        raise ValueError("`lb32_str` must not have any padding")
    return b32decode(lb32_str.upper() + ('=' * (-len(lb32_str) % 8)))


def groupiter(iterable: Iterable[Any], n: int) -> Iterator[List[Any]]:
    """Group iterable's results into n-sized lists."""
    iterable = iter(iterable)
    count = 0
    group = []
    while True:
        try:
            group.append(next(iterable))
            count += 1
            if count % n == 0:
                yield group
                group = []
        except StopIteration:
            if group:
                yield group
            break


def dt_to_timestamp(dt: datetime, ignore_microseconds: bool = False) -> str:
    """Converts a datetime object to timestamp string.

    Args:
        dt: A datetime object to generate a string timestamp from.
        ignore_microseconds: Strip microseconds from the `dt` argument.

    Raises:
        ValueError: If `dt` contains microseconds.

    Returns:
        Timestamp in string format.

    >>> dt_to_timestamp(datetime(2022, 4, 8, 2, 50, 17))
    '2022-04-08 02:50:17'
    >>> dt_to_timestamp(
    ... dt=datetime(2022, 4, 8, 2, 50, 17, 514527),
    ... ignore_microseconds=True)
    '2022-04-08 02:50:17'
    """
    if not ignore_microseconds and dt.microsecond != 0:
        raise ValueError("`dt` has microseconds")
    return dt.strftime(TIMESTAMP_FORMAT)


def timestamp_to_dt(timestamp: str) -> datetime:
    """Converts a timestamp string to a datetime object.

    Args:
        timestamp: A timestamp in string format.

    Returns:
        A datetime object.

    >>> timestamp_to_dt('2022-04-08 02:50:17')
    datetime.datetime(2022, 4, 8, 2, 50, 17)
    """
    return datetime.strptime(timestamp, TIMESTAMP_FORMAT)


def is_timestamp_valid(timestamp: str) -> bool:
    """Check if a timestamp string is valid.

    Args:
        timestamp: Timestamp string to validate.

    Returns:
        `True` if valid and `False` if not.

    >>> is_timestamp_valid('2022-04-08 02:50:17')
    True
    >>> is_timestamp_valid('blahblah')
    False
    >>> is_timestamp_valid('2022-04-08 02:50:17.512345')
    False
    """
    if not isinstance(timestamp, str):
        raise ValueError("`timestamp` must be a string")
    try:
        timestamp_to_dt(timestamp)
    except ValueError:
        return False
    return True


def split_chrp(data: bytes) -> Tuple[bytes, bytes]:
    """Split CHRPed bytes into the CHRP and the following bytes.

    Args:
        data: Bytes to split.

    Raises:
        ValueError: If the string contains a truncated CHRP.

    Returns:
        A tuple containing the CHRP and the following bytes.

    >>> split_chrp(b"ahello")
    (b'a', b'hello')
    """
    chrp = read_chrp(data)
    return chrp, data[len(chrp):]


def read_chrp(data: bytes) -> bytes:
    """Read a CHRP from bytes.

    Args:
        data: String to read the CHRP from.

    Raises:
        ValueError: If the string contains a truncated CHRP.

    Returns:
        The extracted CHRP.

    >>> read_chrp(b'a')
    b'a'
    >>> read_chrp(b'9aaabbbccc')
    b'9aaabbbccc'
    """
    if not data:
        raise ValueError("need more characters")
    char = data[:1]
    if not char.isdigit():
        return char
    length = int(char)
    data = data[:length + 1]
    if len(data) < length + 1:
        raise ValueError("need more characters")
    return data


def validate_author_name_or_raise(author_name: str) -> None:
    if not AUTHOR_NAME_VALIDATE_REGEX.match(author_name):
        raise InvalidAuthorNameError("invalid author name")


def raise_if_duplicate_attachment_names(attachment_names: List[str]) -> None:
    if len(attachment_names) != len(set(attachment_names)):
        raise DuplicateAttachmentNameError("duplicate attachment name")


def validate_attachment_name_or_raise(attachment_name: str) -> None:
    """Detect if a given attachment name is valid.

    Args:
        attachment_name: Name of the file to validate.

    Returns:
        `True` if valid and `False` if not.

    >>> validate_attachment_name_or_raise("inva>lid.jpg")
    Traceback (most recent call last):
     ...
    InvalidAttachmentNameError: attachment name must not contain ">"
    >>> validate_attachment_name_or_raise("test.jpg")
    """
    if '"' in attachment_name:
        raise InvalidAttachmentNameError(
            "attachment name must not contain double quotes")
    if '>' in attachment_name:
        raise InvalidAttachmentNameError('attachment name must not contain ">"')
    if '<' in attachment_name:
        raise InvalidAttachmentNameError('attachment name must not contain "<"')
    if '^' in attachment_name:
        raise InvalidAttachmentNameError("attachment name must not contain '^'")
    if '\n' in attachment_name:
        raise InvalidAttachmentNameError(
            "attachment name must not contain newlines")
    if '\r' in attachment_name:
        raise InvalidAttachmentNameError(
            "attachment name must not contain carriage returns")
    if '\t' in attachment_name:
        raise InvalidAttachmentNameError(
            "attachment name must not contain tabs")
    if '  ' in attachment_name:  # double space
        raise InvalidAttachmentNameError(
            "attachment name must not contain double spaces")


def validate_attachment_name(attachment_name: str) -> bool:
    """Detect if a given attachment name is valid.

    Args:
        attachment_name: Name of the attachment to validate.

    Returns:
        `True` if valid and `False` if not.

    >>> validate_attachment_name("test.jpg")
    True
    >>> validate_attachment_name("<inva^lid>.jpg")
    False
    """
    try:
        validate_attachment_name_or_raise(attachment_name)
    except InvalidAttachmentNameError:
        return False
    return True


def textify_attachment(attachment: Tuple[str, List[str], int, str]) -> str:
    """Convert an attachment tuple into text for inclusion in a luckypost.

    This function achieves the reverse of `untextify_attachment`.

    Args:
        attachment: Tuple containing four values: name, metadata, size and hash.

    Returns:
        Text form of attachment.

    >>> textify_attachment(('test.jpg', [], 1024, 'a234567654'))
    '"test.jpg" 1,024 a234567654'
    >>> textify_attachment(('test.jpg', ['640x480', 'lol'], 1024, 'a234567654'))
    '"test.jpg" (640x480,lol) 1,024 a234567654'
    """
    name, metadata, size, root_hash = attachment
    validate_attachment_name_or_raise(name)
    s = f'"{name}"'
    if metadata:
        s += f' ({",".join(metadata)})'
    s += f" {'{:,}'.format(size)} {root_hash}"
    return s


def untextify_attachment(
        attachment_text: str) -> Tuple[str, List[str], int, str]:
    """Convert an attachment in text form into a tuple.

    This function achieves the reverse of `textify_attachment`.

    Args:
        attachment_text: Text form of the attachment.

    Returns:
        Tuple containing four values: name, metadata, size and hash.

    >>> untextify_attachment('"test.jpg" 1,024 a2345676545')
    ('test.jpg', [], 1024, 'a2345676545')
    """
    match = ATTACHMENT_NO_METADATA_REGEX.match(attachment_text)
    if match:
        name, size_str, root_hash = match.groups()
        metadata = []
    else:
        match = ATTACHMENT_WITH_METADATA_REGEX.match(attachment_text)
        if not match:
            raise ValueError("invalid attachment")
        name, metadata_str, size_str, root_hash = match.groups()
        metadata = metadata_str.split(',')
        if not metadata:  # parenthesis but no metadata
            raise ValueError("invalid attachment")
    size = int(size_str.replace(',', ''))
    return name, metadata, size, root_hash


def validate_body_or_raise(body: str) -> None:
    if '\n' in body:
        raise InvalidBodyError("body must not have newlines")
    if '\r' in body:
        raise InvalidBodyError("body must not have carriage returns")
    if '< ' in body:
        raise InvalidBodyError(
            "body must not have a `<` symbol followed by a space")
    if '> ' in body:
        raise InvalidBodyError(
            "body must not have a `>` symbol followed by a space")
    if '^ ' in body:
        raise InvalidBodyError(
            "body must not have a `^` symbol followed by a space")
    if body[0] not in ('<', '>', '^'):
        raise InvalidBodyError(
            "first character in body must be `>`, `<` or `^`")


def create_luckypost(
        hash_type_chrp: str,
        hash_digest_length: int,
        signature_type_chrp: str,
        passphrase: str,
        timestamp: str,
        channel: str,
        author_name: str,
        attachments: List[Tuple[str, List[str], int, str]],
        body: str,
        extensions: List[str]) -> str:
    """Create a LuckyPost.
    
    Args:
        hash_type_chrp: CHRP of the hashing algorithm to use for the post's ID.
        hash_digest_length: Length of the hash digest used in the post's ID.
        signature_type_chrp: CHRP of the encryption algorithm used to create
          the post's signature.
        passphrase: Passphrase to feed to the signature generator.
        timestamp: Datetime of the post's creation.
        channel: Name of the channel this post belongs to.
        author_name: Name of the post's author.
        attachments: List of attachment tuples (can be empty list).
        body: Luckypost's body in string format.
        extensions: List of CHRPed extension strings (can be empty list).

    Raises:
        InvalidAuthorNameError: if the author name is invalid.
        InvalidBodyError: if the body is invalid.
        InvalidAttachmentNameError: if an attachment name is invalid.

    Returns:
        LuckyPost in "raw string" format.

    >>> create_luckypost(
    ...     hash_type_chrp='a',
    ...     hash_digest_length=24,
    ...     signature_type_chrp='a',
    ...     passphrase='p4ssphr4se',
    ...     timestamp=dt_to_timestamp(datetime(2022, 4, 8, 2, 50, 17)),
    ...     channel='en.test',
    ...     author_name='bob',
    ...     attachments=[],
    ...     body='>Hello world!',
    ...     extensions=[])  # doctest: +ELLIPSIS
    '2022-04-08 02:50:17 en.test bob >Hello world! @ajvr...i65a !a24+3pq...z5h6'
    """
    if not isinstance(hash_type_chrp, str):
        raise ValueError("`hash_type_chrp` must be a string")
    if not isinstance(hash_digest_length, int):
        raise ValueError("`hash_digest_length` must be a number")
    if isinstance(timestamp, datetime):
        raise ValueError("`timestamp` must be in string format")
    if not is_timestamp_valid(timestamp):
        raise ValueError("`timestamp` is invalid")
    validate_body_or_raise(body)
    validate_author_name_or_raise(author_name)
    # TODO: file attachments, etc
    header_and_body = f'{timestamp} {channel} {author_name}'
    raise_if_duplicate_attachment_names([attach[0] for attach in attachments])
    for attachment in attachments:
        header_and_body += f' {textify_attachment(attachment)}'
    header_and_body += f' {body}'
    return create_luckypost_footer(
        header_and_body=header_and_body,
        extensions=extensions,
        hash_type_chrp=hash_type_chrp,
        hash_digest_length=hash_digest_length,
        signature_type_chrp=signature_type_chrp,
        passphrase=passphrase)


def parse_luckypost(luckypost_str: str) -> dict:
    result = {
        'timestamp': get_timestamp_from_luckypost(luckypost_str),
        'channel': get_channel_from_luckypost(luckypost_str),
        'author_name': get_author_name_from_luckypost(luckypost_str),
        'attachments': get_attachments_from_luckypost(luckypost_str),
        'body': get_body_from_luckypost(luckypost_str),
        'extensions': get_extensions_from_luckypost(luckypost_str),
    }
    return result


def bytes_to_bits(data: bytes) -> str:
    return "{:08b}".format(int(data.hex(), 16))


def count_leading_bits(bits: str) -> int:
    count = 0
    for bit in bits:
        if bit != '1':
            break
        count += 1
    return count


def get_power_level(author_address: str, pow_extension: str) -> int:
    chrp, hash_type_and_nonce = split_chrp(pow_extension.encode('utf-8'))
    chrp = chrp.decode('utf-8')
    if chrp != 'p':
        raise ValueError("not a proof-of-work extension")
    hash_type_and_nonce = hash_type_and_nonce.decode('utf-8')
    hash_type_chrp, nonce = split_chrp(hash_type_and_nonce.encode('utf-8'))
    hasher = get_hasher_from_chrp(hash_type_chrp.decode('utf-8'))
    pow_digest = hasher(f"{author_address} {nonce}".encode('utf-8')).digest()
    power_level = count_leading_bits(bytes_to_bits(pow_digest))
    return power_level


def decode_varint(stream: BinaryIO) -> int:
    """Decode a number by reading each byte from a stream.

    Arguments:
        stream:
            File-like object to read bytes from, must implement the
            `read` method.

    Returns:
        Decoded unsigned integer.
    """
    c = stream.read(1)
    if c == b'':
        raise EOFError("failed to read first byte of varint")
    c = ord(c)
    val = c & 127
    while c & 128:
        val += 1
        c = stream.read(1)
        if c == b'':
            raise EOFError("failed to read subsequent byte of varint")
        c = ord(c)
        val = (val << 7) + (c & 127)
    return val


def encode_varint(number: int) -> bytes:
    """Encode a number into a variable amount of bytes.

    There is no limit to how high the integer can be but it cannot be
    below zero.

    The greater the number the more bytes will be needed.

    Arguments:
        number:
            Unsigned integer to b64encode.

    Returns:
        Bytes containing the encoded input.
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("`number` must be a positive integer")
    buf = bytes((number & 127, ))
    while True:
        number >>= 7
        if not number:
            break
        number -= 1
        buf = bytes(((128 | (number & 127)), )) + buf
    return buf


# numbers are spread out along the 0~127 range to give more variety to first
# byte in the hash when encoded using human-readable characters
HASH_FUNCTIONS = {
    1: hashlib.md5,
    2: hashlib.sha1,
    3: hashlib.sha256,
    14: hashlib.sha512,
    28: hashlib.sha224,
    42: hashlib.sha384,
    56: hashlib.sha3_256,
    70: hashlib.sha3_512,
    84: hashlib.sha3_224,
    98: hashlib.sha3_384,
    112: hashlib.blake2b,
    126: hashlib.blake2s,
}


class UnsupportedHashFunctionError(Exception):
    pass


class InvalidHashError(Exception):
    pass


def join_blockhash(
        hash_func_code: int,
        block_size: int,
        digest_bytes: bytes) -> bytes:
    """Join a blockhash from its individual components."""
    return encode_varint(hash_func_code) + encode_varint(block_size) \
        + digest_bytes


def split_blockhash(blockhash_bytes: bytes) -> Tuple[int, int, bytes]:
    """Split a blockhash into its individual components."""
    try:
        stream = BytesIO(blockhash_bytes)
        del blockhash_bytes
        hash_func_code = decode_varint(stream)
        block_size = decode_varint(stream)
        digest_bytes = stream.read()
        del stream
    except EOFError as e:
        raise InvalidHashError("blockhash corrupt or truncated") from e
    return hash_func_code, block_size, digest_bytes


def get_hash_func_code(blockhash_bytes: bytes) -> int:
    """Get the hash function code from a given blockhash."""
    return decode_varint(BytesIO(blockhash_bytes))


def get_block_size(blockhash_bytes: bytes) -> int:
    """Get the number of bytes in the referenced block of data."""
    stream = BytesIO(blockhash_bytes)
    decode_varint(stream)  # skip the first varint
    return decode_varint(stream)


def create_blockhash(
        hash_func_code: int,
        digest_size: int,
        block_data: Union[bytes, BinaryIO, Callable],
        block_size: Optional[int] = None,
        read_chunk_size: int = 256 * 1024,
        digest_only: bool = False) -> bytes:
    """Create a blockhash for a given block using the given settings.

    >>> lb32encode(create_blockhash(56, 32, b'Hello, world!'))  # 56 = sha3-256
    'hag7grncdhnaaxv6tqnb5kwzpo7triimqrz6ihik675wc7fkbrvkoiq'

    >>> lb32encode(create_blockhash(56, 16, b''))
    'haakp76g7c7r5v3gkhauovvamhlge'

    """
    # get content_size from byte string and truncate if needed
    if isinstance(block_data, bytes):
        # truncate bytes if content_size specified
        if block_size is not None:
            block_data = block_data[:block_size]
        else:
            block_size = len(block_data)
    # no content_size specified with a stream input? read entire stream!
    elif block_size is None:
        if hasattr(block_data, 'seek') and hasattr(block_data, 'tell'):
            block_data.seek(0, SEEK_END)
            block_size = block_data.tell()
            block_data.seek(0)
        else:
            if hasattr(block_data, 'readuntil'):
                read_func = block_data.readuntil
            elif hasattr(block_data, 'read'):
                read_func = block_data.read
            elif isinstance(block_data, Callable):
                read_func = block_data
            else:
                raise ValueError("`block_data` is not a supported type")
            block_data = read_func()
            block_size = len(block_data)
    if isinstance(hash_func_code, bool) or not isinstance(hash_func_code, int):
        raise ValueError(
            "`hash_func_code` must be a non-negative integer, got "
            f"{hash_func_code!r}")
    # create bytearray to store the result
    result = bytearray()
    result += encode_varint(hash_func_code)
    result += encode_varint(block_size)
    # construct hashing function
    try:
        hash_func = HASH_FUNCTIONS[hash_func_code]
        if hash_func_code == 112:  # blake2b
            # noinspection PyArgumentList
            hasher = hash_func(
                digest_size=min(hashlib.blake2b.MAX_DIGEST_SIZE, digest_size))
        elif hash_func_code == 126:  # blake2s
            # noinspection PyArgumentList
            hasher = hash_func(
                digest_size=min(hashlib.blake2s.MAX_DIGEST_SIZE, digest_size))
        else:
            hasher = hash_func()
    except KeyError:
        raise UnsupportedHashFunctionError(
            "unsupported hash function: %r" % hash_func_code)
    # feed block to hashing algorithm
    if isinstance(block_data, bytes):
        # if a string then it's in memory all ready, hash it in one go
        hasher.update(block_data)
        del block_data
    else:
        # assume block is a stream of bytes, get read function
        if hasattr(block_data, 'readuntil'):
            read_func = block_data.readuntil
        elif hasattr(block_data, 'read'):
            read_func = block_data.read
        elif isinstance(block_data, Callable):
            read_func = block_data
        else:
            raise ValueError("`block_data` is not a supported type")
        del block_data
        # track how many more bytes are needed to be read from stream
        left_to_read = block_size
        # loop until all bytes are processed
        while True:
            # TODO: I think if is not needed, size is specified
            if block_size:
                to_read = min(left_to_read, read_chunk_size)
            else:
                to_read = read_chunk_size
            # read a chunk from the stream
            chunk = read_func(to_read)
            # no data in chunk? assume stream closed
            if not chunk:
                break
            if block_size is None:  # is content_size-limited
                left_to_read -= len(chunk)
            hasher.update(chunk)
    # get hash digest
    digest_bytes = hasher.digest()
    # increase size of digest to match requested size (if needed)
    # TODO: small optimization potential
    while len(digest_bytes) < digest_size:
        digest_bytes *= 2
    # truncate digest to requested size
    digest_bytes = digest_bytes[:digest_size]
    if digest_only:
        return digest_bytes
    return join_blockhash(hash_func_code, block_size, digest_bytes)


def get_child_count_per_branch(
        leaf_count: int,
        branch_capacity: int) -> Iterable[Tuple[int, int, int]]:
    # zero or one leaves means no branches
    if leaf_count <= 1:
        return []
    # tree height is number of levels in the tree
    tree_height = get_tree_height(leaf_count, branch_capacity)
    # start at the uppermost level of branches (one below leaves)
    tree_level = tree_height - 2
    # loop until no more branches
    child_count = leaf_count
    while True:
        # get number of branches at this level
        branch_count, remainder = divmod(child_count, branch_capacity)
        if remainder:
            branch_count += 1
        # iterate over each branch on this level
        for position in range(branch_count):
            last = position == branch_count - 1
            if last:
                yield tree_level, position, remainder or branch_capacity
            else:
                yield tree_level, position, branch_capacity
        # moving on to the next level
        tree_level -= 1
        # end of the tree? we're done
        if tree_level < 0:
            break
        # all the branches at this layer become children for the next
        child_count = branch_count


def count_children_in_branch(
        leaf_count: int,
        branch_capacity: int,
        position: int,
        tree_level: int) -> int:
    """Determine the number of children in a specific branch.

    Arguments:
        leaf_count:
            Number of leaves in the entire tree.
        branch_capacity:
            The maximum number of children per branch.
        position:
            Position of the branch (similar to "x position"), 0-based.
        tree_level:
            How many layers into the tree (similar to "y position"), 0-based.

    Returns:
        Exact number of children in that specific branch, could be less than
        the branch capacity.
    """
    # TODO: can this be optimized?
    for tl, p, branch_size in \
            get_child_count_per_branch(leaf_count, branch_capacity):
        if position == p and tree_level == tl:
            return branch_size
    raise ValueError(
        f"branch does not exist in tree at {tree_level},{position}")


def get_leaf_count(content_size: int, block_size: int) -> int:
    """Calculates number of leaves in a tree.

    Empty content has no leaves.
    >>> get_leaf_count(0, 256)
    0

    One full message takes only one leaf and no branches.
    >>> get_leaf_count(256, 256)
    1

    One byte beyond block size means two leaves and one branch to
    connect them together.
    >>> get_leaf_count(256 + 1, 256)
    2
    """
    if block_size <= 0:
        raise ValueError("`block_size` must be a positive integer")
    if content_size < 0:
        raise ValueError("`content_size` must not be a negative integer")
    if content_size == 0:
        return 0
    if content_size <= block_size:
        return 1
    leaf_count, remainder = divmod(content_size, block_size)
    if remainder:
        leaf_count += 1
    return leaf_count


def get_branch_capacity(block_size: int, digest_size: int) -> int:
    """Calculate how many hashes can fit in a branch of a given size.

    A branch might not be at full capacity but it will always have at least
    one child.

    Number of hashes per block is limited to the size of the block.
    >>> get_branch_capacity(256, 32)
    8
    """
    capacity = block_size // digest_size
    if capacity <= 1:  # 0 or 1
        raise ValueError("`block_size` too small or `digest_size` too big")
    return capacity


def get_block_type(
        leaf_count: int,
        branch_capacity: int,
        tree_level: int) -> str:
    """Determine the type of blocks at a given tree level for a given tree."""
    tree_height = get_tree_height(leaf_count, branch_capacity)
    if tree_level > tree_height - 1 or tree_level < 0:
        raise ValueError("`tree_level` out-of-range")
    if tree_level < tree_height - 1:
        return 'branch'
    return 'leaf'


def get_branch_count(
        leaf_count: int,
        branch_capacity: int) -> int:
    """Count number of branches in a tree.

    No branches needed if content fits in one leaf.
    >>> get_branch_count(1, 10)
    0

    More than one leaf needs a branch to connect them
    >>> get_branch_count(2, 10)
    1
    """
    return get_branch_count_and_tree_height(
        leaf_count, branch_capacity)[0]


def get_tree_height(leaf_count: int, branch_capacity: int) -> int:
    """Count number of branches in a tree."""
    return get_branch_count_and_tree_height(
        leaf_count, branch_capacity)[1]


def get_block_count(
        leaf_count: int,
        branch_capacity: int) -> int:
    """Count number of blocks (leaf and branch).

    Returns:
        Number of blocks (integer).
    """
    return leaf_count \
        + get_branch_count(leaf_count, branch_capacity)


def get_branch_count_and_tree_height(
        leaf_count: int,
        branch_capacity: int) -> Tuple[int, int]:
    """Count number of branches in a tree and the tree's height."""
    total_branch_count = 0
    child_count = leaf_count
    # one or zero leaves means there is no need for any branches
    if child_count == 0:  # empty content (zero length)
        return 0, 0  # 0 branches, 0 height
    if child_count == 1:
        return 0, 1  # 0 branches, 1 height
    # track height of tree
    tree_height = 1
    # each iteration handles each layer of the tree
    while True:
        tree_height += 1
        # count number of children to put into this branch
        branch_count, remainder = divmod(child_count, branch_capacity)
        # if there's still more children we'll need another branch on
        # this level
        if remainder:
            branch_count += 1
        # add number of branches at this level to the total
        total_branch_count += branch_count
        # only one branch at this level? that's the root node! done!
        if branch_count == 1:
            break
        # all the branches at this layer turn into children for the next
        child_count = branch_count
    return total_branch_count, tree_height


def get_root_block_type(leaf_count: int, branch_capacity: int) -> str:
    """Determine the block type of the root block.

    Args:
        leaf_count: Number of leaves in the tree.
        branch_capacity: Number of blockhashes each branch can hold.

    Returns:
        block type as a string, either 'leaf' or 'branch'.

    >>> get_root_block_type(1, 1)
    'leaf'
    >>> get_root_block_type(2, 10)
    'branch'
    """
    tree_height = get_tree_height(leaf_count, branch_capacity)
    if tree_height == 1:
        return 'leaf'
    else:
        return 'branch'


def iter_leaf_blocks(
        hash_func_code: int,
        digest_size: int,
        content_size: int,
        block_size: int,
        byte_stream: BinaryIO,
        store_block_func: Optional[
            Callable[[str, bytes, bytes], None]] = None) -> Iterator[bytes]:
    """Iterate through each leaf that the given stream would produce."""
    left_to_read = content_size
    while True:
        block = byte_stream.read(min(block_size, left_to_read))
        if not block:
            break
        left_to_read -= len(block)
        if store_block_func:
            block_hash = create_blockhash(hash_func_code, digest_size, block)
            store_block_func('leaf', block_hash, block)
        yield block


def iter_leaf_hashes(
        hash_func_code: int,
        digest_size: int,
        content_size: int,
        block_size: int,
        byte_stream: BinaryIO,
        digest_only=True,
        store_block_func: Optional[Callable[[str, bytes, bytes], None]] = None
) -> Iterator[bytes]:
    """Iterate through each leaf and return each leaf's blockhash digest."""
    return map(
        partial(
            create_blockhash,
            hash_func_code,
            digest_size,
            digest_only=digest_only),
        iter_leaf_blocks(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            content_size=content_size,
            block_size=block_size,
            byte_stream=byte_stream,
            store_block_func=store_block_func))


def join_treehash(
        hash_func_code: int,
        block_size: int,
        root_block_hash: bytes) -> bytes:
    """Construct a tree hash from individual components.

    Arguments:
        hash_func_code:
            Numeric ID of the hash function to use (blockhash hash func code).
        block_size:
            The maximum size each block can be.
        root_block_hash:
            The blockhash digest of the root block in the tree.

    Returns:
        Tree hash as a bytestring.
    """
    return encode_varint(hash_func_code) + \
        encode_varint(block_size) + root_block_hash


def split_treehash(treehash_bytes: bytes) -> Tuple[int, int, bytes]:
    """Split a tree hash into its components.

    Arguments:
        treehash_bytes:
            Tree hash in bytestring form.

    Returns:
        Tuple containing the following values:
            0: Hash function code (blockhash hash func code).
            1: block size.
            2: blockhash digest of the root block (not blockhash, only the
               digest).
    """
    treehash_bytes = BytesIO(treehash_bytes)
    hash_func_code = decode_varint(treehash_bytes)
    block_size = decode_varint(treehash_bytes)
    return hash_func_code, block_size, treehash_bytes.read()


def get_content_size(treehash_bytes: bytes) -> int:
    treehash_bytes = BytesIO(treehash_bytes)
    decode_varint(treehash_bytes)  # skip hash func code
    return decode_varint(treehash_bytes)  # return content size


def get_all_block_sizes(
        digest_size: int,
        content_size: int,
        block_size: int) -> Iterator[Tuple[int, int, int]]:
    # TODO: hopefully optimization is possible
    # TODO: hopefully simplification/tidy up is possible
    # no block
    if content_size == 0:
        return
    child_count = get_leaf_count(content_size, block_size)
    # single block
    if child_count == 1:
        yield 0, 0, content_size
        return
    # get capacity of branches
    branch_capacity = get_branch_capacity(block_size, digest_size)
    # track height of tree
    tree_height = get_tree_height(child_count, branch_capacity)
    tree_level = tree_height - 1
    # iterate over leaves
    _, remainder = divmod(content_size, block_size)
    for position in range(child_count):
        last = position == child_count - 1
        if last and remainder:
            yield tree_level, position, remainder
        else:
            yield tree_level, position, block_size
    # each iteration handles each layer of branches in the tree
    while True:
        tree_level -= 1
        # count number of children to put into this branch
        branch_count, remainder = divmod(child_count, branch_capacity)
        # if there's still more children we'll need another branch on
        # this level
        if remainder:
            branch_count += 1
        # add number of branches at this level to the total
        for position in range(branch_count):
            last = position == branch_count - 1
            if last:  # right-most block on this level of tree
                this_block_size = (remainder or branch_count) * digest_size
            else:
                this_block_size = branch_capacity * digest_size
            yield tree_level, position, this_block_size
        # only one branch at this level? that's the root node! done!
        if branch_count == 1:
            break
        # all the branches at this layer turn into children for the next
        child_count = branch_count


def get_specific_block_size(
        digest_size: int,
        content_size: int,
        block_size: int,
        tree_level: int,
        position: int) -> int:
    # TODO: please optimize this if possible
    for tl, pos, bs in get_all_block_sizes(
            digest_size, content_size, block_size):
        if tl == tree_level and pos == position:
            return bs
    raise ValueError("unable to get block size using these arguments")


def create_blocktree(
        hash_func_code: int,
        digest_size: int,
        block_size: int,
        byte_stream: BinaryIO,
        content_size: Optional[int] = None,
        store_block_func: Optional[
            Callable[[str, bytes, bytes], None]] = None) -> Tuple[int, bytes]:
    """Create leaves and branches from a given stream of bytes.

    Arguments:
        hash_func_code:
            Numeric ID of the hash function to use (blockhash hash func code).
        digest_size:
            Size of the hash digest (blockhash).
        block_size:
            Maximum size of both leaf and branch blocks.
        byte_stream:
            Binary stream to read bytes from, only `read(n)` is used.
        content_size:
            Number of bytes to read from stream, must be specified even
            if the entire stream is to be used.
        store_block_func:
            Function to use to store created blocks.

    Returns:
        Tuple containing content size and treehash of the created tree.
    """
    # content size unspecified? get it from `byte_stream`
    if content_size is None:
        init_pos = byte_stream.tell()  # return to this position afterwards
        byte_stream.seek(0, 2)  # seek to end of byte stream
        content_size = byte_stream.tell() - init_pos  # TODO: correct?
        byte_stream.seek(init_pos)  # time to return to initial position
        del init_pos
    # if content is small enough handle as a single-block tree
    if content_size == 0:  # empty content
        h = create_blockhash(hash_func_code, digest_size, b'', digest_only=True)
        if store_block_func:
            store_block_func('leaf', join_blockhash(hash_func_code, 0, h), b'')
    elif content_size <= block_size:  # fits in one block
        block = byte_stream.read(content_size)
        h = create_blockhash(
            hash_func_code, digest_size, block, digest_only=True)
        if store_block_func:
            store_block_func(
                'leaf', join_blockhash(hash_func_code, content_size, h), block)
    else:  # multi-block
        capacity = get_branch_capacity(block_size, digest_size)
        # get the first level of hash digests
        digests = iter_leaf_hashes(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            content_size=content_size,
            block_size=block_size,
            byte_stream=byte_stream,
            digest_only=True,
            store_block_func=store_block_func)
        # iterate over each level of digests until finished
        while True:
            # get all the hash digests for this branch
            branch = []
            for hd in digests:
                branch.append(hd)
            # hash the branch
            digests = []  # hash digests for the next iteration
            for block in groupiter(branch, capacity):
                block = b''.join(block)  # concatenated list of digests
                block_hash = create_blockhash(
                    hash_func_code, digest_size, block, digest_only=True)
                if store_block_func:
                    store_block_func(
                        'branch',
                        join_blockhash(hash_func_code, len(block), block_hash),
                        block)
                digests.append(block_hash)
            if len(digests) == 1:
                break
        assert len(digests) == 1
        h = digests[0]
    return content_size, join_treehash(hash_func_code, block_size, h)


def split_branch(digest_size: int, byte_stream: BinaryIO) -> Iterator[bytes]:
    """Split a branch block into hash digests.

    This is for the digest component of blockhashes only - not full blockhashes.

    Arguments:
        digest_size:
            Size of the hash digest (blockhash).
        byte_stream:
            Stream containing the branch's bytes.

    Returns:
        Generator that returns individual blockhash digests for each block
        referenced by the provided branch.
    """
    while True:
        block_hash_digest = byte_stream.read(digest_size)
        if block_hash_digest == b'':
            break
        if len(block_hash_digest) != digest_size:
            raise EOFError("ran out of bytes while reading block hash digest")
        yield block_hash_digest


def _process_block(
        hash_func_code: int,
        block_size: int,
        digest_size: int,
        block_hash_digest: bytes,
        content_size: int,
        tree_height: int,
        leaf_count: int,
        tree_level: int,
        position: int,
        branch_capacity: int,
        fetch_block_func: Callable[[str, bytes], bytes]) -> Iterator[bytes]:
    """Helper function called by `read_tree`."""
    # zero-length content has no branches or leaves
    if content_size == 0:
        return
    is_branch = content_size > block_size and tree_level < tree_height - 1
    if is_branch:  # is branch
        branch_size = count_children_in_branch(
            leaf_count=leaf_count,
            branch_capacity=branch_capacity,
            position=position,
            tree_level=tree_level) * digest_size
        assert branch_size > 0
        block_data = fetch_block_func(
            'branch',  # block type
            join_blockhash(hash_func_code, branch_size, block_hash_digest))
        stream = BytesIO(block_data)
        for offset, block_hash_digest in \
                enumerate(split_branch(digest_size, stream)):
            yield from _process_block(
                hash_func_code=hash_func_code,
                block_size=block_size,
                digest_size=digest_size,
                block_hash_digest=block_hash_digest,
                content_size=content_size,
                tree_height=tree_height,
                leaf_count=leaf_count,
                tree_level=tree_level + 1,
                position=(position * branch_capacity) + offset,
                branch_capacity=branch_capacity,
                fetch_block_func=fetch_block_func)
    else:  # block is a leaf
        # different block size for last leaf
        last = leaf_count == 0 or position == leaf_count - 1
        _, remainder = divmod(content_size, block_size)
        if last and remainder:
            block_size = remainder
        assert block_size > 0
        data = fetch_block_func(
            'leaf',
            join_blockhash(hash_func_code, block_size, block_hash_digest))
        yield data


def read_blocktree(
        content_size: int,
        treehash: bytes,
        fetch_block_func: Callable[[str, bytes], bytes]) -> Iterator[bytes]:
    """Iterate over every leaf in the tree."""
    hash_func_code, block_size, root_block_hash = \
        split_treehash(treehash)
    digest_size = len(root_block_hash)
    branch_capacity = get_branch_capacity(block_size, digest_size)
    branch_count, tree_height = get_branch_count_and_tree_height(
        leaf_count=get_leaf_count(content_size, block_size),
        branch_capacity=branch_capacity)
    yield from _process_block(
        hash_func_code=hash_func_code,
        block_size=block_size,
        digest_size=digest_size,
        block_hash_digest=root_block_hash,
        content_size=content_size,
        tree_height=tree_height,
        leaf_count=get_leaf_count(content_size, block_size),
        tree_level=0,  # tree position is 0-based
        position=0,  # think of it like x position
        branch_capacity=branch_capacity,
        fetch_block_func=fetch_block_func)


def read_blocktree_range(
        content_size: int,
        treehash: bytes,
        fetch_block_func: Callable[[str, bytes], bytes],
        offset: int = 0,
        limit: Optional[int] = None) -> Iterator[bytes]:
    """Iterate over all leaves within the specified range.

    This will slice leaves up to get only the requested range if necessary.
    """
    # TODO: make more efficient by not loading unnecessary blocks
    if limit:
        range_end_position = offset + limit
    else:
        range_end_position = None
    position = 0
    for block in read_blocktree(content_size, treehash, fetch_block_func):
        # update current position
        position += len(block)
        # slice the block's beginning
        if offset > 0:
            block_size = len(block)
            block = block[offset:]
            offset -= min(offset, block_size)
            del block_size
        # nothing of the block remaining? get the next one
        if not block:
            continue
        # slice the block's end
        if limit is not None:
            block = block[:limit]
        if block:
            yield block
        if limit is not None:
            limit -= len(block)
        # done if the first byte is after the end of the requested range
        # TODO: gt or gte?
        if range_end_position is not None and position > range_end_position:
            break


class BlockTreeIO:
    """File-like interface to read content stored in a tree."""

    def __init__(
            self,
            content_size: int,
            treehash: bytes,
            fetch_block_func: Callable[[str, bytes], bytes]):
        self.content_size = content_size
        self.treehash = treehash
        self.fetch_block_func = fetch_block_func
        self.reader = None
        self.position = 0
        self.buffer = b''

    def seek(self, offset: int, whence: int = 0) -> None:
        if whence == 0:  # absolute
            self._reset_reader(offset)
            return
        elif whence == 1:  # relative
            if offset == 0:
                return
            elif offset > 0:
                while offset > 0:
                    offset -= len(self.read(min(1024 * 256, offset)))
                assert offset == 0
                return
            elif offset < 0:
                self._reset_reader(self.position + offset)
                return
            else:
                raise ValueError('`offset` must be an integer')
        elif whence == 2:  # from end
            if offset > 0:
                raise ValueError("offset must be negative or zero")
            self._reset_reader(self.content_size + offset)
            return
        else:
            raise ValueError('invalid value for `whence`')

    def _reset_reader(self, offset: int) -> None:
        self.reader = read_blocktree_range(
            content_size=self.content_size,
            treehash=self.treehash,
            offset=offset,
            fetch_block_func=self.fetch_block_func)
        self.position = offset
        self.buffer = b''

    def tell(self) -> int:
        return self.position

    def read(self, num: Optional[int] = None) -> bytes:
        if num is None:
            num = self.content_size
        if not isinstance(num, int):
            raise ValueError("invalid value for `num`")
        if num < 0:
            raise ValueError("invalid value for `num`")
        if self.reader is None:
            self._reset_reader(0)
        while len(self.buffer) < num:
            try:
                self.buffer += next(self.reader)
            except StopIteration:
                break
        data = self.buffer[:num]
        self.buffer = self.buffer[num:]
        self.position += len(data)
        return data


def generate_random_pow_nonce(length: int) -> str:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def mine_random_pow(author_address: str, hash_type_chrp: str):
    best_pow_extension_power_level = 0
    while True:
        nonce = generate_random_pow_nonce(8)
        pow_extension = f"p{hash_type_chrp}{nonce}"
        power_level = get_power_level(author_address, pow_extension)
        if power_level > best_pow_extension_power_level:
            best_pow_extension_power_level = power_level
            yield pow_extension


def iter_to_queue(func, queue) -> None:
    for each in func():
        queue.put(each)


def get_pow_extensions(luckypost_str: str) -> Iterable[str]:
    for extension in get_extensions_from_luckypost(luckypost_str):
        if extension.startswith('p'):
            yield extension


def get_power_levels(luckypost_str: str) -> Dict[str, Tuple[int, str]]:
    result = {}
    author_address = verify_post(luckypost_str)
    for pow_extension in get_pow_extensions(luckypost_str):
        pow_hash_type = \
            read_chrp(pow_extension[1:].encode('utf-8')).decode('utf-8')
        power_level = get_power_level(author_address, pow_extension)
        if pow_hash_type not in result \
                or result[pow_hash_type][0] < power_level:
            result[pow_hash_type] = (power_level, pow_extension)
    return result


def main():
    # import doctest
    # doctest.testmod()
    import argparse
    import getpass
    import multiprocessing as mp

    def mine(mine_args):
        author_address = mine_args.author_address.strip().lstrip('@')
        hash_type_chrp = mine_args.hash_type
        print("Mining...")
        queue = mp.Queue()
        processes = []
        for _ in range(mp.cpu_count()):
            process = mp.Process(
                target=iter_to_queue,
                args=(
                    partial(mine_random_pow, author_address, hash_type_chrp),
                    queue),
                daemon=True)
            process.start()
            processes.append(process)
        best_power_level = 0
        try:
            while True:
                pow_extension = queue.get()
                power_level = get_power_level(author_address, pow_extension)
                if power_level > best_power_level:
                    best_power_level = power_level
                    print(pow_extension, power_level)
        except KeyboardInterrupt:
            print("Mining stopped by user's request.")

    def view(view_args):
        luckypost_str = view_args.luckypost
        verify_post(luckypost_str)
        plp = parse_luckypost(luckypost_str)
        luckypost_id = get_luckypost_id(luckypost_str)
        print(f"ID: {luckypost_id}")
        for pow_hash_type, (power_level, _) \
                in get_power_levels(luckypost_str).items():
            hash_type_name = HASH_TYPE_NAMES[pow_hash_type]
            print(f"POWER level ({hash_type_name}):", power_level)
        print('')
        print(f"{plp['timestamp']} {plp['channel']} {plp['author_name']}")
        for attachment in get_attachments_from_luckypost(luckypost_str):
            filename, metadata, size, treehash = attachment
            if metadata:
                metadata_str = ' '
            else:
                metadata_str = '(' + (','.join(metadata)) + ') '
            size_str = '{:,}'.format(size)
            print(f"\"{filename}\" {metadata_str}{size_str} {treehash}")
        for line in split_body_iter(plp['body']):
            print(line)
        print(get_footer_from_luckypost(luckypost_str).replace(' ', '\n'))

    def verify(verify_args):
        luckypost_str = verify_args.luckypost
        luckypost_id = get_luckypost_id(luckypost_str)
        try:
            verify_post(luckypost_str)
        except InvalidSignatureError:
            print("Authentication failure! Luckypost is corrupt or a forgery!")
            return
        print('Luckypost successfully authenticated!')
        print(f"ID: {luckypost_id}")
        for pow_hash_type, (power_level, _) \
                in get_power_levels(luckypost_str).items():
            hash_type_name = HASH_TYPE_NAMES[pow_hash_type]
            print(f"POWER level ({hash_type_name}):", power_level)

    def create(create_args):
        if create_args.passphrase:
            passphrase = create_args.passphrase
        else:
            passphrase = getpass.getpass("Passphrase: ")
        blocks = {}

        def store_block(_: str, blockhash: bytes, data: bytes) -> None:
            blocks[blockhash] = data
        attachments = []
        for attachment in create_args.attach_file:
            with open(attachment, 'rb') as f:
                content_size, root_hash = create_blocktree(
                    hash_func_code=int(create_args.attachment_hash_type),
                    digest_size=create_args.attachment_digest_length,
                    block_size=create_args.attachment_block_size,
                    byte_stream=f,
                    store_block_func=store_block)
                root_hash = lb32encode(root_hash)
                attachments.append(
                    (basename(f.name), [], content_size, root_hash))
        try:
            luckypost = create_luckypost(
                hash_type_chrp=create_args.hash_type,
                hash_digest_length=create_args.digest_length,
                signature_type_chrp=create_args.signature_type,
                passphrase=passphrase,
                timestamp=dt_to_timestamp(
                    datetime.utcnow(),
                    ignore_microseconds=True),
                channel=create_args.channel,
                author_name=create_args.author,
                attachments=attachments,
                body=create_args.body,
                extensions=create_args.extension)
        except InvalidAuthorNameError as e:
            parser.error(str(e))
            return
        print(luckypost)
        for blockhash_bytes, block_data in blocks.items():
            print(
                '#' +
                urlsafe_b64encode(blockhash_bytes).decode('utf-8').rstrip('=') +
                ':' +
                urlsafe_b64encode(block_data).decode('utf-8').rstrip('='))

    def body_type(body: str) -> str:
        try:
            validate_body_or_raise(body)
        except InvalidBodyError as e:
            parser.error(str(e))
        return body

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    view_subparser = subparsers.add_parser('view')
    view_subparser.set_defaults(func=view)
    view_subparser.add_argument('luckypost', help="luckypost")

    verify_subparser = subparsers.add_parser('verify')
    verify_subparser.set_defaults(func=verify)
    verify_subparser.add_argument('luckypost', help="luckypost")

    mine_subparser = subparsers.add_parser('mine')
    mine_subparser.set_defaults(func=mine)
    mine_subparser.add_argument(
        'hash_type',
        help="hash type chrp",
        metavar='hash-type')
    mine_subparser.add_argument(
        'author_address',
        help="author address",
        metavar='author-address')

    create_subparser = subparsers.add_parser('create')
    create_subparser.set_defaults(func=create)
    create_subparser.add_argument('channel', help="name of channel")
    create_subparser.add_argument('author', help="name of the author")
    create_subparser.add_argument(
        'body',
        help="body of the post",
        type=body_type)
    create_subparser.add_argument(
        '-t', '--hash-type',
        default='a',
        help="hash type of the post's ID")
    create_subparser.add_argument(
        '-l', '--digest-length',
        default=16,
        type=int,
        help="digest length used in the post's ID")
    create_subparser.add_argument(
        '-s', '--signature-type',
        default='a',
        help="type of encryption used to sign the post")
    create_subparser.add_argument(
        '-p', '--passphrase',
        default=None,
        help="passphrase to use to sign the post (otherwise will be prompted)")
    create_subparser.add_argument(
        '-a', '--attach-file',
        action="append",
        default=[],
        help="files to be attached")
    create_subparser.add_argument(
        '-at', '--attachment-hash-type',
        default=1,
        type=int,
        help="hash type of file attachments")
    create_subparser.add_argument(
        '-al', '--attachment-digest-length',
        default=16,
        type=int,
        help="digest length used for file attachments")
    create_subparser.add_argument(
        '-ab', '--attachment-block-size',
        default=1024,
        type=int,
        help="max size of attached file blocks")
    create_subparser.add_argument(
        '-x', '--extension',
        action="append",
        default=[],
        help="extensions")
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
