let structure = null;
let currentScripture = null;
const TESTAMENT_MAP = { "The Old Testament": 1, "The New Testament": 2 };

let round = 0;
const totalRounds = 3;
let scores = [];

// Canonical book order
const BOOK_ORDER = {
    "The Old Testament": [
        "Genesis","Exodus","Leviticus","Numbers","Deuteronomy",
        "Joshua","Judges","Ruth","1 Samuel","2 Samuel",
        "1 Kings","2 Kings","1 Chronicles","2 Chronicles",
        "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs",
        "Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations",
        "Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah",
        "Jonah","Micah","Nahum","Habakkuk","Zephaniah",
        "Haggai","Zechariah","Malachi"
    ],
    "The New Testament": [
        "Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians",
        "2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
        "1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus",
        "Philemon","Hebrews","James","1 Peter","2 Peter","1 John",
        "2 John","3 John","Jude","Revelation"
    ]
};

// Scoring function (matches your Python code)
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

// Load scriptures.json and start game
async function loadGame() {
    const sRes = await fetch("scriptures.json");
    structure = await sRes.json();
    startRound();
}

// Start a round
async function startRound() {
    if (round >= totalRounds) {
        showFinalScore();
        return;
    }

    const rRes = await fetch("scriptures.json");
    const allScriptures = await rRes.json();
    const flatList = [];

    for (const testament in allScriptures) {
        for (const book in allScriptures[testament]) {
            for (const chapter in allScriptures[testament][book]) {
                for (const verse in allScriptures[testament][book][chapter]) {
                    flatList.push({
                        testament, book,
                        chapter: parseInt(chapter),
                        verse: parseInt(verse),
                        text: allScriptures[testament][book][chapter][verse]
                    });
                }
            }
        }
    }

    currentScripture = flatList[Math.floor(Math.random() * flatList.length)];

    const testamentNum = TESTAMENT_MAP[currentScripture.testament];
    const booksForTest = BOOK_ORDER[currentScripture.testament];
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

// Build Testament buttons
function buildTestamentChoice() {
    const div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Testament:</h3>`;

    Object.keys(structure).forEach(testament => {
        const btn = document.createElement("button");
        btn.innerText = testament;
        const testamentNum = TESTAMENT_MAP[testament];
        btn.onclick = () => buildBookChoice(testament, testamentNum);
        div.appendChild(btn);
    });
}

// Build Book buttons
function buildBookChoice(testament, testamentNum) {
    const div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Book:</h3>`;

    const booksForTest = BOOK_ORDER[testament];
    booksForTest.forEach((book, i) => {
        const btn = document.createElement("button");
        btn.innerText = book;
        btn.onclick = () => buildChapterChoice(testament, testamentNum, book, i + 1);
        div.appendChild(btn);
    });
}

// Build Chapter buttons
function buildChapterChoice(testament, testamentNum, book, bookNum) {
    const div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Chapter:</h3>`;

    const chapters = structure[testament][book];
    Object.keys(chapters)
        .map(ch => parseInt(ch))
        .sort((a,b)=>a-b)
        .forEach(chNum => {
            const btn = document.createElement("button");
            btn.innerText = chNum;
            btn.onclick = () => buildVerseChoice(testamentNum, bookNum, chNum);
            div.appendChild(btn);
        });
}

// Build Verse buttons
function buildVerseChoice(testamentNum, bookNum, chapterNum) {
    const div = document.getElementById("choice-area");
    div.innerHTML = `<h3>Choose Verse:</h3>`;

    const verses = structure[currentScripture.testament][currentScripture.book][chapterNum];
    Object.keys(verses)
        .map(v => parseInt(v))
        .sort((a,b)=>a-b)
        .forEach(verseNum => {
            const btn = document.createElement("button");
            btn.innerText = verseNum;
            btn.onclick = () => finishGuess(testamentNum, bookNum, chapterNum, verseNum);
            div.appendChild(btn);
        });
}

// Evaluate guess
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
    setTimeout(startRound, 1500);
}

// Show final score
function showFinalScore() {
    const total = scores.reduce((a,b)=>a+b,0);
    const div = document.getElementById("choice-area");
    div.innerHTML = `
        <h2>Game Over!</h2>
        <p>Scores per Round: ${scores.join(", ")}</p>
        <p>Total Score: ${total}</p>
        <button onclick="restartGame()">Play Again</button>
    `;
}

// Restart game
function restartGame() {
    scores = [];
    round = 0;
    loadGame();
}

// Start the first round
loadGame();