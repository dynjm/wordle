"""
Application based on the game Wordle
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

import random


class Wordle(toga.App):

    def startup(self): # Startup Menu/Main Menu
    
        # main box
        self.startup_box = toga.Box(style=Pack(direction=COLUMN))
        
        # WORDLE section
        wordle_vbox = toga.Box(style=Pack(direction=COLUMN))
        wordle_hbox = toga.Box(style=Pack(direction=ROW))
        wordle_hbox.add(toga.Label("", style=Pack(flex=1)))
        for letter in ['W', 'O', 'R', 'D', 'L', 'E']:
            letter_box = toga.Box(style=Pack(padding=5, background_color='gray'))
            letter_box.add(toga.Button(letter, style=Pack(height=100, width=100, font_size=25)))
            wordle_hbox.add(letter_box)
        wordle_hbox.add(toga.Label("", style=Pack(flex=1)))
        wordle_vbox.add(toga.Label("", style=Pack(flex=1)))
        wordle_vbox.add(wordle_hbox)
        wordle_vbox.add(toga.Label("", style=Pack(flex=1)))
        
        # game mode buttons section
        classic_view = toga.Button('Classic', on_press=self.classic, style=Pack(padding=2, flex=1.5))
        timed_view = toga.Button('Timed', style=Pack(padding=2, flex=1.5))
        
        # game mode boxes section
        classic_box = toga.Box(style=Pack(direction=ROW))
        classic_box.add(toga.Label("", style=Pack(flex=1)))
        classic_box.add(classic_view)
        classic_box.add(toga.Label("", style=Pack(flex=1)))
        
        timed_box = toga.Box(style=Pack(direction=ROW))
        timed_box.add(toga.Label("", style=Pack(flex=1)))
        timed_box.add(timed_view)
        timed_box.add(toga.Label("", style=Pack(flex=1)))
        # CONTINUE MAIN MENU
        
        
        
        
        
        self.startup_box.add(wordle_vbox)
        self.startup_box.add(classic_box)
        self.startup_box.add(timed_box)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.startup_box
        self.main_window.show()
        
    def mainmenu(self, widget):
        # returns to startup menu
        self.main_window.content = self.startup_box

    def classic(self, widget):
    
        # main box
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        # guess section
        guess_label = toga.Label(
            'Guess: ',
            style=Pack(padding=(0, 5))
        )
        self.guess_input = toga.TextInput(style=Pack(flex=1))

        guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
        guess_box.add(guess_label)
        guess_box.add(self.guess_input)

        guess_button = toga.Button(
            'Guess',
            on_press = self.guess,
            style=Pack(padding=5)
        )
        
        # alphabet section
        letter_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.alphabet_array = [toga.Label(i, style=Pack(padding=(0, 0), color='black')) for i in letter_array]
        alphabet_box = toga.Box(style=Pack(direction=ROW, padding=1, alignment=CENTER))
        alphabet_box.add(toga.Label("", style=Pack(flex=1)))
        for letter in self.alphabet_array:
            alphabet_box.add(letter)
        alphabet_box.add(toga.Label("", style=Pack(flex=1)))
        
        # guess boxes section
        guesses_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.guesses_array =  []
        self.buttons_array = []
        for i in range(6):
            word_box = toga.Box(style=Pack(direction=ROW, padding=5))
            word_box.add(toga.Label("", style=Pack(flex=1)))
            word_array = []
            button_row = []
            for i in range(5):
                letter_box = toga.Box(style=Pack(direction=ROW, padding=5, background_color='gray'))
                letter_button = toga.Button('', style=Pack(padding=5, width=50, height=50))
                letter_box.add(letter_button)
                word_array.append(letter_box)
                button_row.append(letter_button)
                word_box.add(letter_box)
            word_box.add(toga.Label("", style=Pack(flex=1)))
            guesses_box.add(word_box)
            self.guesses_array.append(word_array)
            self.buttons_array.append(button_row)
            
        # restart section
        restart_button = toga.Button(
            'Restart',
            on_press = self.reset,
            style=Pack(padding=5)
        )
        
        # back to main menu section
        mainmenu_button = toga.Button('Back to Main Menu', on_press=self.mainmenu, style=Pack(padding=2))
        
        # main window section
        main_box.add(guess_box)
        main_box.add(guess_button)
        main_box.add(alphabet_box)
        main_box.add(guesses_box)
        main_box.add(restart_button)
        main_box.add(mainmenu_button)

        self.main_window.content = main_box
        self.main_window.show()
        
        self.initialize() # initializes word and guess list
        self.current_word, self.guess_count = Game(self.word_list, self.guess_list).startgame() # start a new game
        
    def initialize(self):
        self.word_list = open(str(self.paths.app)+ '/words.txt').read().splitlines()
        self.guess_list = open(str(self.paths.app)+ '/allowed_guesses.txt').read().splitlines()
        
    def guess(self, widget):
        if Guess(self.guess_input.value).checklength() == False:
            self.error_window('The word ' + self.guess_input.value + ' is less than five characters.')
        elif Guess(self.guess_input.value).checkchar() == False:
            self.error_window('The word ' + self.guess_input.value + ' has characters other than letters.')
        else:
            if Guess(self.guess_input.value).checkguess(self.guess_list) == True:
                Interface(self.guess_input.value, self.buttons_array, self.guesses_array).putword(self.guess_count) # place word in boxes if an allowed guess
                Interface(self.guess_input.value, self.buttons_array, self.guesses_array).changecolor(self.guess_count, self.current_word, self.alphabet_array)
                self.guess_count += 1
                
                # if game over or victory conditions, show new window
                game_condition, message_1, message_2 = Game(self.word_list, self.guess_list).checkgame(self.guess_count, self.guess_input.value, self.current_word)
                self.new_window(game_condition, message_1, message_2)
                if game_condition == True:
                    Interface(self.guess_input.value, self.buttons_array, self.guesses_array).resetinterface(self.alphabet_array)
                    self.current_word, self.guess_count = Game(self.word_list, self.guess_list).startgame() # start a new game
                    
            else:
                self.error_window('The word ' + self.guess_input.value + ' is not an allowed guess.')
                
        self.guess_input.value = ''
        
    def reset(self, widget):
        Interface(self.guess_input.value, self.buttons_array, self.guesses_array).resetinterface(self.alphabet_array)
        self.current_word, self.guess_count = Game(self.word_list, self.guess_list).startgame() # start a new game
        self.guess_input.value = ''
        
    def new_window(self, condition, message_1, message_2):
        if condition == True:
            self.main_window.info_dialog(message_1, message_2)
            
    def error_window(self, reason):
        self.main_window.error_dialog('Not Allowed', reason)
        
    def first_view(self, widget):
        first_box = toga.Box()
        self.main_window.content = first_box
        #self.main_window.show()
    
        
class Game(toga.App):

    def __init__(self, word_list, guess_list):
        self._word_list = word_list
        self._guess_list = guess_list

    def startgame(self):
        self._current_word = random.choice(self._word_list) # get new word to guess
        self._guess_count = 0   # clear guess count to 0
        print(self._current_word)
        return self._current_word, self._guess_count
    
    def checkgame(self, guess_count, guess, answer):
        if self.victory(guess, answer) == True:
            return True, 'Victory', 'You have guessed ' + answer + ' as the correct answer.'
        elif self.gameover(guess_count) == True:
            return True, 'Game Over', 'The correct answer is ' + answer + '.'
        return False, '', ''
    
    def gameover(self, guess_count):
        if guess_count == 6:
            return True
        return False
        
    def victory(self, guess, answer):
        if guess.upper() == answer.upper():
            return True
        return False
        
class Interface(toga.App):

    def __init__(self, guess, button_array, box_array):
        self._guess = guess
        self._button_array = button_array
        self._box_array = box_array
        
    def putword(self, guess_count):
        # puts the guess in the boxes
        current_row = self._button_array[guess_count]
        for char in range(5):
            current_row[char].label = self._guess[char].upper()
            
    def changecolor(self, guess_count, answer, alphabet):
        current_row = self._box_array[guess_count]
        green = []
        orange = []
        for char in range(len(self._guess)):
            if self._guess[char] == answer[char]:
                current_row[char].style.background_color = 'green'
                green.append(self._guess[char].upper())
            elif self._guess[char] in answer:
                current_row[char].style.background_color = 'orange'
                orange.append(self._guess[char].upper())
        for letter in alphabet:
            if letter.text in green:
                letter.style.color = 'green'
            elif letter.text in orange and letter.style.color != 'green':
                letter.style.color = 'orange'
                
    def resetinterface(self, alphabet):
        for letter in alphabet:
            letter.style.color = 'black'
        for row in self._button_array:
            for char in range(5):
                row[char].label = ''
        for row in self._box_array:
            for char in range(5):
                row[char].style.background_color = 'gray'
        
        
                
class Guess(toga.App):

    def __init__(self, guess):
        self._guess = guess
        
    def checkguess(self, guess_list):
        # checks if guess is allowed
        if self._guess in guess_list:
            return True
        return False
        
    def checklength(self):
        # checks if guess has 5 letters
        if len(self._guess) == 5:
            return True
        return False
        
    def checkchar(self):
        # checks if all characters in guess are letters
        for char in self._guess:
            if ord(char) < 65:
                return False
            elif ord(char) > 122:
                return False
            elif ord(char) > 90:
                if ord(char) < 97:
                    return False
        return True
        

def main():
    return Wordle()
    
# Notes
# Classic = normal game
# Timed = timer instead of six guesses
