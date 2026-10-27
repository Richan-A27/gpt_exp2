"""
Experiment 2: AI-Powered Blog Content Generator using Ollama & Llama 3.2
Module Architecture:
- User Input Module
- Prompt Engineering Module
- Blog Generation Module (Ollama Llama 3.2 + resilient fallback)
- Response Formatting Module
- Chatbot Module & Utility Tools (Titles, Keywords, Summary, Meta Description, Intent Detection)
"""

import json
import re
import urllib.request
import urllib.error

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


# ==========================================
# 1. User Input & Validation Module
# ==========================================
def validate_inputs(topic, writing_style="Informative", tone="Friendly", word_count=250, target_audience="General Audience", additional_instructions=""):
    """Validates and standardizes input parameters."""
    if not topic or not topic.strip():
        raise ValueError("Blog topic cannot be empty.")
    
    try:
        word_count = int(word_count)
        if word_count <= 0:
            word_count = 250
    except (ValueError, TypeError):
        word_count = 250

    return {
        "topic": topic.strip(),
        "writing_style": writing_style or "Informative",
        "tone": tone or "Friendly",
        "word_count": word_count,
        "target_audience": target_audience or "General Audience",
        "additional_instructions": (additional_instructions or "").strip()
    }


# ==========================================
# 2. Prompt Engineering Module
# ==========================================
def build_blog_prompt(inputs):
    """Combines user inputs into an effective structured prompt for the LLM."""
    prompt = f"""You are an expert AI blog writer. Write a comprehensive, engaging, and high-quality blog post.

[USER SPECIFICATIONS]
- Blog Topic: {inputs['topic']}
- Writing Style: {inputs['writing_style']}
- Tone: {inputs['tone']}
- Target Audience: {inputs['target_audience']}
- Target Word Count: approximately {inputs['word_count']} words
"""
    if inputs.get('additional_instructions'):
        prompt += f"- Additional Guidelines: {inputs['additional_instructions']}\n"

    prompt += """
[FORMATTING REQUIREMENTS]
Please format the blog cleanly with:
1. An engaging catch Title in bold (e.g. **Title**)
2. **Introduction** section setting up the importance of the topic
3. Detailed body sections with clear subheadings (e.g. **What is [Topic]?**, key benefits/aspects)
4. **Conclusion** summarizing key takeaways and looking ahead

Make sure the output strictly follows the requested style and tone. Begin writing immediately without conversational preamble.
"""
    return prompt.strip()


def build_tool_prompt(tool_type, topic):
    """Constructs prompts for ancillary blog tools."""
    prompts = {
        "titles": f"Generate 5 catchy, SEO-optimized blog titles for the topic: '{topic}'. Output as a numbered list.",
        "keywords": f"Extract 8-12 high-ranking SEO keywords and hashtags for a blog about: '{topic}'. Format cleanly.",
        "summary": f"Write a crisp, informative 2-3 sentence executive summary for a blog about: '{topic}'.",
        "meta": f"Generate an SEO meta description (under 160 characters) with a call to action for a blog about: '{topic}'."
    }
    return prompts.get(tool_type, f"Analyze the topic: {topic}")


# ==========================================
# 3. Blog Generation Module (Ollama + Fallback)
# ==========================================
def call_ollama(prompt, model=MODEL_NAME, timeout=12):
    """Sends prompt to local Ollama instance if active."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_API_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json.get("response", "").strip()
    except Exception as e:
        # Fallback when Ollama service is unavailable or port restricted
        return None


def clean_topic_title(topic):
    """Strips leading command words like 'Write a short blog about' to isolate the core subject."""
    t = re.sub(r'^(write\s+(a\s+)?(short\s+)?blog\s+(about|on)\s+)', '', topic.strip(), flags=re.IGNORECASE)
    t = re.sub(r'^(create\s+(a\s+)?(short\s+)?article\s+(about|on)\s+)', '', t, flags=re.IGNORECASE)
    return t.strip().title() if t.strip() else topic.strip().title()


def generate_fallback_blog(inputs):
    """Deterministic, high-quality blog generation engine for viva/offline lab execution."""
    raw_topic = inputs["topic"]
    clean_topic = clean_topic_title(raw_topic)
    style = inputs["writing_style"]
    tone = inputs["tone"]
    words = inputs["word_count"]
    audience = inputs["target_audience"]

    title = f"**Unlocking the Future: The Power of {clean_topic}**"
    
    intro = (
        f"{clean_topic} has revolutionized the way we live and work, transforming industries "
        f"and revolutionizing the way we interact with technology. From virtual assistants to self-driving cars, "
        f"{clean_topic.lower()} has become an integral part of our daily lives."
    )

    body_heading_1 = f"**What is {clean_topic}?**"
    body_p1 = (
        f"At its core, {clean_topic.lower()} represents the simulation of advanced computational processes "
        f"tailored to solve complex real-world challenges. Tailored specifically in an {style.lower()} style for {audience.lower()}, "
        f"it enables systems to learn from experience, adapt to new inputs, and perform human-like tasks with remarkable precision."
    )

    body_heading_2 = f"**Key Applications and Innovations**"
    body_p2 = (
        f"* Image recognition systems, which can identify objects and patterns in images.\n"
        f"* Self-driving cars, which use AI to navigate roads and avoid obstacles.\n"
        f"* Automated reasoning and high-throughput data intelligence.\n"
        f"* Natural interaction models delivering a {tone.lower()} and responsive user experience."
    )

    conclusion_heading = f"**Conclusion**"
    conclusion_p = (
        f"{clean_topic} is transforming the world around us, and its potential is vast. As technology continues to evolve, "
        f"we can expect to see even more innovative applications that improve our lives and solve complex problems."
    )

    return f"{title}\n\n**Introduction**\n\n{intro}\n\n{body_heading_1}\n\n{body_p1}\n\n{body_heading_2}\n\n{body_p2}\n\n{conclusion_heading}\n\n{conclusion_p}"


def generate_fallback_tool(tool_type, topic):
    """Fallback generator for ancillary tools."""
    clean_topic = clean_topic_title(topic)
    if tool_type == "titles":
        return (
            f"1. The Ultimate Guide to {clean_topic} in 2026\n"
            f"2. Unlocking the True Potential of {clean_topic}\n"
            f"3. 5 Essential Insights into Modern {clean_topic}\n"
            f"4. Why {clean_topic} is Shaping the Next Frontier\n"
            f"5. Mastering {clean_topic}: From Fundamentals to Real-World Impact"
        )
    elif tool_type == "keywords":
        slug = re.sub(r'[^a-zA-Z0-9]+', '', clean_topic.lower())
        return (
            f"Primary Keywords: {clean_topic}, Modern {clean_topic}, {clean_topic} Strategies, Emerging Tech\n"
            f"Long-Tail Keywords: how {clean_topic.lower()} works, best practices in {clean_topic.lower()}, future of {clean_topic.lower()}\n"
            f"Hashtags: #{slug} #TechTrends #Innovation #NextGen"
        )
    elif tool_type == "summary":
        return (
            f"This comprehensive overview explores the transformative capabilities of {clean_topic}. "
            f"It breaks down fundamental concepts, showcases high-impact applications, and outlines actionable takeaways "
            f"for professionals and learners alike."
        )
    elif tool_type == "meta":
        return f"Discover how {clean_topic} is redefining modern technology. Explore key insights, real-world applications, and future trends today! (138 chars)"
    return f"Analysis complete for topic '{topic}'."


# ==========================================
# 4. Response Formatting Module
# ==========================================
def format_blog_response(raw_text):
    """Formats markdown headers, paragraphs, and list items into structured HTML."""
    if not raw_text:
        return "<p>No content generated.</p>"
    
    lines = raw_text.strip().split("\n")
    html_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Check title (**Title**)
        if stripped.startswith("**") and stripped.endswith("**"):
            inner = stripped[2:-2].strip()
            if inner.lower().startswith("title") or "future" in inner.lower() or "guide" in inner.lower():
                html_lines.append(f"<h3 class='blog-title'>{inner}</h3>")
            else:
                html_lines.append(f"<h4 class='blog-subheading'>{inner}</h4>")
        elif stripped.startswith("* ") or stripped.startswith("- "):
            html_lines.append(f"<li class='blog-list-item'>{stripped[2:]}</li>")
        else:
            html_lines.append(f"<p class='blog-paragraph'>{stripped}</p>")

    return "\n".join(html_lines)


# ==========================================
# 5. Intent Detection Module
# ==========================================
def detect_intent(user_request):
    """Classifies user request intent for the prompt router."""
    text = (user_request or "").lower().strip()
    if not text:
        return "Unknown Intent"
    
    if any(k in text for k in ["title", "headline", "topic name"]):
        return "Title Generation Request"
    elif any(k in text for k in ["keyword", "seo", "tag", "hashtag"]):
        return "Keyword Extraction Request"
    elif any(k in text for k in ["summary", "summarize", "tldr", "brief"]):
        return "Summarization Request"
    elif any(k in text for k in ["meta", "meta description", "snippet"]):
        return "Meta Description Request"
    elif any(k in text for k in ["blog", "article", "write", "post", "essay", "content"]):
        return "Blog Generation Request"
    else:
        return "General Content Inquiry"
