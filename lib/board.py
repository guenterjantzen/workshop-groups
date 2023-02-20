from .helper import ordered_pairs
from .helper import DEBUG1, DEBUG2, DEBUG3, DEBUG4, DEBUG5
class Board:
    #-----------------------------
    def __init__(self, N, show_modulo=False, ortho=False, sym=False, init_round=True, signs=None, verbose=False):
        self.N = N
        self.NN = N*N
        self.board={}
        self.free_pairs = ordered_pairs(range(self.NN))
        self.norm_row0 = False
        self.double_pairs = set()
        self.double_persons = N*[None]
        self.init_standard_row0()
        self.signs = signs or [str(i) for i in range(self.NN)]
        if signs:
            if len(signs) == N:
                show_modulo = True
            elif len(signs)== self.NN:
                show_modulo = False
        self.ortho=ortho
        self.sym = sym
        self.init_round = init_round and not (show_modulo)
        self.show_modulo= show_modulo
        if verbose:
            print(473, self.signs)
    #-----------------------------
    def init_standard_row0(self):
        #[frozenset({0, 3, 6}), frozenset({1, 4, 7}), frozenset({8, 2, 5})]
        n = self.N
        self.standard_row0=[]
        for i in range(n):
            meeting=set()
            for j in range(n):
                meeting.add(i+j*n)
            self.standard_row0.append(frozenset(meeting))

    #-----------------------------
    def set_meeting(self, meeting, pair):
        n = self.N
        row, col = pair
        info = f'row={row}, col={col}'
        if meeting:
            info=f'{info}, meeting={sorted(meeting)},'
        if DEBUG5: print(f'Board.set_meeting  {info}')
        assert 0 <= row <= n, info
        assert 0 <= col <= n, info

        #Mindestens zwei Runden, also mit Einheitsrund drei
        if n == 6  and row > 2 and col == 0:
            self.show(pair, True)

        self.board[(row,col)] = meeting
        if self.sym:
            if (row, col) == (n-1, n-1):
                self.try_sym_order()

   #-----------------------------
    def get_row0(self):
        n = self.N
        row={}
        is_full_row=True
        for col in range(n):
            if not (0, col) in self.board:
                is_full_row = False
        if is_full_row:
            row = [self.board[(0,i)] for i in range(n)]
        return row

    #-----------------------------
    def is_row0_changed(self):
        n = self.N
        row0 = self.get_row0()
        ret = None
        if len(row0) == n:
            ret = row0 != self.standard_row0
        #print(ret, row0)
        return ret

    #-----------------------------
    def try_sym_order(self):
        n = self.N
        meeting0r = self.board[(0,n-1)]
        check0r = set([n*i+n-1 for i in range(n)])
        if  meeting0r == check0r:
            self.norm_row0 = True
            meeting10 = self.board[(1,0)]
            order = [i % n for i in sorted(meeting10)]
            assert sorted(order) == list(range(n)), order
            board2 = self.board.copy()
            for row, ordered_row in enumerate(order):
                for col in range(n):
                    self.board[(row, col)] = board2[(ordered_row, col)]

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

    def format_meeting(self, lmeeting):
        s=[f'{self.signs[i]:>2}' for i in lmeeting]
        sep = ' '
        return sep.join(s)

    #-----------------------------
    def show(self, comment, do_test = False):
        def build_line(linemeetings, linecomments):
            #print(linemeetings, linecomments)
            linetokens = [self.format_meeting(lmeeting) for lmeeting in linemeetings]
            line_without_comment = " | ".join(linetokens)
            comment = f'{" ".join(linecomments)}'
            line = f'{line_without_comment} {comment}'
            return line

        lines=[]
        ortho = self.ortho

        ok = True
        if do_test:
            lines.append(f'<< board {comment}')

        n = self.N
        row = -1
        if self.init_round:
            for col in range(n):
                lower, upper = n*col, n*col+n
                lmeeting = list(range(lower, upper))
                self.board[(row,col)] = lmeeting
            row = -2
        while row < n-1:
            linemeetings=[]
            linecomments=[]
            row+=1
            for col in range(n):
                meeting = self.board.get((row,col))
                if not meeting:
                    break
                lmeeting = sorted(meeting)
                if self.show_modulo:
                    lmeeting = [i % n for i in lmeeting]
                linemeetings.append(lmeeting)
            if not meeting:
                break
            if do_test and self.double_persons[row]:
                ok = False
            if do_test:
                linecomments.append(f'  -- {self.double_persons[row]}')
            else:
                linecomments.append('')
            if ortho == True:
                orthomeetings=[]
                for orow in range(n):
                    orthomeetings.append([])
                    for ocol in range(n):
                        orthomeetings[orow].append(linemeetings[ocol][orow])
                linemeetings = orthomeetings
            line = build_line(linemeetings, linecomments)
            lines.append(line)
        oktext=''
        if do_test:
            if self.double_pairs:
                ok = False
                oktext=f'ok={ok}'
                lines.append(f'{self.double_pairs}')
            lines.append(f'row={row}, col={col}{oktext}>>')

        for line in lines:
            print(line)
        print()

        return ok
