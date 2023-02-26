#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field


import argparse, sys, os.path, math
from galois_field import GFpn
from lib.wg_gf_lib import SimuGF
from galois_field.core import validator

#----------------------------
def show_examples():
    scriptname = os.path.basename(__file__)
    sample=f"""
samples:
   {scriptname} 11
   {scriptname} 11 -s3
   {scriptname} 11 -s3 -rb
   {scriptname} 10
   {scriptname} 10 -s5 -c2
   {scriptname} 10 -s5 -c2
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
    parser.add_argument("person_count", help="number of participants", type=int)

    parser.add_argument("-s", "--maxsize", nargs='?', help="max teamsize", type=int)
    parser.add_argument("-c", "--groupcount", nargs='?', help="nr of teams ", type=int)
    parser.add_argument("-i", "--irr_poly", help="irregular polynom for construction of Galoisfield (advanced option)", required=False, type=str)
    parser.add_argument("-r", "--representation", help="'b','m' for binaer/modulo (where supported). Default is 'n' for index", default='n', required=False)
    parser.add_argument("-p", "--procedure", help="procedure 'w','op','wst'  wg/optables/ws-test. Default is ws for workshop", default='ws', required=False)
    parser.add_argument("-o", "--ortho", help="orthogonal squares in procedure ws", action="store_true", default='False', required=False)
    parser.add_argument("-v", "--verbose", help="Verbose",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="Debug",
                        action="store_true")
    args = parser.parse_args()

    return args

conductor = {
        4 : {'basis' :2, 'power' :2, 'irr_poly' :'111'},
        8 : {'basis' :2, 'power' :3, 'irr_poly' :'1101'},
       16 : {'basis' :2, 'power' :4, 'irr_poly' :'10011'},
       32 : {'basis' :2, 'power' :5, 'irr_poly' :'100101'},
        9 : {'basis' :3, 'power' :2, 'irr_poly' :'101'},
       25 : {'basis' :5, 'power' :2, 'irr_poly' :'102'},
    }


#----------------------------
def show_lookup_and_exit(lookup, person_count, comment):
    print (comment)
    print (f'Supported partitions for person_count {person_count} are:')
    for match_object in lookup:
        print(match_object)
    sys.exit()

#----------------------------
def evaluate_some_args(args):
    class MatchObject:
        #----------------------------
        def __init__(self, person_count, groupcount, maxsize, minsize, rest):
            self.person_count = person_count
            self.groupcount = groupcount
            self.maxsize = maxsize
            self.minsize = minsize
            self.rest = rest
            assert person_count > 0, person_count
            assert groupcount > 0, groupcount
            assert maxsize > 0, maxsize
            assert minsize > 0, minsize
        #----------------------------
        def __str__(self):
            person_count = self.person_count
            groupcount = self.groupcount
            minsize = self.minsize
            maxsize = self.maxsize
            rest = self.rest

            nmin = groupcount - rest
            nmax = rest
            partition = nmin * [minsize] + nmax * [maxsize]
            partition = '-'.join([str(x) for x in partition])
            assert nmin * minsize + nmax * maxsize == person_count, f'person_count={person_count} partition={partition}, {nmin} {nmax} gc{groupcount}'
            return f'--groupcount {groupcount:>2} --maxsize {maxsize:>2} # {partition}'

    maxsize = args.maxsize
    groupcount = args.groupcount
    person_count = args.person_count
    verbose = args.verbose
    debug = args.debug

    person_param_info=f'person_count={person_count}, groupcount={groupcount}, maxsize={maxsize}'

    lower_groupcount = math.ceil(math.sqrt(person_count))
    upper_groupcount = person_count // 2

    primes100 = {x for x in range(2, 101) if all(x%y for y in range(2, min(x, 11)))}
    all_valid_groupcounts = set(conductor.keys()).union(primes100)
    groupcount_range = range(lower_groupcount, upper_groupcount+1)
    valid_groupcounts = sorted(all_valid_groupcounts.intersection(set(groupcount_range)))
    if verbose:
        print(f'lower_groupcount      {lower_groupcount}')
        print(f'upper_groupcount      {upper_groupcount}')
        print(f'all_valid_groupcounts {all_valid_groupcounts}')
        print(f'valid_groupcounts     {valid_groupcounts}')

    lookup=[]
    if len(valid_groupcounts) > 0:
        for valid_groupcount in valid_groupcounts:
            valid_minsize, rest = divmod(person_count, valid_groupcount)
            if rest == 0:
                valid_maxsize = valid_minsize
            else:
                valid_maxsize = valid_minsize + 1

            valid_minsize0 = math.floor(person_count/valid_groupcount)
            valid_maxsize0 = math.ceil(person_count/valid_groupcount)
            assert valid_minsize0 == valid_minsize, f'valid_minsize0={valid_minsize0}, valid_minsize={valid_minsize0}'
            assert valid_maxsize0 == valid_maxsize, f'valid_maxsize0={valid_maxsize0}, valid_maxsize={valid_maxsize0}'

            match_object = MatchObject(person_count=person_count, groupcount = valid_groupcount, maxsize = valid_maxsize, minsize = valid_minsize, rest=rest)
            lookup.append(match_object)

    if not lookup:
        print(f'No Workshops for {person_count} participants found.')
        sys.exit(0)

    founds = []
    for match_object in lookup:
        match_groupcount=None
        match_maxsize=None
        if groupcount:
            match_groupcount = (groupcount == match_object.groupcount)
            if debug: print(111, f'match_groupcount={match_groupcount}, match_object.groupcount={match_object.groupcount}, groupcount={groupcount}')
        if maxsize:
            match_maxsize = (maxsize == match_object.maxsize)
            if debug: print(222, f'match_maxsize={match_maxsize}, match_object.maxsize={match_object.maxsize}, maxsize={maxsize}')

        match_pair = (match_groupcount, match_maxsize)
        if match_pair in [(True,True),(True,None),(None, True), (None,None)]:
            founds.append(match_object)
            if debug: print(f'333 match_pair={match_pair}, len(founds)={len(founds)}, match_object={match_object}')
        else:
            if debug: print(f'000 match_pair={match_pair}, len(founds)={len(founds)}, match_object={match_object}')

    if not founds:
        show_lookup_and_exit(lookup, person_count, f'4444No Workshop found for {person_param_info}.')

    if founds:
        if len(founds) > 1:
            show_lookup_and_exit(founds, person_count, f'Several Workshops found for person_count {person_count}.')
        elif len(founds) == 1:
            found = founds[0]
            if debug:print(f'678 found = {found}')

    if not groupcount:
        groupcount = found.groupcount
    if not maxsize:
        maxsize = found.maxsize

    if args.debug:
        print(4711, args)
        print(4720, f'person_count={args.person_count}, maxsize={maxsize}, groupcount={groupcount}')

    return maxsize, groupcount

#----------------------------
def main():
    args = parseargs()
    person_count = args.person_count
    representation = args.representation
    procedure = args.procedure
    verbose = args.verbose
    debug = args.debug
    ortho = args.ortho

    maxsize, groupcount = evaluate_some_args(args)
    if debug: print(10453, f'maxsize={maxsize}, groupcount={groupcount}')
    groupcount_is_prime = validator.is_prime(groupcount)

    if groupcount_is_prime:
        irr_poly = None
        basis = groupcount
        power = 1
        if representation == 'b':
            print(f"Representation 'b' is not supported for prime groupcount {groupcount}")

    else:
        assert groupcount in conductor, groupcount

        basis = conductor[groupcount]['basis']
        power = conductor[groupcount]['power']
        irr_poly = args.irr_poly or conductor[groupcount]['irr_poly']
        irr_poly = [int(c) for c in irr_poly]

    assert groupcount == basis**power, (groupcount,basis,power)


    if args.verbose:
        print(args)

    simu_gf = SimuGF()
    simu_gf.work(person_count, basis, power, maxsize, groupcount, irr_poly,
              representation=representation, procedure=procedure, ortho=ortho, verbose=verbose, debug=debug)

#----------------------------
def demo():
    simu = SimuGF()
    representation='n'
    show='ws'
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
