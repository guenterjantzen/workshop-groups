#!/usr/bin/env python3

polydata = [
(2,2,111),

(2,3,1101),
(2,3,1011),
(2,4,10011),
(2,5,100101),

(3,2,101),
(3,2,112),
(3,2,122),

(5,2,102),
(5,2,103),
(5,2,111),
(5,2,141),
(5,2,112),
(5,2,142),
(5,2,123),
(5,2,133),
(5,2,124),
(5,2,134)
]

#https://mast.queensu.ca/~math211/M211OH/m211og43.pdf
#https://mathworld.wolfram.com/IrreduciblePolynomial.html


for polydate in polydata:
    if polydate:
        assert len(polydate)==3, polydate
        basis, power, irr_poly=polydate
        print(f'./wg_gf.py {basis**power} --irr_poly {irr_poly} -rc -pop')
