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
    x1 = FieldElement(47, prime)
    y1 = FieldElement(71, prime)
    p1 = Point(x1, y1, a, b)
    
    for i in range(1,21):
        result = float(i) * p1
        print(result)
        

    

