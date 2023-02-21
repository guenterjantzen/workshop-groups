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
    parser.add_argument("-ms","--maxsize", nargs='?', help="max group size", type=int)
    parser.add_argument("-gc", "--groupcount", nargs='?', help="nr of groups ", type=int)
    args = parser.parse_args()
    return args

#----------------------------
class Work():
    def evaluate_some_args(self, args):
        print(4711, args)

        maxsize = args.maxsize
        groupcount = args.groupcount
        N = args.N

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

        return maxsize, groupcount, partition

def main():
    args=parseargs()
    work = Work()
    maxsize, groupcount, partition = work.evaluate_some_args(args)

    print(partition)
    #     n_div_gc  mod
    #15:4=  3 R 3  3-4-4-4
    #16:4=  4 R 0  4-4-4-4
    #17:4 = 4 R 1  4-4-4-5

    print(4720, f'N={args.N}, maxsize={maxsize}, groupcount={groupcount}')

#----------------------------
if __name__ == '__main__':
    main()
