from flask import Flask, render_template, request
import google.generativeai as genai
from search_google import search_google
from web_crawler import crawl_web

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
    base_user_input = request.form['user_input']
    user_input = base_user_input + " Trả lời 'Không' nếu không thể trả lời chính xác."
    # user_input = base_user_input
    try:
        response = convo.send_message(user_input)
        # print(user_input)
        print(response.text)
        if response.text.startswith("Không"):
            print("Model could not respond. Searching Google for relevant websites...")
            search_results = search_google(base_user_input)

            if search_results:
                # carwl all search results
                i = 0
                for result in search_results:
                    crawl_web(result, f'result/result_{i}.txt')
                    i += 1
                # Combine data from all search results
                data = ""
                for i in range(len(search_results)):
                    with open(f'result/result_{i}.txt', 'r', encoding='utf-8') as f:
                        data += f.read()
                data = data + "Với dữ liệu trên trả lời và giải thích." + base_user_input
                # Send the data to the model for synthesis
                new_convo = model.start_chat(history=[])
                # new_response = new_convo.send_message(data)
                # print(f"'New response:' {new_response.text}")
                response = new_convo.send_message(data)
                print(f"'Response:' {response.text}")
        messages = [
            {'type': 'user-message', 'content': f'You: {base_user_input}'},
            {'type': 'model-message', 'content': f'Model: {response.text}'}
        ]
    except Exception as e:
        print(f"Model could not respond: {e}")
        messages = [
            {'type': 'user-message', 'content': f'You: {base_user_input}'},
            {'type': 'model-message', 'content': f'Không thể trả lời câu hỏi.'}
        ]

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
