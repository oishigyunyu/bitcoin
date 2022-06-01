from ecc import PrivateKey, Signature
from helper import encode_base58
if __name__ == "__main__":
    priv = PrivateKey(5003)
    print(priv.wif(compressed=True, testnet=True))
    priv = PrivateKey(2021**5)
    print(priv.wif(compressed=False, testnet=True))
    priv = PrivateKey(0x54321deadbeaf)
    print(priv.wif(compressed=True, testnet=False))
