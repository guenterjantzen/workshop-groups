#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field


import argparse, sys, os.path, math
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
    parser = ArgumentParser(description='List lexical sorted workshops without pair repetition')
    parser.add_argument("p", help="basis (prim)")
    parser.add_argument("n", help="power")
    #parser.add_argument("N", help="Number of Participants", type=int)
    parser.add_argument("-ms","--maxsize", nargs='?', help="max teamsize", type=int)
    parser.add_argument("-gc", "--groupcount", nargs='?', help="nr of teams ", type=int)

    parser.add_argument("irr_poly", help="irregular polynom for construction of GF(p^n)")
    parser.add_argument("representation", help="representation 'b','i','m' binaer/index/modulo (where supported)")
    parser.add_argument("procedure", help="procedure 'w','op','w2','w2t'  wg/optables/w2/w2-test")
    parser.add_argument("-o","--ortho", help="orthogonal squares in procedure w2", required=False, action="store_true", default='False')
    parser.add_argument("-v", "--verbose", help="Verbose",
                        action="store_true")
    args = parser.parse_args()

    #./wg_gf.py 2 2 111 n w2 --ma 4

    return args

#----------------------------
def evaluate_some_args(args):
    print(4711, args)

    maxsize = args.maxsize
    groupcount = args.groupcount

    basis=int(args.p)
    power=int(args.n)
    N = basis**power

    assert maxsize or groupcount

    def calc_group_size_bounds(N, groupcount, max_size_to_check=None):
        n_div_gc, rest = divmod(N, groupcount)
        if rest == 0:
            maxsize = n_div_gc
        else:
            maxsize = n_div_gc + 1

        if max_size_to_check:
            assert max_size_to_check == maxsize, (f'max group size should be {max_size_to_check}, not {maxsize}')

        minsize = maxsize -1
        return minsize, maxsize, n_div_gc, rest

    if maxsize and not groupcount:
        groupcount = math.ceil(N/maxsize)
    minsize, maxsize, n_div_gc, rest = calc_group_size_bounds(N, groupcount, maxsize)

    nmin = groupcount - rest
    nmax = rest
    partition = nmin * [n_div_gc] + nmax * [n_div_gc + 1]
    partition = '-'.join([str(m) for m in partition])

    return basis, power, N, maxsize, groupcount, partition

#----------------------------
def main():
    args = parseargs()
    basis, power, N, maxsize, groupcount, partition = evaluate_some_args(args)
    print(4720, f'N={N}, maxsize={maxsize}, groupcount={groupcount} partition={partition}')
    #basis, power, delta_part = calc_parameters(args)


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
