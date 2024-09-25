let recorder;
let audio;

document.addEventListener('DOMContentLoaded', () => {
    const generateTopicBtn = document.getElementById('generate-topic');
    const startRecordingBtn = document.getElementById('start-recording');
    const stopRecordingBtn = document.getElementById('stop-recording');
    const topicElement = document.getElementById('topic');
    const transcriptionElement = document.getElementById('transcription');
    const scoreElement = document.getElementById('score');
    const improvementsElement = document.getElementById('improvements');
    const resultsContainer = document.getElementById('results-container');

    generateTopicBtn.addEventListener('click', generateTopic);
    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);

    generateTopic();

    function generateTopic() {
        fetch('/generate_topic')
            .then(response => response.json())
            .then(data => {
                topicElement.textContent = data.topic;
            })
            .catch(error => console.error('Error:', error));
    }

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                recorder = RecordRTC(stream, {
                    type: 'audio',
                    mimeType: 'audio/webm'
                });
                recorder.startRecording();
                startRecordingBtn.disabled = true;
                stopRecordingBtn.disabled = false;
            })
            .catch(error => console.error('Error accessing microphone:', error));
    }

    function stopRecording() {
        recorder.stopRecording(() => {
            audio = recorder.getBlob();
            sendAudioForEvaluation(audio);
            startRecordingBtn.disabled = false;
            stopRecordingBtn.disabled = true;
        });
    }

    function sendAudioForEvaluation(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'speech.webm');

        fetch('/evaluate_speech', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => console.error('Error:', error));
    }

    function displayResults(data) {
        transcriptionElement.textContent = data.transcription;
        scoreElement.textContent = `${data.score}/10`;
        improvementsElement.innerHTML = '';
        if (data.improvements && Array.isArray(data.improvements)) {
            data.improvements.forEach(improvement => {
                const li = document.createElement('li');
                li.textContent = improvement;
                improvementsElement.appendChild(li);
            });
        } else {
            improvementsElement.innerHTML = '<li>No specific improvements suggested.</li>';
        }
        resultsContainer.style.display = 'block';
    }
});
