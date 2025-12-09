from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World</h1>"

@app.route("/test")
def testament():
    return "<h1>Testament</h1>"

@app.route("/book")
def book():
    return "<h1>Book</h1>"

@app.route("/chapter")
def chapter():
    return "<h1>Chapter</h1>"

@app.route("/verse")
def verse():
    return "<h1>Verse</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")