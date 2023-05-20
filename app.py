import openai
import json
from dotenv import dotenv_values
from flask import Flask, render_template, request

config = dotenv_values(".env")
openai.api_key  = config["OPENAI_API_KEY"]

app = Flask(
    __name__,
    template_folder="templates"
)

@app.route("/")
def index():
    completion = openai.Completion.create(
            model="text-davinci-003",
            prompt="give me some joke",
            max_tokens=100,
            temperature=1,
        )
    return completion.choices[0].text
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)