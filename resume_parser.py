import pdfplumber
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_keywords(text):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]
    return list(set(keywords))
