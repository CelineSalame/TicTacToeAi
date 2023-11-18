from tkinter import *
from tkinter import messagebox

class Opener:
    def __init__(self):
        self.root = Tk()

        Label(self.root, text="Do you have what it takes to defeat our A.I ?", font=("OCR-A", 18, "italic"),
              fg="Black").place(x=100, y=100)
        Label(self.root, text="Click here to start...", font=("OCR-A", 12, "italic"),
              fg="Black").place(x=280, y=250)
        Button(self.root, text="START", font="bold", fg="Black", bg="LightBlue", height=1, width=20, padx=10,
               pady=10, command=self.open_window).pack(expand=True)
        Label(self.root, text="Created By: \n Celine Salame \n Thea Saab \n  ", font="OCR-A",
              fg="Black").place(x=290, y=420)

        self.root.geometry('700x600')
        self.root.title('Welcome to Tic Tac Toe !')
        self.root.mainloop()

    def open_window(self):
        self.root.destroy()
        self.window = Game()


class Game(Toplevel):
    def __init__(self):
        self.root = Tk()
        self.board = []
        self.boardCopy = []
        self.xTurn = True
        self.steps = 0
        self.check = ""
        self.botSign = ""
        self.playerSign = ""
        self.comb = "000102101112202122001020011121021222001122021120"
        self.difficulty_selected = False 
        
        self.easy_button = Button(self.root, text="Easy", bg="LightBlue", height=3, width=15,
                                  command=lambda: self.set_difficulty("easy"))
        self.medium_button = Button(self.root, text="Medium", bg="LightBlue", height=3, width=15,
                                    command=lambda: self.set_difficulty("medium"))
        self.hard_button = Button(self.root, text="Hard", bg="LightBlue", height=3, width=15,
                                  command=lambda: self.set_difficulty("hard"))

        self.easy_button.grid(row=2, column=0, padx=50, pady=30)
        self.medium_button.grid(row=2, column=1, padx=50, pady=30)
        self.hard_button.grid(row=2, column=2, padx=50, pady=30)

        self.difficulty = None
        self.algorithm = None
        self.welcomeLabel = Label(self.root, text="START AS", fg="Black", font="OCR-A", width=10, height=10)
        self.welcomeLabel.grid(row=0, columnspan=2, padx=(200, 0))
        self.welcomeLabelUNder = Label(self.root, text="-------", fg="Black", font="OCR-A", width=10, height=10)
        self.welcomeLabelUNder.grid(row=1, columnspan=2, padx=(200, 0))
        self.startAsXButton = Button(self.root, text="X", bg="LightBlue", height=5, width=9,
                                     command=lambda: self.playerChoice(self.startAsXButton))
        self.startAsOButton = Button(self.root, text="O", bg="LightBlue", height=5, width=9,
                                     command=lambda: self.playerChoice(self.startAsOButton))
        self.startAsXButton.grid(row=1, column=0, padx=(0, 0), pady=50)
        self.startAsOButton.grid(row=1, column=2, padx=(0, 0), pady=50)

        self.boardSetup()

    def boardSetup(self):
        self.root.title("tic tac toe")
        self.welcomeLabel.grid()
        self.startAsXButton.grid()
        self.startAsOButton.grid()

        self.root.mainloop()

    def set_difficulty(self, level):
        self.difficulty = level
        self.easy_button.config(state="disabled")
        self.medium_button.config(state="disabled")
        self.hard_button.config(state="disabled")
        self.difficulty_selected = True

        # Additional setup or actions based on difficulty level, if needed
        if self.difficulty == "easy":
            self.algorithm = self.minimax_dfs
        elif self.difficulty == "medium":
            self.algorithm = self.minimax
        elif self.difficulty == "hard":
            self.algorithm = self.minimax_alphabeta

        if self.playerSign:
            self.gridButtons() 

    def start(self):
        if self.botSign == "X":
            self.compMove()

    def playerChoice(self, b):
        if b['text'] == "X":
            self.playerSign = "X"
            self.botSign = "O"

        else:
            self.playerSign = "O"
            self.botSign = "X"

        
        self.startAsXButton.config(state="disabled")
        self.startAsOButton.config(state="disabled")
        

        # Only proceed to gridButtons if difficulty is selected
        if self.difficulty_selected:
            self.gridButtons()


    def gridButtons(self):
        self.welcomeLabel.destroy()
        self.startAsXButton.destroy()
        self.startAsOButton.destroy()
        self.welcomeLabelUNder.destroy()
        for i in range(0, 3):
            self.board.append([])
            self.boardCopy.append([])
            for j in range(0, 3):
                self.board[i].append(
                    Button(self.root, text=' ', font=("Helvetica", 20), width=11, height=6,
                           bg="SystemButtonFace", command=lambda i=i, j=j: self.insertLetter(self.board[i][j])))
                self.board[i][j].grid(row=i, column=j)
                self.boardCopy[i].append(self.board[i][j]["text"])
        self.restart_button = Button(self.root, text="Restart Game", fg="Black", font="OCR-A", bg="LightBlue", command=self.restart_game)
        self.restart_button.grid(row=0, column=3, padx=10, columnspan=2)
        exit_button = Button(self.root, text="Quit",fg="Black", font="OCR-A", bg="LightBlue", command=self.root.destroy)
        exit_button.grid(row=0, column=5, padx=10, pady=10)
        self.start()

    def restart_game(self):
        # Destroy the current game window
        self.root.destroy()

        # Re-create the game window
        self.__init__()

    @staticmethod
    def spaceIsFree(button):
        if button["text"] == ' ':
            return True
        return False

    def freeSpaces(self):
        counter = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardCopy[i][j] == " ":
                    counter += 1
        return counter

    def insertLetter(self, button, who="player"):
        if not self.spaceIsFree(button):
            messagebox.showerror("Error", "This box is already taken \nPlease choose an empty box")
        else:
            if who == "comp":
                button["text"] = self.botSign
                self.steps += 1
                self.xTurn = not self.xTurn
            else:
                button["text"] = self.playerSign
                self.steps += 1
                self.xTurn = not self.xTurn
                self.refreshCopyBoard()
                if self.steps < 9:
                    self.compMove()

        if self.steps >= 5 and self.board[0][0]["state"] != "disabled":
            self.checkWin(self.botSign)
            self.checkWin(self.playerSign)
        if self.steps >= 9:
            if not self.checkWin(self.playerSign) and not self.checkWin(self.botSign):
                messagebox.showinfo("DRAW", "Nobody won ")
                self.disableAllButtons()

        

    def checkDraw(self):
        for lign in self.board:
            for button in lign:
                if self.spaceIsFree(button):
                    return False
        return True

    def checkDrawCopy(self):
        for lign in self.boardCopy:
            for mark in lign:
                if mark == " ":
                    return False
        return True

    def checkWin(self, check):
        i = 0
        while i < len(self.comb):
            if self.board[int(self.comb[i])][int(self.comb[i + 1])]["text"] == \
                    self.board[int(self.comb[i + 2])][int(self.comb[i + 3])]["text"] == \
                    self.board[int(self.comb[i + 4])][int(self.comb[i + 5])]["text"] == check:
                self.board[int(self.comb[i])][int(self.comb[i + 1])]["bg"] = \
                    self.board[int(self.comb[i + 2])][int(self.comb[i + 3])]["bg"] = \
                    self.board[int(self.comb[i + 4])][int(self.comb[i + 5])]["bg"] = 'LightGreen'
                self.disableAllButtons()
                messagebox.showinfo("CONGRATS", check + " has won ")
                return True
            i += 6
        return False 



    def checkWinCopy(self, check):
        i = 0
        while i < len(self.comb):
            if self.boardCopy[int(self.comb[i])][int(self.comb[i + 1])] == \
                    self.boardCopy[int(self.comb[i + 2])][int(self.comb[i + 3])] == \
                    self.boardCopy[int(self.comb[i + 4])][int(self.comb[i + 5])] == check:
                return True
            i += 6
        return False

    def disableAllButtons(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.board[i][j]["state"] = "disabled"

    def refreshCopyBoard(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.boardCopy[i][j] = self.board[i][j]["text"]

    def compMove(self):
        if self.botSign == "X" and self.steps == 0:
            self.insertLetter(self.board[0][0], "comp")
        else:
            if self.algorithm == self.minimax_alphabeta :
                bestScore = -1000
                bestMovei = None
                bestMovej = None
                for i in range(0, 3):
                    for j in range(0, 3):
                        if self.boardCopy[i][j] == ' ':
                            self.boardCopy[i][j] = self.botSign
                            #score = self.minimax_dfs(False)
                            score = self.minimax_alphabeta(False, -1000, 1000)
                            self.boardCopy[i][j] = ' '
                            if score > bestScore:
                                bestScore = score
                                bestMovei = i
                                bestMovej = j
                
                self.insertLetter(self.board[bestMovei][bestMovej], "comp")
            elif self.algorithm == self.minimax_dfs :
                bestScore = -1000
                bestMovei = None
                bestMovej = None
                for i in range(0, 3):
                    for j in range(0, 3):
                        if self.boardCopy[i][j] == ' ':
                            self.boardCopy[i][j] = self.botSign
                            score = self.minimax_dfs(False)
                            #score = self.minimax(False, -1000, 1000)
                            self.boardCopy[i][j] = ' '
                            if score > bestScore:
                                bestScore = score
                                bestMovei = i
                                bestMovej = j

                self.insertLetter(self.board[bestMovei][bestMovej], "comp")

            elif self.algorithm == self.minimax :
                bestScore = -1000
                bestMovei = None
                bestMovej = None
                for i in range(0, 3):
                    for j in range(0, 3):
                        if self.boardCopy[i][j] == ' ':
                            self.boardCopy[i][j] = self.botSign
                            score = self.minimax_dfs(False)
                            #score = self.minimax(False, -1000, 1000)
                            self.boardCopy[i][j] = ' '
                            if score > bestScore:
                                bestScore = score
                                bestMovei = i
                                bestMovej = j
                self.insertLetter(self.board[bestMovei][bestMovej], "comp")


    def minimax(self, isMaximizing):
        if self.checkWinCopy(self.botSign):
            return 1 * self.freeSpaces()
        elif self.checkWinCopy(self.playerSign):
            return -1 * self.freeSpaces()
        elif self.checkDrawCopy():
            return 0

        if isMaximizing:
            elmnts = [-1000, self.botSign, False, max]
        else:
            elmnts = [1000, self.playerSign, True, min]

        bestScore = elmnts[0]
        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardCopy[i][j] == ' ':
                    self.boardCopy[i][j] = elmnts[1]
                    score = self.minimax(elmnts[2])
                    self.boardCopy[i][j] = ' '
                    bestScore = elmnts[3](score, bestScore)

        return bestScore


    def minimax_alphabeta(self, isMaximizing, alpha, beta):
        if self.checkWinCopy(self.botSign):
            return 1 * self.freeSpaces()
        elif self.checkWinCopy(self.playerSign):
            return -1 * self.freeSpaces()
        elif self.checkDrawCopy():
            return 0

        if isMaximizing:
            elmnts = [-1000, self.botSign, False, max]
        else:
            elmnts = [1000, self.playerSign, True, min]

        bestScore = elmnts[0]
        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardCopy[i][j] == ' ':
                    self.boardCopy[i][j] = elmnts[1]
                    score = self.minimax_alphabeta(elmnts[2], alpha, beta)
                    self.boardCopy[i][j] = ' '
                    bestScore = elmnts[3](score, bestScore)
                    if not elmnts[2]:
                        alpha = elmnts[3](alpha, bestScore)
                        if beta <= alpha:
                            break
                    else:
                        beta = elmnts[3](beta, bestScore)
                        if beta <= alpha:
                            break
        return bestScore

    def minimax_dfs(self, isMaximizing):
        if self.checkWinCopy(self.botSign):
            return 1 * self.freeSpaces()
        elif self.checkWinCopy(self.playerSign):
            return -1 * self.freeSpaces()
        elif self.checkDrawCopy():
            return 0

        if isMaximizing:
            elmnts = [self.botSign, False, max]
        else:
            elmnts = [self.playerSign, True, min]

        bestScore = float('-inf') if elmnts[2] == max else float('inf')

        for i in range(0, 3):
            for j in range(0, 3):
                if self.boardCopy[i][j] == ' ':
                    self.boardCopy[i][j] = elmnts[0]
                    score = self.minimax_dfs(elmnts[2])
                    self.boardCopy[i][j] = ' '
                    bestScore = elmnts[2](score, bestScore)

        return bestScore



myGame = Opener()
