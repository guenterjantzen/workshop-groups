from lib.helper import ordered_pairs
from lib.helper import DEBUG1, DEBUG2, DEBUG3, DEBUG4, DEBUG5
class Board:
    #-----------------------------
    def __init__(self, N, show_modulo):
        self.N = N
        self.NN = N*N
        self.show_modulo= show_modulo
        self.board={}
        self.free_pairs = ordered_pairs(range(self.NN))
        self.double_pairs = set()
        self.double_persons = N*[None]

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
        self.double_pairs = set()
        self.double_persons = n*[None]
        row = -1
        while row < n-1:
            row += 1
            self.double_persons[row] = set()
            row_persons = set()
            for col in range(n):
                meeting = self.board.get((row,col))
                if not meeting:
                    break
                #self.double_pairs
                meet_pairs = ordered_pairs(meeting)

                self.double_pairs = self.double_pairs.union(meeting_pairs.intersection(meet_pairs))

                #row_double_persons
                self.double_persons[row] = sorted(meeting.intersection(row_persons))

                #assignments
                meeting_pairs = meeting_pairs.union(meet_pairs)
                row_persons = row_persons.union(meeting)
            if not meeting:
                break

        self.double_pairs = sorted(self.double_pairs)

    #-----------------------------
    @staticmethod
    def format_meeting(lmeeting):
        s=[f'{person:>2}' for person in lmeeting]
        sep = ' '
        return f'[{sep.join(s)}]'

    #-----------------------------
    def show(self, comment, do_test = False):
        ok = True
        #print (f'<< board {comment}')
        row = -1
        n = self.N
        while row < n-1:
            row+=1
            deltarow = [None]*n
            for col in range(n):
                meeting = self.board.get((row,col))
                lmeeting = sorted(meeting)
                if self.show_modulo:
                    lmeeting = [x % n for x in lmeeting]
                if not lmeeting:
                    break
                print (Board.format_meeting(lmeeting), end=' ')
            if not lmeeting:
                break
            if do_test and self.double_persons[row]:
                ok = False
            if do_test:
                print(f'  -- {self.double_persons[row]}')
            else:
                print('')
            if False and row > 0:
                for col in range(n):
                     print (deltarow[col], end=' ')
                print()
        oktext=''
        if do_test:
            if self.double_pairs:
                ok = False
                oktext=f'ok={ok}'
                print(f'{self.double_pairs}')
            print(f'row={row}, col={col}{oktext}>>')
        print()
        return ok
