let currentBlogRaw = "";

async function generateBlog() {
  const topic = document.getElementById("topic").value.trim();
  const writing_style = document.getElementById("writing_style").value;
  const tone = document.getElementById("tone").value;
  const word_count = document.getElementById("word_count").value;
  const target_audience = document.getElementById("target_audience").value;

  if (!topic) {
    alert("Please enter a blog topic.");
    return;
  }

  const btn = document.getElementById("btn-generate-blog");
  const originalText = btn.innerHTML;
  btn.innerHTML = "⏳ Generating...";
  btn.disabled = true;

  try {
    const response = await fetch("/generate_blog", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: topic,
        writing_style: writing_style,
        tone: tone,
        word_count: word_count,
        target_audience: target_audience
      })
    });

    const data = await response.json();
    if (data.success) {
      currentBlogRaw = data.blog_raw;
      document.getElementById("blog-output").innerHTML = data.blog_html;
      document.getElementById("blog-output-container").style.display = "block";
      document.getElementById("blog-output-container").scrollIntoView({ behavior: "smooth" });
    } else {
      alert("Error: " + (data.error || "Generation failed"));
    }
  } catch (err) {
    console.error(err);
    alert("Request failed. Ensure the server is running.");
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
}

async function runTool(toolType) {
  const topic = document.getElementById("topic").value.trim() || "Artificial Intelligence";
  const container = document.getElementById("tool-output-container");
  const outputPre = document.getElementById("tool-output");
  const label = document.getElementById("tool-output-label");

  label.textContent = `Generated ${toolType.toUpperCase()} for: "${topic}"`;
  outputPre.textContent = "Processing tool request...";
  container.style.display = "block";

  try {
    const res = await fetch("/blog_tool", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool_type: toolType, topic: topic })
    });
    const data = await res.json();
    if (data.success) {
      outputPre.textContent = data.result;
    } else {
      outputPre.textContent = "Failed to run tool.";
    }
  } catch (err) {
    outputPre.textContent = "Error executing tool request.";
  }
}

async function detectUserIntent() {
  const userRequest = document.getElementById("intent_input").value.trim();
  if (!userRequest) {
    alert("Please enter a user request.");
    return;
  }

  const btn = document.getElementById("btn-detect-intent");
  btn.disabled = true;

  try {
    const res = await fetch("/detect_intent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_request: userRequest })
    });
    const data = await res.json();
    if (data.success) {
      document.getElementById("intent-badge").textContent = data.intent;
      document.getElementById("intent-output-container").style.display = "flex";
    }
  } catch (err) {
    alert("Intent detection failed.");
  } finally {
    btn.disabled = false;
  }
}

function copyBlog() {
  if (!currentBlogRaw) return;
  navigator.clipboard.writeText(currentBlogRaw).then(() => {
    alert("Blog content copied to clipboard!");
  }).catch(() => {
    alert("Failed to copy. Please copy manually.");
  });
}

function newChat() {
  document.getElementById("topic").value = "";
  document.getElementById("blog-output").innerHTML = "";
  document.getElementById("blog-output-container").style.display = "none";
  currentBlogRaw = "";
}

window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("demo") === "1" || params.get("autoload") === "1") {
    generateBlog();
    runTool("titles");
    detectUserIntent();
  }
});
