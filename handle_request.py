from flask import Flask, redirect, url_for, render_template
# redirect - redirects user from pages they aren't supposed to be in
from main import diversity, equity, inclusion


app = Flask(__name__)

# give route to show Flask the path to get to the function
@app.route("/")  # the / is default url
def home():
    return render_template('diversity.html')

@app.route("/diversity")
def run_diversity():
    diversity("sample_dataset.csv")

@app.route("/equity")
def run_equity():
    equity("sample_dataset.csv")

@app.route("/inclusion")
def run_inclusion():
    inclusion("sample_dataset.csv")

# @app.route("/<name>")  # can input parameter directly in the URL
# def user(name):
#     return ("Hello " + name + "!")

@app.route("/admin")
def admin():
    return redirect(url_for("home")) # redirect to the function named "home"


if __name__ == "__main__":
    app.run()
