import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros([9,])
        self.turn = 1
        self.win = 0
        self.done = 0
    
    def reset(self, turn):
        self.board = np.zeros([9,])
        self.turn = turn
        self.win = 0
        self.done = 0
        return self.board.copy(), self.turn, self.win, self.done
    
    def _judge_win(self):
        row0 = self.board[0] + self.board[1] + self.board[2]
        row1 = self.board[3] + self.board[4] + self.board[5]
        row2 = self.board[6] + self.board[7] + self.board[8]
        col0 = self.board[0] + self.board[3] + self.board[6]
        col1 = self.board[1] + self.board[4] + self.board[7]
        col2 = self.board[2] + self.board[5] + self.board[8]
        crs0 = self.board[0] + self.board[4] + self.board[8]
        crs1 = self.board[2] + self.board[4] + self.board[6]
        if row0 == 3 or row1 == 3 or row2 == 3 or col0 == 3 or col1 == 3 or col2 == 3 or crs0 == 3 or crs1 == 3:
            return 1, 1
        if row0 == -3 or row1 == -3 or row2 == -3 or col0 == -3 or col1 == -3 or col2 == -3 or crs0 == -3 or crs1 == -3:
            return -1, 1
        if not (self.board == 0).any():
            return 0, 1
        return 0, 0
        
    def step(self, i):
        if self.done:
            raise Exception('游戏已结束！')
        if self.board[i] != 0:
            raise Exception('该处无法下子！')
        self.board[i] = self.turn
        self.turn = -self.turn
        self.win, self.done = self._judge_win()
        return self.board.copy(), self.turn, self.win, self.done
    
    def draw_board(self):
        output_str = []
        for i in range(9):
            if self.board[i] == 0:
                output_str.append(str(i))
            else:
                output_str.append('o' if self.board[i] == 1 else 'x')
        print(output_str[0] + '|' + output_str[1] + '|' + output_str[2] + '  ' + ('o' if self.turn == 1 else 'x'))
        print(output_str[3] + '|' + output_str[4] + '|' + output_str[5])
        print(output_str[6] + '|' + output_str[7] + '|' + output_str[8])