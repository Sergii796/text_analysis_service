from transformers import pipeline

context_analyzer_bert = pipeline("fill-mask", model="bert-base-uncased")
context_analyzer_roberta = pipeline("fill-mask", model="roberta-base")
context_analyzer_gpt2 = pipeline("text-generation", model="gpt2")

def analyze_context_bert(text):
    masked_text = text.replace("[MASK]", "[MASK]")  
    results = context_analyzer_bert(masked_text)
    return [{"word": result["token_str"], "score": result["score"]} for result in results]

def analyze_context_roberta(text):
    masked_text = text.replace("[MASK]", "<mask>") 
    results = context_analyzer_roberta(masked_text)
    return [{"word": result["token_str"], "score": result["score"]} for result in results]

def analyze_context_gpt2(text):
    try:
        results = context_analyzer_gpt2(
            text,
            max_length=150,  
            temperature=0.7, 
            top_k=50,        
            top_p=0.9,      
            num_return_sequences=1
        )
        generated_text = results[0]["generated_text"]
        return remove_redundancy(generated_text)
    except Exception as e:
        raise RuntimeError(f"GPT-2 Error: {str(e)}")

def remove_redundancy(text):
    sentences = text.split(". ")
    seen_sentences = set()
    filtered_sentences = []

    for sentence in sentences:
        if sentence.lower() not in seen_sentences:
            filtered_sentences.append(sentence)
            seen_sentences.add(sentence.lower())

    return ". ".join(filtered_sentences)

def analyze_context(text, method="gpt2"):
    if method == "bert":
        return analyze_context_bert(text)
    elif method == "roberta":
        return analyze_context_roberta(text)
    elif method == "gpt2":
        return analyze_context_gpt2(text)
    else:
        raise ValueError("Invalid method specified. Choose from 'bert', 'roberta', or 'gpt2'.")
