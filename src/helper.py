from base64 import encode
from unittest import TestSuite, TextTestRunner
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58(s):
    count = 0
    for c in s:
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

    return prefix + result 

def encode_base58_checksum(b):
    return encode_base58((b + hash256(b)[:4]))

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def little_endian_to_int(x):
    return int.from_bytes(x, 'little')
    
def int_to_little_endian(x, length):
    return x.to_bytes(length, 'little')

def read_variant(s):
    '''
    ストリームからの可変長の整数を読み取る
    '''
    i = s.read(1)[0]
    if i == 0xfd:
        # 0x2dは次の2バイトが整数なのを示す
        return little_endian_to_int(s.read(2))
    
    elif i == 0xfe:
        # 0x2dは次の4バイトが整数なのを示す
        return little_endian_to_int(s.read(4))

    elif i == 0xff:
        # 0x2dは次の8バイトが整数なのを示す
        return little_endian_to_int(s.read(8))
    
    else:
        # このほかは単なる整数
        return i

def encode_variant(i):
    '''
    整数をvariantとしてエンコードする
    '''
    if i < 0xfd:
        return bytes([i])
    
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)

    elif i < 0x100000000:
        return b'\xfd' + int_to_little_endian(i, 4)

    elif i < 0x10000000000000000:
        return b'\xfd' + int_to_little_endian(i, 8)
    
    else:
        raise ValueError('integer too large: {}'.format(i))
