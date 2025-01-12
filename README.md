# Short - AI Voice Assistant
Voice-Enabled AI Assistant Web Application (Note:Use your own API Keys)

## Overview

Short is a simple, interactive voice assistant built using Python with Flask for the backend and HTML/CSS/JavaScript for the frontend. It integrates Google's Gemini AI model for natural language processing, Google's Speech Recognition for speech-to-text, and ElevenLabs for text-to-speech, allowing you to have spoken interactions with an AI through your browser. Short aims to be a minimal example of a personal voice AI that captures audio input, converts to text, generates an AI response, converts it back to audio and finally plays the audio in a seamless interaction that has automated detection, to provide natural interface

## Features

*   **Voice Input:** Captures user speech using a browser microphone.
*   **Speech-to-Text:** Transcribes the audio input using Google's Speech Recognition service.
*   **AI Response Generation:** Utilizes Google's Gemini AI model to generate relevant responses.
*   **Text-to-Speech:** Converts the AI-generated text into spoken audio with ElevenLabs' text-to-speech.
*   **Automatic Detection:** The application uses `speech_recognition` to automatically start processing after you have finished speaking, providing a very natural and hands free approach similar to how major voice assistants work.
*   **Cross-browser functionality:** The application is meant to be able to run in various browsers such as Chrome and FireFox, but not for every version of every single browser. It may not be tested on every version of each, though.

## Setup

Follow these instructions to get the project running locally:

### Prerequisites

*   **Python 3.7+**
*   **`pip`** (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```
    _Replace `your-username/your-repository` with the appropriate repository url_

2.  **Create a virtual environment:** (Optional but highly recommended)

    ```bash
    python3 -m venv short_env
    source short_env/bin/activate  # On macOS and Linux
    # short_env\Scripts\activate  On Windows
    ```

3.  **Install required Python packages:**

    ```bash
    pip install flask speechrecognition google-generativeai elevenlabs
    ```

4.  **Obtain API Keys:**
    * You will need a Google Gemini API Key from [Google AI Studio](https://makersuite.google.com/)
    * You also need a Eleven Labs API Key from [Eleven Labs Beta](https://beta.elevenlabs.io/)
5. **Place the API keys** in `app.py`. The configuration lines must be filled:

    ```python
        genai.configure(api_key="YOUR_GEMINI_API_KEY")
        elevenlabs_api_key = "YOUR_ELEVENLABS_API_KEY"
    ```
6.   **Start the application**

     ```bash
    python app.py
     ```
    
    You can now access the website in [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Please enable the correct permission on your browser.
 
## Usage
    * On your local website Click on the circles
    *  Speak to the application
    *  Wait for audio output
   
## License
     MIT

## Acknowledgments

* Google's Gemini for providing robust Natural Language Processing AI service.
* Google's Speech Recognition service to interpret user voice audio inputs.
* Eleven Labs for fast generation of good quality voice AI responses.
