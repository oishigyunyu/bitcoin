# -*- coding:utf-8 -*-
from ecc import PrivateKey, Signature


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