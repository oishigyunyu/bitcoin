from tarfile import FIFOTYPE
from attr import field
from ecc import FieldElement

if __name__ == '__main__':
    prime = 31
    a = FieldElement(3, prime)
    b = FieldElement(24, prime)
    b_inv = b**(b.prime - 2)
    result = a * b_inv
    print(result)
    a = FieldElement(17, prime)
    a_inv = a**(a.prime - 2)
    result = a_inv**3
    print(result)
    a = FieldElement(4, prime)
    a_inv = a**(a.prime - 2)
    a = a_inv**4
    b = FieldElement(11, prime)
    result = a * b
    print(result)