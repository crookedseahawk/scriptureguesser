let structure = null;
let currentScripture = null;
let correctPath = null;
const TESTAMENT_MAP = {
    "The Old Testament": 1,
    "The New Testament": 2
};

let round = 0;
const totalRounds = 3;
let scores = [];

async function loadGame() {
    // Load full structure
    let sRes = await fetch("/structure");
    structure = await sRes.json();

    startRound();
}

// Start a new round
async function startRound() {
    if (round >= totalRounds) {
        showFinalScore();
        return;
    }

    // Load random scripture
    let rRes = await fetch("/random");
    currentScripture = await rRes.json();

    const testamentNum = TESTAMENT_MAP[currentScripture.testament];
    const booksForTest = Object.keys(structure[currentScripture.testament]);
    const bookNum = booksForTest.indexOf(currentScripture.book) + 1;

    correctPath = [
        testamentNum,
        bookNum,
        currentScripture.chapter,
        currentScripture.verse
    ];

    document.getElementById("scripture-box").innerText = currentScripture.text;
    document.getElementById("score-area").innerHTML = "";

    buildTestamentChoice();
}

// JS scoring function (same as your Python version)
function calcScore(guess, correct) {
    const MAX_POINTS = 5000;
    const D = 200;
    const weights = [400, 100, 20, 1];

    let total = 0;
    for (let i = 0; i < 4; i++) {
        if (guess[i] === correct[i]) continue;
        total += weights[i] * Math.abs(guess[i] - correct[i]);
    }

    return Math.floor(MAX_POINTS * Math.exp(-total / D));
}

// Build Testament buttons
function buildTestamentChoice() {
    let div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Testament:</h3>`;

    Object.keys(structure).forEach(testament => {
        let btn = document.createElement("button");
        btn.innerText = testament;
        const testamentNum = TESTAMENT_MAP[testament];
        btn.onclick = () => buildBookChoice(testament, testamentNum);
        div.appendChild(btn);
    });
}

// Build Book buttons
function buildBookChoice(testament, testamentNum) {
    let div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Book:</h3>`;

    Object.keys(structure[testament]).forEach((book, i) => {
        let btn = document.createElement("button");
        btn.innerText = book;
        btn.onclick = () => buildChapterChoice(testament, testamentNum, book, i + 1);
        div.appendChild(btn);
    });
}

// Build Chapter buttons
function buildChapterChoice(testament, testamentNum, book, bookNum) {
    let div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Chapter:</h3>`;

    const chapters = structure[testament][book];
    Object.keys(chapters)
    .map(ch => parseInt(ch))
    .sort((a, b) => a - b)
    .forEach(chNum => {
        let btn = document.createElement("button");
        btn.innerText = chNum;
        btn.onclick = () => buildVerseChoice(testamentNum, bookNum, chNum);
        div.appendChild(btn);
});
}

// Build Verse buttons
function buildVerseChoice(testamentNum, bookNum, chapterNum) {
    let div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Verse:</h3>`;

    const verses = structure[currentScripture.testament][currentScripture.book][chapterNum];
    Object.keys(verses)
    .map(v => parseInt(v))
    .sort((a, b) => a - b)
    .forEach(verseNum => {
        let btn = document.createElement("button");
        btn.innerText = verseNum;
        btn.onclick = () => finishGuess(testamentNum, bookNum, chapterNum, verseNum);
        div.appendChild(btn);
});
}

// Evaluate the guess
function finishGuess(t, b, c, v) {
    const guess = [t, b, c, v];
    const score = calcScore(guess, correctPath);
    scores.push(score);
    round += 1;

    document.getElementById("score-area").innerHTML = `
        <h3>Round ${round} Score: ${score}</h3>
        <p>Correct Path: ${correctPath.join(" → ")}</p>
        <p>Your Guess: ${guess.join(" → ")}</p>
    `;

    // Move to next round after short delay
    setTimeout(startRound, 1500);
}

// Show final cumulative score
function showFinalScore() {
    const total = scores.reduce((a, b) => a + b, 0);
    let div = document.getElementById("choice-area");
    div.innerHTML = `
        <h2>Game Over!</h2>
        <p>Scores per Round: ${scores.join(", ")}</p>
        <p>Total Score: ${total}</p>
        <button onclick="restartGame()">Play Again</button>
    `;
}

// Restart the game
function restartGame() {
    scores = [];
    round = 0;
    loadGame();
}

// Start the first round
loadGame();