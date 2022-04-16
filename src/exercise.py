from ecc import FieldElement



def make_field(p):
    field = []
    for i in range(1, p):
        num = FieldElement(i, p)
        num = num**(p-1)
        field.append(num.num)
    return field

if __name__ == '__main__':
    num_list = [7, 11, 17, 31]
    for prime in num_list:
        print(make_field((prime)))