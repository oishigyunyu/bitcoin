# -*- coding:utf-8 -*-
from ecc import PrivateKey


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