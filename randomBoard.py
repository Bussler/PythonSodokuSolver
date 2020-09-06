import random


def isValid(board, pos, lelement):  # check, if a number is legit
    y, x = pos
    # row
    for i in range(0, len(board[y])):
        if(board[y][i] == lelement and i != x):  # found a duplicate, wrong!
            return False
    # cols
    for i in range(0, len(board)):
        if(board[i][x] == lelement and i != y):
            return False
    # square
    xSquareIt = x // 3
    ySquareIt = y // 3
    for i in range(xSquareIt*3, (xSquareIt*3)+3):  # check the 3*3 boxes
        for j in range(ySquareIt*3, (ySquareIt*3)+3):
            if(board[j][i] == lelement and i != x and j != y):
                return False

    return True


class SodokuBoard:

    board = []

    def __init__(self, board):  # Bissel witzlos
        if(board is None):
            self.createBoard()
            self.fillBoard((0, 0))
        else:
            self.board = board

    def printBoard(self):
        for y in range(0, len(self.board)):
            for x in range(0, len(self.board[y])):
                if(x == len(self.board[y])-1):
                    print(self.board[y][x])
                else:
                    print(self.board[y][x], ", ", sep='', end='')

    def createBoard(self):
        for y in range(0, 9):
            row = []
            for x in range(0, 9):
                row.append(0)
            self.board.append(row)

    def fillBoard(self, pos):  # create random sodoku board with backtracking
        y, x = pos
        choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        while(len(choices) > 0):
            num = random.choice(choices)
            choices.remove(num)
            if(isValid(self.board, (y, x), num)):
                self.board[y][x] = num

                newPos = self.nextPos(pos)
                if(newPos is None):
                    return True
                else:
                    if(self.fillBoard(newPos)):
                        return True
                self.board[y][x] = 0

        return False

    def nextPos(self, pos):
        y, x = pos
        if(x == len(self.board[y])-1):
            if(y == len(self.board)-1):
                return None  # done
            else:
                return (y+1, 0)
        else:
            return (y, x+1)
