import spacy
from transformers import pipeline

nlp_en = spacy.load("en_core_web_sm")
nlp_uk = spacy.load("uk_core_news_sm")  

ner_transformers = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def recognize_entities_spacy_en(text):
    doc = nlp_en(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

def recognize_entities_spacy_uk(text):
    doc = nlp_uk(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

def recognize_entities_transformers(text):
    entities = ner_transformers(text)
    return [{"text": entity["word"], "label": entity["entity"]} for entity in entities]

def recognize_entities(text, method="spacy_en"):
    if method == "spacy_en":
        return recognize_entities_spacy_en(text)
    elif method == "spacy_uk":
        return recognize_entities_spacy_uk(text)
    elif method == "transformers":
        return recognize_entities_transformers(text)
    else:
        raise ValueError("Invalid method specified. Choose from 'spacy_en', 'spacy_uk', or 'transformers'.")
