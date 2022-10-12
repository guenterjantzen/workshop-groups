#!/usr/bin/env python3

def f_mod(block,row,col,p):
    return (block + (row * col) % p ) % p

def f(block,row,col,p):
    mod_val=f_mod(block,row,col,p)
    return p*(col%p)+mod_val

with open('p-square-workshops.txt','w') as fw, open('p-square-workshops-modulo-p.txt','w') as fw_mod:
    for p in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,57,59,61,67,71,73,79,83,87,89,97):
        if p==29:
            break
        fw.write(    f'\nWorkshop-Gruppenaufteilung für {p*p}-Workshops\n')
        fw_mod.write(f'\nWorkshop-Gruppenaufteilung modulo {p} für {p*p}-Workshops\n')

        num_format_width=len(str(p*p))
        for row in range (p):
            blocks=[]
            for block in range (p):
                part = ' '.join([f'{f(block,row,col,p):{num_format_width}d}' for col in range(p)])
                fw.write(f'{part} | ')
                part = ' '.join([f'{f_mod(block,row,col,p):{num_format_width}d}' for col in range(p)])
                fw_mod.write(f'{part} | ')

            fw.write('\n')
            fw_mod.write('\n')
