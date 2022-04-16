from ecc import FieldElement

if __name__ == '__main__':
    prime = 97
    print(FieldElement(95, prime) * FieldElement(45, prime) * FieldElement(31, prime))
    print(FieldElement(17, prime) * FieldElement(13, prime) * FieldElement(19, prime) * FieldElement(44, prime))
    print((FieldElement(12, prime)**7) * (FieldElement(77, prime)**49))