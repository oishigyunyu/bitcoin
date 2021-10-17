# -*- coding:utf-8 -*-
from ecc import PrivateKey, Signature
from helper import encode_base58

a = PrivateKey(5000)
a = a.point.sec(compressed=False)
print(a.hex())

a = PrivateKey(2018**5)
a = a.point.sec(compressed=False)
print(a.hex())

a = PrivateKey(0xdeadbeef12345)
a = a.point.sec(compressed=False)
print(a.hex())

a = PrivateKey(5001)
a = a.point.sec(compressed=True)
print(a.hex())

a = PrivateKey(2019**5)
a = a.point.sec(compressed=True)
print(a.hex())

a = PrivateKey(0xdeadbeef54321)
a = a.point.sec(compressed=True)
print(a.hex())

print('--------')
print('ex3')

r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

a = Signature(r, s)
a = a.der()
print(a.hex())

print('-----------')
print('ex4')
h = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
print(encode_base58(bytes.fromhex(h)))

h = 'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c'
print(encode_base58(bytes.fromhex(h)))

h = 'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6'
print(encode_base58(bytes.fromhex(h)))

print('--------------')
print('ex5')

a = PrivateKey(5002)
a = a.point.adress(compressed=False, testnet=True)
print(a)

a = PrivateKey(2020**5)
a = a.point.adress(testnet=True)
print(a)

a = PrivateKey(0x12345deadbeef)
a = a.point.adress(testnet=False)
print(a)

print('-------------------')
print('ex5')

a = PrivateKey(5003)
a.point.adress(compressed=False, testnet=True)
print(a.wif(compressed=True, testnet=True))

a = PrivateKey(2021**5)
a.point.adress(testnet=True)
print(a.wif(compressed=False, testnet=True))

a = PrivateKey(0x54321deadbeef)
a.point.adress(testnet=False)
print(a.wif(compressed=True, testnet=False))
