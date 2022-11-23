from ecc import PrivateKey
if __name__ == "__main__":
    secret = "secretsecretsecret"
    priv = PrivateKey(secret)
    pub_address = priv.point.address(compressed=True, testnet=True)
    print(pub_address)
