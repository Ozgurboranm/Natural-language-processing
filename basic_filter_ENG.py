import re
import nltk
from nltk.corpus import stopwords
from langdetect import detect

# Download the list of English stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def process_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
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

        # Remove words with length 1 or 2
        sentence = ' '.join(word for word in sentence.split() if len(word) > 2)

        # If the sentence contains non-English letters or characters, remove the entire sentence
        if re.search(r'[^a-zA-Z\s]', sentence):
            continue

        # If the sentence is shorter than 3 words, remove the entire sentence
        if len(sentence.split()) < 3:
            continue

        # Detect the language of the sentence, if it's not English, remove the sentence
        try:
            if detect(sentence) != 'en':
                continue
        except:
            continue

        processed_sentences.append(sentence)

    # Write the results to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_sentences))

    print(f"The file '{output_file}' has been successfully created and processed.")

# Start the process
process_text('input.txt', 'final.txt')
