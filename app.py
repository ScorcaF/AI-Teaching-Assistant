import os
# from PIL import Image
# import pytesseract

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
global language
language = 'italian'

@app.route("/", methods=("GET", "POST"))
def index():
    global language
    if request.method == "POST":
        language = request.form.get("language", "italian")
    return render_template("index.html")


@app.route('/essay_writing', methods=("GET", "POST"))
def essay_writing():
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
        return redirect(url_for("essay_writing", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("essay_writing.html", result=result)


@app.route('/math', methods=("GET", "POST"))
def math():
    global language
    if request.method == "POST":
        problem = request.form["problem"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Solve the following problem highlighting the mathematical operations"
                   f" and commenting them."
                   f"The problem is the following: : {problem}"
                   f"The answer must be delievered completely in {language}.",
            temperature=0.1,
            max_tokens=2048,
        )
        return redirect(url_for("math", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("math.html", result=result)

@app.route('/latin_translation', methods=("GET", "POST"))
def latin_translation():
    global language
    if request.method == "POST":
        text = request.form["problem"]
        prompt = f"Tranlate the following text from ancient Latin to {language}: \"{text}\""
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.1,
            max_tokens=4096 - 2*len(prompt),
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1
        )
        return redirect(url_for("latin_translation", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("latin_translation.html", result=result)

@app.route('/greek_translation', methods=("GET", "POST"))
def greek_translation():
    global language
    if request.method == "POST":
        text = request.form["problem"]
        prompt = f"Tranlate the following text from ancient Greek to {language}: \"{text}\""
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.1,
            max_tokens=4096 - 2*len(prompt),
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1
        )
        return redirect(url_for("latin_translation", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("latin_translation.html", result=result)
