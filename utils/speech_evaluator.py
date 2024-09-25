import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string

# Download required NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

def transcribe_speech(audio_data):
    recognizer = sr.Recognizer()
    try:
        transcription = recognizer.recognize_google(audio_data)
        print(f"Transcription: {transcription}")  # Added print statement
        return transcription
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")  # Added print statement
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")  # Added print statement
        return "Could not request results from the speech recognition service"

def evaluate_speech(transcription):
    print(f"Evaluating speech: {transcription}")  # Added print statement
    words = word_tokenize(transcription.lower())
    sentences = sent_tokenize(transcription)
    stop_words = set(stopwords.words('english'))
    
    # Remove punctuation and stop words
    words = [word for word in words if word not in string.punctuation and word not in stop_words]
    
    word_count = len(words)
    sentence_count = len(sentences)
    unique_words = len(set(words))
    
    # Calculate scores
    length_score = min(word_count / 100, 2)  # 2 points for 100+ words
    complexity_score = min(unique_words / word_count * 5, 3)  # 3 points for vocabulary diversity
    structure_score = min(sentence_count / 5, 2)  # 2 points for 5+ sentences
    
    # Placeholder for more advanced metrics
    content_score = 2  # Placeholder score for content relevance and coherence
    delivery_score = 1  # Placeholder score for delivery (would require audio analysis)
    
    total_score = length_score + complexity_score + structure_score + content_score + delivery_score
    normalized_score = round(total_score / 10 * 10, 1)  # Score out of 10
    
    improvements = []
    if length_score < 2:
        improvements.append("Try to speak for a longer duration to fully develop your ideas.")
    if complexity_score < 2:
        improvements.append("Use a wider variety of words to enhance your vocabulary.")
    if structure_score < 1.5:
        improvements.append("Structure your speech with more distinct points or paragraphs.")
    if content_score < 1.5:
        improvements.append("Focus on developing your main arguments with supporting details.")
    if delivery_score < 0.8:
        improvements.append("Work on your delivery, including pace and clarity of speech.")
    
    print(f"Evaluation results - Score: {normalized_score}, Improvements: {improvements}")  # Added print statement
    return normalized_score, improvements
