import json, os, random, math
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Load JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "scriptures.json")

with open(JSON_PATH, "r") as f:
    scriptures = json.load(f)

# Flatten scripture path list
SCRIPTURES_LIST = []
for testament, books in scriptures.items():
    for book, chapters in books.items():
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                SCRIPTURES_LIST.append({
                    "testament": testament,
                    "book": book,
                    "chapter": int(chapter),
                    "verse": int(verse),
                    "text": text
                })

@app.route("/random")
def get_random():
    return jsonify(random.choice(SCRIPTURES_LIST))

@app.route("/structure")
def get_structure():
    """Returns the nested structure (for book/chapter/verse menus)."""
    return jsonify(scriptures)

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug=True)
