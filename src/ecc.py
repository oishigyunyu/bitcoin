from __future__ import annotations

from typing import Union


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
        result = self.num == other.num and self.prime == other.prime
        return result

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
        x: Union[int, float, None],
        y: Union[int, float, None],
        a: Union[int, float, None],
        b: Union[int, float, None],
    ) -> None:
        self.a: Union[int, float, None] = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        elif self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError("({}, {}) is not on the curve.".format(x, y))

    def __eq__(self, other: "Point") -> bool:
        return self == other

    def __ne__(self, other: "Point") -> bool:
        return not (self == other)

    def __add__(self, other: "Point") -> Union["Point", None]:
        if self.a != other.a or self.b != other.b:
            raise TypeError(
                "Points {}, {} are not on the same curve.".format(self, other)
            )
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            s: float = (other.y - self.y) / (other.x - self.y)
            x: float = s ** 2 - self.x - other.x
            y: float = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        if self == other:
            s_eq: float = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x_eq: float = s_eq ** 2 - 2 * self.x
            y_eq: float = s_eq * (self.x - x) - self.y
            return self.__class__(x_eq, y_eq, self.a, self.b)
        if self == other and self.y == other.y:
            return self.__class__(None, None, self.a, self.b)
