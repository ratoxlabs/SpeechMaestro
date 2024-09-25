import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import string
import re

# Download required NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

def transcribe_speech(audio_data):
    recognizer = sr.Recognizer()
    try:
        transcription = recognizer.recognize_google(audio_data)
        print(f"Transcription: {transcription}")
        return transcription
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")
        return "Could not request results from the speech recognition service"

def evaluate_speech(transcription):
    print(f"Evaluating speech: {transcription}")
    
    # Perform necessary text analysis
    words = word_tokenize(transcription.lower())
    sentences = sent_tokenize(transcription)
    stop_words = set(stopwords.words('english'))
    words_no_stop = [word for word in words if word not in stop_words and word not in string.punctuation]
    
    # Evaluate each category
    clarity_structure_score = evaluate_clarity_structure(sentences, words_no_stop)
    content_relevance_score = evaluate_content_relevance(words_no_stop)
    language_style_score = evaluate_language_style(words, words_no_stop)
    purpose_impact_score = evaluate_purpose_impact(sentences, words_no_stop)
    audience_awareness_score = evaluate_audience_awareness(words_no_stop)
    
    # Calculate total score
    total_score = (clarity_structure_score + content_relevance_score + language_style_score + 
                   purpose_impact_score + audience_awareness_score) / 5
    
    # Generate improvements based on scores
    improvements = generate_improvements(clarity_structure_score, content_relevance_score, 
                                         language_style_score, purpose_impact_score, 
                                         audience_awareness_score)
    
    normalized_score = round(total_score * 10, 1)  # Score out of 10
    print(f"Evaluation results - Score: {normalized_score}, Improvements: {improvements}")
    return normalized_score, improvements

def evaluate_clarity_structure(sentences, words_no_stop):
    sentence_count = len(sentences)
    avg_sentence_length = len(words_no_stop) / sentence_count if sentence_count > 0 else 0
    
    # Check for transition words
    transition_words = set(['however', 'therefore', 'moreover', 'furthermore', 'consequently', 'meanwhile', 'nevertheless'])
    transition_word_count = sum(1 for word in words_no_stop if word in transition_words)
    
    # Simple scoring based on sentence count, average length, and transition words
    score = min(sentence_count / 10, 1) + min(avg_sentence_length / 20, 1) + min(transition_word_count / 5, 1)
    return score / 3  # Normalize to 0-1 range

def evaluate_content_relevance(words_no_stop):
    # This is a simplified evaluation. In a real-world scenario, you'd compare against a known topic or use more advanced NLP techniques.
    relevant_keywords = set(['speech', 'communication', 'audience', 'message', 'topic', 'argument', 'point'])
    keyword_count = sum(1 for word in words_no_stop if word in relevant_keywords)
    return min(keyword_count / 10, 1)  # Normalize to 0-1 range

def evaluate_language_style(words, words_no_stop):
    # Vocabulary diversity
    vocab_diversity = len(set(words_no_stop)) / len(words_no_stop) if words_no_stop else 0
    
    # Check for advanced language constructs (e.g., bigrams)
    bigrams = list(ngrams(words, 2))
    advanced_constructs = [('not', 'only'), ('on', 'the', 'other', 'hand'), ('in', 'conclusion')]
    advanced_construct_count = sum(1 for gram in bigrams if gram in advanced_constructs)
    
    score = (vocab_diversity + min(advanced_construct_count / 3, 1)) / 2
    return score

def evaluate_purpose_impact(sentences, words_no_stop):
    # Simple classification based on key phrases
    informative_words = set(['explain', 'describe', 'inform', 'demonstrate'])
    persuasive_words = set(['convince', 'argue', 'persuade', 'urge'])
    
    informative_count = sum(1 for word in words_no_stop if word in informative_words)
    persuasive_count = sum(1 for word in words_no_stop if word in persuasive_words)
    
    purpose_score = max(informative_count, persuasive_count) / len(sentences)
    return min(purpose_score, 1)

def evaluate_audience_awareness(words_no_stop):
    # Simplified evaluation based on language complexity
    complex_words = [word for word in words_no_stop if len(word) > 8]
    complexity_ratio = len(complex_words) / len(words_no_stop) if words_no_stop else 0
    return min(complexity_ratio * 5, 1)  # Normalize to 0-1 range

def generate_improvements(clarity_score, content_score, language_score, purpose_score, audience_score):
    improvements = []
    if clarity_score < 0.6:
        improvements.append("Work on structuring your speech with a clear introduction, body, and conclusion.")
    if content_score < 0.6:
        improvements.append("Try to include more relevant examples and data to support your main points.")
    if language_score < 0.6:
        improvements.append("Enhance your vocabulary and use more diverse language constructs.")
    if purpose_score < 0.6:
        improvements.append("Clarify the main purpose of your speech and ensure it aligns with your content.")
    if audience_score < 0.6:
        improvements.append("Adjust your language complexity to better suit your target audience.")
    return improvements

