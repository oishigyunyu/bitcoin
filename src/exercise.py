from ecc import PrivateKey, Signature
from helper import encode_base58
if __name__ == "__main__":
    secret = "secretsecretsecret"
    priv = PrivateKey(secret)
    pub_address = priv.point.address(compressed=True, testnet=True)
    print(pub_address)