from operator import truediv
from ecc import Point, FieldElement

def solve(x: int, y: int) -> bool:
    prime: int = 223
    left: int = y**2 % prime
    right: int = (x**3 + 7) % prime
    if left == right:
        return True
    else:
        return False

if __name__ == "__main__":
    points = [[192, 105], [17, 56], [200, 119], [1, 193], [42, 99]]
    for i, point in enumerate(points):
        result = solve(point[0], point[1])
        print(i, result)