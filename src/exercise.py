from ecc import PrivateKey, Signature
from helper import encode_base58
if __name__ == "__main__":
    priv = PrivateKey(5002)
    print(priv.point.address(compressed=False, testnet=True))
    priv = PrivateKey(2020**5)
    print(priv.point.address(compressed=True, testnet=True))
    priv = PrivateKey(0x12345deadbeaf)
    print(priv.point.address(compressed=True, testnet=False))
