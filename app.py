from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import google.generativeai as genai
import base64
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure APIs
genai.configure(api_key="AIzaSyA_H5o_h9WhwD700WycZg7uhhK9G4pwzGU")
elevenlabs_api_key = "sk_b2ef27a7f0f489b41e6130c9e77bf0a3d51f2ced468e7bf7"
client = ElevenLabs(api_key=elevenlabs_api_key)

# Voice ID for ElevenLabs
VOICE_ID = "dFL9bzYmnpBkY6f0KZip"  # Replace with your voice ID

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    try:
        # Capture and transcribe user speech
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for input...")
            audio = recognizer.listen(source, phrase_time_limit=5)
            user_input = recognizer.recognize_google(audio)
            print(f"User said: {user_input}")
        
        # Generate AI response
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        response.resolve()
        if response.text:
            ai_response = response.text
        else:
            ai_response = "No response from the AI model."
        print(f"AI Response: {ai_response}")
        
        # Generate audio for the response
        audio_stream = client.generate(
            text=ai_response,
            voice=VOICE_ID,
            stream=False
        )
        audio_data = b"".join(audio_stream)

        # Validate audio data
        if not audio_data:
            raise ValueError("No audio data received from ElevenLabs API.")

        # Encode audio data as Base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return jsonify({'response': ai_response, 'audio': audio_base64})

    except sr.UnknownValueError:
        logging.error("Speech recognition failed to understand the input.")
        return jsonify({'response': "Sorry, I could not understand the audio.", 'audio': None}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'response': "An error occurred while processing your request.", 'audio': None}), 500

if __name__ == '__main__':
    app.run(debug=True)
