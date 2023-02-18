#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field


import argparse, sys, os.path
from galois_field import GFpn
from lib.wg_gf_lib import SimuGF

#----------------------------
def show_examples():
    scriptname = os.path.basename(__file__)
    sample=f"""
samples:
   {scriptname} 2 2 111 b w

   {scriptname} 2 3 1101 b w #basis=2 power=3 irr_poly=[1, 1, 0 ,1] #y^3=1+y^2 y^3-y^2-1=0
   {scriptname} 2 3 1011 b w

   {scriptname} 3 2 101 b w
   {scriptname} 3 2 112 b w
   {scriptname} 3 2 122 b w

   {scriptname} 5 2 102 b w
   """
    print(sample)


#----------------------------
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        show_examples()
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

#----------------------------
def parseargs():
    parser = ArgumentParser(description='List lexical sorted complete quadratic workshops with n*n persons and team size n.')
    parser.add_argument("p", help="basis (prim)")
    parser.add_argument("n", help="power")
    parser.add_argument("irr_poly", help="irregular polynom for construction of GF(p^n)")
    parser.add_argument("representation", help="representation 'b','i','m' binaer/index/modulo (where supported)")
    parser.add_argument("procedure", help="procedure 'w','op','w2','w2t'  wg/optables/w2/w2-test")
    parser.add_argument("-o","--ortho", help="orthogonal squares in procedure w2", required=False, action="store_true", default='False')
    parser.add_argument("-v", "--verbose", help="Verbose",
                        action="store_true")
    args = parser.parse_args()
    return args


#----------------------------
def main():
    args = parseargs()

    basis=int(args.p)
    power=int(args.n)
    irr_poly=[int(c) for c in args.irr_poly]
    representation = args.representation
    procedure = args.procedure
    verbose = args.verbose
    ortho = args.ortho
    if args.verbose:
        print(args)

    simu = SimuGF()
    simu.work(basis, power, irr_poly, representation=representation, procedure=procedure, ortho=ortho, verbose=verbose)


def demo():
    simu = SimuGF()
    representation='n'
    show='w2'
# Generating the field GF(2^3)
    basis=2
    power=3

    irr_poly=[1, 1, 0 ,1] #y^3=1+y^2 y^3-y^2-1=0

    simu.work(basis, power, irr_poly, representation, show)

    basis=2
    power=3
    irr_poly=[1, 0, 1 ,1] #x^3=1+1 x^3-x-1=0

    #GF(3^2)
    basis=3
    power=2
    irr_poly_f=[1, 0 ,1] #f=x^2+1
    irr_poly_g=[1, 1 ,2] #g=x^2+x-1
    irr_poly_h=[1, 2 ,2] #h=x^2-x-1

    simu.work(basis, power, irr_poly_f, representation, show)
    simu.work(basis, power, irr_poly_g, representation, show)
    simu.work(basis, power, irr_poly_h, representation, show)


if __name__ == '__main__':
    main()
    #demo()
