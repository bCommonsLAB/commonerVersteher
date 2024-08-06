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
                file=f,
                language="de"
            )
        
        transcript = response['text']

        # for develop: transcript="Ich bin in der Stadt und möchte mich mit Menschen treffen um mit ihnen ein Bier zu trinken!"
        # app.logger.debug(transcript);

        language = response.get('language', 'de')  # Default to 'de' if language is not provided

        # Construct the prompt
        # prompt = config['jsonbuild'] + transcript

        prompt = """
            Analysiere folgenden Deutschen Text und gib die Ergebnisse im JSON-Format zurück:
            Ergebnisformat:
            {
                "Transcript": string 1,
                "Eindruck": string 2,
                "Gemeinschaft": integer 3,
                "Vertrauen": integer 4,
                "Gegenseitig": integer 5,
                "Nachhaltig": integer 6,
                "Inklusion": integer 7,
                "Kommerziell": integer 8,
                "SozialesMiteinander": integer 9,
                "GleichrangigeSelbstOrganisation": integer 10,
                "SorgendesSelbstbestimmtesWirtschaften": integer 11
            }
            string 1: "Transcript" sollte den Text nochmal beinhalten.
            string 2: "Reflektiere" unter Eindruck den Inhalt, wie gut der Text die Werte des Commoning widerspiegelt. Welche Inhalte des Textes entsprechen besonders der Logik des Commoning, und welche widersprechen ihr besonders? 
            integer 3: Der Wert für "Gemeinschaft" sollte die Verbundenheit der Menschen durch eine Zahl zwischen 0 und 100 ausdrücken, wobei 0 sehr egoistisch ist und 100 sehr gemeinschaftssinnig ist.
            integer 4: Der Wert für "Vertrauen" sollte die Vertrauenswürdigkeit des Textes durch eine Zahl zwischen 0 und 100 ausdrücken, wobei 0 sehr mistrauisch ist und 100 sehr vertrauenswürdig ist.
            integer 5: Der Wert für "Gegenseitig" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie einladend und offenherzig der Text für eine kollaboration ist, wobei 0 sehr abweisend ist und 100 sehr einladend ist.
            integer 6: Der Wert für "Nachhaltig" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie bewust man mit Ressourcen umgeht, wobei 0 sehr verschwenderisch und 100 sehr bewust und sparspam ist.
            integer 7: Der Wert für "Inklusion" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie Inklussiv der Text ist, wobei 0 bestimmte Menschen ausgrenzt und 100 alle einschliesst.
            integer 8: Der Wert für "Kommerziell" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie sehr der Text profitorientiertes Wirtschaften ausdrückt, wobei 0 eine sehr bedürfnisorientiertes Wirtschaften und 100 sehr profitorientiertes Wirtschaften bedeutet.
            integer 9: Der Wert für "SozialesMiteinander" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie sehr der Text Zusammenarbeit und Förderung von Beziehungen ausdrückt, wobei 0 asoziales Verhalten und 100 sehr soziales Verhalten ausdrückt.
            integer 10: Der Wert für "GleichrangigeSelbstOrganisation" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie sehr der Text das Aushandeln auf Augenhöhe fördert, wobei 0 sehr Rangordnungsorientiert ist und 100 die Begenung auf Augenhöhe fördert.
            integer 11: Der Wert für "SorgendesSelbstbestimmtesWirtschaften" sollte durch eine Zahl zwischen 0 und 100 ausdrücken, wie sehr der Text sorgendes und selbstbestimmtes Wirtschaften ausdrückt, wobei 0 sehr fremdbestimmtes profititorientiertes Wirtschaften ist und 100 selbstbestimmtes und bedürfnisorientiertes Wirtschaften ausdrückt.
            Transcript: """
        prompt = prompt + transcript

        # Send prompt to OpenAI's GPT-3.5-turbo
        completion_response = openai.ChatCompletion.create(
            model=config['modelname'],
            messages=[
                {"role": "system", "content": "Du bist ein Wissenschaftler, der sich im Bereich Commoning sehr gut auskennt und die Lehre von Silke Helfrich verkörpert, die sie in ihren Publikationen, u.a. Frei fair & Lebendig die macht der Commos publiziert hat. Analysiere die texte in diesem Geist und gebe sie in einer verständlichen Sprache zurück!"},
                {"role": "user", "content": prompt}
            ]
        )

        try:
            result = completion_response['choices'][0]['message']['content'].strip()
            json_result = json.loads(result)
            app.logger.error(json_result)

        except Exception as e:
            app.logger.debug(completion_response)
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