from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
import yake

from nltk.corpus import stopwords

kw_model = KeyBERT()
stop_words = stopwords.words("english")

def extract_keywords_keybert(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
    return [kw[0] for kw in keywords]

def extract_keywords_tfidf(text, top_n=5):
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=100)
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [word for word, score in sorted_scores[:top_n]]

def extract_keywords_yake(text, top_n=5):
    yake_extractor = yake.KeywordExtractor(lan="en", n=2, top=top_n)
    keywords = yake_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def extract_keywords(text, method="keybert"):
    if method == "keybert":
        return extract_keywords_keybert(text)
    elif method == "tfidf":
        return extract_keywords_tfidf(text)
    elif method == "yake":
        return extract_keywords_yake(text)
    else:
        raise ValueError("Invalid method specified. Choose from 'keybert', 'tfidf', or 'yake'.")
