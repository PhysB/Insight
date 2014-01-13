from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/<pagename>")
def regularpage(pagename=None):
    """
    Route not found by the other routes above.
    """
    return "You've arrived at " + pagename

if __name__ == "__main__":
    app.run()