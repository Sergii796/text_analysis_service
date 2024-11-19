from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline

vader_analyzer = SentimentIntensityAnalyzer()
sentiment_transformers = pipeline("sentiment-analysis")

def analyze_sentiment_vader(text):
    sentiment = vader_analyzer.polarity_scores(text)
    return {
        "compound": sentiment["compound"],
        "negative": sentiment["neg"],
        "neutral": sentiment["neu"],
        "positive": sentiment["pos"]
    }

def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return {
        "compound": polarity,
        "negative": max(0, -polarity),
        "neutral": 1 - abs(polarity),
        "positive": max(0, polarity)
    }

def analyze_sentiment_transformers(text):
    result = sentiment_transformers(text)[0]
    label = result["label"].lower()
    score = result["score"]
    return {
        "compound": score if label == "positive" else -score if label == "negative" else 0,
        "negative": score if label == "negative" else 0,
        "neutral": score if label == "neutral" else 0,
        "positive": score if label == "positive" else 0
    }

def analyze_sentiment(text, method="vader"):
    if method == "vader":
        return analyze_sentiment_vader(text)
    elif method == "textblob":
        return analyze_sentiment_textblob(text)
    elif method == "transformers":
        return analyze_sentiment_transformers(text)
    else:
        raise ValueError("Invalid method specified. Choose from 'vader', 'textblob', or 'transformers'.")
