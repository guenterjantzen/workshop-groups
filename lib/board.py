from lib.helper import ordered_pairs
from lib.helper import DEBUG1, DEBUG2, DEBUG3, DEBUG4, DEBUG5
class Board:
    #-----------------------------
    def __init__(self, N):
        self.N = N
        self.NN = N*N
        self.board={}
        self.free_pairs = ordered_pairs(range(1, 1 + self.NN))

    #-----------------------------
    def set_meeting(self, meeting, pair):
        n = self.N
        row, col = pair
        self.set_row = row
        self.set_col = col
        info = f'row={row}, col={col}'
        if meeting:
            info=f'{info}, meeting={sorted(meeting)},'
        if DEBUG5: print(f'Board.set_meeting  {info}')
        assert 0 <= row <= n, info
        assert 0 <= col <= n, info
        self.board[(row,col)] = meeting

    #-----------------------------
    def unset_meeting(self, pair):
        n = self.N
        row, col = pair
        info = f'row={row}, col={col}'
        if DEBUG5: print(f'Board.unset_meeting  {info}')
        assert 0 <= row <= n, info
        assert 0 <= col <= n, info
        self.board[(row,col)] = None

    #-----------------------------
    def test(self):
        n = self.N
        meeting_pairs = set()
        double_pairs = set()
        double_persons = n*[None]
        row = -1
        while row < n-1:
            row += 1
            double_persons[row] = set()
            row_persons = set()
            for col in range(n):
                meeting = self.board.get((row,col))
                if not meeting:
                    break
                #double_pairs
                meet_pairs = ordered_pairs(meeting)

                double_pairs = double_pairs.union(meeting_pairs.intersection(meet_pairs))

                #row_double_persons
                double_persons[row] = sorted(meeting.intersection(row_persons))

                #assignments
                meeting_pairs = meeting_pairs.union(meet_pairs)
                row_persons = row_persons.union(meeting)
            if not meeting:
                break

        double_pairs = sorted(double_pairs)
        return  double_persons, double_pairs

    #-----------------------------
    def show_(self, comment, do_test = False):
        ok = True
        if do_test:
            double_persons, double_pairs = self.test()
        print (f'<< board {comment}')
        row = -1
        n = self.N
        while row < n-1:
            row+=1
            for col in range(n):
                meeting = self.board.get((row,col))
                if not meeting:
                    break
                print (sorted(meeting), end=' ')
            if not meeting:
                break
            if do_test and double_persons[row]:
                ok = False
            if do_test: 
                print(f'  -- {double_persons[row]}')
            else:
                print()
        oktext=''
        if do_test and double_pairs:
            ok = False
            oktext=f'ok={ok}'
            print(f'{double_pairs}')
        print(f'row={row}, col={col}{oktext}>>')
        return ok
  #-----------------------------
    def show(self, comment, do_test = False):
        ok = True
        if do_test:
            double_persons, double_pairs = self.test()
        print (f'<< board {comment}')
        row = -1
        n = self.N
        firstrow = [None]*n
        while row < n-1:
            row+=1
            deltarow = [None]*n
            for col in range(n):
                meeting = self.board.get((row,col))
                lmeeting = sorted(meeting)       
                #lmeeting = [x %n for x in lmeeting]       
                if not lmeeting:
                    break
                if row == 0:
                   firstrow[col]=sorted(self.board[(0,col)])
                else:          
                    #print(f'{row} firstrow[{col}]={firstrow[col]} {firstrow}')
                    delta = [lmeeting[i]-firstrow[col][i] for i in range(n)]   
                    #deltarow[col]=tuple(sorted(delta))
                    deltarow[col]=tuple(delta)
                print (lmeeting, end=' ')
            if not lmeeting:
                break
            if do_test and double_persons[row]:
                ok = False
            if do_test: 
                print(f'  -- {double_persons[row]}')
            else:
                print('')
            if False and row > 0:
                for col in range(n):
                     print (deltarow[col], end=' ')
                print()                
        oktext=''
        if do_test and double_pairs:
            ok = False
            oktext=f'ok={ok}'
            print(f'{double_pairs}')
        print(f'row={row}, col={col}{oktext}>>')
        return ok
