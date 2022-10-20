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
    
    def showTowers(self):
        print(f'towers: {self.tower_info}')
    
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
            board.showTowers()
            
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
    
    board = Board('''
    01234
    12340
    23401
    34012
    40123''') 
    work([], board, comment='\n5 Standard Zykl LQ')

    board = Board('''
    012345
    123450
    234501
    345012
    450123
    501234''') 
    work([], board, comment='\n6 Z2Z3 LQ')
 
    board = Board('''
    012345
    120453
    201534
    345012
    453120
    534201''') 
    work([], board, comment='\n6 Standard Zykl LQ')
    
    board = Board('''
    012345
    120453
    201534
    354021
    435102
    543210
    ''')   
    
    work([], board, comment='\n6 S3 LQ')
    board = Board('''
    012345
    120453
    201534
    354021
    435102
    543210
    ''')   
    
    work([], board, comment='\n6 https://statpages.info/latinsq.html LQ')   
    board = Board('''
    A B F C E D 
    B C A D F E 
    C D B E A F 
    D E C F B A 
    E F D A C B 
    F A E B D C 
    ''') 
    work([], board, comment='\n7 Standard Zykl LQ')
    
    board = Board('''
    01234567
    12305674
    23016745
    30127456
    45670123
    56741230
    67452301
    74563012
    ''') 
    work([], board, comment='\n8 Z2Z4 LQ')
    
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
        
    
