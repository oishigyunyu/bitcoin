from operator import truediv
import ecc
from helper import run
from typing import Any
from ecc import Point, FieldElement

def main() -> Any:
    run(ecc.ECCTest('test_on_curve'))


if __name__ == "__main__":
    points_list = [[[170, 142], [60, 139]],
              [[47, 71], [17, 56]],
              [[143, 98], [76, 66]]]
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    for i, points in enumerate(points_list):
        if i != 0:
        print(f'number: {i}')
        x1 = FieldElement(points[0][0], prime)
        y1 = FieldElement(points[0][1], prime)
        x2 = FieldElement(points[1][0], prime)
        y2 = FieldElement(points[1][1], prime)
        print(x1)
        print(x2)
        print(y1)
        print(y2)

        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        print(p1 + p2)
