# **HubNLP Documentation**

### **Introduction**
HubNLP is a simple, user-friendly NLP utility library designed to make NLP tasks easier and more accessible. It includes functions for Named Entity Recognition (NER), word feature extraction, attention-based models, and more.

---

## **Installation**
You can install HubNLP via pip:

```bash
pip install HubNLP
```

---

## **Functions and Features**

### 1. **`print_developer_info()`**
Prints the information about the developer of the library.

#### **Usage**:
```python
from HubNLP import print_developer_info

print_developer_info()
```

#### **Output**:
```
Developer: Self-nasu
Library: HubNLP
Email: nexiotech.2024@gmail.com
```

---

### 2. **`print_library_tagline()`**
Prints the tagline or description of the library.

#### **Usage**:
```python
from HubNLP import print_library_tagline

print_library_tagline()
```

#### **Output**:
```
HubNLP - A simple NLP utility library
```

---

### 3. **`load_ner_data(file_path)`**
Loads NER data in CoNLL format (which includes words, part-of-speech tags, and NER tags).

#### **Arguments**:
- `file_path` (str): The path to the CoNLL format text file.

#### **Returns**:
A list of sentences, where each sentence is represented as a list of tuples `(word, pos, ner)`.

#### **Usage**:
```python
from HubNLP import load_ner_data

file_path = "path/to/conll_file.txt"
sentences = load_ner_data(file_path)

print(sentences)
```

#### **Example Output**:
```python
[[("John", "NNP", "B-PER"), ("Smith", "NNP", "I-PER")],
 ["London", "NNP", "B-LOC"]]
```

---

### 4. **`extract_word_features(sentence, index)`**
Extracts features for a specific word in a sentence for NLP tasks (e.g., NER or POS tagging).

#### **Arguments**:
- `sentence` (list): A list of tuples representing a sentence, where each tuple contains `(word, POS, [optional] NER tag)`.
- `index` (int): The index of the word in the sentence for which features are to be extracted.

#### **Returns**:
A dictionary containing features for the word.

#### **Usage**:
```python
from HubNLP import extract_word_features

sentence = [("John", "NNP"), ("is", "VBZ"), ("running", "VBG")]
features = extract_word_features(sentence, 2)

print(features)
```

#### **Example Output**:
```python
{
    'word': 'running',
    'postag': 'VBG',
    'is_upper': False,
    'is_title': False,
    'is_digit': False,
    '-1:word': 'is',
    '-1:postag': 'VBZ',
    'BOS': False,
    '+1:word': '',
    '+1:postag': '',
    'EOS': True
}
```

---

### 5. **`AttentionLayer` Class**
Defines a custom attention layer that applies a Bi-directional LSTM followed by an attention mechanism.

#### **Usage**:
```python
from HubNLP import AttentionLayer
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Bidirectional, LSTM

# Example to use AttentionLayer
class CustomModel(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, max_seq_len, lstm_units):
        super(CustomModel, self).__init__()
        self.embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)
        self.attention_layer = AttentionLayer(lstm_units)
        self.dense = Dense(64, activation='relu')
        self.output_layer = Dense(4, activation='softmax')  # For 4-class classification
    
    def call(self, inputs):
        review_input, aspect_input = inputs
        review_embedded = self.embedding(review_input)
        aspect_embedded = self.embedding(aspect_input)
        context_vector = self.attention_layer([review_embedded, aspect_embedded])
        x = self.dense(context_vector)
        return self.output_layer(x)
```

---

### 6. **`build_attention_model(vocab_size, embedding_dim, max_seq_len, lstm_units)`**
Builds a model architecture with an attention mechanism for tasks like aspect-based sentiment analysis.

#### **Arguments**:
- `vocab_size` (int): The size of the vocabulary.
- `embedding_dim` (int): The dimensionality of the embedding layer.
- `max_seq_len` (int): The maximum sequence length for input.
- `lstm_units` (int): The number of units in the Bi-directional LSTM layer.

#### **Returns**:
A compiled Keras model.

#### **Usage**:
```python
from HubNLP import build_attention_model

vocab_size = 5000  # Size of the vocabulary
embedding_dim = 128  # Dimensionality of embeddings
max_seq_len = 100  # Max sequence length
lstm_units = 64  # Number of LSTM units

model = build_attention_model(vocab_size, embedding_dim, max_seq_len, lstm_units)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()
```

---

## **Additional Notes**
- The library is designed to work with **TensorFlow** and **Keras** for neural network-based models, and the functions can be used independently or together for various NLP tasks.
- If you're using the attention-based models, make sure that you have **TensorFlow** installed in your environment:
  ```bash
  pip install tensorflow
  ```

---

## **Conclusion**
HubNLP provides a range of utilities that make it easy to handle tasks like NER, feature extraction, and building attention-based models for sentiment analysis. With its simple API, you can integrate these functionalities into your own projects with minimal effort.