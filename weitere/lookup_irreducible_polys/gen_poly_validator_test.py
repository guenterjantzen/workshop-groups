#!/usr/bin/env python3

import numpy as np
from galois_field.core import validator

def experiment(fw):
    primes = [n for n in range(2,100) if validator.is_prime(n)]
    for p in primes:
        for i in range (1,p):
            poly_array = [1] + (p-2)*[0]+[i]
            poly = np.poly1d(poly_array)
            is_irreducible = validator.is_irreducible_poly(poly, p)
            if is_irreducible:
                print (p, poly_array)
                fw.write(f"    (np.poly1d([1] + ({p}-2)*[0]+[{i}]), {p}, True),\n")
                break

HEADER="""#!/usr/bin/env python3

import numpy as np
import pytest

from galois_field.core import validator

@pytest.mark.parametrize('poly, p, expected', [
"""

FOOTER="""])
def test_is_irreducible_poly(poly, p, expected):
    assert validator.is_irreducible_poly(poly, p) == expected
"""

def main():
    with open('poly_validator_test.py', 'w') as fw:
        fw.write(HEADER)
        experiment(fw)
        fw.write(FOOTER)
if __name__ == '__main__':
    main()
