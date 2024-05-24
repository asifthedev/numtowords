from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure API key
API_KEY = "AIzaSyAcsgQkDQWXXvkuAQSZzsCUbxUdDdrt6i0"
genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Assume you are a website page that converts mathematical numbers into words for example 500 to Five Hundred. Nothin less nothing more. You have been banned for saying anything other than that in response. Only converts the number into words. Say 'Invalid input' if user enter something else other than number",
)

chat_session = model.start_chat(history=[])

def convert_number_to_words(number):
    response = chat_session.send_message(str(number))
    return response.text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = convert_number_to_words(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
