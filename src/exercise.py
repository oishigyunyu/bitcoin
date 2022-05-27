from ecc import PrivateKey

if __name__ == "__main__":
    nums = [5000, 2018**5, 0xdeadbeef12345]
    for num in nums:
        priv = PrivateKey(num)
        print(num, ' -> ', priv.point.sec().hex())

