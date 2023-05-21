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

def get_and_render_prompt(text):
    message=f"""
    You're a color palette generating assistant that responds to <Text> prompt for color palettes.
    You must generate color palettes that fit the theme, mood, tone, or instructions in the <Text> prompt.
    You must not generate the same color twice in palettes.

    The palettes should be between 2 to 8 colors.

    Desired Format: a JSON array of hexadecimal color codes

    Text: {text}
    Result:
    """

    completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=100,
            temperature=1,
        )

    colors = json.loads(completion.choices[0].text)
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    # GET QUERY FROM THE FORM
    query = app.logger.info(request.form.get("query"))

    # OPEN AI COMPLETION CALL
    colors = get_and_render_prompt(query)

    # PRINT RETURN COLORS
    app.logger.info(colors)

    # RETURN LIST OF COLORS
    return {"colors": colors}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)