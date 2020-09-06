import randomBoard as rB
import random


boardTest = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
            ]


def getNextEmpty(board):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            if(board[y][x] == 0):
                return (y, x)
    return None


def validateBoard(board):
    if len(board) != 9:
        return False
    for row in board:
        if len(row) != 9:
            return False
    return True


def solveSodoku(board):
    pos = getNextEmpty(board)
    if(pos is None):
        return True
    y, x = pos
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while(len(choices) > 0):
        num = random.choice(choices)
        choices.remove(num)
        if(rB.isValid(board, (y, x), num)):
            board[y][x] = num
            if(solveSodoku(board)):
                return True
            board[y][x] = 0  # don't forget to set back for backtracing!
    return False


# SodBoard = rB.SodokuBoard(boardTest)
# solveSodoku(SodBoard.board)
# SodBoard.printBoard()
