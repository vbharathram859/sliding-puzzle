import numpy as np
import heapq
import collections
import time
N = 5

class Puzzle(object):
    def __init__(self):
        self.board = np.zeros((N, N), dtype=np.uint64)  # stores the array
        for i in range(N):
            for j in range(N):
                self.board[i, j] = N*i+j+1  # set the array to be solved
        self.board[N-1, N-1] = 0  # 0 -> black space
        self.indices = [N-1, N-1]  # stores the indices of the blank space
        self.set_up()  # scramble the board

    def get_board(self):
        return self.board

    def play_game(self):
        solved = np.zeros((N, N), dtype=np.uint64)
        for i in range(N):
            for j in range(N):
                solved[i, j] = i*N+j+1
        solved[N-1, N-1] = 0

        print("To make a move, give the direction in which you wish to move a tile using WASD keys. The tile reading "
              "0 is the blank tile")

        while not np.array_equal(solved, self.board):
            x = input("Move: ")
            move(x, self.board, self.indices)
            print(self.board)

    def set_up(self):  # to make sure that the board is solvable, we make a number of random moves to set up the board
        for i in range(1000):
            self.rand_move()

    def rand_move(self):
        rand = np.random.randint(0, 4)  # 4 possible moves, select one
        if rand == 0:
            if not move('w', self.board, self.indices):  # if that move is not possible (if it is the move is made)
                return self.rand_move()  # then make a different move
        elif rand == 1:
            if not move('a', self.board, self.indices):
                return self.rand_move()
        elif rand == 2:
            if not move('s', self.board, self.indices):
                return self.rand_move()
        elif rand == 3:
            if not move('d', self.board, self.indices):
                return self.rand_move()


def move(dir, board, indices):  # takes w, a, s, or d as input (dir), numpy array (NxN, board), indices of 0 in board
    ind1 = indices[0]
    ind2 = indices[1]
    if dir == 'w':
        if ind1 == N - 1:  # then there is no possible 'w' move and the move is illegal
            return False
        board[ind1, ind2] = board[ind1 + 1, ind2]  # make the swap on the board
        board[ind1 + 1, ind2] = 0
        indices[0] += 1  # since we just moved the blank space
    elif dir == 's':
        if ind1 == 0:  # no possible 's' move
            return False
        board[ind1, ind2] = board[ind1 - 1, ind2]
        board[ind1 - 1, ind2] = 0
        indices[0] -= 1
    elif dir == 'a':
        if ind2 == N - 1:  # no possible 'a' move
            return False
        board[ind1, ind2] = board[ind1, ind2 + 1]
        board[ind1, ind2 + 1] = 0
        indices[1] += 1
    elif dir == 'd':
        if ind2 == 0:  # no possible 'd' move
            return False
        board[ind1, ind2] = board[ind1, ind2 - 1]
        board[ind1, ind2 - 1] = 0
        indices[1] -= 1
    else:  # if the input is not w, a, s, or d
        return False
    return True  # then the move was possible


class Solver(object):
    def __init__(self, puzzle):  # takes a Puzzle class
        self.game = puzzle
        self.correct = np.zeros((N, N), dtype=np.uint64)  # to create the solved array
        for i in range(N):
            for j in range(N):
                self.correct[i, j] = i * N + j + 1
        self.correct[N-1, N-1] = 0  # blank is in bottom right

    def find_path(self, cur):
        lst = []
        while True:
            lst.append(cur[1])  # add board to path
            if cur[3] is not None:  # if this node has a parent
                cur = cur[3]  # then find the parent's parent
            else:
                break
        lst.reverse()  # reverse so the first item is the starting state
        for i in range(len(lst)):
            print(f"{i+1}:\n {lst[i]}")  # since we also print the start state, there will be n+1 states printed out when something requires n+1 moves

    def find_path_BFS(self, cur):  # different find_path for BFS since "cur" is different (doesn't have priority, moves)
        lst = []
        while True:
            lst.append(cur[0])  # add board to path
            if cur[2] is not None:  # if this node has a parent
                cur = cur[2]  # then find the parent's parent
            else:
                break
        lst.reverse()  # reverse so the first item is the starting state
        for i in range(len(lst)):
            print(f"{i+1}:\n {lst[i]}")  # since we also print the start state, there will be n+1 states printed out when something requires n moves

    def A_Star(self):
        cur1 = self.game.get_board()  # cur1 is the current array
        cur2 = self.game.indices  # cur2 is the current location of the blank
        cur = [-1, (0, cur1, cur2, None, 0)]  # cur[0] for priority, cur[1] will be the "node". cur[1][0] will be the time. cur[1][1] stores board, cur[1][2] stores indices for blank, cur[1][3] will store parent, cur[1][4] stores the number of moves so far
        if np.array_equal(cur[1][1], self.correct):  # if the first state is correct
            cur[0] = 0
        cur = tuple(cur)
        visited = set()  # set so that we have O(1) time to check if x in visited
        visited.add(str(cur1))
        queue = []

        while True:
            if cur[0] == cur[1][4]:  # if this is the end state—then cur[0] will just be the number of moves (every tile will be in the right spot)
                self.find_path(cur[1])  # then print out the path
                return True
            for i in range(4):  # at most 4 possible moves, go through each
                if i == 0:
                    cur_move = 'w'  # cur_move stores direction we are testing
                elif i == 1:
                    cur_move = 'a'
                elif i == 2:
                    cur_move = 's'
                else:
                    cur_move = 'd'
                move_new = cur[1][1].copy()  # the board
                move_new_ind = cur[1][2].copy()  # indices of blank
                check = move(cur_move, move_new, move_new_ind)  # create a new state of the board. If not possible, check is False
                if check and str(move_new) not in visited:  # if move is possible and gives us a new state
                    num = 0  # will be the priority
                    for a in range(N):
                        for b in range(N):
                            if move_new[a, b] != 0:
                                cor_b = (move_new[a, b]-1) % N  # finds the correct second index of this number
                                cor_a = (move_new[a, b] - cor_b) // N  # finds the correct first index of this number
                                num += (abs(a - cor_a) + abs(b - cor_b))  # num is sum of how far this number is from both indices it is supposed to be at
                    num_moves = cur[1][4] + 1  # number of moves so far
                    num += num_moves  # adding this helps find a more efficient path
                    heapq.heappush(queue, (int(num), (time.time(), move_new, move_new_ind, cur[1], num_moves)))  # add to queue—num is the priority, and time.time() is incase the priorities are the same—then check the time they were added
                    visited.add(str(move_new))  # add to visited

            if len(queue) == 0:  # if queue is empty, this board is not solvable
                print("This is not solvable!")
                return False
            else:
                cur = heapq.heappop(queue)  # update cur

    def Dijkstra(self):  
        cur1 = self.game.get_board()  # cur1 is the current array
        cur2 = self.game.indices  # cur2 is the current location of the blank
        cur = (cur1, cur2, None)  # cur[2] will store parent
        visited = set()  # set so that we have O(1) time to check if x in visited
        visited.add(str(cur1))
        queue = collections.deque()

        while True:
            if np.array_equal(cur[0], self.correct):  # if this is the end state
                self.find_path_BFS(cur)  # then print out the path
                return True
            for i in range(4):  # at most 4 possible moves, go through each
                if i == 0:
                    cur_move = 'w'  # cur_move stores direction we are testing
                elif i == 1:
                    cur_move = 'a'
                elif i == 2:
                    cur_move = 's'
                else:
                    cur_move = 'd'
                move_new = cur[0].copy()  # the board
                move_new_ind = cur[1].copy()  # indices of blank
                check = move(cur_move, move_new, move_new_ind)  # create a new state of the board. If not possible, check=False
                if check and str(move_new) not in visited:  # if move is possible and gives us a new state
                    queue.appendleft((move_new, move_new_ind, cur))  # add to queue
                    visited.add(str(move_new))  # add to visited

            if len(queue) == 0:  # if queue is empty, this board is not solvable
                print("This is not solvable!")
                return False
            else:
                cur = queue.pop()  # update cur
    def GBFS(self):   # Greedy Best First Search
        cur1 = self.game.get_board()  # cur1 is the current array
        cur2 = self.game.indices  # cur2 is the current location of the blank
        cur = [-1, (0, cur1, cur2, None)]  # cur[0] for priority, cur[1] will be the "node". cur[1][0] will be the time. cur[1][1] stores board, cur[1][2] stores indices for blank, cur[1][3] will store parent
        if np.array_equal(cur[1][1], self.correct):  # if the first state is correct
            cur[0] = 0
        cur = tuple(cur)
        visited = set()  # set so that we have O(1) time to check if x in visited
        visited.add(str(cur1))
        queue = []

        while True:
            if cur[0] == 0:  # if this is the end state—then cur[0] will just be the number of moves (every tile will be in the right spot)
                self.find_path(cur[1])  # then print out the path
                return True
            for i in range(4):  # at most 4 possible moves, go through each
                if i == 0:
                    cur_move = 'w'  # cur_move stores direction we are testing
                elif i == 1:
                    cur_move = 'a'
                elif i == 2:
                    cur_move = 's'
                else:
                    cur_move = 'd'
                move_new = cur[1][1].copy()  # the board
                move_new_ind = cur[1][2].copy()  # indices of blank
                check = move(cur_move, move_new, move_new_ind)  # create a new state of the board. If not possible, check is False
                if check and str(move_new) not in visited:  # if move is possible and gives us a new state
                    num = 0 
                    for a in range(N):
                        for b in range(N):
                            if move_new[a, b] != 0:
                                cor_b = (move_new[a, b]-1) % N  # finds the correct second index of this number
                                cor_a = (move_new[a, b] - cor_b) // N  # finds the correct first index of this number
                                num += (abs(a - cor_a) + abs(b - cor_b))  # num is sum of how far this number is from both indices it is supposed to be at
                    heapq.heappush(queue, (int(num), (time.time(), move_new, move_new_ind, cur[1])))  # add to queue—num is the priority, and time.time() is incase the priorities are the same—then check the time they were added
                    visited.add(str(move_new))  # add to visited

            if len(queue) == 0:  # if queue is empty, this board is not solvable
                print("This is not solvable!")
                return False
            else:
                cur = heapq.heappop(queue)  # update cur

def main():
    p = Puzzle()
    s = Solver(p)
    s.GBFS()



if __name__ == "__main__":
    main()
