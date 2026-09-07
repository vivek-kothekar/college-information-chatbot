import os
import uuid
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from knowledge_base import KnowledgeBase
from gemini_service import GeminiService

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize Local Knowledge Base and Gemini Service
kb = KnowledgeBase()
gemini_service = GeminiService(kb)

@app.route("/")
def index():
    """Renders the main chatbot interactive interface."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main Chat API Endpoint.
    Accepts: { "message": "...", "session_id": "..." (optional) }
    Returns: { "answer": "...", "sources": [{"title": "...", "url": "..."}], "session_id": "..." }
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "").strip() or str(uuid.uuid4())

    if not message:
        return jsonify({
            "error": "Empty message provided.",
            "answer": "Please enter a question about SBJITMR.",
            "sources": []
        }), 400

    try:
        response = gemini_service.answer_query(message, session_id=session_id)
        return jsonify(response)
    except Exception as e:
        print(f"Error handling /api/chat: {e}")
        return jsonify({
            "answer": "An unexpected error occurred while processing your request. Please try again or visit https://www.sbjit.edu.in/",
            "sources": [{"title": "Official SBJITMR Website", "url": "https://www.sbjit.edu.in/"}],
            "session_id": session_id
        }), 500

@app.route("/api/clear", methods=["POST"])
def clear_chat():
    """Resets memory for a specific session."""
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "").strip()
    if session_id:
        gemini_service.clear_session(session_id)
    return jsonify({"status": "cleared", "session_id": session_id})

@app.route("/api/health", methods=["GET"])
def health():
    """Status endpoint reporting Knowledge Base and Gemini connectivity."""
    return jsonify({
        "status": "healthy",
        "knowledge_base_files_loaded": len(kb.data),
        "gemini_api_configured": bool(gemini_service.client),
        "institute": "S. B. Jain Institute of Technology, Management & Research, Nagpur"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"Starting SBJITMR AI Chatbot on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
