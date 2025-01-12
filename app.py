from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
import google.generativeai as genai
import base64
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure APIs
genai.configure(api_key="AIzaSyCegsY2kp1OVzWTx5Vdom1k0mJFOrWiits")  
elevenlabs_api_key = "sk_2f09d95c42bd022daee83243a57ef05106d2e5597a40af4d"
client = ElevenLabs(api_key=elevenlabs_api_key)

# Voice ID for ElevenLabs
VOICE_ID = "dFL9bzYmnpBkY6f0KZip"


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    try:
        # Step 1: Capture and transcribe user speech
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            logging.info("Listening for user input...")
            audio = recognizer.listen(source, phrase_time_limit=5)

        # Recognize user speech
        try:
            user_input = recognizer.recognize_google(audio)
            logging.debug(f"Recognized text: {user_input}")
        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand audio")
            return jsonify({'response': "Could not understand audio.", 'audio': None}), 400  # Return 400 for bad request
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return jsonify({'response': "Speech recognition service is unavailable.", 'audio': None}), 500


        # Step 2: Generate AI response using Gemini API
        logging.debug("Generating response using Gemini API...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_input)
            ai_text = response.text
            logging.debug(f"AI Response: {ai_text}")

        except Exception as e:
                logging.error(f"Error with Gemini API: {e}")
                return jsonify({'response': "Error with the AI model.", 'audio': None}), 500

        # Step 3: Generate audio for the response
        logging.debug("Generating audio response with ElevenLabs...")
        try:
            audio_stream = client.generate(
                text=ai_text,
                voice=VOICE_ID,
                stream=False,
                optimize_streaming_latency=3
            )
            audio_data = b"".join(audio_stream)
            if not audio_data:
                raise ValueError("No audio data received from ElevenLabs API.")
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        except Exception as e:
            logging.error(f"Error with ElevenLabs API: {e}")
            return jsonify({'response': "Error with audio service.", 'audio': None}), 500

        return jsonify({'response': ai_text, 'audio': audio_base64})

    except Exception as e:
         logging.exception(f"An unexpected error occurred: {e}")
         return jsonify({'response': "An unexpected error occurred.", 'audio': None}), 500


if __name__ == '__main__':
    app.run(debug=True)
    
