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


   https://mast.queensu.ca/~math211/M211OH/m211og43.pdf
   https://mathworld.wolfram.com/IrreduciblePolynomial.html
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
    parser = ArgumentParser(description='GF Tables ')
    parser.add_argument("p", help="basis (prim)")
    parser.add_argument("n", help="power")
    parser.add_argument("i", help="irr poly")
    parser.add_argument("r", help="Darstellung 'b' oder 'i' binaer/index")
    parser.add_argument("s", help="Darstellung 'w','o','w2'  wg/optables/test (w2 ignores arg r)")
    parser.add_argument("-v", "--verbose", help="Ausführlichere Anzeige",
                        action="store_true")
    args = parser.parse_args()
    return args


#----------------------------
def main():
    args = parseargs()

    basis=int(args.p)
    power=int(args.n)
    irr_poly=[int(c) for c in args.i]
    representation = args.r
    show = args.s
    verbose=args.verbose
    simu = SimuGF()
    simu.work(basis, power, irr_poly, representation, show, verbose)


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
