#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn

from .board import Board


class MiniGF():
    def __init__(self, els, els_index, sign_list, info):
        self.els = els
        self.els_index = els_index
        self.sign_list = sign_list
        self.info=info
        self.n = len(self.els)

    def fill_optables(self):
        self.op_plus={}
        self.op_mult={}

        for i, el1 in enumerate(self.els):
            for j, el2 in enumerate(self.els):
                i_plus_j=self.els_index[str(el1 + el2)]
                i_mult_j=self.els_index[str(el1 * el2)]
                self.op_plus[(i,j)] = i_plus_j
                self.op_mult[(i,j)] = i_mult_j


    def show_optables(self):
        print (f'\nWorkshop {self.info} +')
        for i in range(self.n):
            for j in range(self.n):
                i_plus_j = self.op_plus[(i,j)]
                sign = self.sign_list[i_plus_j]
                print (sign, end=' ')
            print()

        print (f'\nWorkshop {self.info} *')
        for i in range(self.n):
            for j in range(self.n):
                i_mult_j = self.op_mult[(i,j)]
                sign = self.sign_list[i_mult_j]
                print (sign, end=' ')
            print()

    def __add__(self, other):
        if isinstance(other, MiniGF):
            return MiniGF(self.value + other.value)

    def __mul__(self, other):
        if isinstance(other, MiniGF):
            return MiniGF(self.value * other.value)

    def __str__(self):
        return str(self.value)

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
        for h, el_h in enumerate(self.els):#block
            for i, el_i in enumerate(self.els):   #zeile
                for j, el_j in enumerate(self.els): #spalte
                    if (h,i,j) not in table:
                        el = el_j*el_i + el_h
                        sign =self.elToSign[str(el)]
                        table[(h,i,j)] = sign

        print (f'\nWorkshop {self.info} ')

        n = len(self.els)
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    sign = table[(h,i,j)]
                    print(sign, end=' ')
                print(' | ', end='')
            print()


    def show_workshop2(self):
        table={}
        for h, el_h in enumerate(self.els):#block
            for i, el_i in enumerate(self.els):   #zeile
                for j, el_j in enumerate(self.els): #spalte
                    if (h,i,j) not in table:
                        el = el_j*el_i + el_h
                        sign = self.elToSign[str(el)]
                        index_b = self.sign_index[sign]
                        table[(h,i,j)] = index_b

        print (f'\nWorkshop2 {self.info} ')

        n = len(self.els)
        board = Board(N=n,show_modulo=False)

        for row in range(n):
            for col in range(n):
                pair = (row,col)
                meeting=set()
                for j in range(n):
                    index_b = table[(col,row,j)]
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
