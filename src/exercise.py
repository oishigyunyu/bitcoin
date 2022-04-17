from operator import truediv
import ecc
from helper import run
from typing import Any

def main() -> Any:
    run(ecc.ECCTest('test_on_curve'))

if __name__ == "__main__":
    main()