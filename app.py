from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Keywords for scoring
market_keywords = ["market", "customers", "users", "audience", "niche", "industry", "consumers"]
monetize_keywords = ["sell", "subscription", "ads", "freemium", "commission", "pay", "revenue", "pricing"]
tech_keywords = ["app", "api", "website", "ai", "machine learning", "hardware", "blockchain", "saas"]
channels_keywords = ["seo", "ads", "facebook", "instagram", "tiktok", "partnership", "sales", "cold email"]
regulatory_keywords = ["health", "finance", "investment", "bank", "medical", "drugs", "legal", "insurance"]

def score_presence(text, keywords):
    text_l = text.lower()
    return sum(1 for k in keywords if k in text_l) / len(keywords)

def detect_red_flags(text):
    text_l = text.lower()
    return [k for k in regulatory_keywords if k in text_l]

def evaluate_idea(text):
    market = score_presence(text, market_keywords)
    monetize = score_presence(text, monetize_keywords)
    tech = score_presence(text, tech_keywords)
    channels = score_presence(text, channels_keywords)
    red_flags = detect_red_flags(text)

    score = (0.30 * market + 0.25 * monetize + 0.20 * channels + 0.15 * tech) * 100
    score -= 15 * len(red_flags)
    score = max(0, min(100, round(score)))

    if score >= 70:
        verdict = "Good idea — promising"
    elif score >= 40:
        verdict = "Questionable — needs validation"
    else:
        verdict = "High risk / early concept — substantial doubts"

    pros, cons = [], []
    if market > 0.2: pros.append("Target market or customers mentioned.")
    else: cons.append("Market / customers not clearly described.")
    if monetize > 0.2: pros.append("Potential revenue model suggested.")
    else: cons.append("Monetization path unclear.")
    if channels > 0.2: pros.append("Acquisition channels mentioned.")
    else: cons.append("Customer acquisition plan not described.")
    if tech > 0.2: pros.append("Technical approach indicated.")
    else: cons.append("Technical complexity not addressed.")
    if red_flags: cons.append("Regulatory concerns: " + ", ".join(red_flags))

    steps = [
        "Write a one-sentence value proposition (who + problem + solution).",
        "Define your target customer and top 3 acquisition channels."
    ]
    if monetize <= 0.2: steps.append("Sketch at least one revenue model.")
    if market <= 0.2: steps.append("Do quick customer interviews to validate demand.")
    if tech > 0.7: steps.append("Prototype an MVP to test technical assumptions.")

    return {
        "score": score,
        "verdict": verdict,
        "pros": pros,
        "cons": cons,
        "risks": red_flags if red_flags else ["No immediate regulatory flags detected."],
        "next_steps": steps
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    idea = data.get("idea", "").strip()
    if not idea:
        return jsonify({"error": "Please enter a business idea"}), 400
    return jsonify(evaluate_idea(idea))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
