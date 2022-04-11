from tkinter import ttk
import tkinter as tk
from tkinter import *
import random
import time
import enchant


class Boggle(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(pady=20)
        self.buttonList = []
        self.last_button_clicked = []
        self.tbutvar = tk.StringVar()
        self.word = ""
        self.time = 90
        self.create_boggle()

    def create_boggle(self):
        # make all the widgets. or at least most of them
        """
        We want:
        4x4 grid; 16 widgets in total

        """
        # top level frames
        top_frame = tk.Frame(master=self)
        bottom_frame = tk.Frame(master=self)
        top_frame.pack()
        bottom_frame.pack(padx=45, pady=45)

        # button to finalise a word
        final_butt = Button(top_frame, text="OK", command=self.finalizeWord, height=3, width=6)
        final_butt.pack(anchor=NW)

        # create a timer
        timerbutt = Button(top_frame, text="90", command=self.updateTimer, textvariable=self.tbutvar, height=3, width=6)
        timerbutt.pack(anchor=NE)

        # create a list of letters/alphabets????    1
        letters = self.generate_letters()

        # create the boggle dice
        # buttons_list = [[0] * 4] * 4
        buttons_list = []
        for i in range(4):
            row = []
            for j in range(4):
                button = Button(bottom_frame, text=letters[4 * i + j],
                                command=lambda index=(i, j): self.click_tile(index), height=2, width=5)
                button.grid(row=i, column=j)
                row.append(button)
                # buttons_list[i][j] = Button(bottom_frame, text=str(i) + str(j))
                # buttons_list[i][j].grid(row=i, column=j)
            buttons_list.append(row)

        self.buttonList = buttons_list
        # self.display_letters(buttons_list, letters)

        # finesse sizing a bit

    def generate_letters(self):
        # # The alphabet
        # letters_list = []
        # for i in range(65,81):
        #     letters_list.append(chr(i))
        # letters_list.append('Qu')
        # for i in range(82, 91):
        #     letters_list.append(chr(i))
        #
        # # The other way you can do it
        # # second_list = ['Qu']
        # # for c in "ABCDEFGHIJKLMNOPRSTUVWXYZ":
        # #     second_list.append(c)
        # # print(second_list)

        """
        imagine six dies; each face with a letter on it
        vowels occur twice as often as consonants???
        r's, d's, s's and n's occur more frequently (maybe 50%)
        
        """
        dice = [['A', 'E', 'I', 'O', 'U', 'Y'],
                ['B', 'C', 'D', 'F', 'G', 'H'],
                ['R', 'U', 'S', 'I', 'O', 'M'],
                ['J', 'K', 'L', 'A', 'C', 'E'],
                ['O', 'N', 'M', 'P', 'R', 'Qu'],
                ['S', 'R', 'N', 'T', 'U', 'M'],
                ['A', 'E', 'I', 'O', 'U', 'Y'],
                ['H', 'I', 'P', 'T', 'D', 'N'],
                ['W', 'X', 'Y', 'Z', 'S', 'I'],
                ['G', 'K', 'A', 'L', 'F', 'O'],
                ['C', 'U', 'O', 'X', 'P', 'U'],
                ['N', 'R', 'T', 'D', 'E', 'Z'],
                ['A', 'H', 'K', 'S', 'B', 'Y'],
                ['F', 'O', 'A', 'P', 'W', 'L'],
                ['S', 'V', 'T', 'N', 'R', 'H'],
                ['G', 'E', 'S', 'M', 'B', 'Y']]

        # Create a list of 16 letters
        boggle_board_letters = []
        for i in range(16):
            random_index = random.randrange(0, 6)
            boggle_board_letters.append(dice[i][random_index])

        print(boggle_board_letters)
        return boggle_board_letters

    def display_letters(self, buttons, letters):
        # for variable in buttons:
        #     for stuff in variable:
        #         print(stuff)

        # buttons[0][0]['text'] = "X"
        # buttons[3][3]['text'] = "X"
        #
        x = 0
        for row in buttons:
            for button in row:
                button['text'] = letters[x]

                x += 1

    # keep tab of the tiles clicked
    # If there is a pause of 0.5 seconds, document the sequence of clicks as one word
    # or start out with hitting "enter" or "space" to confirm a word

    def click_tile(self, index_coord):
        i, j = index_coord
        if self.last_button_clicked == []:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i and self.last_button_clicked[1] == j:
            pass
        elif self.last_button_clicked[0] == i and self.last_button_clicked[1] == j + 1:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i + 1 and self.last_button_clicked[1] == j:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i - 1 and self.last_button_clicked[1] == j:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i - 1 and self.last_button_clicked[1] == j - 1:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i + 1 and self.last_button_clicked[1] == j - 1:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i - 1 and self.last_button_clicked[1] == j + 1:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i + 1 and self.last_button_clicked[1] == j + 1:
            self.word += self.buttonList[i][j].cget("text")
        elif self.last_button_clicked[0] == i and self.last_button_clicked[1] == j - 1:
            self.word += self.buttonList[i][j].cget("text")

        self.last_button_clicked = [i, j]

    # Check if word created is a valid word
    # If it is, store it in a list, calculate score and display the word in the side

    def finalizeWord(self):
        self.check_word()
        self.word = ""

    def check_word(self):
        mot = enchant.Dict("en_US")
        if len(self.word) > 2:
            print(self.word, mot.check(self.word))
        else:
            print("Invalid word")

    def store_words(self):
        pass

    def keep_score(self):
        pass

    # def timer(self):
    #     var = 10
    #     while var > 0:
    #         # decrement every second
    #         var -= 1
    #         self.update()
    #         time.sleep(1)
    #         self.tbutvar.set(var)
    #         print(var)

    def updateTimer(self):
        self.tbutvar.set(self.time)
        self.after(1000, self.updateTimer)
        self.time -= 1
# When you click a tile, it calls "Click_tile" and gets the text of the tile
# a timer is reset and start counting to 0.5s
# The tile is checked for adjacency with any previous tiles
# That text is held in a buffer
# Each subsequent click concatenates those characters
# The resulting string is searched against the dictionary, after the timer runs out
