from flask import Flask, render_template, request, jsonify
from utils.topic_generator import generate_topic
from utils.speech_evaluator import transcribe_speech, evaluate_speech
import speech_recognition as sr

app = Flask(__name__)

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
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        
        transcription = transcribe_speech(audio_data)
        score, improvements = evaluate_speech(transcription)

        return jsonify({
            'transcription': transcription,
            'score': score,
            'improvements': improvements
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
