import WordMatrix
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory='.'), name="static")

@app.get("/")
def get_HomePage():
    with open("/static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("update_word")   #getting game status label; how many words left to play
@app.get("update_score")   #getting status label; how many games won 
@app.get("update_attempts")    #getting status label; how many attempts left 
@app.get("scrambled_word")      #getting the scrambled letters
@app.get("hint")       #click hint button to show word meaning
@app.get("check_submit")
@app.get("feedback")
@app.get("restart_game")
@app.get("getNewWord")
@app.get("replay")