from ecc import PrivateKey, Signature

if __name__ == "__main__":
    r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
    s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
    sig = Signature(r, s)
    print(sig.der().hex())