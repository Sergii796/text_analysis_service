from flask import Flask, request, jsonify, render_template
from config import Config
from services.keyword_extraction import extract_keywords
from services.entity_recognition import recognize_entities
from services.contextual_analysis import analyze_context
from services.sentiment_analysis import analyze_sentiment
from services.question_answering import answer_question

app = Flask(__name__)
app.config.from_object(Config)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "script-src 'self';"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/keyword_analysis")
def keyword_analysis():
    return render_template("keyword_analysis.html")

@app.route("/entity_recognition")
def entity_recognition():
    return render_template("entity_recognition.html")

@app.route("/contextual_analysis")
def contextual_analysis():
    return render_template("contextual_analysis.html")

@app.route("/sentiment_analysis")
def sentiment_analysis():
    return render_template("sentiment_analysis.html")

@app.route("/question_answering")
def question_answering():
    return render_template("question_answering.html")

@app.route("/analyze_keywords", methods=["GET", "POST"])
def analyze_keywords():
    if request.method == "POST":
        text = request.json.get("text")
        method = request.json.get("method", "keybert")
        keywords = extract_keywords(text, method=method)
        return jsonify({"keywords": keywords})
    else:
        return jsonify({"error": "This endpoint supports POST only."}), 405

@app.route("/recognize_entities", methods=["POST"])
def recognize_entities_endpoint():
    text = request.json.get("text")
    method = request.json.get("method", "spacy_en")
    entities = recognize_entities(text, method=method)
    return jsonify({"entities": entities})

@app.route("/contextual_analysis", methods=["POST"])
def contextual_analysis_api():
    try:
        text = request.json.get("text")
        method = request.json.get("method", "gpt2")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        context = analyze_context(text, method=method)
        return jsonify({"context": context})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sentiment_analysis", methods=["POST"])
def sentiment_analysis_api():
    text = request.json.get("text")
    method = request.json.get("method", "vader")
    sentiment = analyze_sentiment(text, method=method)
    return jsonify({"sentiment": sentiment})

@app.route("/question_answering", methods=["POST"])
def question_answering_api():
    text = request.json.get("text")
    question = request.json.get("question")
    method = request.json.get("method", "bert")

    if not text or not question:
        return jsonify({"error": "Both context and question are required."}), 400

    try:
        answer = answer_question(text, question, method=method)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
