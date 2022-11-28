from __future__ import annotations

import hashlib
import hmac
from random import randint
from typing import Union
from unittest import TestCase

from helper import encode_base58_checksum, hash160


class FieldElement:
    def __init__(self: FieldElement, num: int, prime: int):
        if num >= prime or num < 0:
            error: str = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num: int = num
        self.prime: int = prime

    def __repr__(self: FieldElement) -> str:
        return "FieldElement_{}({})".format(self.prime, self.num)

    def __eq__(self: FieldElement, other: FieldElement) -> bool:  # type: ignore[override]
        if isinstance(other, FieldElement):
            if other is None:
                return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self: FieldElement, other: FieldElement) -> bool:  # type: ignore[override]
        # this should be the inverse of the == operator
        return not (self == other)

    def __add__(self: FieldElement, other: FieldElement) -> FieldElement:
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num: int = (self.num + other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __sub__(self: FieldElement, other: FieldElement) -> FieldElement:
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num: int = (self.num - other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __mul__(self: FieldElement, other: FieldElement) -> FieldElement:
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num: int = (self.num * other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __pow__(self: FieldElement, exponent: int) -> FieldElement:
        n: int = exponent % (self.prime - 1)
        num: int = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self: FieldElement, other: FieldElement) -> FieldElement:
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        # use fermat's little theorem:
        # self.num**(p-1) % p == 1
        # this means:
        # 1/n == pow(n, p-2, p)
        num: int = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __rmul__(self: FieldElement, coefficient: int) -> FieldElement:
        num: int = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)


assert FieldElement.__add__.__annotations__ == {"other": "FieldElement"}


class FieldElementTest(TestCase):
    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        self.assertEqual(a + b, FieldElement(17, 31))
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_rmul(self):
        a = FieldElement(24, 31)
        b = 2
        self.assertEqual(b * a, a + a)

    def test_pow(self):
        a = FieldElement(17, 31)
        self.assertEqual(a**3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a**5 * b, FieldElement(16, 31))

    def test_div(self):
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a**-3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a**-4 * b, FieldElement(13, 31))


# tag::source1[]
class Point:
    def __init__(
        self: Point,
        x: Union[int, None],
        y: Union[int, None],
        a: Union[int, None],
        b: Union[int, None],
    ) -> None:
        self.a: Union[int, None] = a
        self.b: Union[int, None] = b
        self.x: Union[int, None] = x
        self.y: Union[int, None] = y
        if self.x is None and self.y is None:
            return
        if (
            self.y is not None
            and self.x is not None
            and a is not None
            and x is not None
        ):
            if self.y**2 != self.x**3 + a * x + b:
                raise ValueError("({}, {}) is not on the curve".format(x, y))

    # end::source1[]

    def __eq__(self: Point, other: Point) -> bool:  # type: ignore[override]
        return (
            self.x == other.x
            and self.y == other.y
            and self.a == other.a
            and self.b == other.b
        )

    def __ne__(self, other: Point) -> bool:  # type: ignore[override]
        # this should be the inverse of the == operator
        return not (self == other)

    def __repr__(self: Point) -> str:
        if self.x is None:
            return "Point(infinity)"
        elif isinstance(self.x, FieldElement):
            return "Point({},{})_{}_{} FieldElement({})".format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime
            )
        else:
            return "Point({},{})_{}_{}".format(self.x, self.y, self.a, self.b)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(
                "Points {}, {} are not on the same curve".format(self, other)
            )
        # Case 0.0: self is the point at infinity, return other
        if self.x is None:
            return other
        # Case 0.1: other is the point at infinity, return self
        if other.x is None:
            return self

        # Case 1: self.x == other.x, self.y != other.y
        # Result is point at infinity
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Case 2: self.x ≠ other.x
        # Formula (x3,y3)==(x1,y1)+(x2,y2)
        # s=(y2-y1)/(x2-x1)
        # x3=s**2-x1-x2
        # y3=s*(x1-x3)-y1
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        # Case 4: if we are tangent to the vertical line,
        # we return the point at infinity
        # note instead of figuring out what 0 is for each type
        # we just use 0 * self.x
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

        # Case 3: self == other
        # Formula (x3,y3)=(x1,y1)+(x1,y1)
        # s=(3*x1**2+a)/(2*y1)
        # x3=s**2-2*x1
        # y3=s*(x1-x3)-y1
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

    # tag::source3[]
    def __rmul__(self, coefficient):
        coef = coefficient
        current = self  # <1>
        result = self.__class__(None, None, self.a, self.b)  # <2>
        while coef:
            if coef & 1:  # <3>
                result += current
            current += current  # <4>
            coef >>= 1  # <5>
        return result


assert Point.__add__.__annotations__ == {"other": "Point"}
# end::source3[]


class PointTest(TestCase):
    def test_ne(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_on_curve(self):
        with self.assertRaises(ValueError):
            Point(x=-2, y=4, a=5, b=7)
        # these should not raise an error
        Point(x=3, y=-7, a=5, b=7)
        Point(x=18, y=77, a=5, b=7)

    def test_add0(self):
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        a = Point(x=-1, y=1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=-77, a=5, b=7))


# tag::source2[]
class ECCTest(TestCase):
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)  # <1>
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)  # <1>

    # end::source2[]

    def test_add(self):
        # tests the following additions on curve y^2=x^3-7 over F_223:
        # (192,105) + (17,56)
        # (47,71) + (117,141)
        # (143,98) + (76,66)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        additions = (
            # (x1, y1, x2, y2, x3, y3)
            (192, 105, 17, 56, 170, 142),
            (47, 71, 117, 141, 60, 139),
            (143, 98, 76, 66, 47, 71),
        )

        # loop over additions
        # initialize x's and y's as FieldElements
        # create p1, p2 and p3 as Points
        # check p1+p2==p3
        raise NotImplementedError

    def test_rmul(self):
        # tests the following scalar multiplications
        # 2*(192,105)
        # 2*(143,98)
        # 2*(47,71)
        # 4*(47,71)
        # 8*(47,71)
        # 21*(47,71)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            # (coefficient, x1, y1, x2, y2)
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            # initialize the second point based on whether it's the point at infinity
            if x2_raw is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)

            # check that the product is equal to the expected point
            self.assertEqual(s * p1, p2)


# tag::source6[]
A = 0
B = 7
# end::source6[]
# tag::source4[]
P = 2**256 - 2**32 - 977
# end::source4[]
# tag::source9[]
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# end::source9[]


# tag::source5[]
class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)

    def sqrt(self):
        return self ** ((P + 1) // 4)


# end::source5[]


# tag::source7[]
class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)  # <1>

    # end::source7[]

    def __repr__(self):
        if self.x is None:
            return "S256Point(infinity)"
        else:
            return "S256Point({}, {})".format(self.x, self.y)

    # tag::source8[]
    def __rmul__(self, coefficient):
        coef = coefficient % N  # <1>
        return super().__rmul__(coef)

    # end::source8[]

    # tag::source12[]
    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)  # <1>
        u = z * s_inv % N  # <2>
        v = sig.r * s_inv % N  # <3>
        total = u * G + v * self  # <4>
        return total.x.num == sig.r  # <5>

    def sec(self, compressed=True):
        if compressed:
            if self.y.num % 2 == 0:
                return b"\x02" + self.x.num.to_bytes(32, "big")
            else:
                return b"\x03" + self.x.num.to_bytes(32, "big")
        else:
            return (
                b"\x04"
                + self.x.num.to_bytes(32, "big")
                + self.y.num.to_bytes(32, "big")
            )

    @classmethod
    def parse(cls, sec_bin):
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], "big")
            y = int.from_bytes(sec_bin[33:65], "big")
        is_even = sec_bin[0] == 2

        x = S256Field(int.from_bytes(sec_bin[1:], "big"))
        # y^2 = x^3 + 7の右辺の計算
        alpha = x**3 + S256Field(B)
        # 左辺を解く
        beta = alpha.sqrt()
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        else:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta

        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b"\x6f"
        else:
            prefix = b"\x00"

        return encode_base58_checksum(prefix + h160)


# tag::source10[]
G = S256Point(
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)
# end::source10[]


class S256Test(TestCase):
    def test_order(self):
        point = N * G
        self.assertIsNone(point.x)

    def test_pubpoint(self):
        # write a test that tests the public point for the following
        points = (
            # secret, x, y
            (
                7,
                0x5CBDF0646E5DB4EAA398F365F2EA7A0E3D419B7E0330E39CE92BDDEDCAC4F9BC,
                0x6AEBCA40BA255960A3178D6D861A54DBA813D0B813FDE7B5A5082628087264DA,
            ),
            (
                1485,
                0xC982196A7466FBBBB0E27A940B6AF926C1A74D5AD07128C82824A11B5398AFDA,
                0x7A91F9EAE64438AFB9CE6448A1C133DB2D8FB9254E4546B6F001637D50901F55,
            ),
            (
                2**128,
                0x8F68B9D2F63B5F339239C1AD981F162EE88C5678723EA3351B7B444C9EC4C0DA,
                0x662A9F2DBA063986DE1D90C2B6BE215DBBEA2CFE95510BFDF23CBF79501FFF82,
            ),
            (
                2**240 + 2**31,
                0x9577FF57C8234558F293DF502CA4F09CBC65A6572C842B39B366F21717945116,
                0x10B49C67FA9365AD7B90DAB070BE339A1DAF9052373EC30FFAE4F72D5E66D053,
            ),
        )

        # iterate over points
        for secret, x, y in points:
            # initialize the secp256k1 point (S256Point)
            point = S256Point(x, y)
            # check that the secret*G is the same as the point
            self.assertEqual(secret * G, point)

    def test_verify(self):
        point = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        r = 0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395
        s = 0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4
        self.assertTrue(point.verify(z, Signature(r, s)))
        z = 0x7C076FF316692A3D7EB3C3BB0F8B1488CF72E1AFCD929E29307032997A838A3D
        r = 0xEFF69EF2B1BD93A66ED5219ADD4FB51E11A840F404876325A1E8FFE0529A2C
        s = 0xC7207FEE197D27C618AEA621406F6BF5EF6FCA38681D82B2F06FDDBDCE6FEAB6
        self.assertTrue(point.verify(z, Signature(r, s)))


# tag::source11[]
class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature({:x},{:x})".format(self.r, self.s)

    def der(self):
        rbin = self.r.to_bytes(32, byteorder="big")
        rbin = rbin.lstrip(b"\x00")
        if rbin[0] & 0x80:
            rbin = b"\x00" + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, byteorder="big")
        sbin = sbin.lstrip(b"\x00")
        if sbin[0] & 0x80:
            sbin = b"\x00" + sbin
        result += bytes([2, len(sbin)]) + sbin

        return bytes([0x30, len(result)]) + result


# end::source11[]


# tag::source13[]
class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G  # <1>

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    # end::source13[]

    # tag::source14[]
    def sign(self, z):
        k = self.deterministic_k(z)  # <1>
        r = (k * G).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret.to_bytes(32, "big")
        s256 = hashlib.sha256
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if candidate >= 1 and candidate < N:
                return candidate  # <2>
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, "big")
        if testnet:
            prefix = b"\xef"
        else:
            prefix = b"\x80"
        if compressed:
            suffix = b"\x01"
        else:
            suffix = b""

        return encode_base58_checksum(prefix + secret_bytes + suffix)


class PrivateKeyTest(TestCase):
    def test_sign(self):
        pk = PrivateKey(randint(0, N))
        z = randint(0, 2**256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))
