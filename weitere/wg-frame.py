#!/usr/bin/env python3

import sys, os.path, argparse, math
from galois_field.core import validator

#----------------------------
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        #show_examples()
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

#----------------------------
def parseargs():
    parser = ArgumentParser(prog = os.path.basename(__file__),
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument("N", help="Number of Participants", type=int)
    parser.add_argument("-s","--maxsize", nargs='?', help="max groupsize", type=int)
    parser.add_argument("-c", "--groupcount", nargs='?', help="group count", type=int)
    args = parser.parse_args()
    return args

#----------------------------
def main():
    args=parseargs()
    print(4711, args)

    maxsize=args.maxsize
    groupcount=args.groupcount
    N=args.N

    assert maxsize or groupcount

    if groupcount:
        div, mod=divmod(N,groupcount)
        maxsize0 = div if mod==0 else div+1
        if maxsize:
            assert maxsize0==maxsize, (f'max groupsize should be {maxsize0}, not {maxsize}')
        else:
            maxsize = maxsize0
    elif maxsize:
        groupcount = math.ceil(N/maxsize)
        div, mod=divmod(N,groupcount)

    nmin = groupcount - mod
    nmax = mod

    partition = nmin * [div] + nmax * [div +1]
    partition = '-'.join([str(m) for m in partition])

    print(partition)
    #     div  mod
   #15:4=  3 R 3  3-4-4-4
   #16:4=  4 R 0  4-4-4-4
   #17:4 = 4 R 1  4-4-4-5


    print(4720, f'N={N}, maxsize={maxsize}, groupcount={groupcount}')


    #cnt_minsize = groupcount

#----------------------------
if __name__ == '__main__':
    main()
