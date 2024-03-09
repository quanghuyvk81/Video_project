from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyD12up981Q7Tr_hvK97rBAD6IK-hpTX07Y")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

convo = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('index.html', messages=[])

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = convo.send_message(user_input)

    messages = [
        {'type': 'user-message', 'content': f'You: {user_input}'},
        {'type': 'model-message', 'content': f'Model: {response.text}'}
    ]

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
