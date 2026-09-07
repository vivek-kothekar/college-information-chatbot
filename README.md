# 🎓 SBJITMR AI Assistant & Chatbot

> An intelligent, anti-hallucination conversational AI assistant for **S. B. Jain Institute of Technology, Management & Research (SBJITMR), Nagpur** (Autonomous, DTE Code: 4197, Affiliated to RTMNU, NAAC 'A' Grade).

---

## 🌟 Overview

The **SBJITMR AI Chatbot** delivers instant, authoritative answers regarding admissions, degree programs, faculty directories, fee structures, examination portals, placements, and campus facilities. It utilizes a **hybrid dual-layer architecture**:

1. **Instant Verified Knowledge Engine (<1ms):** Deterministically routes institutional queries to 17 curated, ground-truth JSON knowledge bases with exact source citations.
2. **Google Gemini Generative Layer:** Employs Google Gemini (`gemini-2.5-flash` / `gemini-1.5-flash`) grounded with an in-memory digest of all institutional data for natural language flexibility while preventing hallucinations.

---

## 🚀 Key Features

- **Authoritative Grounding:** Every verified answer includes links to official SBJITMR pages (`https://www.sbjit.edu.in/`).
- **Comprehensive Coverage across 17 Knowledge Modules:**
  - 🏛️ **College & Governance:** History (est. 2008), Sir Shantilal Badjate Trust, Governing Body, Academic Council.
  - 👨‍🏫 **Deans & Administration:** All deans (Academics, Student Affairs, R&D), CEO, Principal, Registrar.
  - 📚 **Departments & Intakes:** B.Tech (CSE 240, AI&ML 120, Data Science 120, ETC 60, EE 30, ME 30), BCA, MCA, MBA, M.Tech.
  - 📝 **Admissions & Lateral Entry:** First-Year B.Tech via MHT-CET/JEE, Direct Second Year (DSY) for diploma holders, required documents, CAP procedures, and helpline contacts.
  - 💰 **Fee Structure & NEFT:** Updated tuition and development fees across all categories and official bank transfer details.
  - 📊 **Examinations & Results:** Semester exam registration guidelines, revaluation policies, and direct links to the live result portal.
  - 💼 **Training & Placement:** Top recruiters (TCS, Infosys, Cognizant, Wipro, etc.), highest package, and placement cell contacts.
  - 🧑‍🎓 **Campus Life & Clubs:** NSS, NCC, Technotsav, Manthan, sports facilities, and bus transportation routes.
- **Fast, Responsive UI:** Pure Vanilla HTML5, CSS3, and JavaScript interface with interactive question chips, markdown rendering, and source badges.
- **100% Automated Test Suite:** 49 test cases verifying token overlap, department routing, edge-case safety, and API resilience.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask 3.0+
- **LLM Integration:** Google GenAI SDK (`google-genai`), `gemini-2.5-flash`
- **Knowledge Base:** 17 in-memory JSON data structures
- **Frontend:** Semantic HTML5, Modern CSS3 (Glassmorphism & responsive layouts), Vanilla JavaScript
- **Testing:** Python `unittest`

---

## 📂 Project Structure

```
├── app.py                  # Flask web server & REST API endpoints (/api/chat, /api/health)
├── gemini_service.py       # Dual-layer orchestrator: KB retriever + Gemini grounding fallback
├── knowledge_base.py       # In-memory KB manager, fuzzy matching, and rule-based query router
├── test_chatbot.py         # Complete automated test suite (49 test cases)
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment template for API keys
├── .gitignore              # Git ignore rules protecting secrets & build artifacts
├── data/                   # 17 structured ground-truth JSON files
│   ├── administration.json
│   ├── admissions.json
│   ├── college.json
│   ├── committees.json
│   ├── contacts.json
│   ├── deans.json
│   ├── departments.json
│   ├── examinations.json
│   ├── facilities.json
│   ├── faculty.json
│   ├── fees.json
│   ├── important_links.json
│   ├── placements.json
│   ├── qa_pairs.json
│   ├── scholarships.json
│   ├── sources.json
│   └── student_activities.json
├── static/                 # Static frontend assets
│   ├── css/style.css       # Clean, modern, responsive styling
│   ├── js/chat.js          # Chat client logic, streaming, UI updates
│   └── images/             # Institutional logos & icons
└── templates/              # HTML templates
    └── index.html          # Main chat interface
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/sbjitmr-ai-chatbot.git
cd sbjitmr-ai-chatbot
```

### 2. Create and Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=5000
```
> 🔑 **Get an API key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate a free API key.

### 5. Run the Server
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Tests

To run the full automated test suite (49 tests):
```bash
python test_chatbot.py
```

Expected output:
```text
Ran 49 tests in ~1.5s
OK
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web application interface |
| `POST` | `/api/chat` | Send question and receive verified JSON response |
| `GET` | `/api/health` | Health check (KB file count, API status) |

### Sample Chat Request:
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Can a student take admission in direct second year if they did a diploma?"}'
```

---

## 📄 License & Attribution

- Built for academic demonstration and student guidance for **S. B. Jain Institute of Technology, Management & Research, Nagpur**.
- All official data referenced from the official institutional portal: [https://www.sbjit.edu.in/](https://www.sbjit.edu.in/).
