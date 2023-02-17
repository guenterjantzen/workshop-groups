#!/usr/bin/env python3

import numpy as np
#import pytest

from galois_field.core import validator

#@pytest.mark.parametrize('poly, p, expected', [
#    (np.poly1d([1] + (3-2)*[0]+[1]), 3, True),
#    (np.poly1d([1] + (5-2)*[0]+[2]), 5, True),
#    (np.poly1d([1] + (7-2)*[0]+[2]), 7, True),
#])
def is_irreducible_poly(p, poly_array):
    poly = np.poly1d(poly_array)
    print(f'-------{p}-------')
    print(poly)
    print (validator.is_irreducible_poly(poly, p))
    print()

def main():
    is_irreducible_poly(2, [1,1,1])
    is_irreducible_poly(3, [1,1,2])      #x^2+x+2
    is_irreducible_poly(2, [1,0,0,0,1])  #x^4+1


main()
