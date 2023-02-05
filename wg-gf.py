#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn

class SimuGF:
    def work(self, basis, power, irr_poly, representation, show_ops=False):
        gf = GFpn(basis, irr_poly)

        self.info = f'GF({basis}^{power}), {irr_poly}'

        if show_ops:
            self.show = self.show_optables
        else:
            self.show = self.show_workshop

        elToBin={}
        BinToEl={}

        els_info=[]
        els=[]
        for i in range(basis**power):
            k=i
            l=[]
            while k !=0:
                k, rest = divmod(k, basis)
                l.append(rest)

            while len(l) < power:
                l.append(0)
            l.reverse()
            el = gf.elm(l)
            els_info.append((l, str(el)))
            els.append(el)
            if representation=='b':
                b=''.join(map(str,l))
            else:
                b=str(i)
            #print (i,b)
            elToBin[str(el)]=b
            BinToEl[b]=el
        self.show(els, elToBin)

    def show_workshop(self, els, elToBin):
        table={}
        for h, el_h in enumerate(els):#block
            for i, el_i in enumerate(els):   #zeile
                for j, el_j in enumerate(els): #spalte
                    if (h,i,j) not in table:
                        el = el_j*el_i + el_h
                        b=elToBin[str(el)]
                        table[(h,i,j)] = b

        print (f'\nWorkshop {self.info} ')

        n = len(els)
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    b = table[(h,i,j)]
                    print(b, end=' ')
                print(' | ', end='')
            print()

    def show_optables(self, els, elToBin):
        print (f'\nWorkshop {self.info} +')
        for el1 in els:
            for el2 in els:
                el = el1+el2
                b=elToBin[str(el)]
                print (b, end=' ')
            print()
        print (f'\nWorkshop {self.info} *')
        for el1 in els:
            for el2 in els:
                el = el1*el2
                b=elToBin[str(el)]
                print (b, end=' ')
            print()


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
