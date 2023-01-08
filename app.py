import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
global language


@app.route("/", methods=("GET", "POST"))
def index():
    global language
    if request.method == "POST":
        language = request.form.get("language", "english")
    return render_template("index.html")


@app.route('/history', methods=("GET", "POST"))
def history():
    global language
    if request.method == "POST":
        theme = request.form["theme"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Write an essay on the following topic: {theme.capitalize()}. " 
                   f"The essay needs to be written acting as an expert." 
                   f"The theme must be delivered completely in {language}." 
                   f"Write an assay as long as possible." 
                   f"Do not insert personal comment or referrals to any sentiment." 
                   f"Do not use phrases twice.",
            temperature=0.1,
            max_tokens=3400,
        )
        return redirect(url_for("history", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("history.html", result=result)


@app.route('/math', methods=("GET", "POST"))
def math():
    global language
    if request.method == "POST":
        problem = request.form["problem"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"The problem solution needs to be written highlighting the mathematical operations"
                   f" and commenting them."
                   f"The problem is the following: : {problem}"
                   f"The answer must be delievered completely in {language}.",
            temperature=0.1,
            max_tokens=2048,
        )
        return redirect(url_for("math", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("math.html", result=result)

