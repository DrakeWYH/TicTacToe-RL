import numpy as np

from tictactoe import TicTacToe

def hashBoard(board):
    result = 0
    for i in range(9):
        if board[i] == -1:
            result += 2 * 3 ** i
        else:
            result += board[i] * 3 ** i
    return int(result)

def choose_action(board, mode='best', epsilon=0.2):
    global q_table
    q_action = q_table[hashBoard(board)]
    ac_idx = np.argwhere(board == 0).flatten()
    q_action = q_action[board == 0]
    if mode == 'best':
        best_idx = np.argmax(q_action)
        return ac_idx[best_idx]
    if mode == 'advn':
        if np.random.random() > epsilon:
            best_idx = np.argmax(q_action)
            return ac_idx[best_idx]
        else:
            n_action = n_table[hashBoard(board)][board == 0]
            min_idx = np.argmin(n_action)
            return ac_idx[min_idx]
    if mode == 'rand':
        if np.random.random() > epsilon:
            best_idx = np.argmax(q_action)
            return ac_idx[best_idx]
        else:
            rand_idx = np.random.choice(ac_idx.shape[0])
            return ac_idx[rand_idx]
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
    q_table = np.load('model/tictactoe_qlearning.npz')['q_table']
    
    ttt = TicTacToe()
    while True:
        board, turn, win, done = ttt.reset(np.random.choice([1, -1], 1)[0])
        while not done:
            if turn == 1:
                action = choose_action(board, mode='best')
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