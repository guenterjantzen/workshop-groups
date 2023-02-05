#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn

from lib.wg_gf_lib import SimuGF

def parseargs():
    parser = argparse.ArgumentParser(description='GF Tables ')
    parser.add_argument("p", help="basis (prim)")
    parser.add_argument("n", help="power")
    parser.add_argument("i", help="irr poly")
    parser.add_argument("r", help="Darstellung 'b' oder 'i' binaer/index)")
    parser.add_argument("-O", "--ops", help="show optables",action="store_true")
    args = parser.parse_args()
    return args

#----------------------------

def main():
    scriptname = os.path.basename(__file__)
    sample=f"""
Beispiele:
    {scriptname} 2 2 111 b

    {scriptname} 2 3 1101 b  #basis=2 power=3 irr_poly=[1, 1, 0 ,1] #y^3=1+y^2 y^3-y^2-1=0
    {scriptname} 2 3 1011 b

    {scriptname} 3 2 112 b
    {scriptname} 3 2 122 b
    """
    print(sample)

    args = parseargs()
    print(args)

    p,n,i,r,show_ops = args.p, args.n, args.i, args.r, args.ops

    basis=int(p)
    power=int(n)
    irr_poly=[int(c) for c in i]
    representation = args.r
    simu = SimuGF()
    simu.work(basis, power, irr_poly, representation, show_ops)


def demo():
    simu = SimuGF()
    representation='n'
# Generating the field GF(2^3)
    basis=2
    power=3

    irr_poly=[1, 1, 0 ,1] #y^3=1+y^2 y^3-y^2-1=0

    simu.work(basis, power, irr_poly, representation)

    basis=2
    power=3
    irr_poly=[1, 0, 1 ,1] #x^3=1+1 x^3-x-1=0

    #GF(3^2)
    basis=3
    power=2
    irr_poly_f=[1, 0 ,1] #f=x^2+1
    irr_poly_g=[1, 1 ,2] #g=x^2+x-1
    irr_poly_h=[1, 2 ,2] #h=x^2-x-1

    simu.work(basis, power, irr_poly_f, representation)
    simu.work(basis, power, irr_poly_g, representation)
    simu.work(basis, power, irr_poly_h, representation)


if __name__ == '__main__':
    main()
    #demo()
