#!/usr/bin/env python3

#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

import argparse
import os.path
from galois_field import GFpn, GFp

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
    def show_optables(self, info, signs):
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
    def work(self, person_count, basis, power, irr_poly, representation, procedure='w', ortho=False, verbose=False):
        if power > 1:
            gf = GFpn(basis, irr_poly)
        elif power == 1:
            gf = GFp(basis)

        info = f'GF({basis}^{power}){(irr_poly or "")}'

        self.person_count = person_count
        self.do_test = False
        self.ortho = ortho
        self.verbose = verbose

        if procedure=='op':
            self.show = self.show_optables
        elif procedure=='w':
            self.show = self.show_workshop
        elif procedure=='ws':
            self.show = self.show_workshop2
        elif procedure=='wst':
            self.show = self.show_workshop2
            self.do_test = True

        signs =  []

        els=[]
        els_index = {}

        self.n = basis ** power

        if representation=='b':
            self.show_modulo=True
        elif representation=='m':
            self.show_modulo=True
        elif representation=='n':
            self.show_modulo=False

        for i in range(self.n):
            k = i
            l = []
            if power > 1:
                while k !=0:
                    k, rest = divmod(k, basis)
                    l.append(rest)

                while len(l) < power:
                    l.append(0)
                l.reverse()

                el = gf.elm(l)
            else:
                el = gf.elm(i)
            els.append(el)
            els_index[str(el)] = i

            if representation=='b':
                if l:
                    sign=''.join(map(str,l))
                else:
                    sign=str(i)
                signs.append(sign)
            elif representation=='m':
                sign=str(i)
                signs.append(sign)
            elif representation=='n':
                pass
            else:
                assert False, representation

        if not self.show_modulo:
            assert not signs, signs
            signs=[str(i) for i in range(self.n *self.n)]

        self.miniGF = miniGF =MiniGF(els, els_index, signs)
        miniGF.fill_optables()

        if verbose:
            print (455, els)
            print (456, signs)
            for i in range(min(len(els),len(signs))):
                print('-- ', i, els[i], signs[i])


        self.show(info, signs)

    #-----------------------------
    def show_optables(self, info, signs):
        self.miniGF.show_optables(info, signs)

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
    def show_workshop(self, info, signs):
        n = self.n
        table = self.fill_table()

        print (f'\nWorkshop {info} for {self.person_count} persons')
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    el = table[(h,i,j)]
                    print(signs[el.value], end=' ')
                print(' | ', end='')
            print()

    #-----------------------------
    def show_workshop2(self, info, signs):
        n = self.n
        table = self.fill_table()

        print (f'\nWorkshop2 {info} for {self.person_count} persons')
        board = Board(N = n, person_count=self.person_count, show_modulo = self.show_modulo, ortho = self.ortho, signs=signs, verbose=self.verbose)
        for row in range(n):
            for col in range(n):
                pair = (row,col)
                meeting=set()
                for j in range(n):
                    index_b = table[(col,row,j)].value
                    person_index = j * n + int(index_b)
                    meeting.add(person_index)
                board.set_meeting(meeting, pair)
        if self.do_test:
            board.test()
        board.show(comment=';)', do_test = self.do_test)

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
