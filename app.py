from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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   '

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # Get user input from the form
        user_input = request.form['user_input']

        # Call ChatGPT to get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
        )

        # Extract the generated answer from the response
        answer = response['choices'][0]['message']['content']

        # Return the answer as JSON
        return jsonify({'answer': answer})

    except openai.error.OpenAIError as e:
        error_message = str(e)
        error_code = e.code

        # Log the error information
        if error_code is not None:
            app.logger.error(f'OpenAI API Error - Code: {error_code}, Message: {error_message}')
        else:
            app.logger.error(f'OpenAI API Error - Message: {error_message}')

        return jsonify({'error': error_message, 'error_code': error_code})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
