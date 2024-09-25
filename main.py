from flask import Flask, render_template, request, jsonify
from utils.topic_generator import generate_topic
from utils.speech_evaluator import transcribe_speech, evaluate_speech
import speech_recognition as sr
import logging
from pydub import AudioSegment
import io

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_topic', methods=['GET'])
def get_topic():
    topic = generate_topic()
    return jsonify({'topic': topic})

@app.route('/evaluate_speech', methods=['POST'])
def evaluate():
    if 'audio' not in request.files:
        app.logger.error("No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    recognizer = sr.Recognizer()

    try:
        app.logger.info("Processing audio file")
        # Convert the incoming audio to WAV format
        audio = AudioSegment.from_file(audio_file, format="webm")
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)

        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)

        app.logger.info("Transcribing speech")
        transcription = transcribe_speech(audio_data)
        app.logger.info(f"Transcription result: {transcription}")

        app.logger.info("Evaluating speech")
        score, improvements = evaluate_speech(transcription)
        app.logger.info(f"Evaluation result - Score: {score}, Improvements: {improvements}")

        return jsonify({
            'transcription': transcription,
            'score': score,
            'improvements': improvements
        })
    except Exception as e:
        app.logger.error(f"Error during speech evaluation: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
