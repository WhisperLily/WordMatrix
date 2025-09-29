import random   #Use the random module to enable the random selection of words and scrambling
import csv      #CSV library to read CSV files


class Game:     #this class manages anything to do with words
    def __init__(self):      #Initialise variables
     #list of predefined words/funcs to be used for the game.
        self.dictionary = {}
        self.load_dictionary()  # Call the function below to fill the dictionary
        self.UsedWords = []    #track words already used in a game to prevent repetition
        self.current_word = ""
        self.scrambled = ""
        self.score = 0
        self.attempts = 3
        self.word_level = 1

    def load_dictionary(self):  # func to read CSV file and put it in the dict variable
        with open('WordMatrix-Dict.csv', 'r') as file:  # Open CSV file for reading
            reader = csv.DictReader(file)  # create a CSV reader that treats each row as a dictionary
            for row in reader:  # go through each row in the CSV file one by one
                print(row.keys())
                word = row['Word'].lower()  # get the word from the 'word' column and make it lowercase
                hint = row['Meaning']  # get the hint from the 'meaning' column
                self.dictionary[word] = hint  # Store the word and meaning in the dictionary


    def get_new_word(self):  #Function to scramble a chosen word
        word = random.choice(list(self.dictionary.keys()))  #choose a random word from the list and assign it to the variable 'word'

        while word in self.UsedWords: #loop to choose a word that hasn't been used
            word = random.choice(list(self.dictionary.keys()))  #get a new word

        self.current_word = word
        self.UsedWords.append(word)  #mark the word as used

        letters = list(word)          #Convert chosen word string into a list of letters
        random.shuffle(letters)       #Shuffle letters of the word in the list
        self.scrambled = ''.join(letters)       #Convert the shuffled letters back into a string 
        
        return self.scrambled


    def hint(self, word): #function to get hints (for frontend when user clicks hint)
        word_hint = self.dictionary[word]
        return word_hint     