from ecc import FieldElement, Point





if  __name__ == '__main__':
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    x1 = FieldElement(170, prime)
    y1 = FieldElement(142, prime)
    x2 = FieldElement(60, prime)
    y2 = FieldElement(139, prime)
    p1 = Point(x1, y1, a, b)
    p2 = Point(x2, y2, a, b)
    print(p1+p2)
    print('---------------------')
    x1 = FieldElement(47, prime)
    y1 = FieldElement(71, prime)
    x2 = FieldElement(17, prime)
    y2 = FieldElement(56, prime)
    p1 = Point(x1, y1, a, b)
    p2 = Point(x2, y2, a, b)
    print(p1+p2)
    print('---------------------')
    x1 = FieldElement(143, prime)
    y1 = FieldElement(98, prime)
    x2 = FieldElement(76, prime)
    y2 = FieldElement(66, prime)
    p1 = Point(x1, y1, a, b)
    p2 = Point(x2, y2, a, b)
    print(p1+p2)
    print('---------------------')