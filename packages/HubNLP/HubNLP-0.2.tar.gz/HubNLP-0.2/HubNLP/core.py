import tensorflow as tf
from tensorflow.keras.layers import Layer, Input, Embedding, Bidirectional, LSTM, Dense


class AttentionLayer(Layer):
    """
    Custom Attention Layer that uses a Bi-directional LSTM followed by an attention mechanism.
    """
    def __init__(self, lstm_units):
        super(AttentionLayer, self).__init__()
        self.lstm_units = lstm_units
        self.lstm = Bidirectional(LSTM(self.lstm_units, return_sequences=True))  # Create LSTM layer here

    def call(self, inputs):
        """
        Forward pass for the Attention layer.

        Args:
            inputs (tuple): Tuple of text and aspect embeddings.

        Returns:
            context_vector (tensor): Weighted sum of LSTM outputs based on attention scores.
        """
        text_embedded, aspect_embedded = inputs
        
        # Process the text using a Bi-directional LSTM
        lstm_out = self.lstm(text_embedded)  # Apply LSTM to text embeddings
        
        # Aspect representation as query
        query = tf.reduce_mean(aspect_embedded, axis=1)  # shape: (batch_size, 128)
        
        # Ensure the query shape is compatible for matmul
        query = tf.expand_dims(query, axis=1)  # shape: (batch_size, 1, 128)
        
        # Attention mechanism
        attention_scores = tf.matmul(lstm_out, query, transpose_b=True)  # shape: (batch_size, seq_len, 1)
        attention_weights = tf.nn.softmax(attention_scores, axis=1)
        
        # Weighted sum of LSTM outputs based on attention weights
        context_vector = tf.reduce_sum(attention_weights * lstm_out, axis=1)  # shape: (batch_size, lstm_units * 2)
        
        return context_vector

def build_attention_model(vocab_size, embedding_dim, max_seq_len, lstm_units):
    """
    Build a model with an attention layer for aspect-based sentiment analysis.
    
    Args:
        vocab_size (int): The size of the vocabulary.
        embedding_dim (int): The dimensionality of the embedding layer.
        max_seq_len (int): The maximum sequence length for input.
        lstm_units (int): The number of units in the LSTM layer.
    
    Returns:
        model (tf.keras.Model): The compiled Keras model.
    """
    # Input layers
    review_input = Input(shape=(max_seq_len,))
    aspect_input = Input(shape=(max_seq_len,))
    
    # Embedding layer
    embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)
    review_embedded = embedding_layer(review_input)
    aspect_embedded = embedding_layer(aspect_input)
    
    # Attention layer
    attention_layer = AttentionLayer(lstm_units)
    context_vector = attention_layer([review_embedded, aspect_embedded])
    
    # Fully connected layer
    dense_layer = Dense(64, activation='relu')(context_vector)
    output_layer = Dense(4, activation='softmax')(dense_layer)  # 4 classes for polarity

    # Model
    model = tf.keras.models.Model(inputs=[review_input, aspect_input], outputs=output_layer)
    return model




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
