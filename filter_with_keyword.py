import re
import nltk
from nltk.corpus import stopwords
from langdetect import detect

# Add your keywords here
keywords = ["keyword1", "keyword2"]

# Download the list of English stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def text_processing(source_file, result_file):
    with open(source_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    processed_sentences = []
    for sentence in sentences:
        # Remove punctuation
        sentence = re.sub(r'[^\w\s]', '', sentence)

        # Convert all words to lowercase
        sentence = sentence.lower()

        # Remove numbers and numerical expressions
        sentence = re.sub(r'\d+', '', sentence)

        # Remove stopwords
        sentence = ' '.join(word for word in sentence.split() if word not in stop_words)

        # Remove words that are 1 or 2 letters long
        sentence = ' '.join(word for word in sentence.split() if len(word) > 2)

        # If the sentence contains non-English letters or characters, remove the entire sentence
        if re.search(r'[^a-zA-Z\s]', sentence):
            continue

        # If the sentence is shorter than 3 words, remove the entire sentence
        if len(sentence.split()) < 3:
            continue

        # Test if the sentence is in English
        try:
            if detect(sentence) != 'en':
                continue
        except:
            continue

        # Keyword check
        if not any(word in sentence for word in keywords):
            continue

        processed_sentences.append(sentence)

    # Write the results to a file
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_sentences))

    print(f"'{result_file}' file has been successfully created and processed.")

# Start the process
text_processing('input.txt', 'final_with_keyword.txt')
