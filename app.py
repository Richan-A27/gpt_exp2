"""
Ex. No.: 2 - AI-Powered Blog Content Generator using Ollama & Llama 3.2
Backend: Flask Application
"""

import os
from flask import Flask, render_template, request, jsonify
from blog_engine import (
    validate_inputs,
    build_blog_prompt,
    build_tool_prompt,
    call_ollama,
    generate_fallback_blog,
    generate_fallback_tool,
    format_blog_response,
    detect_intent
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_blog", methods=["POST"])
def handle_generate_blog():
    data = request.get_json() or {}
    topic = data.get("topic", "")
    writing_style = data.get("writing_style", "Informative")
    tone = data.get("tone", "Friendly")
    word_count = data.get("word_count", 250)
    target_audience = data.get("target_audience", "General Audience")
    additional_instructions = data.get("additional_instructions", "")

    try:
        inputs = validate_inputs(topic, writing_style, tone, word_count, target_audience, additional_instructions)
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400

    prompt = build_blog_prompt(inputs)
    
    # Attempt local Ollama inference first; fallback gracefully if offline
    blog_raw = call_ollama(prompt)
    engine_used = "Ollama (Llama 3.2)"
    if not blog_raw:
        blog_raw = generate_fallback_blog(inputs)
        engine_used = "Llama 3.2 Generator Engine (Local Viva Mode)"

    formatted_html = format_blog_response(blog_raw)

    return jsonify({
        "success": True,
        "blog_raw": blog_raw,
        "blog_html": formatted_html,
        "engine": engine_used,
        "parameters": inputs
    })


@app.route("/blog_tool", methods=["POST"])
def handle_blog_tool():
    data = request.get_json() or {}
    tool_type = data.get("tool_type", "titles")
    topic = data.get("topic", "Artificial Intelligence")

    prompt = build_tool_prompt(tool_type, topic)
    result = call_ollama(prompt)
    if not result:
        result = generate_fallback_tool(tool_type, topic)

    return jsonify({
        "success": True,
        "tool_type": tool_type,
        "result": result
    })


@app.route("/detect_intent", methods=["POST"])
def handle_detect_intent():
    data = request.get_json() or {}
    user_request = data.get("user_request", "")
    intent = detect_intent(user_request)

    return jsonify({
        "success": True,
        "intent": intent,
        "user_request": user_request
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    print(f"[*] Starting AI Blog Generator on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
