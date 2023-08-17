let number1 = document.getElementById('number1');
let number2 = document.getElementById('number2');
let answer = document.getElementById('answer');
let submitButton = document.getElementById('submit');
let message = document.getElementById('message');
let playAgainButton = document.getElementById('playAgain');
let maxNumber = 2;
let timeLeft = 10; // start with 10 seconds
let timeDisplay = document.createElement('div');
let score = 0;
let highScore = localStorage.getItem('highScore') ? parseInt(localStorage.getItem('highScore')) : 0;
let highScoreDisplay = document.createElement('div');
let timerStarted = false;
let timerInterval;

timeDisplay.classList.add('timeDisplay');
highScoreDisplay.classList.add('highScoreDisplay');

document.querySelector('.container').prepend(timeDisplay);
document.querySelector('.container').prepend(highScoreDisplay);

function updateTimeDisplay() {
    timeDisplay.textContent = `Time left: ${timeLeft} seconds`;
}

function updateHighScoreDisplay() {
    highScoreDisplay.textContent = `High Score: ${highScore}`;
}

function generateNumbers() {
    let n1 = Math.floor(Math.random() * maxNumber) + 1;
    let n2 = Math.floor(Math.random() * maxNumber) + 1;

    number1.textContent = n1;
    number2.textContent = n2;
}

function endGame() {
    message.textContent = "Time's up! Game over!";
    message.style.color = 'red';
    clearInterval(timerInterval);
    answer.disabled = true;
    submitButton.style.display = 'none';

    if (score > highScore) {
        highScore = score;
         localStorage.setItem('highScore', highScore.toString());
        updateHighScoreDisplay();
    }

    playAgainButton.style.display = 'inline-block';
}

function playRandomWrongSound() {
    // Generate a random number between 1 and 3
    let randomNum = Math.floor(Math.random() * 3) + 1;
    console.log(randomNum)

    // Play the corresponding audio
    document.getElementById(`wrongSound${randomNum}`).play();
    console.log( document.getElementById(`wrongSound${randomNum}`))
    console.log('sdifjo')
}

function resetGame() {
    maxNumber = 2;
    score = 0;
    timeLeft = 10;
    timerStarted = false;
    answer.disabled = false;
    submitButton.disabled = false;
    submitButton.style.display = 'inline-block';
    playAgainButton.style.display = 'none';
    answer.value = ''
    message.textContent = '';
    updateTimeDisplay();
    generateNumbers();
}

playAgainButton.addEventListener('click', resetGame);

function startTimer() {
    timerInterval = setInterval(() => {
        timeLeft--;
        updateTimeDisplay();
    
        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
    timerStarted = true;
}

answer.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        checkAnswer();
    }
});

submitButton.addEventListener('click', checkAnswer);

function checkAnswer() {

    if (!timerStarted) {
        startTimer();
    }

    let userAnswer = parseInt(answer.value);
    let correctAnswer = parseInt(number1.textContent) * parseInt(number2.textContent);

    if (userAnswer === correctAnswer) {
        maxNumber++;
        score++;    
        timeLeft += 3;  // Add 5 seconds for a correct answer
        generateNumbers();
        message.textContent = 'Correct! Keep going!';
        message.style.color = 'green';
        answer.value = '';
    } else {
        playRandomWrongSound()
        timeLeft--;
        generateNumbers();
        message.textContent = `Tanga! That's the wrong answer! The correct answer was ${correctAnswer }`;
        message.style.color = 'red';
        answer.value = '';
    }
}

updateTimeDisplay();
updateHighScoreDisplay();
generateNumbers();
