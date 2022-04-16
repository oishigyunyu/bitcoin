from ecc import FieldElement, Point

if __name__ == "__main__":
    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)
    x = FieldElement(15, prime)
    y = FieldElement(86, prime)
    p = Point(x, y, a, b)
    print(2 * p)
