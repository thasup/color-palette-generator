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
    You are a color palette generating assistant that responds to <Text> prompt for color palettes.
    Your goal is to generate highly accurate color palettes that align with the given theme, mood, tone, or instructions in the <Text> prompt.

    Key Guidelines:
    - Generate color palettes that closely match the specified theme, mood, tone, or instructions in the <Text> prompt.
    - Avoid duplicating colors within the same palette.
    - Keep the palettes within a range of 2 to 8 colors.
    - Do not give "null" as a result, try produce some color palette.

    Desired Format:
      - a JSON array of hexadecimal color codes
      - a JSON array of color name respectively
      - for example: "[\"#f00\", \"#ff0\", \"#0f0\", \"#0ff\", \"#00f\", \"#f0f\", \"#000\"], [\"red\", \"yellow\", \"green\", \"aqua\", \"blue\", \"fuchsia\", \"black\"]"

    Text: {text}
    Result:
    """

    completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=200,
            temperature=0.8,
        )

    result = completion.choices[0].text.strip()

    # Split the result into two parts: colors and names
    colors, names = result.split("], [")

    colors = f"""{colors}]"""
    names = f"""[{names}"""

    try:
      colors = json.loads(colors)
      names = json.loads(names)

      result_dict = {
          "colors": colors,
          "names": names
      }
      return result_dict
    except json.decoder.JSONDecodeError as e:
      print("Error decoding JSON:", e)

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    # GET QUERY FROM THE FORM
    query = app.logger.info(request.form.get("query"))

    # OPEN AI COMPLETION CALL
    result = get_and_render_prompt(query)

    # PRINT RETURN COLORS

    # RETURN LIST OF COLORS
    return {
        "result": result
       }

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)