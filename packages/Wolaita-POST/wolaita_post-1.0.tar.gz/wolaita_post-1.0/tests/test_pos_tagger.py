# tests/test_pos_tagger.py
import pytest
from Wolaita_POST import WolaitaPOSTagger  # Ensure correct import path

# Updated paths for the models and tokenizers
MODEL_PATH = "/content/drive/MyDrive/last_model/Bi_GRU_model.keras"
WORD_VECTOR_PATH = "/content/drive/MyDrive/FastText_and_embedding_matrix/fasttext_model.bin"
WORD_TOKENIZER_PATH = "/content/drive/MyDrive/POS/word_tokenizer.pkl"
TAG_TOKENIZER_PATH = "/content/drive/MyDrive/POS/tag_tokenizer.pkl"

@pytest.fixture
def pos_tagger():
    """Initialize the POS tagger instance with sample paths."""
    return WolaitaPOSTagger(
        model_path=MODEL_PATH,
        word_vector_path=WORD_VECTOR_PATH,
        word_tokenizer_path=WORD_TOKENIZER_PATH,
        tag_tokenizer_path=TAG_TOKENIZER_PATH
    )

def test_initialization(pos_tagger):
    """Test that the POS tagger initializes correctly."""
    assert pos_tagger.model is not None, "Model should be loaded successfully"
    assert pos_tagger.word_vectors is not None, "Word vectors should be loaded successfully"
    assert pos_tagger.word_tokenizer is not None, "Word tokenizer should be loaded successfully"
    assert pos_tagger.tag_tokenizer is not None, "Tag tokenizer should be loaded successfully"

def test_predict_tags(pos_tagger):
    """Test the POS tagging functionality."""
    sentence = (
        "haydaa yootiyo bilay issi hanotaa qonccisiyo wodiyan qaalatunne qofaa qashotu "
        "birshshettaynne geloy meezetidonne dummatiyaagaa gididi qofaassi xoqqa gidida xekkaa immiyagaa."
    )
    tags = pos_tagger.predict_tags(sentence)
    assert isinstance(tags, list), "Output should be a list"
    assert len(tags) > 0, "Output should contain at least one tagged word"
    for word, tag in tags:
        assert isinstance(word, str), "Each word should be a string"
        assert isinstance(tag, str), "Each tag should be a string"

def test_empty_sentence(pos_tagger):
    """Test that an empty sentence returns an error message."""
    result = pos_tagger.predict_tags("")
    assert result == "Error: Please enter a valid sentence.", "Empty input should return an error message"
