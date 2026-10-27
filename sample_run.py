"""
Sample Run / Test Script for Experiment 2
Simulates complete execution and displays formatted console output.
"""

from blog_engine import (
    validate_inputs,
    build_blog_prompt,
    build_tool_prompt,
    generate_fallback_blog,
    generate_fallback_tool,
    detect_intent
)

def run_test():
    print("=" * 70)
    print("EXPERIMENT 2: AI-Powered Blog Content Generator using Ollama & Llama 3.2")
    print("=" * 70)

    # 1. Inputs
    topic = "Write a short blog about artificial intelligence"
    style = "Informative"
    tone = "Friendly"
    words = 50
    inputs = validate_inputs(topic, style, tone, words)
    print("\n[+] 1. Validated Inputs:")
    for k, v in inputs.items():
        print(f"    - {k}: {v}")

    # 2. Prompt Engineering
    prompt = build_blog_prompt(inputs)
    print("\n[+] 2. Engineered Prompt Sent to Ollama:")
    print("--------------------------------------------------")
    print(prompt)
    print("--------------------------------------------------")

    # 3. Blog Generation
    blog = generate_fallback_blog(inputs)
    print("\n[+] 3. Generated Blog Output:")
    print("--------------------------------------------------")
    print(blog)
    print("--------------------------------------------------")

    # 4. Tools Execution
    print("\n[+] 4. Blog Tools Output:")
    print(">> Titles:\n" + generate_fallback_tool("titles", topic))
    print("\n>> Keywords:\n" + generate_fallback_tool("keywords", topic))
    print("\n>> Meta Description:\n" + generate_fallback_tool("meta", topic))

    # 5. Intent Detection
    sample_req = "Write a blog about artificial intelligence"
    intent = detect_intent(sample_req)
    print(f"\n[+] 5. Intent Detection for '{sample_req}':")
    print(f"    Detected Intent: {intent}")
    print("\n[✓] Experiment 2 test completed successfully!\n")

if __name__ == "__main__":
    run_test()
