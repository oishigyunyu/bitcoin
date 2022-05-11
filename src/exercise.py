from operator import truediv
from tarfile import FIFOTYPE
import ecc
from helper import run
from typing import Any
from ecc import Point, FieldElement

def main() -> Any:
    run(ecc.ECCTest('test_on_curve'))


if __name__ == "__main__":
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    x1 = FieldElement(192, prime)
    y1 = FieldElement(105, prime)
    x2 = FieldElement(17, prime)
    y2 = FieldElement(56, prime)
    p1 = Point(x1, y1, a, b)
    p2 = Point(x2, y2, a, b)
    print(p1+p2)
    print('---')
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

    

