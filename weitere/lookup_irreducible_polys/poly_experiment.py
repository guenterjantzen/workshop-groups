#!/usr/bin/env python3

import numpy as np
from galois_field.core import validator

def experiment(rng):
    primes = [n for n in rng if validator.is_prime(n)]
    for p in primes:
        for i in range (1,p):
            poly_array = [1] + (p-2)*[0]+[i]
            poly = np.poly1d(poly_array)
            is_irreducible = validator.is_irreducible_poly(poly, p)
            if is_irreducible:
                print (p, poly_array)
                break

def main():
    experiment(range(2,100))

if __name__ == '__main__':
    main()
