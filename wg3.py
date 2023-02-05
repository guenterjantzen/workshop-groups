#!/usr/bin/env python3

import argparse
from lib.simu import Simu

#----------------------------
def parseargs(choices):
    parser = argparse.ArgumentParser(description='List lexical sorted complete quadratic workshops with n*n persons and team size n.')
    parser.add_argument("n", help="team size ",
                        type=int, choices=choices)

    parser.add_argument("-f", "--first", help="show only the first solution found",
                        action="store_true")

    parser.add_argument("-m", "--mod", help="show all values mod n",
                        action="store_true")

    parser.add_argument("-s", "--sym", help="other row sort for detecting symmetries",
                        action="store_true")

    parser.add_argument("-o", "--ortho", help="show orthogonal squares instead of workshop",
                        action="store_true")


    parser.add_argument("-t", "--test", help="internal validation",
                        action="store_true")

    args = parser.parse_args()
    return args

#----------------------------

def main():
    CHOICES=[2, 3, 4, 5, 6]
    args = parseargs(CHOICES)
    n = args.n
    test =  args.test
    mod = args.mod
    first = args.first
    sym =  args.sym
    simu = Simu(args.n, show_modulo=args.mod, break_after_first=args.first, sym=args.sym, ortho=args.ortho, do_test=args.test)
    simu._break=False
    simu.pruefe(row=-1, col=n-1, level=0)
    print (simu.count_full_solutions)

#-----------------------------

if __name__ == '__main__':
    main()
