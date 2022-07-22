class Counter():
    'n Basis, m Stellenzahl'
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.a= m * [0]

    def incr(self, k=0):
        a, n = self.a, self.n
        a[k] = (a[k] + 1) % n
        if a[k] == 0:
            self.incr(k+1)

    def __str__(self):
        return ''.join(map(str, self.a[::-1]))

#----------------------

def gen_indexes(n, debug=False):
    counter = Counter(n,n-1)
    maxcounter = n**(n-1)
    indexes=[]
    for i in range(maxcounter):
        index = counter.a[::-1]
        indexes.append(index)

        if debug: print(i, index)
        if i == maxcounter-1:
            break
        counter.incr()
    return indexes

#----------------------

def gen_meetings(row, col, n, debug=False):
    #Bsp. n=3
    # valranges=(range(1,4), range(4,7), range(7,10))
    # valranges=((1,2,3),(4,5,6),(7,8,9))

    valranges=[range(n*i, n*(i+1))  for i in range(n)]
    if debug:
        print ([list(vr) for vr in valranges])


    indexes = gen_indexes(n, debug=debug)

    meetings=[]
    for index in indexes:
        fullindex = [col] + index
        lmeeting = [valranges[i][fullindex[i]] for i in range(n) ]
        if debug:
            print (fullindex, lmeeting)
        meeting =  frozenset(lmeeting)
        meetings.append(meeting)
    return meetings

#----------------------

def test_gen_meetings(n, debug=True):
    row =0
    col =1
    meetings = gen_meetings(row=row, col=col, n=n, debug=debug)
    for i, meeting in enumerate(meetings):
        print(i, sorted(meeting))

#----------------------

def main():
    args = sys.argv[1:] or ['3']
    assert len(args)==1
    n = int(args[0])
    print('n=',n)

    test_gen_meetings(n, debug=False)

#-----------------------------

if __name__ == '__main__':
    import sys
    main()
