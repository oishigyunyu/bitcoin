from ecc import S256Point, G, N
from helper import hash256


def check_hash(p, z, r, s):
    s_inv = pow(s, N - 2, N)
    u = z * s_inv % N
    v = r * s_inv % N
    return (u * G + v * p).x.num == r


if __name__ == '__main__':
    e = 12345
    z = int.from_bytes(hash256(b'Programming Bitcoin!'), 'big')
    k = 1234567890
    r = (k * G).x.num
    k_inv = pow(k, N - 2, N)
    s = (z + r * e) * k_inv % N
    point = e * G
    print(point)
    print(hex(z))
    print(hex(r))
    print(hex(s))
