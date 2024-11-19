from transformers import pipeline

qa_pipeline_bert = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
qa_pipeline_distilbert = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def answer_question_bert(context, question):
    result = qa_pipeline_bert(question=question, context=context)
    return result["answer"]

def answer_question_distilbert(context, question):
    result = qa_pipeline_distilbert(question=question, context=context)
    return result["answer"]

def answer_question(context, question, method="bert"):
    if method == "bert":
        return answer_question_bert(context, question)
    elif method == "distilbert":
        return answer_question_distilbert(context, question)
    else:
        raise ValueError("Invalid method specified. Choose from 'bert' or 'distilbert'.")
