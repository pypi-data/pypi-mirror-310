import json
from nltk.corpus import stopwords

# Load contraction mappings from a JSON file
def load_contraction_map(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Load custom stopwords from a text file
def load_custom_stopwords(custom_stopwords_path=None):
    # Load default stopwords
    stopword_list = set(stopwords.words('english'))

    # Exclude negation words
    stopword_list -= set(['not', 'no'])

    # Add custom stopwords
    if custom_stopwords_path:
        with open(custom_stopwords_path, 'r') as file:
            additional_stopwords = set(file.read().splitlines())
            stopword_list.update(additional_stopwords)

    return list(stopword_list)
