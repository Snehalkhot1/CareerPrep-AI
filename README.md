# CAREERPREP A
## 🚀 Live Demo
[Click here to view the deployed project](https://careerprep-ai-gwtc.onrender.com/)

### *AI-Powered Internship Tracking and Mock Interview System*

> **College Advanced Programming Concepts (APC) Capstone Project**  
> **Target Level**: 3rd-Year B.Tech / B.E. Computer Science & Engineering  
> **Application Tagline**: *"Prepare. Practice. Get Hired."*

---

## 1. Project Overview & Description

**CareerPrep AI** is an intelligent, full-stack career preparation portal engineered to bridge the transition between college academics and campus placements. It provides Computer Science students with an integrated workflow: discovering and tracking technical internships, automatically customizing mock technical panels for target job profiles, practicing live voice-recorded mock interviews, and receiving objective, rubric-based AI performance evaluations with targeted study recommendations.

The system is architected to operate **100% autonomously out of the box** in **Demo/Fallback Mode** with zero external API key requirements (ideal for college viva evaluation and offline lab testing), while providing full plug-and-play support for **Google Gemini** when an API key is supplied in `.env`.

---

## 2. Key Features

- 💼 **Internship Tracker & Opportunity Directory**:
  - Discover curated tech internships across Python, Java, Web Development, Data Science, AI/ML, and Cloud/DevOps.
  - Multi-criteria filtering: keyword search, technology stack, location (Pune, Bangalore, Mumbai, Remote, etc.), stipend ranges, and work arrangement (Work From Home, Hybrid, On-site).
  - Multi-state application funnel tracking (`Saved`, `Interested`, `Applied`, `Interview Scheduled`, `Selected`, `Rejected`).
  - **Live Refresh Engine**: Normalizes and deduplicates opportunities from public open API feeds without scraping.
- 🎯 **Direct Internship &rarr; Interview Pipeline**:
  - Click **"Prepare for Interview"** on any internship card to immediately auto-configure an interview targeting that exact role and technology stack.
- 🤖 **AI Technical Question Generator**:
  - Configurable by Role, Technology (Python, Java, C++, JavaScript, SQL, AI/ML), Difficulty (Easy, Medium, Hard), and Format (Technical, Theory, Coding, Behavioral, Mixed).
  - Returns structured questions with key expected conceptual answer points.
- ✍️ **Interactive Practice Mode**:
  - Step-by-step self-paced learning mode. Submit answers and receive instantaneous rubric evaluations highlighting covered points, missing concepts, and coaching advice.
- 🎙️ **Live AI Mock Interview Simulation**:
  - Browser-native voice recording using the **MediaRecorder API** with audio playback preview.
  - Real-time Speech-to-Text utilizing the browser's native **Web Speech API** (`webkitSpeechRecognition`).
  - Graceful text fallback if microphone hardware is unavailable or permission is denied.
  - Live MM:SS interview timer and question progress tracking.
- 📊 **Objective Rubric Answer Evaluation**:
  - Transparent 4-dimensional assessment:
    - **Technical Correctness (35%)**: Conceptual accuracy and terminology.
    - **Answer Relevance (25%)**: Alignment with the specific prompt.
    - **Completeness (20%)**: Depth of explanation and edge cases.
    - **Clarity (20%)**: Articulation, structure, and readability.
- 📈 **Comprehensive Evaluation & Feedback Report**:
  - Overall score percentage and letter grade assignment (A+, A, B, C, D).
  - Interactive Radar Competency Chart visualizing strengths across all four dimensions.
  - Bulleted demonstrated strengths, identified growth areas, and targeted topic recommendations.
  - Question-by-question breakdown showing candidate responses versus expected points.
- 📜 **Historical Performance Ledger**:
  - Persistent interview log with timestamps, role tags, score badges, and drill-down links to previous reports.
- 👤 **Student Profile Management**:
  - Editable profile storing academic credentials, skill chips, career preferences, and resume document uploads.

---

## 3. Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend** | Python 3.13 / Flask 3.1 | Lightweight, modular WSGI micro-framework, easy to explain in viva |
| **Database** | SQLite + Flask-SQLAlchemy 3.1 | Zero-configuration embedded relational database with clean ORM models |
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 | Modern responsive dark-blue theme with semantic HTML and no bloated build tools |
| **Data Viz** | Chart.js 4.4 | Clean client-side radar and doughnut visualizations |
| **AI Engine** | Google Gemini + Deterministic Rubric Engine | Hybrid architecture: Gemini cloud inference when key is provided; intelligent offline question bank and NLP rubric evaluator in Demo Mode |
| **Audio/Speech**| Browser MediaRecorder & Web Speech API | Client-side audio recording and real-time speech-to-text without heavy external speech server dependencies |
| **Testing** | Pytest 9.1 | Automated test suite verifying models, routes, filtering, and evaluation rubrics |

---

## 4. System Architecture

```
+-----------------------------------------------------------------------------+
|                                CLIENT BROWSER                               |
|  [HTML5 / Jinja2]   [CSS3 Dark-Blue]   [MediaRecorder]   [Web Speech STT]   |
+-----------------------------------------------------------------------------+
                                       ▲
                                       │ HTTP / JSON API
                                       ▼
+-----------------------------------------------------------------------------+
|                              FLASK BACKEND                                  |
|                                                                             |
|   ┌────────────────┐   ┌─────────────────┐   ┌───────────────────────────┐  |
|   │ Student Routes │   │ Tracker Routes  │   │ Mock Interview Controller │  |
|   └────────┬───────┘   └────────┬────────┘   └─────────────┬─────────────┘  |
|            │                    │                          │                |
|   ┌────────▼───────┐   ┌────────▼────────┐   ┌─────────────▼─────────────┐  |
|   │ Profile Model  │   │ Internship Model│   │ AI Engine (Gemini / Demo) │  |
|   └────────┬───────┘   └────────┬────────┘   └─────────────┬─────────────┘  |
|            │                    │                          │                |
|            └────────────────────┼──────────────────────────┘                |
|                                 ▼                                           |
|                     ┌────────────────────────┐                              |
|                     │ Flask-SQLAlchemy (ORM) │                              |
|                     └───────────┬────────────┘                              |
+---------------------------------┼-------------------------------------------+
                                  ▼
                     ┌────────────────────────┐
                     │  careerprep.db (SQLite)│
                     │  - students            │
                     │  - internships         │
                     │  - applications        │
                     │  - interviews          │
                     │  - interview_questions │
                     │  - interview_answers   │
                     └────────────────────────┘
```

---

