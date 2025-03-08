import random   #Use the random module to enable the random selection of words and scrambling

class display: #this class handles the instructions displayed to the player.
    def __init__(self):
        self.instruction = """ 
         Welcome to the Word Shuffle!
         You're given a scrambled word, and you must unscramble it to guess the correct word.
         You get 3 words per game, and for each word, 3 attempts to guess correctly.
         Let's start!
            """
    def show_display(self):
         print(self.instruction)

class WordManager:  #this class manages anything to do with words
    def __init__(self):      #Initialise variables
     #list of predefined words to be used for the game.
        self.dictionary = ['example','mischievous','conscientious','xylophone','ambiguous','consistency','hypnotic','labyrinth','scrabble','curtain',
                           'phenomenon','financial', 'precipitate', 'homogeneous','artificial','intelligence','machine','learning','engineering', 'neighbour'
                           'verbatim','monopoly','nauseous','javascript','scholarship','psychiatrist','ancient','authorise','semantic','beseech',
                           'besmirched','entrepreneurial','outreach','relationship','penultimate','verbose','internship','experience']
        self.UsedWords = []*3    #track words already used in a game to prevent repetition
    
    def ScrambleWord(self, word):  #Function to scramble a chosen word
        word = list(word)          #Convert chosen word string into a list of letters
        random.shuffle(word)       #Shuffle letters of the word in the list
        return ''.join(word)       #Convert the shuffled letters back into a string 


class GamePlay(WordManager):    #This class encapsulates the attributes and methods/functions for the game logic
    def __init__(self):         #Initialise variables
        super().__init__()      #Inherit from the parent class
        self.display = display()
        self.points = 0         #The players' score starts at 0
        self.attempt = 3        #The player only has 3 attempts to guess the word correctly/unscramble the word
        
    def play_game(self):
        self.display.show_display()  #display the instruction
        for x in range(3): #a loop to play turn 3 times; 3 words in a game
            word = random.choice(self.dictionary)  #choose a random word from the list and assign it to the variable 'word'
            
            while word in self.UsedWords: #loop to choose a word that hasn't been used
                word = random.choice(self.dictionary)
                
            scrambled = self.ScrambleWord(word)  #put scrambled word into a variable 'scrambled'
            print('Scrambled Word:', scrambled)
            self.UsedWords.append(word)  #mark the word as used
          
            
            def PlayerAttempts(self, word):  #Function to handle player's attempts to guess each word
                for attempt in range(self.attempt):
                        player_guess = input('  Your Guess:')
                        player_guess = player_guess.lower().strip()  #convert input into lower case and remove backspace at beginning and end
                        if player_guess == word:  #check that player input is the same as chosen word.
                            print('Correct!')
                            self.points += 1   #Increment score by 1 for correct guesses
                            break    #exit the attempt loop if guess is correct
                        else:
                            if attempt < self.attempt - 1:   #check if there are attempts left
                                print(f" Wrong! guess again, {self.attempt - attempt - 1} attempts left.")  #show how many attempts left
    
                else:
                    print(f"The word is: {word}")  #display the word if no attempts remaining
            PlayerAttempts(self, word)  #Call player_attempts function to handle guessing logic
            
        print(f"Game Over! Your Score:{self.points}")

        def replays(self):  #Function to prompt for replay
            replay = input('Do you want to play again? (Y|N)')
            replay = replay.upper().strip()
            if replay == 'Y':  #if the user wants to play again
                self.points = 0         #Reset score for a new game
                self.UsedWords = []*3   #Reset used words for a new game
                self.play_game()        #Start the new game
                
            elif replay == 'N':   #Exit message if user doesn't want to play again 
                print('Thanks for playing, Bye!')
                
            else: #Check inputs not Y or N
                while replay != 'Y' and replay != 'N': #for input not y or n, print error message until player inputs y or n
                     #Convert input to uppercase and remove backspace before and after the inputted word
                    replay = input('Invalid input. Please enter Y or N ').upper().strip() 
                if replay == 'Y':    #if the user wants to play again
                    self.points = 0        #Reset score for a new game
                    self.UsedWords = []*3  #Reset used words for a new game
                    self.play_game()       #Start the new game
                elif replay == 'N':     #Exit message if user doesn't want to play again 
                    print('Thanks for playing, Bye!')    
                     
        replays(self)

# Start the game
game = GamePlay()
game.play_game()
        
        

