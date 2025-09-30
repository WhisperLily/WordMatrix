//load the stats and word
document.addEventListener('DOMContentLoaded', () => {
    LoadGame();            
});


function fitWordToBox() {   //stop long words from going outside gameboard
    const box = document.getElementById('scrambled-word');
    let fontSize = 64; // start at 4rem (16px * 4)
    box.style.fontSize = fontSize + 'px';

    while (box.scrollWidth > box.clientWidth && fontSize > 12) { // minimum font size 12px
        fontSize -= 1;
        box.style.fontSize = fontSize + 'px';
    }
}


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
        fitWordToBox();
    })
    .catch(error => console.error(error));
}


//submit guess  ONCLICK; Playgame
function submit_guess(){
    //sending the guess
    const guess = document.getElementById('guess-input').value

    if (!guess) { //do not submit if input is empty
        const feedback = document.getElementById('feedback');
        feedback.textContent = "Please enter a guess!";
        feedback.classList.add('wrong');
        return; // stop submission
    }

    fetch ('/api/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({guess: guess})
    })
    .then(play_response => play_response.json())
    .then(data =>{

        //GUESS IS CORRECT
        if (data.correct === true){
            if (data.game_over === 'False') {      //if they guessed correctly, still wordlevel remaining
                document.getElementById('feedback').classList.remove('correct', 'wrong');
                document.getElementById('feedback').classList.add('correct');
                document.getElementById("feedback").textContent = "Your guess is correct!!";
                setTimeout(() => {
                    document.getElementById('feedback').style.display = 'none';
                },2000);
                document.getElementById('feedback').style.display = 'block';
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                document.getElementById("word-hint").style.display='none';
                setTimeout(() => {
                    document.getElementById("scrambled-word").textContent = data.scrambled
                    fitWordToBox();
                }, 2000);
            }
            else if (data.game_over === 'True'){     //guessed correctly but game over
                document.getElementById("score").textContent = data.score;
                document.getElementById('feedback').classList.remove('correct', 'wrong');
                document.getElementById('feedback').classList.add('correct');
                document.getElementById("feedback").textContent = "Your guess is correct!!";
                document.getElementById('feedback').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('feedback').classList.remove('correct', 'wrong');
                    document.getElementById("feedback").textContent = "Game Over!"
                }, 2000);
                document.getElementById("final-score").textContent = data.score;
                setTimeout(() => {
                    document.getElementById("game-board").style.display = 'none';   //hide game board
                    document.getElementById("game-over").style.display='block';      //show game over box
                }, 2000);    //show the game over div!!
            }
            document.getElementById('guess-input').value = '';
        }
        else if (data.correct === false){  //GUESS IS INCORRECT
            if (data.game_over === 'attempts left') {     //attempts and word level remaining
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                document.getElementById('feedback').classList.remove('correct', 'wrong');
                document.getElementById('feedback').classList.add('wrong');
                document.getElementById("feedback").textContent = "Wrong! Try again";
                setTimeout(() => {
                    document.getElementById('feedback').style.display = 'none';
                },5000);
                document.getElementById('feedback').style.display = 'block';
            }
            else if (data.game_over === 'False') {     //no attempts left but word level left
                document.getElementById("current-word").textContent = data.word_level;
                document.getElementById("score").textContent = data.score;
                document.getElementById("attempts").textContent = data.attempts;
                document.getElementById('feedback').classList.remove('correct', 'wrong');
                document.getElementById('feedback').classList.add('wrong');
                document.getElementById("feedback").textContent = "The word was:" + data.actual.toUpperCase();
                setTimeout(() => {
                    document.getElementById('feedback').style.display = 'none';
                },5000);
                document.getElementById('feedback').style.display = 'block';
                document.getElementById("word-hint").style.display='none';
                setTimeout(() =>{
                    document.getElementById("scrambled-word").textContent = data.scrambled
                    fitWordToBox();
                }, 2000);
            }
            else if (data.game_over === 'True') {     //no attempt and word level left 
                document.getElementById("score").textContent = data.score;
                document.getElementById("feedback").textContent = "Game Over! The word was: " +  data.actual.toUpperCase();
                document.getElementById("final-score").textContent = data.score;
                setTimeout(() => {
                    document.getElementById('feedback').style.display = 'none';
                },5000);
                document.getElementById('feedback').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('feedback').classList.remove('correct', 'wrong');
                    document.getElementById("game-board").style.display = 'none';
                    document.getElementById("game-over").style.display='block'
                }, 2000);     //show the game over div!!
            }
            // Clear input after processing the guess
            document.getElementById('guess-input').value = '';
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
        document.getElementById("word-hint").style.display='none';
        document.getElementById("scrambled-word").textContent = data.scrambled;
        fitWordToBox();
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//skip word
let skipsLeft = 3;  // max skips allowed

function Skip_Word(){
    if (skipsLeft <= 0) { //if no skips left
        const feedback = document.getElementById('feedback');
        feedback.textContent = "You have no skips left!";
        feedback.classList.add('wrong');
        return; // stop skipping
    }

    fetch ('/api/skip', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("word-hint").style.display='none';
        document.getElementById("scrambled-word").textContent = data.scrambled;
        fitWordToBox();
        skipsLeft--;  // decrease remaining skips
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//get hint
function get_hint(){
    fetch ('/api/hint', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("word-hint").style.display='block';
        document.getElementById("word-hint").textContent = data.hint;
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}


//play again
function replay(){
    document.getElementById("game-over").style.display='none';
    document.getElementById("game-board").style.display = 'block';
    fetch ('/api/replay', {method: 'GET' })    //sends request
    .then(response => response.json())   // converts the HTTP response to usable JSON
    .then(data => {
        document.getElementById("current-word").textContent = data.word_level;
        document.getElementById("score").textContent = data.score;
        document.getElementById("attempts").textContent = data.attempts;
        document.getElementById("word-hint").style.display='none';
        document.getElementById("scrambled-word").textContent = data.scrambled;
        fitWordToBox();
    })      //get the actual game data and can update the frontend
    .catch(error => console.error(error));      //handle errors
}

