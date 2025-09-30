import WordMatrix as wm
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI()
app.mount("/static", StaticFiles(directory='.'), name="static")

game=wm.Game()

class GuessRequest(BaseModel):
    guess: str


@app.get("/")   #get the homepage
def get_HomePage():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/api/start")
def start_game():
    game.score = 0
    game.word_level = 1
    game.attempts = 3
    scrambled = game.get_new_word()
    
    return {
        "scrambled": scrambled,      #display the scrambled word to frontend to be unscrambled
        "score": game.score,
        "word_level": game.word_level,
        "attempts": game.attempts
    }


@app.post("/api/submit") #you click submit to play the game
def check_guess(data: GuessRequest):    #check if gusess is correct
    guess = data.guess.lower().strip()  #player's inout guess, make it lowercase and strip spaces

    if guess == game.current_word:  #if the guess is correct
        game.score += 1     #increment the score
        game.word_level += 1        #go to ned word level; 3 in a single game
        game.attempts = 3       #reset the attempts cuz 3 guess for a word
        
        if game.word_level > 3:     # check if we've finished the 3rd word level if so game is over, have to replay
            return {"correct": True, "game_over": 'True', "score": game.score}    #if so game over
        
        scrambled = game.get_new_word() #if not, get new word for next level
        return {    #return display values
            "correct": True,
            "game_over": 'False',
            "scrambled": scrambled,
            "score": game.score,
            "word_level": game.word_level,
            "attempts": game.attempts
        }
    else:       #if player guessed wrong;
        game.attempts -= 1  #reduce their current attempt
        
        if game.attempts == 0:  #if they are wrong and have used up all their attempts
            old_word = game.current_word
            game.word_level += 1      #move to next word level, no more tries
            game.attempts = 3       #reset attempt for new word
            
            if game.word_level > 3:     #check if no more word level, then game is over but they still guessed wrong
                return {"correct": False, 
                        "actual":game.current_word,
                        "game_over": 'True', 
                        "score": game.score
                    }
            
            scrambled = game.get_new_word()     #if theres another level, get the new word to guess
            return {
                "correct": False,       #attempts is finished and their guess is wrong
                "game_over": 'False',
                "actual":old_word,
                "scrambled": scrambled,
                "score": game.score,
                "word_level": game.word_level,
                "attempts": game.attempts
            }
        
        #if they have attempts left;
        return {
            "correct": False,
            "game_over": "attempts left",
            "score": game.score,
            "word_level": game.word_level,
            "attempts": game.attempts
        }


@app.get("/api/skip")
def skip_word():    #skip word but keep current game level, score, attempt
    scrambled = game.get_new_word()     #the new word
    return {
        "scrambled": scrambled,      #display the scrambled word to frontend to be unscrambled
        "score": game.score,
        "word_level": game.word_level,
        "attempts": game.attempts
    }


@app.get("/api/restart")
def new_game():
    return start_game()

        
@app.get("/api/hint")
def get_hint():
    thehint = game.hint(game.current)
    return{"hint":thehint}
    
             
@app.get("/api/replay")
def replay_game():
    game.UsedWords = []  #clear used words
    return start_game()  #already resets score, attempts, word_level

