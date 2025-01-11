from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
import google.generativeai as genai
import base64
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the Gemini and ElevenLabs API keys
genai.configure(api_key="Gemini_API_Key")
model = genai.GenerativeModel('gemini-pro')
elevenlabs_api_key = "ElevenLabs_API_Key"
client = ElevenLabs(api_key=elevenlabs_api_key)
welcome_voice = None
try:
  logging.debug("Attempting to generate the welcome voice...")
  welcome_stream = client.generate(text="Hello! Sir, How can I help you today?", voice = "dFL9bzYmnpBkY6f0KZip", stream = False)
  welcome_data = b"".join([chunk for chunk in welcome_stream])
  welcome_voice = base64.b64encode(welcome_data).decode('utf-8')
  logging.debug("Welcome audio generated and encoded successfully.")

except Exception as e:
  logging.error(f"Error generating welcome voice: {e}")

@app.route('/')
def index():
    logging.debug("Root route accessed.")
    return render_template('index.html', welcome_voice=welcome_voice)

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text', '')
    logging.debug(f"Received text from client: {text}")
    if text:
        try:
            logging.debug("Generating content from Gemini...")
            response = model.generate_content(text)
            response.resolve()
            if response.text:
               gemini_text = response.text
               logging.debug(f"Gemini response: {gemini_text}")
            else:
               gemini_text = "No response from the AI model."
               logging.debug(f"Gemini API did not generate a text output.")

            logging.debug(f"Generating ElevenLabs audio for: {gemini_text}")
            audio_stream = client.generate(
                text = gemini_text,
                voice = "dFL9bzYmnpBkY6f0KZip",  # Make sure to replace this with your voice ID
                stream = False
             )
            audio_data = b"".join([chunk for chunk in audio_stream])
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            logging.debug("ElevenLabs audio generated and base64 encoded.")
            return jsonify({'response': gemini_text, 'audio': audio_base64})
        except Exception as e:
            logging.error(f"Error during processing: {e}")
            return jsonify({'response': 'An error occurred'}), 500
    else:
       logging.warning("No text received")
       return jsonify({'response': 'No Text received'}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
