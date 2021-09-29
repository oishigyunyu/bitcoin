from ecc import FieldElement, Point





if  __name__ == '__main__':
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    x1 = FieldElement(192, prime)
    y1 = FieldElement(105, prime)
    x2 = FieldElement(17, prime)
    y2 = FieldElement(56, prime)
    p1 = Point(x1, y1, a, b)
    p2 = Point(x2, y2, a, b)
    print(p1)
    print(p2)
    add = p1+p2
    print(add)