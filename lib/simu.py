from .board import Board
from .helper import ordered_pairs
from .helper import DEBUG1, DEBUG2, DEBUG3, DEBUG4, DEBUG5
from .gen_meetings import gen_meetings

#----------------------
class Simu:
    #-----------------------------
    def __init__(self, N, show_modulo=False, break_after_first=True, sym=False, init_round=True, ortho=False, do_test=False):
        self.N = N
        self.NN = NN = N*N
        self.free_pairs = ordered_pairs(range(NN))
        self.board = Board(N, person_count=NN, show_modulo=show_modulo, ortho=ortho, sym=sym, init_round=init_round)
        self.do_test = do_test
        self.break_after_first = break_after_first
        self.reset_all_persons_free()
        self.count_full_solutions = 0
        self.row0_changed = False

    #-----------------------------
    def reset_all_persons_free(self):
        self.free_persons = set(range(self.NN))

    #-----------------------------
    def test_conditions(self, meeting, meet_pairs, pair):
        n = self.N
        ret = False

        if DEBUG1: print(f'test_conditions(meeting={sorted(meeting)}, meet_pairs={meet_pairs}')

        row, col = pair
        is_growing=True
        if col > 0 or row > 0:
            if col > 0:
                pair0 = row0, col0 =  self.prev_row_col(row, col)
            elif col==0 and row > 0:
                pair0 = row0, col0 = row - 1, col
            assert row0 in range(n), pair
            assert col0 in range(n), pair
            prev_meeting = self.board.board[pair0]
            is_growing = sorted(meeting) > sorted(prev_meeting)
            if col > 0:
                assert sorted(meeting) > sorted(prev_meeting), [pair, sorted(meeting) , pair0, sorted(prev_meeting)]


        no_round_doubles = workshop_condition = False
        if is_growing:
            no_round_doubles = meeting <= self.free_persons
            if no_round_doubles:
                workshop_condition = meet_pairs <= self.free_pairs

        if no_round_doubles and workshop_condition and is_growing:
            ret = True

        if DEBUG3:
            if not ret: print(f'test_conditions: meeting={sorted(meeting)} '+
                         f'is_growing:{is_growing}, ' +
                         f'no_round_doubles:{no_round_doubles}, ' +
                         f'workshop_condition:{workshop_condition}, ret={ret}')

        return ret

    #-----------------------------
    def set_meeting(self, meeting, meet_pairs, pair):
        self.board.set_meeting(meeting, pair)
        self.set_free(meeting, meet_pairs, pair)

    #-----------------------------
    def unset_meeting(self, meeting, meet_pairs, pair):
        self.board.unset_meeting(pair)
        self.unset_free(meeting, meet_pairs, pair)

    #-----------------------------
    def set_free(self, meeting, meet_pairs, pair):
        self.free_pairs -= meet_pairs
        self.free_persons -= meeting
        if not self.free_persons:
            if self.free_pairs:
                self.reset_all_persons_free()

    #-----------------------------
    def unset_free(self, meeting, meet_pairs, pair):
        self.free_pairs = self.free_pairs.union(meet_pairs)
        if len(self.free_persons) == self.NN:
            self.free_persons = set(meeting)
        else:
            self.free_persons = self.free_persons.union(meeting)
        assert self.free_persons, (meeting, meet_pairs, pair)

    #-----------------------------
    def next_row_col(self, row, col):
        #row0, col0 = row, col
        n = self.N
        col = (col + 1) % n
        if col == 0:
            row += 1
        #print (f' next {(row0, col0)} -> {(row, col)}')
        return row, col

    #-----------------------------
    def prev_row_col(self, row, col):
        #row0, col0 = row, col
        n = self.N
        if col == 0:
            row -= 1
            col = n - 1
        else:
            col = (col - 1) % n
        #print (f' prev {(row0, col0)} -> {(row, col)}')
        return row, col

    #-----------------------------
    def pruefe(self, row, col, level):
        if self._break:
            return
        n = self.N
        indent=level*4*' '
        prefix__in  = f'<IN  {level}<< {indent}, pruefe '
        prefix_out = f'<OUT {level}<< {indent}, pruefe '
        if DEBUG4: print(f'{prefix__in} row={row}, col={col}')

        if DEBUG1: print(f'5100, pruefe  row={row}, col={col}')
        row, col = self.next_row_col(row, col)
        if DEBUG1: print(f'5200, pruefe  row={row}, col={col}')

        pair = row, col
        if row >= n:
            if self.board.is_row0_changed() == True:
                self._break=True
            else:
                self.count_full_solutions +=1
                if self.do_test:
                    self.board.test()
                self.board.show(str(pair)+" dontshow", do_test=self.do_test)
                if self.break_after_first:
                    self._break=True
            return
        else:
            for meeting in gen_meetings(row=row, col=col, n=n):
                meet_pairs = ordered_pairs(meeting)
                success_meeting = self.test_conditions(meeting, meet_pairs, pair)
                if DEBUG4: print(f'{prefix__in} meeting={sorted(meeting)},  row={row}, col={col}, success={success_meeting}')
                if success_meeting:
                    #self.test_set_unset(meeting, meet_pairs, pair)
                    self.set_meeting(meeting, meet_pairs, pair)
                    self.pruefe(row, col, level+1)
                    self.unset_meeting(meeting, meet_pairs, pair)
        if DEBUG4: print(f'{prefix_out} row={row}, col={col}')

    #-----------------------------
    def store_globals(self):
        self.free_pairs0 = self.free_pairs.copy()
        self.free_persons0 = self.free_persons.copy()

    #-----------------------------
    def restore_globals(self):
        self.free_pairs = self.free_pairs0.copy()
        self.free_persons = self.free_persons0.copy()

    #-----------------------------
    def test_set_unset(self, meeting, meet_pairs, pair):
        context = (meeting, pair)
        self.store_globals()
        self.set_meeting(meeting, meet_pairs, pair)
        self.unset_meeting(meeting, meet_pairs, pair)
        assert self.free_persons == self.free_persons0, (context, self.free_persons , self.free_persons0)
        assert self.free_pairs == self.free_pairs0, (context, self.free_pairs , self.free_pairs0)
        self.restore_globals()
