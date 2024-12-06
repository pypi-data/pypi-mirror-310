import pickle
import numpy as np
import tensorflow as tf
from nltk import word_tokenize
from keras.preprocessing.sequence import pad_sequences
import fasttext
import nltk

# Download required NLTK data
nltk.download('punkt')

# Constants
MAX_SEQ_LENGTH = 91

# /content/drive/MyDrive/Wolaita_POST/Wolaita_POST/wolaita_pos_tagger.py

class WolaitaPOSTagger: # This is line 15, where the class definition starts.
    """
    Wolaita Part-of-Speech Tagger using a pre-trained model.
    """
    # Add at least one indented statement within the class definition.
    # A simple `pass` statement is enough if the class has no content yet.
    pass  

    def __init__(self, model_path, word_vector_path, word_tokenizer_path, tag_tokenizer_path):
        # ... rest of your __init__ method ...
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as e:
            raise ValueError(f"Error loading model from {model_path}: {e}")

        # Load FastText model
        try:
            self.word_vectors = fasttext.load_model(word_vector_path)
        except Exception as e:
            raise ValueError(f"Error loading FastText model from {word_vector_path}: {e}")

        # Load tokenizers
        self.word_tokenizer = self._load_pickle(word_tokenizer_path, "word tokenizer")
        self.tag_tokenizer = self._load_pickle(tag_tokenizer_path, "tag tokenizer")

        # Reverse mappings for decoding predictions
        self.reverse_word_index = {v: k for k, v in self.word_tokenizer.word_index.items()}
        self.reverse_tag_index = {v: k for k, v in self.tag_tokenizer.word_index.items()}

        # Track Out-Of-Vocabulary (OOV) words
        self.oov_words = []

    def _load_pickle(self, file_path, file_type):
        """Helper method to load pickle files."""
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise ValueError(f"Error loading {file_type} from {file_path}: {e}")

    def _get_embedding(self, word):
        """
        Retrieve FastText embedding for a given word.
        Assigns random embedding for OOV words and tracks them.
        """
        if word in self.word_vectors:
            return self.word_vectors.get_word_vector(word)
        else:
            # Assign a random embedding and track the OOV word
            self.oov_words.append(word)
            return np.random.uniform(-0.1, 0.1, self.word_vectors.get_dimension())

    def predict_tags(self, sentence):
        """Predict Part-of-Speech tags for the input sentence."""
        if not sentence.strip():
            return "Error: Please enter a valid sentence."

        # Tokenize and encode the sentence
        tokenized_sentence = word_tokenize(sentence)
        encoded_sentence = [self.word_tokenizer.word_index.get(word, 0) for word in tokenized_sentence]
        X_Samp = pad_sequences([encoded_sentence], maxlen=MAX_SEQ_LENGTH, padding="post", value=0)

        # Predict tags using the model
        try:
            predictions = self.model.predict(X_Samp)
            predicted_tags = np.argmax(predictions, axis=-1)
        except Exception as e:
            return f"Error during prediction: {e}"

        # Generate word-tag pairs
        results = []
        for w, pred in zip(X_Samp[0], predicted_tags[0]):
            if w != 0:
                word = self.reverse_word_index.get(w, "UNK")
                tag = self.reverse_tag_index.get(pred, "UNK")
                results.append((word, tag))

        return results

    def get_embedding_matrix(self):
        """
        Generate the embedding matrix for the model using FastText embeddings.
        Logs OOV statistics and warnings if OOV percentage is high.
        """
        embedding_size = self.word_vectors.get_dimension()
        vocab_size = len(self.word_tokenizer.word_index) + 1
        embedding_matrix = np.zeros((vocab_size, embedding_size))

        for word, index in self.word_tokenizer.word_index.items():
            embedding_matrix[index] = self._get_embedding(word)

        # Calculate and log OOV statistics
        oov_percentage = len(self.oov_words) / vocab_size * 100
        print(f"Number of OOV words: {len(self.oov_words)}")
        print(f"OOV Percentage: {oov_percentage:.2f}%")
        if self.oov_words:
            print("Sample OOV words:", self.oov_words[:10])  # Display up to 10 OOV words

        # Warning for high OOV percentage
        if oov_percentage > 30.0:  # 30% threshold
            print("Warning: OOV percentage exceeds 30%. Consider reviewing tokenization or embeddings.")

        return embedding_matrix
