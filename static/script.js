document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const chatHistory = document.getElementById("chatHistory");
  const typingIndicator = document.getElementById("typingIndicatorRow");
  const clearChatBtn = document.getElementById("clearChatBtn");
  const categoryChips = document.querySelectorAll(".category-chip");
  const suggestedScroll = document.getElementById("suggestedPillsScroll");

  // Session ID Management
  let sessionId = sessionStorage.getItem("sbjit_session_id");
  if (!sessionId) {
    sessionId = "sbjit_" + Math.random().toString(36).substring(2, 11) + "_" + Date.now();
    sessionStorage.setItem("sbjit_session_id", sessionId);
  }

  // Category to Suggested Questions Mapping
  const categoryQuestions = {
    all: [
      "Who is the Principal?",
      "Who is the Dean Academics?",
      "What is the admission process?",
      "What are the fees?",
      "Tell me about placements.",
      "Who is the CSE HOD?",
      "What scholarships are available?",
      "Is transport available?",
      "Where can I check results?",
      "What is the vision and mission?"
    ],
    administration: [
      "Who is the Principal?",
      "Who is the CEO?",
      "Who is the Dean Academics?",
      "Who is the Dean Students Affairs?",
      "Who is the Dean Engineering?",
      "Who is the Registrar?",
      "Who is the Controller of Examination?"
    ],
    admissions: [
      "What is the admission process?",
      "What are the eligibility criteria for B.Tech?",
      "What are the fees?",
      "What is the DTE Code for SBJITMR?",
      "What documents are required for admission?",
      "Give me admission helpline contact numbers."
    ],
    departments: [
      "What departments are available?",
      "What courses are offered?",
      "Who is the CSE HOD?",
      "What is the CSE AI & ML department?",
      "What is the Data Science department?",
      "What is the MBA department?"
    ],
    examinations: [
      "Where can I check results?",
      "Where can I find exam timetable?",
      "Who is the Controller of Examination?",
      "What is the CGPA to percentage conversion formula?",
      "What is the revaluation process?"
    ],
    placements: [
      "Tell me about placements.",
      "What is the highest and average package?",
      "Who are the recruiters?",
      "Who is the TPO?",
      "What placement training is provided?"
    ],
    student_affairs: [
      "What student activities are available?",
      "Tell me about NSS.",
      "Tell me about NCC.",
      "What sports facilities are available?",
      "Tell me about Technotsav and Manthan."
    ],
    facilities: [
      "Tell me about the library.",
      "Who is the librarian?",
      "Is transport available?",
      "Tell me about the buses.",
      "What campus facilities are available?"
    ],
    contact: [
      "What is the official contact number?",
      "What is the official email?",
      "Where is SBJITMR located?",
      "When was SBJITMR established?",
      "What is the official website?"
    ]
  };

  // Update Suggested Question Pills
  function updateSuggestedQuestions(category) {
    const questions = categoryQuestions[category] || categoryQuestions.all;
    suggestedScroll.innerHTML = "";
    questions.forEach(q => {
      const btn = document.createElement("button");
      btn.className = "suggested-pill";
      btn.setAttribute("data-query", q);
      btn.textContent = q;
      btn.addEventListener("click", () => {
        chatInput.value = q;
        submitMessage();
      });
      suggestedScroll.appendChild(btn);
    });
  }

  // Category Chip Clicks
  categoryChips.forEach(chip => {
    chip.addEventListener("click", () => {
      categoryChips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      const category = chip.getAttribute("data-category");
      updateSuggestedQuestions(category);
    });
  });

  // Attach click to default suggested pills
  document.querySelectorAll(".suggested-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      chatInput.value = pill.getAttribute("data-query");
      submitMessage();
    });
  });

  // Auto-resize chat textarea
  chatInput.addEventListener("input", () => {
    chatInput.style.height = "auto";
    chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + "px";
  });

  // Enter to send, Shift+Enter for newline
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitMessage();
    }
  });

  // Form submit
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    submitMessage();
  });

  // Clear chat button
  clearChatBtn.addEventListener("click", async () => {
    if (confirm("Are you sure you want to clear this conversation?")) {
      try {
        await fetch("/api/clear", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId })
        });
      } catch (err) {
        console.warn("Clear session error:", err);
      }
      
      // Reset DOM to only welcome message
      const welcome = document.getElementById("welcomeMessageRow");
      chatHistory.innerHTML = "";
      if (welcome) {
        chatHistory.appendChild(welcome);
      }
      chatInput.value = "";
      chatInput.style.height = "auto";
      chatInput.focus();
    }
  });

  // Submit Message Handler
  async function submitMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Reset input
    chatInput.value = "";
    chatInput.style.height = "auto";
    sendBtn.disabled = true;

    // Append User Message
    appendUserMessage(text);

    // Show Typing Indicator & Scroll
    showTyping(true);
    scrollToBottom();

    // Helper for fetch with 1 auto-retry on 502/503/network error
    async function executeChatRequest(isRetry = false) {
      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, session_id: sessionId })
        });

        // If Render is starting up (502 / 503 / 504), wait and auto-retry once
        if ((response.status === 502 || response.status === 503 || response.status === 504) && !isRetry) {
          console.warn("Render service is spinning up, auto-retrying in 3 seconds...");
          await new Promise(res => setTimeout(res, 3000));
          return await executeChatRequest(true);
        }

        let data = null;
        try {
          data = await response.json();
        } catch (jsonErr) {
          console.warn("Non-JSON response received:", jsonErr);
        }

        showTyping(false);

        if (response.ok && data && data.answer) {
          appendBotMessage(data.answer, data.sources || []);
        } else if (response.status === 502 || response.status === 503 || response.status === 504) {
          appendBotMessage(
            "⏳ **Server is waking up:** On Render's free tier, the application sleeps after inactivity and takes 30–60 seconds to spin up. The server is now warming up—please resend your question in a few seconds!",
            [{ title: "Official SBJITMR Website", url: "https://www.sbjit.edu.in/" }]
          );
        } else {
          appendBotMessage(
            (data && data.answer) || "I encountered an issue retrieving the information. Please check the official website at https://www.sbjit.edu.in/",
            (data && data.sources) || [{ title: "Official SBJITMR Website", url: "https://www.sbjit.edu.in/" }]
          );
        }
      } catch (error) {
        console.error("Chat error:", error);
        if (!isRetry) {
          console.warn("Network glitch, auto-retrying once in 2 seconds...");
          await new Promise(res => setTimeout(res, 2000));
          return await executeChatRequest(true);
        }
        showTyping(false);
        appendBotMessage(
          "⏳ **Server Connection Notice:** The backend service may still be spinning up from its initial deployment or free-tier sleep. Please refresh the page or try your question again in 15 seconds.",
          [{ title: "Official SBJITMR Website", url: "https://www.sbjit.edu.in/" }]
        );
      } finally {
        sendBtn.disabled = false;
        chatInput.focus();
        scrollToBottom();
      }
    }

    await executeChatRequest();
  }

  // Append User Bubble
  function appendUserMessage(text) {
    const timeStr = getCurrentTime();
    const row = document.createElement("div");
    row.className = "message-row user-row";
    row.innerHTML = `
      <div class="avatar user-avatar">
        <i class="fa-solid fa-user"></i>
      </div>
      <div class="message-content">
        <div class="message-bubble user-bubble">
          <p>${escapeHtml(text)}</p>
        </div>
        <div class="message-time">${timeStr}</div>
      </div>
    `;
    chatHistory.appendChild(row);
  }

  // Append Bot Bubble with Markdown Parsing and Source Pills
  function appendBotMessage(markdownText, sources) {
    const timeStr = getCurrentTime();
    const formattedHtml = parseMarkdown(markdownText);
    
    const row = document.createElement("div");
    row.className = "message-row bot-row";
    
    let sourcesHtml = "";
    if (sources && sources.length > 0) {
      const pills = sources.map(s => {
        const title = s.title || "Official Source";
        const url = s.url || "https://www.sbjit.edu.in/";
        return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer" class="source-link-pill"><i class="fa-solid fa-link"></i> ${escapeHtml(title)}</a>`;
      }).join(" ");

      sourcesHtml = `
        <div class="source-box">
          <span class="source-title"><i class="fa-solid fa-circle-check"></i> Official Sources & References:</span>
          <div class="source-pills">
            ${pills}
          </div>
        </div>
      `;
    }

    row.innerHTML = `
      <div class="avatar bot-avatar">
        <i class="fa-solid fa-robot"></i>
      </div>
      <div class="message-content">
        <div class="message-header">
          <span class="author-name">SBJITMR Assistant</span>
          <span class="message-badge">Verified Source</span>
        </div>
        <div class="message-bubble bot-bubble">
          ${formattedHtml}
          ${sourcesHtml}
        </div>
        <div class="message-time">${timeStr}</div>
      </div>
    `;

    chatHistory.appendChild(row);
  }

  // Typing Indicator Toggle
  function showTyping(show) {
    if (show) {
      typingIndicator.classList.remove("hidden");
      chatHistory.appendChild(typingIndicator);
    } else {
      typingIndicator.classList.add("hidden");
    }
  }

  // Auto Scroll
  function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  // Helper: Format Time
  function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  // Helper: Escape HTML
  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Lightweight Markdown to HTML Parser
  function parseMarkdown(md) {
    if (!md) return "";

    let html = md;

    // Headings
    html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Blockquotes
    html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Inline Code
    html = html.replace(/`([^`]+)`/gim, '<code>$1</code>');

    // Links [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

    // Unordered Lists
    html = html.replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gims, '<ul>$1</ul>');
    // Deduplicate nested <ul> tags
    html = html.replace(/<\/ul>\s*<ul>/gim, '');

    // Paragraphs: split double newlines
    const paragraphs = html.split(/\n\n+/);
    html = paragraphs.map(p => {
      p = p.trim();
      if (!p) return "";
      if (p.startsWith("<h") || p.startsWith("<ul") || p.startsWith("<ol") || p.startsWith("<blockquote")) {
        return p;
      }
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join("");

    return html;
  }
});
