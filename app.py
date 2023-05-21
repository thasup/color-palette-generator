import openai
import json
import ast
from dotenv import dotenv_values
from flask import Flask, render_template, request

config = dotenv_values(".env")
openai.api_key  = config["OPENAI_API_KEY"]

app = Flask(
    __name__,
    template_folder="templates",
    static_url_path="",
    static_folder="static"
)

def get_and_render_prompt(text):
    message=f"""
    Color Palette Generator

    Generate color palettes that match the given theme, mood, or instructions.

    Instructions:
    - Provide a verbal description of the color palette you want.
    - Avoid duplicating colors within the same palette.
    - Keep the palette size between 2 to 8 colors.
    - Keep strictly response in the desired format.

    Example Usage:
    - Instruction: Generate a color palette for a Google brand.
    - Output:"["#4285f4", "#34a853", "#fbbc05", "#ea4335"], ["Google Blue", "Google Green", "Google Yellow", "Google Red"]"

    - Instruction: Generate a color palette for ocean pastels color palette.
    - Output:"["#83ADFC", "#53CBED", "#22D9DB", "#14D59C", "#0EC36F", "#2EAC8D", "#2A8FBC"], ["Sky Blue", "Light Blue", "Turquoise", "Mint Green", "Emerald Green", "Teal", "Navy Blue"]"

    Desired Response JSON Format:"["#color1", "#color2", ...], ["name1", "name2", ...]"

    Instruction: Generate a color palette for {text}

    Result:
    """

    completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=500,
            temperature=1.2,
        )

    # Remove leading and trailing whitespaces from the input string
    result = completion.choices[0].text.strip()

    # Adjust the input string to make it valid JSON
    valid_json_str = "[" + result + "]"


    try:
      # Parse the valid JSON string into a Python list
      result_array = json.loads(valid_json_str)

      # Extract the separate lists from the resulting array
      colors = result_array[0]
      names = result_array[1]

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

    return {
        "result": result
       }

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)