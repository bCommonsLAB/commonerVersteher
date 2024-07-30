from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from pathlib import Path
import openai
from gtts import gTTS
import threading
import time
from langdetect import detect, DetectorFactory

# Load configuration from config.json
config_path = Path(__file__).parent / "config.json"
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
CORS(app)

openai.api_key = config['myopenkey']

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        app.logger.error('No audio file found')
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio']
    audio_file_path = 'audio.mp3'
    audio_file.save(audio_file_path)

    try:
        # Transcribe audio using OpenAI's Whisper API
        with open(audio_file_path, 'rb') as f:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=f
            )
        transcript = response['text']
        language = response.get('language', 'de')  # Default to 'de' if language is not provided

        # Construct the prompt
        prompt = config['jsonbuild'] + transcript

        # Send prompt to OpenAI's GPT-3.5-turbo
        completion_response = openai.ChatCompletion.create(
            model=config['modelname'],
            messages=[
                {"role": "system", "content": "Du bist ein hilfsbereiter Assistent und gibst nur die sachen aus die was dir befehlt werden und alles ist auf deutsch allso verwende  keine anderen sprachen!"},
                {"role": "user", "content": prompt}
            ]
        )

        try:
            result = completion_response['choices'][0]['message']['content'].strip()
            json_result = json.loads(result)
        except Exception as e:
            app.logger.error(f'Error processing OpenAI response: {e}')
            return jsonify({'error': 'Error processing OpenAI response'}), 500

        return jsonify(json_result), 200

    except Exception as e:
        app.logger.error(f'Error during transcription or processing: {e}')
        return jsonify({'error': 'Error during transcription or processing'}), 500

    finally:
        # Delete the audio file regardless of the outcome
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

def delayed_delete(file_path, delay=5):
    """Delete the specified file after a delay."""
    def delete_file():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            app.logger.error(f"Error deleting file {file_path}: {e}")

    thread = threading.Thread(target=delete_file)
    thread.start()

@app.route('/tts', methods=['POST', 'OPTIONS'])
def tts():
    if request.method == 'OPTIONS':
        return '', 200  # Respond to CORS preflight request

    data = request.get_json()
    text = data.get('text')
    section = data.get('section')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Determine the language based on the section
        if section in ['german-transcription', 'german-summary']:
            language = 'de'
        else:
            language = detect(text)  # General detection for other sections

        speech_file_path = Path(__file__).parent / "speech.mp3"
        tts = gTTS(text, lang=language)
        tts.save(speech_file_path)

        response = send_file(speech_file_path, as_attachment=True)
        
        # Schedule the file for deletion after a delay
        delayed_delete(speech_file_path)

        return response

    except Exception as e:
        app.logger.error(f'Error during TTS processing: {e}')
        return jsonify({'error': 'Error during TTS processing'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)