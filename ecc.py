from unittest import TestCase
from field_element import FieldElement
from point import Point


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
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = y
        self.y = y

        if self.x is None and self.y is None:
            return
        
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve.'.format(x, y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not(self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise ValueError('Points {}, {} are not on the same curve.'.format(self, other))
        
        if self.x is None:
            return other
        
        if other.x is None:
            return self
        
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)


if __name__ == '__main__':
    a, b = 5, 7
    x1, y1 = -1, -1
    x2, y2 = -1, -1
    s = (3 * x1**2 +a) / (2 * y1)
    x3 = s**2 - 2 * x1
    y3 = s * (x1 - x3) - y1
    print(f'x3:{x3}, y3:{y3}')


class FieldElement:
    def __init__(self, num: int, prime: int):
        if num >= prime or num < 0:
            error = 'Num {} not in field ranfe 0 to {}'.format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self) -> str:
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other: any) -> bool:
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other: any) -> bool:
        if other is None:
            return False
        return self.num != other.num and self.prime != other.prime

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields.')
        num = (self.num + other.num) % self.prime
        return __class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields.')
        num = (self.num - other.num) % self.prime
        return __class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields.')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        #  num = (self.num ** exponent) % self.prime
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truedev__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields.')
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)


if __name__ == '__main__':
    prime = 31
    print(3*pow(24, prime-2, prime) % prime)
    print(pow(17, prime-4) % prime)
    print(pow(4, prime- 5, prime) * 11 % prime)