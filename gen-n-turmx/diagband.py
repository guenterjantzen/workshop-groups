# Erweitertes n-Türme Problem:

# Statt Schachbrett wird ein n mal n Brett mit einem lateinischen Quadrat der Ordnung n verwendet. Zeichen sind die Ziffern 0 .. n-1.
# Zeilen und Spalten sind mit 0 .. n-1 durchnummeriert. Eine Lösung besteht aus 5 Feldern, bei denen keine Spalte oder Zeile doppelt vorkommt. 
# (Wie n Türme im Schach, die sich nicht gegenseitig bedrohen).
# Zusätzlich soll gelten, dass jeder Turm auf einem anders beschrifteten Feld steht



class Board():
    def __init__(self, block):
        self.board = self.board_from_textblock(block)
        self.towers=[]

    def board_from_textblock(self, block):
        linesplit = block.splitlines()
        board={}
        self.n = n = 0
        i=-1
        for line0 in linesplit:
            line=line0.replace(' ','').strip()
            if line:
                i += 1
                if not n:
                    self.n=n=len(line)
                    self.used_signs = set(range(n))
                    linedict = {c:idx for idx,c in enumerate(line)}
                    #print(f'linedict: {linedict}')
                else:                
                    assert n==len(line),(line,i)
                lineset={linedict[c] for c in line}
                linelist=[linedict[c] for c in line]
                assert n==len(lineset),(line,lineset, i)
                assert self.used_signs == lineset,(line,i)
                for j in range(n):
                    board[i,j] = linelist[j]
        return board
        
    def check(self):
        ok = True

        ok_towers_i = self.towers_i == self.used_signs
        ok_towers_j = self.towers_j == self.used_signs
        ok_towers_x = self.towers_x == self.used_signs
        ok = ok_towers_i and ok_towers_j and ok_towers_x
        
        self.tower_info = sorted({f'{(i,j)} -> {self.board[i,j]}' for (i,j) in self.towers})  
        return ok
    
    def setTowers(self, towers):
        self.towers=towers                                                                         
        self.towers_i = {i for (i,j) in self.towers}
        self.towers_j = {j for (i,j) in self.towers}
        self.towers_x = {self.board[i,j] for (i,j) in self.towers}
        
        self.sorted_towers_i = sorted(self.towers_i)
        self.sorted_towers_j = sorted(self.towers_j)
        self.sorted_towers_x = sorted(self.towers_x)
    
    def genDiagBandWorkshop(self):
#towers: ['(0, 3) -> 3', '(1, 0) -> 1', '(2, 2) -> 0', '(3, 1) -> 2']
#inv_towers: [(0, (2, 2)), (1, (1, 0)), (2, (3, 1)), (3, (0, 3))]
#(0, 3) 3
#(1, 0) 1
#(2, 2) 0
#(3, 1) 2


#(2, 2) 0
#(1, 0) 1
#(3, 1) 2
#(0, 3) 3

#     0  1  2  3
#---+-----------
# 0 | 0  1  2 <3>   
# 1 | 1 <0> 3  2
# 2 |<2> 3  0  1
# 3 | 3  2 <1> 0   
#   |
#   | Zeilen sortiert: 0-3 1-0 2-2 3-1
# 0 | 1 <0> 3  2
# 1 | 3  2 <1> 0 
# 2 |<2> 3  0  1
# 3 | 0  1  2 <3>
#   |
#   | Spalten sortiert: 0-2 1-0 2-1 3-3
# 0 |<0> 3  1  2
# 1 | 2 <1> 3  0 
# 2 | 3  0 <2> 1
# 3 | 1  2  0 <3>

#0|123 1|032 2|013 3|021


#(0, 3) 3 0|1
#(1, 1) 0
#(2, 0) 2
#(3, 2) 1
        DEBUG = self.tower_info == ['(0, 3) -> 3', '(1, 0) -> 1', '(2, 2) -> 0', '(3, 1) -> 2']
        if DEBUG:
            print(f'towers: {self.tower_info}')
            
            inv_towers={}
            
            towers_i={}
            towers_j={}
            
            inv_towers_i={}
            inv_towers_j={}
            
            sort_board={}
            
            for tower in self.towers:  
                i,j = tower[0],tower[1]
                x = self.board[i,j]
                towers_i[i]=x
                towers_j[j]=x
                inv_towers_i[x]=i
                inv_towers_j[x]=j
                inv_towers[x]=tower
                print(tower, x)      
                

            print(f'towers_i: {(towers_i)}') 
            print(f'towers_j: {(towers_j)}')
            print(f'inv_towers_i: {sorted(inv_towers_i.items())}') 
            print(f'inv_towers_j: {sorted(inv_towers_j.items())}')                
            print(f'inv_towers: {sorted(inv_towers.items())}')
            
            
            #for x,(i,j) in sorted(inv_towers.items()): 
            #   sort_board[]

            self.showBoard("original") 
            ii_jj={}
            for x in range(self.n):
                ii=inv_towers_i[x]
                jj=inv_towers_j[x]
                ii_jj[ii]=jj
            print(f'ii_jj: {(ii_jj)}') 
            
            for i in range(self.n):    
               for j in range(self.n):
                   jj=inv_towers_j[j]
                   sort_board[ii_jj[i],jj]=self.board[i,j]
            print()
            print("zeilensortierung")       
            for i in range(self.n):
                for j in range(self.n):
                    print(f'{sort_board[i,j]:<2}', end='')
                print()
            print()
            
                    
            
            
            diagband={}
            
            
            
            for x,(i,j) in sorted(inv_towers.items()): 

                
                print(x,i,j)
                dbx=[]
                v = x+1 % self.n
                #w=
                #dbx.append(
                
            
        
    
    def showBoard(self, comment):
        print(comment)
        for i in range(self.n):
            for j in range(self.n):
                print(f'{self.board[i,j]:<2}', end='')
            print()
        
    def free_fields(self):
        free_i = self.used_signs - self.towers_i
        free_j = self.used_signs - self.towers_j
        #print(f'self.towers_i: {self.towers_i} self.towers_j: {self.towers_j}')
        #print(f'free_i: {free_i} free_j: {free_j}')
        free_fields = [(i,j) for i in free_i for j in free_j]
        return free_fields

#------------------------------    
def work(towers, board, comment):
    if not towers:
        board.showBoard(comment)
        print()
    towers0 = board.towers[:]
    board.setTowers(towers)
    assert towers == board.towers
    check = False
    if len(towers)==board.n:
        check=board.check()  
        if check:
            board.genDiagBandWorkshop()
            
    free_fields = board.free_fields()
    #print(f'free_fields: {free_fields}')
    max_sorted_towers = max(sorted(towers) or [(-1,-1)])
    #print (max_sorted_towers)
    for (i,j) in free_fields:
        if (i,j) > max_sorted_towers:
            work(towers+[(i,j)], board, comment)
        


#------------------------------
def main():
    board = Board('0123\n1032\n2301\n3210')
    work([], board, comment='Klein Vier')  
    return
#=========================    

    board = Board('''
    01234
    12340
    23401
    34012
    40123''') 
    work([], board, comment='\n5 Standard Zykl LQ')
    
#========================= 
    board = Board('''
    012345
    123450
    234501
    345012
    450123
    501234''') 
    work([], board, comment='\n6 Standard Zykl LQ')
    
 #========================= 
    board = Board('''
    012345
    120453
    201534
    345012
    453120
    534201''') 
    work([], board, comment='\n6 Z2Z3 LQ')
    
 #=========================    
    board = Board('''
123456
231564
312645
465132
546213
654321
    ''')   
    work([], board, comment='\n6 S3 LQ')
        
#=========================     
    board = Board('''
    A B F C E D 
    B C A D F E 
    C D B E A F 
    D E C F B A 
    E F D A C B 
    F A E B D C 
    ''') 
    work([], board, comment='\n6 https://statpages.info/latinsq.html LQ')
    
#========================= 
    board = Board('''
0123456
1234560
2345601
3456012
4560123
5601234
6012345
    ''') 
    work([], board, comment='\n7 Standard Zykl LQ')
    
#=========================    
    board = Board('''
12345678
23416785
34127856
41238567
56781234
67852341
78563412
85674123
    ''') 
    work([], board, comment='\n8 Z2Z4 LQ')
    
    board = Board('''
12345678
21438765
38167452
45276381
54721836
67854123
76583214
83612547
    ''') 
    work([], board, comment='\n8 D4 LQ')    
    
#=========================    
    board = Board('''
01234567
12345670
23456701
34567012
45670123
56701234
67012345
70123456
    ''') 
    work([], board, comment='\n8 Standard Zykl LQ')
    
#========================= 
    board = Board('''    
1 2 9 3 8 4 7 5 6 
2 3 1 4 9 5 8 6 7 
3 4 2 5 1 6 9 7 8 
4 5 3 6 2 7 1 8 9 
5 6 4 7 3 8 2 9 1 
6 7 5 8 4 9 3 1 2 
7 8 6 9 5 1 4 2 3 
8 9 7 1 6 2 5 3 4 
9 1 8 2 7 3 6 4 5 
6 5 7 4 8 3 9 2 1 
7 6 8 5 9 4 1 3 2 
8 7 9 6 1 5 2 4 3 
9 8 1 7 2 6 3 5 4 
1 9 2 8 3 7 4 6 5 
2 1 3 9 4 8 5 7 6 
3 2 4 1 5 9 6 8 7 
4 3 5 2 6 1 7 9 8 
5 4 6 3 7 2 8 1 9     
''') 
    work([], board, comment='\n9 https://statpages.info/latinsq.html LQ')
    
#=========================     
    board = Board('''
012345678
123456780
234567801
345678012
456780123
567801234
678012345
780123456
801234567
    ''') 
    work([], board, comment='\n9 Standard Zykl LQ')    
    
#=========================     
    board = Board('''
0123456789
1234567890
2345678901
3456789012
4567890123
5678901234
6789012345
7890123456
8901234567
9012345678
    ''') 
    work([], board, comment='\n10 Standard Zykl LQ')     
#===========================================


def main1():
    def check(block, towers, comment):
        board = Board(block)
        board.setTowers(towers)   
        check=board.check()
        print(f'check: {check} {comment}')

    check('''
    0123
    1230
    2301
    3012
    ''', [(0,0),(1,1),(2,2),(3,3)],  'board 1')
    
    check('0123\n1230\n2301\n3012', [(0,0),(1,1),(2,2),(3,3)], 'board 2')
    
    check('0123\n1032\n2301\n3210', [(0,0),(1,3),(2,1),(3,2)],  'board 3')    
    
    
if __name__ == '__main__':
    main()
        
    
