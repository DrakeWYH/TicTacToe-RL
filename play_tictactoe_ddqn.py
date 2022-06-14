import numpy as np
import torch
import torch.nn as nn

from tictactoe import TicTacToe

def b9tob27(b9):
    b9 = b9.reshape([-1, 9])
    b27 = np.zeros([b9.shape[0], 9, 3])
    b27[b9 == 0, 0] = 1
    b27[b9 == 1, 1] = 1
    b27[b9 == -1, 2] = 1
    return b27.reshape([-1, 27])
    
class DQN(nn.Module): # Q(s)
    def __init__(self, n_input=3*3*3, n_output=3*3, n_hidden=81):
        super().__init__()
        self._fc1 = nn.Linear(n_input, n_hidden)
        self._fc2 = nn.Linear(n_hidden, n_output)
        self._sigmoid = nn.Sigmoid()
        
    def forward(self, board):
        board = torch.from_numpy(b9tob27(board)).float()
        x = self._fc1(board)
        y = self._fc2(self._sigmoid(x))
        return y
    
    def choose_action(self, board, mode='best', epsilon=0.2): # 不能批量处理
        board = board.flatten()
        if board.shape[0] != 9:
            print('只能处理一个棋盘。')
            return None
        
        ac_idx = np.where(board == 0)[0]
        if ac_idx.shape[0] == 0:
            print('已无法下子。')
            return None
        
        q = self.forward(board).detach().numpy()[0][ac_idx]
        
        if mode == 'best':
            idx = np.argmax(q)
            return ac_idx[idx]
        if mode == 'advn':
            if np.random.random() > epsilon:
                idx = np.argmax(q)
                return ac_idx[idx]
            else:
                idx = np.random.choice(ac_idx.shape[0])
                return ac_idx[idx]
        else:
            raise Exception('没有这种方法。')
        return None

def clean_output():
    import os
    import platform
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')
    
if __name__ == '__main__':
    ai = DQN()
    ai.load_state_dict(torch.load('model/tictactoe_ddqn.pkl'))
    
    ttt = TicTacToe()
    while True:
        board, turn, win, done = ttt.reset(np.random.choice([1, -1], 1)[0])
        while not done:
            if turn == 1:
                action = ai.choose_action(board, mode='best')
            elif turn == -1:
                clean_output()
                ttt.draw_board()
                action = int(input('输入下子位置：'))
                
            board, turn, win, done = ttt.step(action)
        clean_output()
        ttt.draw_board()
        if win == 1:
            print('电脑获胜！')
        elif win == -1:
            print('玩家获胜！')
        else:
            print('平局！')
        
        s = input('是否进行下一局游戏？（y/n）')
        if s == 'y':
            continue
        else:
            break