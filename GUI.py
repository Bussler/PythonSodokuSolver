import pygame
import copy
import solveTerminal as so
import randomBoard as rb
import GUIHelper
import csv
import threading
import time


class SodokuGrid:
    board = [
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

    solution = []
    curSelection = ()
    makingNotes = False
    ZeroesLeft = -1

    def __init__(self, window, width, height, board):
        self.width = width
        self.height = height
        self.curSelection = None
        self.makingNotes = False
        self.ZeroesLeft = -1
        if board is not None:
            self.board = board
        self.origBoard = copy.deepcopy(self.board)
        self.solution = copy.deepcopy(self.board)
        if not so.validateBoard(self.solution) or not so.solveSodoku(self.solution):
            self.printNotSolvable(window)
            global run
            run = False
            return
        self.drawGrid(window, NeonBlue)
        self.fillGrid(window)
        self.checkForWin()

    def printNotSolvable(self, window):  # TODO create specific TXT function
        window.fill(Black)
        menuFont = pygame.font.SysFont("comicsans", 50)
        gameText = menuFont.render("Not solvable!", True, White)
        gameTextRect = gameText.get_rect()
        gameTextRect.center = (540/2, (540/2)-150)
        window.blit(gameText, gameTextRect)
        pygame.display.update()
        pygame.time.delay(1000)

    def drawGrid(self, window, color):
        thiccness = 1
        for i in range(0, 9):
            if i % 3 == 0 and i != 0:
                thiccness = 5
            else:
                thiccness = 1
            pygame.draw.line(window, color, (0, i*(self.width/9)), (self.width, i*(self.width/9)), thiccness)
            pygame.draw.line(window, color, (i*(self.height/9), 0), (i*(self.height/9), self.height), thiccness)

    def fillGrid(self, window):
        for i in range(0, 9):
            for j in range(0, 9):
                myfont = pygame.font.SysFont("comicsans", 40)
                gridElem = self.board[i][j]
                if gridElem == 0:
                    gridElem = ""
                text = myfont.render(str(gridElem), False, White)
                window.blit(text, (j*(self.height/9)+20, i*(self.width/9)+20))

    def showSolution(self, window):
        self.drawGrid(window, NeonBlue)
        for i in range(0, 9):
            for j in range(0, 9):
                myfont = pygame.font.SysFont("comicsans", 40)
                gridElem = self.solution[i][j]
                text = myfont.render(str(gridElem), False, White)
                window.blit(text, (j*(self.height/9)+20, i*(self.width/9)+20))

    def eraseText(self, window):
        for i in range(0, 9):
            for j in range(0, 9):
                window.fill(Black, (j*(self.height/9)+20, i*(self.width/9)+20, 30, 30))

    def eraseComments(self, screen):
        for i in range(0, 9):
            for j in range(0, 9):
                screen.fill(Black, (j*(self.height/9)+4, i*(self.width/9)+4, 13, 20))

    def clickBoard(self, pos):  # map mouse pos to board pos and register for writing
        x = pos[0] // (self.width/9)
        y = pos[1] // (self.height/9)
        self.curSelection = (int(x), int(y))
        # print(self.curSelection, self.board[self.curSelection[1]][self.curSelection[0]])

    def placeNumber(self, screen, number):
        solNum = self.solution[self.curSelection[1]][self.curSelection[0]]
        gridNum = self.board[self.curSelection[1]][self.curSelection[0]]
        if solNum == number and gridNum == 0:  # correct input
            self.board[self.curSelection[1]][self.curSelection[0]] = number
            self.eraseText(screen)
            self.fillGrid(screen)
            self.checkForWin()
            self.drawGrid(screen, NeonBlue)
        else:  # wrong input
            print("Wrong Num")
            self.drawGrid(screen, Red)

    def placeComment(self, screen, number):
        screen.fill(Black, (self.curSelection[0]*(self.height/9)+4, self.curSelection[1]*(self.width/9)+4, 13, 20))  # delete prev note
        myfont = pygame.font.SysFont("comicsans", 30)
        text = myfont.render(str(number), False, EmeraldGreen)
        screen.blit(text, (self.curSelection[0]*(self.height/9)+5, self.curSelection[1]*(self.width/9)+5))

    def checkForWin(self):
        if self.ZeroesLeft == -1:
            counter = 0
            for i in range(0, 9):
                for j in range(0, 9):
                    if self.board[i][j] == 0:
                        counter += 1
            self.ZeroesLeft = counter
        else:
            self.ZeroesLeft -= 1
            if self.ZeroesLeft == 0:
                print("TODO YOU WIN")
                global run
                run = False


run = True
Black = (0, 0, 0)
White = (255, 255, 255)
NeonBlue = (62, 204, 252)
DarkBlue = (0, 48, 143)
EmeraldGreen = (10, 221, 8)
Red = (190, 0, 0)


def checkEvents(Grid, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global run
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mPos = pygame.mouse.get_pos()
            Grid.clickBoard(mPos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Grid.eraseText(screen)
                Grid.showSolution(screen)
            if event.key == pygame.K_BACKSPACE:
                Grid.board = copy.deepcopy(Grid.origBoard)
                Grid.ZeroesLeft = -1
                Grid.checkForWin()
                Grid.eraseText(screen)
                Grid.eraseComments(screen)
                Grid.fillGrid(screen)
            if event.key == pygame.K_LALT:
                if Grid.makingNotes is False:
                    Grid.makingNotes = True
                else:
                    Grid.makingNotes = False
            if event.key == pygame.K_1 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 1)
                else:
                    Grid.placeComment(screen, 1)
            if event.key == pygame.K_2 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 2)
                else:
                    Grid.placeComment(screen, 2)
            if event.key == pygame.K_3 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 3)
                else:
                    Grid.placeComment(screen, 3)
            if event.key == pygame.K_4 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 4)
                else:
                    Grid.placeComment(screen, 4)
            if event.key == pygame.K_5 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 5)
                else:
                    Grid.placeComment(screen, 5)
            if event.key == pygame.K_6 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 6)
                else:
                    Grid.placeComment(screen, 6)
            if event.key == pygame.K_7 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 7)
                else:
                    Grid.placeComment(screen, 7)
            if event.key == pygame.K_8 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 8)
                else:
                    Grid.placeComment(screen, 8)
            if event.key == pygame.K_9 and Grid.curSelection is not None:
                if Grid.makingNotes is False:
                    Grid.placeNumber(screen, 9)
                else:
                    Grid.placeComment(screen, 9)


def mainMenu(clock, FPS, screen):
    screen.fill(Black)
    menuFont = pygame.font.SysFont("comicsans", 50)
    gameText = menuFont.render("Sodoku Solver", True, White)
    gameTextRect = gameText.get_rect()
    gameTextRect.center = (540/2, (540/2)-150)
    screen.blit(gameText, gameTextRect)

    runMenu = True
    while runMenu:
        clock.tick(FPS)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runMenu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        if GUIHelper.button(screen, "Start Solving", 540/2, 540/2, 150, 40, click):
            runMenu = False
            GUISolveSod(clock, FPS, screen)  # Start solving process
            break

        if GUIHelper.button(screen, "Load Board", 540/2, (540/2)+50, 150, 40, click):
            runMenu = False
            GUILoadBoard(clock, FPS, screen)
            break

        if GUIHelper.button(screen, "createBoard", 540/2, (540/2)+100, 150, 40, click):
            runMenu = False
            GUICreateBoard(clock, FPS, screen)
            break

        pygame.display.update()


def GUICreateBoard(clock, FPS, screen):
    screen.fill(Black)
    SodBoard = rb.SodokuBoard(None)
    Grid = SodokuGrid(screen, 540, 540, SodBoard.board)
    global run
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # TODO event handling for Creating Random Board Scene

        pygame.display.update()


def GUISolveSod(clock, FPS, screen, givenBoard=None):
    screen.fill(Black)
    Grid = SodokuGrid(screen, 540, 540, givenBoard)

    while run:
        clock.tick(FPS)

        checkEvents(Grid, screen)

        pygame.display.update()


def GUILoadBoard(clock, FPS, screen):
    screen.fill(Black)
    menuFont = pygame.font.SysFont("comicsans", 40)
    gameText = menuFont.render("Please input file path", True, White)
    gameTextRect = gameText.get_rect()
    gameTextRect.center = (540/2, (540/2)-150)
    screen.blit(gameText, gameTextRect)
    inputBox = GUIHelper.InputBox(540/2-250, 540/2-100, 200, 30)

    runmenu = True
    while runmenu:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runmenu = False
            inputText = inputBox.handle_event(event)
            if inputText is not None:
                board = []
                with open(inputText, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        boardRow = []
                        for i in range(0, len(row)):
                            boardRow.append(int(row[i]))
                        board.append(boardRow)
                    runmenu = False
                    GUISolveSod(clock, FPS, screen, board)
                    return

        inputBox.update()
        inputBox.draw(screen)
        pygame.display.update()


def main():
    pygame.display.set_caption("SodokuSolve")

    screen = pygame.display.set_mode((540, 540))
    clock = pygame.time.Clock()
    FPS = 60

    mainMenu(clock, FPS, screen)


pygame.init()
main()
pygame.quit()
