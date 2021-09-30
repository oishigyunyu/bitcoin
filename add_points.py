from ecc import FieldElement, Point





if  __name__ == '__main__':
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    x = FieldElement(15, prime)
    y = FieldElement(86, prime)
    p = Point(x, y, a, b)
    one = p
    zero = FieldElement(0, prime)
    for i in range(1000):
        print(p+p)
        if p == zero:
            print(i+1)
            break