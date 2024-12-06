def print_developer_info():
    """
    Prints the developer's name and library details.
    """
    print("Library Name: HubNLP")
    print("Developed by: Nexio Tech")

def print_library_tagline():
    """
    Prints a tagline for the library.
    """
    print("HubNLP - Simplifying NLP for Everyone!")


def load_ner_data(file_path):
    """
    Load a text file in CoNLL format for Named Entity Recognition (NER).

    Args:
        file_path (str): Path to the CoNLL format text file.

    Returns:
        list: A list of sentences, where each sentence is represented as a list
              of tuples (word, POS, NER tag).
              
              Example:
              [[("John", "NNP", "B-PER"), ("Smith", "NNP", "I-PER")],
               [("London", "NNP", "B-LOC")]]
    """
    sentences = []
    sentence = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # New sentence
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                parts = line.split()
                if len(parts) == 4 and parts[0] != "-DOCSTART-":  # Skip DOCSTART
                    word, pos, chunk, ner = parts
                    sentence.append((word, pos, ner))
    return sentences


def extract_word_features(sentence, index):
    """
    Extract features for a specific word in a sentence for NLP tasks (e.g., NER or POS tagging).

    Args:
        sentence (list): A list of tuples representing a sentence, 
                         where each tuple contains (word, POS, [optional] NER tag).
        index (int): The index of the word in the sentence for which features are extracted.

    Returns:
        dict: A dictionary containing features for the word.
    """
    word = sentence[index][0]
    postag = sentence[index][1]

    features = {
        'word': word.lower(),
        'postag': postag,
        'is_upper': word.isupper(),
        'is_title': word.istitle(),
        'is_digit': word.isdigit(),
    }

    # Features for the previous word
    if index > 0:
        prev_word = sentence[index - 1][0]
        prev_postag = sentence[index - 1][1]
        features.update({
            '-1:word': prev_word.lower(),
            '-1:postag': prev_postag,
        })
    else:
        features['BOS'] = True  # Beginning of Sentence

    # Features for the next word
    if index < len(sentence) - 1:
        next_word = sentence[index + 1][0]
        next_postag = sentence[index + 1][1]
        features.update({
            '+1:word': next_word.lower(),
            '+1:postag': next_postag,
        })
    else:
        features['EOS'] = True  # End of Sentence

    return features
