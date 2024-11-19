import nltk

nltk.data.path.append('C:/Users/teres/Documents/text_analysis_service/.venv/nltk_data')

nltk.download('punkt', download_dir='C:/Users/teres/Documents/text_analysis_service/.venv/nltk_data')

from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

context = "Albert Einstein was a theoretical physicist who developed the theory of relativity."
question = "Who developed the theory of relativity?"

result = qa_pipeline(question=question, context=context)
print(result["answer"])