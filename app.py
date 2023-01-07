import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        theme = request.form["theme"]
        language = request.form["language"]
        length = request.form["length"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(theme, language),
            temperature=0.1,
            max_tokens=int(length),
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(theme, language):
    return f"Write an essay on the following topic: {theme.capitalize()}. " \
           f"The essay needs to be written acting as an expert." \
           f"The theme must be delivered completely in {language}." \
           f"Write an assay as long as possible." \
           f"Do not insert personal comment or referrals to any sentiment." \
           f"Do not use phrases twice."

