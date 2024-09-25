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
                console.log('Generated topic:', data.topic);
                topicElement.textContent = data.topic;
            })
            .catch(error => console.error('Error generating topic:', error));
    }

    function startRecording() {
        console.log('Starting recording...');
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                recorder = RecordRTC(stream, {
                    type: 'audio',
                    mimeType: 'audio/webm'
                });
                recorder.startRecording();
                startRecordingBtn.disabled = true;
                stopRecordingBtn.disabled = false;
                console.log('Recording started');
            })
            .catch(error => console.error('Error accessing microphone:', error));
    }

    function stopRecording() {
        console.log('Stopping recording...');
        recorder.stopRecording(() => {
            audio = recorder.getBlob();
            sendAudioForEvaluation(audio);
            startRecordingBtn.disabled = false;
            stopRecordingBtn.disabled = true;
            console.log('Recording stopped');
        });
    }

    function sendAudioForEvaluation(audioBlob) {
        console.log('Sending audio for evaluation...');
        const formData = new FormData();
        formData.append('audio', audioBlob, 'speech.webm');

        fetch('/evaluate_speech', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received evaluation data:', data);
            displayResults(data);
        })
        .catch(error => {
            console.error('Error during evaluation:', error);
            alert('An error occurred during speech evaluation. Please try again.');
        });
    }

    function displayResults(data) {
        console.log('Displaying results:', data);
        if (data.error) {
            console.error('Error in evaluation results:', data.error);
            alert(`Error: ${data.error}`);
            return;
        }

        transcriptionElement.textContent = data.transcription || 'No transcription available';
        scoreElement.textContent = data.score ? `${data.score}/10` : 'N/A';
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
