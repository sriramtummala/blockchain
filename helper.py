from unittest import TestSuite, TextTestRunner
import hashlib
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)


def hash256(s):
    # two rounds of sha256
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hash160(s):
    # sha256 followed by ripemd160
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def encode_base58(s):
    count = 0
    for c in s:  # <1>
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result  # <3>


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])


def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, 'big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:4]))
    return combined[1:-4]


def little_endian_to_int(b):
    # little_endian_to_int takes byte sequence as a little-endian number.
    # Returns an integer
    return int.from_bytes(b, 'little')


def int_to_little_endian(n, length):
    # endian_to_little_endian takes an integer and returns the little-endian
    # byte sequence of length
    return n.to_bytes(length, 'little')

# completed part 1 #
