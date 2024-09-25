let recorder;
let audio;
let selectedTopic;

document.addEventListener('DOMContentLoaded', () => {
    const generateTopicBtn = document.getElementById('generate-topic');
    const startRecordingBtn = document.getElementById('start-recording');
    const stopRecordingBtn = document.getElementById('stop-recording');
    const topicsElement = document.getElementById('topics');
    const recordingContainer = document.getElementById('recording-container');
    const transcriptionElement = document.getElementById('transcription');
    const scoreElement = document.getElementById('score');
    const improvementsElement = document.getElementById('improvements');
    const resultsContainer = document.getElementById('results-container');

    generateTopicBtn.addEventListener('click', generateTopics);
    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);

    generateTopics();

    function generateTopics() {
        fetch('/generate_topic')
            .then(response => response.json())
            .then(data => {
                console.log('Generated topics:', data.topics);
                topicsElement.innerHTML = '';
                data.topics.forEach((topic, index) => {
                    const button = document.createElement('button');
                    button.textContent = topic;
                    button.classList.add('topic-button');
                    button.addEventListener('click', () => selectTopic(topic));
                    topicsElement.appendChild(button);
                });
                recordingContainer.style.display = 'none';
                selectedTopic = null;
            })
            .catch(error => console.error('Error generating topics:', error));
    }

    function selectTopic(topic) {
        selectedTopic = topic;
        document.querySelectorAll('.topic-button').forEach(btn => {
            btn.classList.remove('selected');
            if (btn.textContent === topic) {
                btn.classList.add('selected');
            }
        });
        recordingContainer.style.display = 'block';
    }

    function startRecording() {
        if (!selectedTopic) {
            alert('Please select a topic before recording.');
            return;
        }
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
        formData.append('topic', selectedTopic);

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
