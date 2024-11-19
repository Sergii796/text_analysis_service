async function fetchData(url, data) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error fetching data from ${url}:`, error);
        return { error: "An error occurred. Please try again later." };
    }
}

async function analyzeKeywords() {
    const text = document.getElementById("keyword_text").value.trim();
    const method = document.getElementById("keyword_method").value;

    if (!text) {
        document.getElementById("keyword_result").innerHTML = `<div class="result-box error">Please provide text for keyword analysis.</div>`;
        return;
    }

    const result = await fetchData("/analyze_keywords", { text, method });

    if (result.error) {
        document.getElementById("keyword_result").innerHTML = `<div class="result-box error">${result.error}</div>`;
    } else {
        const highlightedText = highlightKeywords(text, result.keywords);
        document.getElementById("keyword_result").innerHTML = `<div class="result-box"><p>Keywords Highlighted: ${highlightedText}</p></div>`;
    }
}

async function recognizeEntities() {
    const text = document.getElementById("entity_text").value.trim();
    const method = document.getElementById("entity_method").value;

    if (!text) {
        document.getElementById("entity_result").innerHTML = `<div class="result-box error">Please provide text for entity recognition.</div>`;
        return;
    }

    const result = await fetchData("/recognize_entities", { text, method });

    if (result.error) {
        document.getElementById("entity_result").innerHTML = `<div class="result-box error">${result.error}</div>`;
    } else {
        document.getElementById("entity_result").innerHTML = `<div class="result-box"><ul>${formatEntities(result.entities)}</ul></div>`;
    }
}

function formatEntities(entities) {
    return entities.map(entity => `<li><strong>${entity.label}:</strong> ${entity.text}</li>`).join("");
}

async function analyzeSentiment() {
    const text = document.getElementById("sentiment_text").value.trim();
    const method = document.getElementById("sentiment_method").value;

    if (!text) {
        document.getElementById("sentiment_result").innerHTML = `<div class="result-box error">Please provide text for sentiment analysis.</div>`;
        return;
    }

    const result = await fetchData("/sentiment_analysis", { text, method });

    if (result.error) {
        document.getElementById("sentiment_result").innerHTML = `<div class="result-box error">${result.error}</div>`;
    } else {
        document.getElementById("sentiment_result").innerHTML = `<div class="result-box">${formatSentiment(result.sentiment)}</div>`;
    }
}

function formatSentiment(sentiment) {
    return `
        <ul>
            <li><strong>Compound:</strong> ${sentiment.compound}</li>
            <li><strong>Negative:</strong> ${sentiment.negative}</li>
            <li><strong>Neutral:</strong> ${sentiment.neutral}</li>
            <li><strong>Positive:</strong> ${sentiment.positive}</li>
        </ul>
    `;
}

function formatContextualAnalysis(contextResults, method) {
    if (method === "gpt2") {
        return `<p><strong>Generated Text:</strong> ${contextResults}</p>`;
    } else if (method === "bert" || method === "roberta") {
        return `
            <ul>
                ${contextResults.map(result => `
                    <li><strong>Word:</strong> ${result.word} - 
                        <strong>Score:</strong> ${(result.score * 100).toFixed(2)}%</li>
                `).join("")}
            </ul>
        `;
    } else {
        return `<p>Error: Unsupported method selected.</p>`;
    }
}

async function contextualAnalysis() {
    const text = document.getElementById("context_text").value;
    const method = document.getElementById("context_method").value;

    if (!text) {
        document.getElementById("context_result").innerHTML = `
            <div class="result-box">Please enter text for analysis.</div>`;
        return;
    }

    try {
        const response = await fetch("/contextual_analysis", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, method })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Unknown server error");
        }

        const result = await response.json();
        document.getElementById("context_result").innerHTML = `
            <div class="result-box">${formatContextualAnalysis(result.context, method)}</div>`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("context_result").innerHTML = `
            <div class="result-box">Error: ${error.message}</div>`;
    }
}

async function answerQuestion() {
    const text = document.getElementById("qa_text").value.trim();
    const question = document.getElementById("question").value.trim();
    const method = document.getElementById("qa_method").value;

    if (!text || !question) {
        document.getElementById("qa_result").innerHTML = `<div class="result-box error">Please provide both context and question.</div>`;
        return;
    }

    try {
        const response = await fetch("/question_answering", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, question, method }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();

        if (result.error) {
            document.getElementById("qa_result").innerHTML = `<div class="result-box error">${result.error}</div>`;
        } else {
            document.getElementById("qa_result").innerHTML = `<div class="result-box"><strong>Answer:</strong> ${result.answer}</div>`;
        }
    } catch (error) {
        console.error("Error during question answering:", error);
        document.getElementById("qa_result").innerHTML = `<div class="result-box error">An error occurred. Please try again later.</div>`;
    }
}

function highlightKeywords(text, keywords) {
    let highlightedText = text;

    keywords.forEach(keyword => {
        const escapedKeyword = keyword.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
        const regex = new RegExp(`\\b${escapedKeyword}\\b`, 'gi');
        highlightedText = highlightedText.replace(regex, `<span class="keyword-highlight">${keyword}</span>`);
    });

    return highlightedText;
}

function toggleTheme() {
    const body = document.body;
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    }
}

function toggleNav() {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("show");
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
});
