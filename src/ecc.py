class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num {} not in field in range 0 to {}'.format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime
    
    def __repr__(self):
        return 'Field Element_{}({})'.format(self.prime, self.num)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not(self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime) 
    
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in differnt Fields')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiple two numbers in differnt Fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        num = pow(self.num, exponent, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add divide numbers in differnt Fields')
        other_inv = pow(other.num, self.prime - 2, self.prime)
        num = (self.num * other_inv.num) % self.prime
        return self.__class__(num, self.prime)