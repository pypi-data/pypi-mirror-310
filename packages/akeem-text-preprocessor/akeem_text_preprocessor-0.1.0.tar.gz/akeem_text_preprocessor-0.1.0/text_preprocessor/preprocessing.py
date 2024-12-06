import re
import unicodedata
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Initialize tokenizer and lemmatizer
tokenizer = ToktokTokenizer()
lemmatizer = WordNetLemmatizer()

# Load NLTK's default stopwords
default_stopword_list = stopwords.words('english')


# Strip HTML tags
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    return re.sub(r'\s+', ' ', stripped_text).strip()


# Remove accented characters
def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')


# Remove special characters
def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
    return re.sub(pattern, '', text)


# Stopword removal
def remove_stopwords(text, stopword_list):
    tokens = tokenizer.tokenize(text)
    # Retain negations like 'not' and 'no'
    filtered_tokens = [word for word in tokens if word.lower() not in stopword_list or word.lower() in ["not", "no"]]
    return ' '.join(filtered_tokens)


# Lemmatize text
def lemmatize_text(text, use_pos_tagging=False):
    tokens = tokenizer.tokenize(text)
    if use_pos_tagging:
        from nltk import pos_tag
        pos_tags = pos_tag(tokens)
        pos_map = {'N': 'n', 'V': 'v', 'J': 'a', 'R': 'r'}  # Map to WordNet POS tags
        lemmatized = [lemmatizer.lemmatize(word, pos=pos_map.get(tag[0], 'n')) for word, tag in pos_tags]
    else:
        lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized)


# Main preprocessing function
def preprocess_text(text, html_stripping=True, accented_char_removal=True, lower_case=True,
                    special_char_removal=True, remove_digits=False, stopword_removal=True,
                    custom_stopwords=None, lemmatization=True, use_pos_tagging=False):
    """
    Comprehensive text preprocessing pipeline.
    """
    if html_stripping:
        text = strip_html_tags(text)
    if accented_char_removal:
        text = remove_accented_chars(text)
    if lower_case:
        text = text.lower()
    if special_char_removal:
        text = remove_special_characters(text, remove_digits)
    if stopword_removal:
        stopword_list = default_stopword_list if not custom_stopwords else custom_stopwords
        text = remove_stopwords(text, stopword_list)
    if lemmatization:
        text = lemmatize_text(text, use_pos_tagging)
    return text