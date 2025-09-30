//load the stats and word
document.addEventListener('DOMContentLoaded', () => {
    LoadGame();
});


//when click sunbmit button
document.getElementById('submit-btn').addEventListener('click', (e) => {
    e.preventDefault();
    submit_guess();
});
//for enter key:
document.getElementById('guess-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submit_guess();
    }
});


//show initial state
function LoadGame(){
    fetch ('/api/start', {
        method: 'POST'
    })
    .then(start_response => start_response.json())
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("scrambled-word").textContent = data.scrambled;
    })
    .catch(error => console.error(error));
}


//submit guess  ONCLICK; Playgame
function submit_guess(){
    //sending the guess
    const guess = document.getElementById('guess-input').value

    fetch ('/api/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({guess: guess})
    })
    .then(play_response => play_response.json())
    .then(data =>{

        //GUESS IS CORRECT
        if (data.correct === True){
            if (data.game_over === 'False') {      //if they guessed correctly, still wordlevel remaining
                document.getElementById('feedback').classList.add('correct');
                document.getElementById("feedback").textContent = "Your guess is correct!!";
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                setTimeout(() => {
                    document.getElementById("scrambled-word").textContent = data.scrambled
                }, 300);
            }
            else if (data.game_over === 'True'){     //guessed correctly but game over
                document.getElementById("score").textContent = data.score;
                document.getElementById('feedback').classList.add('correct');
                document.getElementById("feedback").textContent = "Your guess is correct!!";
                setTimeout(() => {
                    document.getElementById('feedback').classList.remove('correct');
                    document.getElementById("feedback").textContent = "Game Over!"
                }, 300);
                document.getElementById("final-score").textContent = data.score;
                setTimeout(() => {
                    document.getElementById("game-board").style.display = 'none';   //hide game board
                    document.getElementById("game-over").style.display='block'      //show game over box
                }, 500);    //show the game over div!!
            }
        }
        else if (data.correct === False){  //GUESS IS INCORRECT
            if (data.game_over === 'attempts left') {     //attempts and word level remaining
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                document.getElementById('feedback').classList.add('wrong');
                document.getElementById("feedback").textContent = "Wrong! Try again";
            }
            else if (data.game_over === 'False') {     //no attempts left but word level left
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                document.getElementById('feedback').classList.add('wrong');
                document.getElementById("feedback").textContent = "The word was:" + data.actual;
                setTimeout(() =>{
                    document.getElementById("scrambled-word").textContent = data.scrambled
                }, 500);
            }
            else if (data.game_over === 'True') {     //no attempt and word level left 
                document.getElementById("score").textContent = data.score;
                document.getElementById("feedback").textContent = "Game Over! The word was:" + data.actual;
                document.getElementById("final-score").textContent = data.score;
                setTimeout(() => {
                    document.getElementById('feedback').classList.remove('wrong');
                    document.getElementById("game-over").style.display='block'
                }, 500);     //show the game over div!!
            }
        }
    })
    .catch(error => console.error(error));
}

//new game
function new_Game(){
    fetch ('/api/restart', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("scrambled-word").textContent = data.scrambled;
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//skip word
function Skip_Word(){
    fetch ('/api/skip', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("scrambled-word").textContent = data.scrambled;
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//get hint
function get_hint(){
    fetch ('/api/hint', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementsByClassName("word-hint").textContent = data.hint
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//play again
function replay(){
    fetch ('/api/replay', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("scrambled-word").textContent = data.scrambled;
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}

