#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn

from .board import Board


class GF_OP():
    op_plus={}
    op_mult={}

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, GF_OP):
            return GF_OP(GF_OP.op_plus[(self.value, other.value)])

    def __mul__(self, other):
        if isinstance(other, GF_OP):
            return GF_OP(GF_OP.op_mult[(self.value, other.value)])

    def __str__(self):
        return str(self.value)

class MiniGF():
    def __init__(self, els, els_index, sign_list, info):
        self.els = els
        self.els_index = els_index
        self.sign_list = sign_list
        self.info=info
        self.n = len(self.els)

    def fill_optables(self):
        GF_OP.op_plus={}
        GF_OP_mult={}

        for i, el1 in enumerate(self.els):
            for j, el2 in enumerate(self.els):
                i_plus_j=self.els_index[str(el1 + el2)]
                i_mult_j=self.els_index[str(el1 * el2)]
                GF_OP.op_plus[(i,j)] = i_plus_j
                GF_OP.op_mult[(i,j)] = i_mult_j


    def show_optables(self):
        print (f'\nWorkshop {self.info} +')
        for i in range(self.n):
            for j in range(self.n):
                a = GF_OP(i)
                b = GF_OP(j)
                sign = self.sign_list[a+b]
                print (sign, end=' ')
            print()

        print (f'\nWorkshop {self.info} *')
        for i in range(self.n):
            for j in range(self.n):
                a = GF_OP(i)
                b = GF_OP(j)
                sign = self.sign_list[a*b]
                print (sign, end=' ')
            print()



class SimuGF:

    def work(self, basis, power, irr_poly, representation, show='w', verbose=False):
        gf = GFpn(basis, irr_poly)

        self.info = f'GF({basis}^{power}), {irr_poly}'

        if show=='o':
            self.show = self.show_optables
        elif show=='w':
            self.show = self.show_workshop
        elif show=='w2':
            self.show = self.show_workshop2

        self.elToSign={}
        SignToEl={}


        self.sign_list =  []
        self.sign_index = {}

        els_info=[] #kann weg
        self.els=[]
        self.els_index = {}

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
            els_info.append((l, str(el))) #kann weg
            print (l, str(el))
            self.els.append(el)
            self.els_index[str(el)] = i

            if representation=='b':
                sign=''.join(map(str,l))
            else:
                sign=str(i)
            #print (i,sign)
            self.elToSign[str(el)] = sign
            SignToEl[sign] = el
            self.sign_index[sign]=i
            self.sign_list.append(sign)

        self.miniGF = miniGF =MiniGF(self.els, self.els_index, self.sign_list, self.info)

        miniGF.fill_optables()


        if verbose:
            for i,(sign,el) in enumerate(sorted(SignToEl.items())):
                print('-- ', i, sign, str(el))
        self.show()

    def show_optables(self):
        self.miniGF.show_optables()

    def show_workshop(self):
        table={}
        n = len(self.els)
        for h in range(n): #block
            for i in range(n):   #zeile
                for j in range(n): #spalte
                    if (h,i,j) not in table:
                        e_h, e_i, e_j = GF_OP(h), GF_OP(i), GF_OP(j)
                        el = e_j * e_i + e_h
                        table[(h,i,j)] = el

        print (f'\nWorkshop {self.info} ')

        n = len(self.els)
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    el = table[(h,i,j)]
                    print(self.sign_list[el.value], end=' ')
                print(' | ', end='')
            print()


    def show_workshop2(self):
        table={}
        for h, el_h in enumerate(self.els):#block
            for i, el_i in enumerate(self.els):   #zeile
                for j, el_j in enumerate(self.els): #spalte
                    if (h,i,j) not in table:
                        e_h, e_i, e_j = GF_OP(h), GF_OP(i), GF_OP(j)
                        el = e_j * e_i + e_h
                        table[(h,i,j)] = el

        print (f'\nWorkshop2 {self.info} ')

        n = len(self.els)
        board = Board(N=n,show_modulo=False)

        for row in range(n):
            for col in range(n):
                pair = (row,col)
                meeting=set()
                for j in range(n):
                    index_b = table[(col,row,j)].value
                    person_index = j * n + int(index_b)
                    meeting.add(person_index)
                board.set_meeting(meeting, pair)
        board.test()
        board.show(comment=';)', do_test=True)



#----------------------------

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
    demo()
