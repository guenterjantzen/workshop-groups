#!/usr/bin/env python3

import numpy as np
import pytest

from galois_field.core import validator

@pytest.mark.parametrize('poly, p, expected', [
    (np.poly1d([1] + (3-2)*[0]+[1]), 3, True),
    (np.poly1d([1] + (5-2)*[0]+[2]), 5, True),
    (np.poly1d([1] + (7-2)*[0]+[2]), 7, True),
    (np.poly1d([1] + (11-2)*[0]+[3]), 11, True),
    (np.poly1d([1] + (13-2)*[0]+[2]), 13, True),
    (np.poly1d([1] + (17-2)*[0]+[3]), 17, True),
    (np.poly1d([1] + (19-2)*[0]+[4]), 19, True),
    (np.poly1d([1] + (23-2)*[0]+[2]), 23, True),
    (np.poly1d([1] + (29-2)*[0]+[2]), 29, True),
    (np.poly1d([1] + (31-2)*[0]+[7]), 31, True),
    (np.poly1d([1] + (37-2)*[0]+[2]), 37, True),
    (np.poly1d([1] + (41-2)*[0]+[6]), 41, True),
    (np.poly1d([1] + (43-2)*[0]+[9]), 43, True),
    (np.poly1d([1] + (47-2)*[0]+[2]), 47, True),
    (np.poly1d([1] + (53-2)*[0]+[2]), 53, True),
    (np.poly1d([1] + (59-2)*[0]+[3]), 59, True),
    (np.poly1d([1] + (61-2)*[0]+[2]), 61, True),
    (np.poly1d([1] + (67-2)*[0]+[4]), 67, True),
    (np.poly1d([1] + (71-2)*[0]+[2]), 71, True),
    (np.poly1d([1] + (73-2)*[0]+[5]), 73, True),
    (np.poly1d([1] + (79-2)*[0]+[2]), 79, True),
    (np.poly1d([1] + (83-2)*[0]+[3]), 83, True),
    (np.poly1d([1] + (89-2)*[0]+[3]), 89, True),
    (np.poly1d([1] + (97-2)*[0]+[5]), 97, True),
])
def test_is_irreducible_poly(poly, p, expected):
    assert validator.is_irreducible_poly(poly, p) == expected
