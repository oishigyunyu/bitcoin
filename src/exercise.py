from ecc import PrivateKey

if __name__ == "__main__":
    nums = [5001, 2019**5, 0xdeadbeef54321]
    for num in nums:
        priv = PrivateKey(num)
        print(num, ' -> ', priv.point.sec(compressed=True).hex())

