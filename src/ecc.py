from __future__ import annotations
from typing import Any, Union
from unittest import TestCase
import sys
from random import randint
from regex import R

sys.setrecursionlimit(10000)


class FieldElement:
    def __init__(self, num: int, prime: int) -> None:
        if num >= prime or num < 0:
            error = "Num {} not in field in range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self) -> str:
        return "Field Element_{}({})".format(self.prime, self.num)

    def __eq__(self, other: "FieldElement") -> bool:
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime
    

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __add__(self, other: "FieldElement") -> "FieldElement":
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in differnt Fields")
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other: "FieldElement") -> "FieldElement":
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in differnt Fields")
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        if self.prime != other.prime:
            raise TypeError("Cannot multiple two numbers in differnt Fields")
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent: int) -> "FieldElement":
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        if self.prime != other.prime:
            raise TypeError("Cannot add divide numbers in differnt Fields")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)


class Point:
    def __init__(
        self,
        x: Any,
        y: Any,
        a: Any,
        b: Any,
    ) -> None:
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError("({}, {}) is not on the curve.".format(x, y))

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b

    def __ne__(self, other: "Point") -> bool:
        return not (self == other)
    
    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))
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
    
    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result

P = 2**256 - 2**32 - 977

N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

A = 0
B = 7

class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)
    
    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)


class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        
        else:
            super().__init__(x=x, y=y, a=a, b=b)
    
    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * G + v * self
        return total.x.num == sig.r

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s
    
    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N-1)
        r = (k * G).x.num
        k_inv = pow(k, N-2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

class ECCTest(TestCase):
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invaild_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
            
        for x_raw, y_raw in invaild_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1s = [[170, 142], [47, 71], [143, 98]]
        p2s = [[60, 139], [17, 56], [76, 66]]
    
        for i in range(len(p1s)):
            x1 = FieldElement(p1s[i][0], prime)
            y1 = FieldElement(p1s[i][1], prime)
            x2 = FieldElement(p2s[i][0], prime)
            y2 = FieldElement(p2s[i][1], prime)
            p1 = Point(x1, y1, a, b)
            p2 = Point(x2, y2, a, b)
            print(p1+p2)
