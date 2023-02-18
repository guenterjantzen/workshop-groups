#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn

from .board import Board

#-----------------------------
class GF_OP():
    op_plus={}
    op_mult={}
    signs=[]
    def __init__(self, value):
        self.value = value

    #-----------------------------
    def __add__(self, other):
        if isinstance(other, GF_OP):
            return GF_OP(GF_OP.op_plus[(self.value, other.value)])
    #-----------------------------
    def __mul__(self, other):
        if isinstance(other, GF_OP):
            return GF_OP(GF_OP.op_mult[(self.value, other.value)])
    #-----------------------------
    def __str__(self):
        return GF_OP.signs[self.value]

#-----------------------------
class MiniGF():
    def __init__(self, els, els_index, signs):
        GF_OP.op_plus={}
        GF_OP_mult={}
        GF_OP.signs = signs

        self.els = els
        self.els_index = els_index
        self.n = len(self.els)

    #-----------------------------
    def fill_optables(self):
        for i, el1 in enumerate(self.els):
            for j, el2 in enumerate(self.els):
                i_plus_j=self.els_index[str(el1 + el2)]
                i_mult_j=self.els_index[str(el1 * el2)]
                GF_OP.op_plus[(i,j)] = i_plus_j
                GF_OP.op_mult[(i,j)] = i_mult_j

    #-----------------------------
    def show_optables(self, info):
        print (f'\n{info} +')
        for i in range(self.n):
            for j in range(self.n):
                a = GF_OP(i)
                b = GF_OP(j)
                print (str(a + b), end=' ')
            print()

        print (f'\n{info} *')
        for i in range(self.n):
            for j in range(self.n):
                a = GF_OP(i)
                b = GF_OP(j)
                print (str(a * b), end=' ')
            print()

#-----------------------------
class SimuGF:
    #-----------------------------
    def work(self, basis, power, irr_poly, representation, procedure='w', verbose=False):
        gf = GFpn(basis, irr_poly)

        info = f'GF({basis}^{power}), {irr_poly}'

        if procedure=='o':
            self.show = self.show_optables
        elif procedure=='w':
            self.show = self.show_workshop
        elif procedure=='w2':
            self.show = self.show_workshop2

        signs =  []
        sign_index = {}

        els=[]
        els_index = {}

        self.n = basis ** power
        for i in range(self.n):
            k = i
            l = []
            while k !=0:
                k, rest = divmod(k, basis)
                l.append(rest)

            while len(l) < power:
                l.append(0)
            l.reverse()

            el = gf.elm(l)
            els.append(el)
            els_index[str(el)] = i

            self.show_modulo=False
            if representation=='b':
                sign=''.join(map(str,l))
            else:
                if representation=='m':
                    self.show_modulo=True
                sign=str(i)

            sign_index[sign]=i
            signs.append(sign)

        self.miniGF = miniGF =MiniGF(els, els_index, signs)
        miniGF.fill_optables()

        if verbose:
            for i in range(self.n):
                print('-- ', i, signs[i], els[i])

        self.show(info)

    #-----------------------------
    def show_optables(self, info):
        self.miniGF.show_optables(info)

    #-----------------------------
    def fill_table(self):
        table={}
        n = self.n
        for h in range(n): #block
            for i in range(n): #zeile
                for j in range(n): #spalte
                    if (h,i,j) not in table:
                        e_h, e_i, e_j = GF_OP(h), GF_OP(i), GF_OP(j)
                        el = e_j * e_i + e_h
                        table[(h,i,j)] = el
        return table

    #-----------------------------
    def show_workshop(self, info):
        n = self.n
        table = self.fill_table()

        print (f'\nWorkshop {info}')
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    el = table[(h,i,j)]
                    print(str(el), end=' ')
                print(' | ', end='')
            print()

    #-----------------------------
    def show_workshop2(self, info):
        n = self.n
        table = self.fill_table()

        print (f'\nWorkshop2 {info}')
        board = Board(N=n,show_modulo=self.show_modulo)
        for row in range(n):
            for col in range(n):
                pair = (row,col)
                meeting=set()
                for j in range(n):
                    #board arbeitet noch nicht mit signs. wir nehmen den index
                    index_b = table[(col,row,j)].value
                    person_index = j * n + int(index_b)

                    meeting.add(person_index)
                board.set_meeting(meeting, pair)
        board.test()
        board.show(comment=';)', do_test=True)

#-----------------------------
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

#-----------------------------
if __name__ == '__main__':
    demo()
