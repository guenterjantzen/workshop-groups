def pos_val_range(col, pos, n):
    if pos == 0:
        rng = [col]
    else:
        rng = list(range((pos) * n + 1, (1 + pos) * n + 1))
    return rng

#-----------------------------
def gen_meetings(row, col, n, debug=False):
    def rg(pos):
        return pos_val_range(col=col+1, pos=pos, n=n)
    MIN,MAX = 0,-1
    index=n*[0]
    lmeeting = [rg(pos)[index[pos]] for pos in range(n)]
    meeting =  frozenset({v for v in lmeeting if v != None})
    if debug: print(index, lmeeting, sorted(meeting), 'first')
    meetings=[meeting]

    stop=False
    while stop==False: #lmeeting != rng_max:
        index[n-1]  += 1

        i = n
        while i > 1:
            i -= 1

            if index[i] == len(rg(i)):
                index[i] = 0
                if i-1==1 and index[i-1] == len(rg(i-1))-1:
                    stop = True
                    if debug: print ('stop')
                else:
                    index[i-1] +=1
        if not stop:
            lmeeting = [rg(pos)[index[pos]] for pos in range(n)]
            meeting =  frozenset({v for v in lmeeting if v != None})

            if debug: print(index, lmeeting, sorted(meeting))
            meetings.append(meeting)
            if debug: print([sorted(m) for m in meetings])
    return meetings

#-----------------------------
def test_pos_val_range(n):
    col =1
    for pos in range(n):
        print( f'pos_val_range({col}, {pos}) = {pos_val_range(col, pos, n)} ' )

def test_gen_meetings(n, debug=True):
    row =0
    col =1
    gen_meetings(row=row, col=col, n=n, debug=debug)

def main():
    args = sys.argv[1:] or ['3']
    assert len(args)==1
    n = int(args[0])
    print('n=',n)

    #test_pos_val_range(n)
    test_gen_meetings(n)

#-----------------------------

if __name__ == '__main__':
    import sys
    main()
