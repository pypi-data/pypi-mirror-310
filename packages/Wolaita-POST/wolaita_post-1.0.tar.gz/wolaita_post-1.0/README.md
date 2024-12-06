# Wolaita_POST
## Overview
Wolaita_POST is a Python framework tailored for accurate Part-of-Speech (POS) tagging of the Wolaita language. Leveraging advanced deep learning models, including Bi-GRU and others, it integrates FastText embeddings to enhance tagging performance. The framework uses pretrained models, streamlining deployment and boosting accuracy. Designed for researchers and developers working with Natural Language Processing (NLP) in lesser-resourced languages, Wolaita_POST provides a robust solution for Wolaita language text analysis, making it a valuable tool in the NLP field.

## Features
- Accurate POS Tagging: Utilizes deep learning models (Bi-GRU, Bi-LSTM, etc.) to achieve precise Part-of-Speech tagging for Wolaita language text.
- Pretrained Models: Ready-to-use pretrained models for quick deployment and high accuracy.
- FastText Embeddings: Incorporates FastText word embeddings to capture subword information and improve performance on low-resource languages.
- Easy Integration: Simple API that allows researchers and developers to integrate POS tagging into their NLP pipelines.
- Supports Wolaita Language: Specifically designed for the Wolaita language, addressing the challenges of processing lesser-resourced languages.
- Customizable: Flexible configuration to accommodate different models, tokenizers, and word vectors based on project requirements.
- Efficient Deployment: Enables easy deployment for various NLP applications, such as machine translation and named entity recognition (NER).

## Installation
To install Wolaita_POST, you can use pip:
- pip install Wolaita_POST

##Usage

After installation, you can use Wolaita_POST as follows:
1. Import the package:

from Wolaita_POST import pos_tagger
2. Set file paths for your pretrained model, word vectors, and tokenizers:
- model_path = "/content/drive/MyDrive/POS/Bi_GRU_model.h5"  # Adjust if your model file has a different extension
- word_vector_path = "/content/drive/MyDrive/POS/fasttext_compatible.bin"
- word_tokenizer_path = "/content/drive/MyDrive/POS/wolaita_tokenizerX.pkl"
- tag_tokenizer_path = "/content/drive/MyDrive/POS/wolaita_tag_tokenizerY.pkl"

3. Initialize the POS tagger:

pos_tagger = WolaitaPOSTagger(
    model_path=model_path,
    word_vector_path=word_vector_path,
    word_tokenizer_path=word_tokenizer_path,
    tag_tokenizer_path=tag_tokenizer_path
)

4. Use the POS tagger to tag Wolaita text:

text = ['Insert your sample text here']

tagged_text = pos_tagger.tag(text)

print(tagged_text)

The tagged_text will contain the part-of-speech tags for the given Wolaita text.

##Running Tests
If you want to verify functionality, you can use pytest. Run this command in your project directory:

- !pytest /content/drive/MyDrive/Wolaita_POST/tests > test_report.txt

##License
This project is licensed under the MIT License. See the LICENSE file for more details.

##Contributing
Contributions are welcome! If you have suggestions for improving the package or find any issues, feel free to open a pull request or submit an issue on GitHub.

##Acknowledgements
Special thanks to the developers and researchers who contributed to this project, making it possible to expand NLP resources for the Wolaita language.

