from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv

# Load .env file explicitly (more reliable)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)
CORS(app)

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# 🚨 Safety check (IMPORTANT for debugging)
if not api_key:
    raise ValueError("API key not found. Check your .env file!")

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        text = request.json.get("text", "")

        prompt = f"""
        Analyze the following terms and conditions.

        Respond STRICTLY in this format:

        Summary:
        - ...

        Risks:
        - (High) ...
        - (Medium) ...
        - (Low) ...

        Safety Score: <number between 1 to 10>

        Final Recommendation: <Accept or Not Recommended>

        Text:
        {text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text if response.text else "No response from AI"

        return jsonify({"result": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"result": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)