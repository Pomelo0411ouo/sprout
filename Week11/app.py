from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/school")
def school():
    return redirect("https://www.wlsh.tyc.edu.tw/")