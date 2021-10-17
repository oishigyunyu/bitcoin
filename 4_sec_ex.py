from ecc import PrivateKey


a = PrivateKey(5000)
print(a.point.sec.hex())