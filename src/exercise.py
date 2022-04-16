from ecc import FieldElement

if __name__ == '__main__':
    prime = 19
    ks = [1, 3, 7, 13, 18]
    max_range = 18
    for k in ks:
        field = []
        for i in range(max_range + 1):
            field_elem = FieldElement(i, prime)
            field_elem = field_elem * FieldElement(k, prime)
            field.append(field_elem.num)
        print('k={}:'.format(k), field)