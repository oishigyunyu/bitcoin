import ecc
from helper import run

if __name__ == "__main__":
    run(ecc.ECCTest("test_on_curve"))
    run(ecc.ECCTest("test_add"))
