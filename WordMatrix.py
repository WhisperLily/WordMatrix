import random   #Use the random module to enable the random selection of words and scrambling
import csv      #CSV library to read CSV files

class WordManager:  #this class manages anything to do with words
    def __init__(self):      #Initialise variables
     #list of predefined words/funcs to be used for the game.
        self.dictionary = {}
        self.load_dictionary()  # Call the function below to fill the dictionary
        self.UsedWords = []    #track words already used in a game to prevent repetition

    def load_dictionary(self):  # func to read CSV file and put it in the dict variable
        with open('WordMatrix-Dict.csv', 'r') as file:  # Open CSV file for reading
            reader = csv.DictReader(file)  # create a CSV reader that treats each row as a dictionary
            for row in reader:  # go through each row in the CSV file one by one
                print(row.keys())
                word = row['Word'].lower()  # get the word from the 'word' column and make it lowercase
                hint = row['Meaning']  # get the hint from the 'meaning' column
                self.dictionary[word] = hint  # Store the word and meaning in the dictionary
    
    def ScrambleWord(self, original_word):  #Function to scramble a chosen word
        word_letters = list(original_word)          #Convert chosen word string into a list of letters
        random.shuffle(word_letters)       #Shuffle letters of the word in the list
        return ''.join(word_letters)       #Convert the shuffled letters back into a string 


class GamePlay(WordManager):    #This class encapsulates the attributes and methods/functions for the game logic
    def __init__(self):         #Initialise variables
        super().__init__()      #Inherit from the parent class
        self.points = 0         #The players' score starts at 0
        self.attempt = 3        #The player only has 3 attempts to guess the word correctly/unscramble the word

    def PlayerAttempts(self, original_word):  #Function to handle player's attempts to guess each word
                for attempt in range(self.attempt):
                    player_guess = input('  Your Guess:')
                    player_guess = player_guess.lower().strip()  #convert input into lower case and remove backspace at beginning and end
                    if player_guess == original_word:  #check that player input is the same as chosen word.
                        print('Correct!')
                        self.points += 1   #Increment score by 1 for correct guesses
                        return True  # Word guessed correctly
                    else:
                        if attempt < self.attempt - 1:   #check if there are attempts left
                            print(f" Wrong! guess again, {self.attempt - attempt - 1} attempts left.")  #show how many attempts left
    
                print(f"The word is: {original_word}")  #display the word if no attempts remaining
                return False  # Word not guessed
       
    def play_game(self):
        for x in range(3): #a loop to play turn 3 times; 3 words in a game
            original_word = random.choice(list(self.dictionary.keys()))  #choose a random word from the list and assign it to the variable 'word'
            
            while original_word in self.UsedWords: #loop to choose a word that hasn't been used
                original_word = random.choice(list(self.dictionary.keys()))
                
            scrambled = self.ScrambleWord(original_word)  #put scrambled word into a variable 'scrambled'
            print(f'Scrambled Word:  {scrambled}')
            self.UsedWords.append(original_word)  #mark the word as used
          
            

            self.PlayerAttempts(original_word)  #Call player_attempts function to handle guessing logic
            
        print(f"Game Over! Your Score:{self.points}")
        self.replays()
        self.get_hint(original_word) 

    def replays(self):  #Function to prompt for replay
        replay = input('Do you want to play again? (Y|N)').upper().strip()

        while replay not in ['Y', 'N']:
            replay = input('Invalid input. Please enter Y or N: ').upper().strip()
            
        if replay == 'Y':
            self.points = 0
            self.UsedWords = []  # Fix: was []*3 which is wrong
            self.play_game()
        else:
            print('Thanks for playing, Bye!')

    def get_hint(self, word): #function to get hints (for frontend when user clicks hint)
        word_hint = self.dictionary[word]
        print(f'Hint: {word_hint}')

# Start the game
game = GamePlay()
game.play_game()
        
        

