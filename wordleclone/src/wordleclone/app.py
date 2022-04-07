
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import random

class WordleClone(toga.App):

    def startup(self):
    
        # initializes list of words and possible guesses
        self.word_list = open(str(self.paths.app)+ '/words.txt').read().splitlines()
        self.guess_list = open(str(self.paths.app)+ '/allowed_guesses.txt').read().splitlines()
        
        # new game at startup, gets a new word, sets guess count to 0
        self.current_word, self.guess_count = self.new_game()
    
        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.guess_label = toga.Label(
            'Guess: ',
            style=Pack(padding=(0, 5))
        )
        self.guess_input = toga.TextInput(style=Pack(flex=1))

        guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
        guess_box.add(self.guess_label)
        guess_box.add(self.guess_input)
        
        guess_button = toga.Button(
            'Guess',
            on_press=self.new_guess,
            style=Pack(padding=5)
        )
        
        restart_button = toga.Button(
            'Restart',
            on_press=self.reset,
            style=Pack(padding=5)
        )
        
        self.alphabet = toga.Label('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', style=Pack(text_align='center'))
        
        guesses_box = toga.Box(style=Pack(direction=COLUMN, padding=1, alignment='center'))
        guesses_box.add(self.alphabet)
        
        self.word_button_array = []
        self.word_box_array = []
        for j in range(6):
            word_box = toga.Box(style=Pack(direction=ROW, padding=1))
            letter_button_array = []
            letter_box_array = []
            for i in range(5):
                letter_box = toga.Box(style=Pack(direction=ROW, padding=1, background_color='gray'))
                letter_button = toga.Button('', style=Pack(padding=2.5, flex=1, height=55, width=55))
                letter_box.add(letter_button)
                word_box.add(letter_box)
                letter_button_array.append(letter_button)
                letter_box_array.append(letter_box)
            guesses_box.add(word_box)
            self.word_button_array.append(letter_button_array)
            self.word_box_array.append(letter_box_array)
        
        main_box.add(guess_box)
        main_box.add(guess_button)
        main_box.add(guesses_box)
        main_box.add(restart_button)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
    def get_new_word(self):
        return random.choice(self.word_list)
        
    def new_game(self):
        current_word = self.get_new_word()
        return current_word, 0
        
    def new_guess(self, widget):
    
        if self.guess_input.value in self.guess_list:
            for i in range(5):
                self.word_button_array[self.guess_count][i].label = self.guess_input.value[i].upper()
                if self.guess_input.value[i].lower() == self.current_word[i].lower():
                    self.word_box_array[self.guess_count][i].style.background_color = 'green'
                elif self.guess_input.value[i].lower() in self.current_word.lower():
                    self.word_box_array[self.guess_count][i].style.background_color = 'orange'
            self.guess_count += 1
            
            if self.current_word.lower() == self.guess_input.value.lower():
                self.main_window.info_dialog(
                    'Congratulations!',
                    'You guessed the correct word'
                )
                return
            
        else:
            if len(self.guess_input.value) != 5:
                error_msg = ' does not have five characters'
            else:
                for char in self.guess_input.value:
                    if 97 > ord(char) > 90 or 65 > ord(char) or ord(char) > 122:
                        error_msg = ' has character/s other than letters'
                        break
                else:
                    error_msg = ' is not in the list of allowed guesses'
            self.main_window.error_dialog(
                'Error',
                '{}{}'.format(self.guess_input.value, error_msg)
            )
        self.guess_input.value = ''
        
        if self.guess_count == 6:
            self.main_window.info_dialog(
                'Game Over',
                'The correct word is {}'.format(self.current_word)
            )
    
    def clear_guesses(self):
        for i in range(6):
            for j in range(5):
                self.word_box_array[i][j].style.background_color = 'gray'
                self.word_button_array[i][j].label = ''
                
    def reset(self, widget):
        self.clear_guesses()
        self.current_word, self.guess_count = self.new_game()
        
def main():
    return WordleClone()
