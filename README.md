# CAREERPREP AI
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

## 5. Folder Structure

```
CareerPrep-AI/
│
├── app.py                      # Flask main entrypoint and route declarations
├── config.py                   # Environment & application configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment settings
├── .env                        # Local environment variables (not committed)
├── .gitignore                  # Git exclusions
├── README.md                   # Complete academic documentation & setup guide
├── careerprep.db               # SQLite database file (auto-generated)
│
├── database/
│   ├── __init__.py
│   └── database.py             # SQLAlchemy instance, table creation & seeding
│
├── models/
│   ├── __init__.py
│   ├── student.py              # Student profile model
│   ├── internship.py           # Internship opportunity model
│   ├── application.py          # Application tracking model
│   └── interview.py            # Interview, questions, answers, practice models
│
├── internship/
│   ├── __init__.py
│   ├── sources.py              # Public feed adapter, deduplication & normalization
│   ├── filters.py              # Multi-attribute search & filter engine
│   └── tracker.py              # Status updates & dashboard metric aggregator
│
├── ai/
│   ├── __init__.py
│   ├── ai_service.py           # AI client (Gemini + Demo mode switch)
│   ├── question_generator.py   # Tailored technical question generator
│   ├── evaluator.py            # 4-dimensional scoring rubric evaluator
│   └── feedback.py             # Performance scorecard & recommendation synthesizer
│
├── interview/
│   ├── __init__.py
│   ├── interview.py            # Interview session lifecycle & persistence
│   ├── session.py              # Stepper & session state helpers
│   └── scoring.py              # Composite score formulas & letter grading
│
├── speech/
│   ├── __init__.py
│   ├── recorder.py             # Audio file storage & validation
│   └── speech_to_text.py       # Configurable STT provider & fallback bridge
│
├── templates/
│   ├── base.html               # Master layout with responsive navbar & alerts
│   ├── index.html              # Landing page with 4 main cards & features
│   ├── dashboard.html          # Student KPI dashboard & Chart.js visualizations
│   ├── profile.html            # Profile editor & resume upload
│   ├── internships.html        # Directory with filters & "Prepare for Interview"
│   ├── interview_setup.html    # Simulation configuration modal
│   ├── questions.html          # Generated questions & expected points
│   ├── practice.html           # Interactive practice mode with coaching feedback
│   ├── mock_interview.html     # Live interview screen with voice recorder & timer
│   ├── feedback.html           # Evaluation report with radar chart
│   └── history.html            # Chronological log of past interviews
│
├── static/
│   ├── css/
│   │   └── style.css           # Professional dark-blue/blue theme stylesheet
│   └── js/
│       ├── script.js           # Flash auto-dismiss and UI behaviors
│       ├── interview.js        # Interview timer & answer submission handler
│       └── recorder.js         # MediaRecorder & SpeechRecognition integration
│
├── uploads/                    # Local storage for uploaded resumes & audio clips
│   └── recordings/
│
└── tests/
    ├── __init__.py
    └── test_basic.py           # Automated Pytest suite
```

---

## 6. Installation & Running Instructions (Windows PowerShell)

Follow these step-by-step instructions in **Windows PowerShell** or the **VS Code Terminal**:

### Step 1: Open Project Directory
```powershell
cd C:\Users\khot6\OneDrive\Desktop\Python_mini
```

### Step 2: Create Python Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
> **PowerShell Execution Policy Note**: If Windows prevents script execution, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\venv\Scripts\Activate.ps1
> ```

### Step 4: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Copy the template file to create `.env` (already configured to run in Demo Mode by default):
```powershell
copy .env.example .env
```
*(Optional: If you wish to enable Google Gemini, open `.env` in VS Code and paste your key into `GEMINI_API_KEY=your_key_here`)*.

### Step 6: Run Automated Tests (Verification)
```powershell
.\venv\Scripts\pytest -v
```
*Expected Output*: `7 passed in ~3s` with zero warnings.

### Step 7: Launch the Application
```powershell
python app.py
```
*Expected Terminal Output*:
```
=================================================================
 ⚡ CAREERPREP AI — INTERNSHIP TRACKING & MOCK INTERVIEW SYSTEM
=================================================================
 * Operating Mode: Demo Mode: Offline Question Bank & Rubric Evaluator
 * Server running on: http://127.0.0.1:5000
 * Press Ctrl+C in terminal to stop.
=================================================================
```

### Step 8: Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```

### Stopping the Server
In the PowerShell terminal, press `Ctrl + C` to gracefully terminate the Flask server.

---

## 7. College Viva & Academic Project Documentation

### A. Problem Statement
Securing technical internships is a critical milestone for engineering students. However, students face three distinct bottlenecks:
1. **Scattered Opportunities**: Difficulty tracking internship postings across disparate portals and manually organizing application deadlines.
2. **Disconnected Preparation**: Studying generic interview questions that do not reflect the specific tech stack requested by the hiring company.
3. **Lack of Objective Feedback**: Traditional mock interviews with peers lack structured scoring rubrics, objective answer evaluation, and personalized study roadmaps.

### B. Existing System vs. Proposed System

| Dimension | Existing System | Proposed CareerPrep AI System |
| :--- | :--- | :--- |
| **Tracking** | Manual spreadsheets (Excel / Notion) | Automated database with one-click status transitions (`Saved` to `Selected`) |
| **Interview Prep**| Static question lists on forums | AI-driven dynamic questions tailored by role, tech stack, and difficulty |
| **Simulation** | None or peer practice | Realistic panel simulation with browser voice recording and live timer |
| **Evaluation** | Subjective peer opinion | Transparent 4-dimensional rubric (Correctness, Relevance, Depth, Clarity) |
| **Integration** | Disconnected tools | Direct 1-click pipeline from Internship Card &rarr; Mock Panel &rarr; Feedback Report |

### C. Functional Requirements
- **FR-01 (Profile)**: The system shall allow students to maintain academic details, skills, and target roles.
- **FR-02 (Discovery & Tracking)**: The system shall filter internships and track status changes.
- **FR-03 (De-duplication)**: External feed refreshes must prevent duplicate company/role entries.
- **FR-04 (Question Generation)**: The system shall generate structured JSON questions with expected points.
- **FR-05 (Voice & Audio)**: The system shall capture candidate voice responses and transcribe them into text.
- **FR-06 (Fallback)**: If voice or external AI is unavailable, text mode and local question banks must activate seamlessly.
- **FR-07 (Evaluation)**: Answers must be evaluated across Technical, Relevance, Completeness, and Clarity rubrics.
- **FR-08 (Reporting)**: The system shall generate a detailed scorecard report with radar chart analytics.

### D. Non-Functional Requirements
- **Reliability**: Zero crashes when external APIs or microphone hardware are missing.
- **Security**: Strict `.env` credential management; SQL parameterization via SQLAlchemy.
- **Performance**: Sub-500ms page render times using local SQLite and client-side charting.
- **Usability**: Responsive dark-blue interface adhering to modern accessibility guidelines.

### E. Data Flow Diagrams (DFD)

#### Level 0 DFD (Context Diagram)
```
[Student User] ────(Profile, Answers, Tracking)────► [CareerPrep AI System]
[Student User] ◄───(Internships, Questions, Feedback)─ [CareerPrep AI System]
```

#### Level 1 DFD
```
[Student] ──► (1.0 Profile Management) ──────► [students table]
    │
    ├──► (2.0 Internship Tracker) ──────────► [internships table] ──► [applications table]
    │          │
    │          └─ "Prepare for Interview"
    │                     │
    ├──► (3.0 Question Generation) ──────────► [interview_questions table]
    │          │
    ├──► (4.0 Mock Interview & Voice STT) ──► [interview_answers table]
    │          │
    └──► (5.0 AI Answer Evaluation) ────────► [interviews table] ──► [Feedback Report UI]
```

### F. Entity-Relationship (ER) Design
- **Student** (1 to M) &rarr; **Application**
- **Internship** (1 to M) &rarr; **Application**
- **Student** (1 to M) &rarr; **Interview**
- **Internship** (1 to M) &rarr; **Interview** *(Optional Foreign Key)*
- **Interview** (1 to M) &rarr; **InterviewQuestion**
- **InterviewQuestion** (1 to 1) &rarr; **InterviewAnswer**

---

## 8. College Viva Q&A (Sample Viva Questions & Answers)

1. **Q: Why did you choose Flask over Django for this project?**  
   *A: Flask is a micro-framework that gives complete visibility and control over application structure, routing, and database sessions without the boilerplate overhead of Django. This modularity makes every component easy to explain and demonstrate in a viva.*

2. **Q: How does the application operate without an active internet connection or Gemini API key?**  
   *A: The system implements an Adapter Design Pattern in `ai/ai_service.py`. If `GEMINI_API_KEY` is empty or network fails, `DEMO_MODE` activates automatically. Questions are sourced from an extensive local question bank, and answers are evaluated using a deterministic NLP rubric in `ai/evaluator.py`.*

3. **Q: How does voice recording work in the browser without third-party plugins?**  
   *A: It uses the HTML5 `navigator.mediaDevices.getUserMedia()` API combined with the `MediaRecorder` API in `static/js/recorder.js`. The recorded audio stream is packaged into an audio blob for preview and backend storage.*

4. **Q: How is Speech-to-Text achieved?**  
   *A: The client utilizes the native browser `SpeechRecognition` / `webkitSpeechRecognition` API to transcribe spoken words into the answer textarea in real-time. If the browser lacks support or microphone permission is denied, the candidate can seamlessly type their response without halting the interview.*

5. **Q: How are answers objectively evaluated in the rubric?**  
   *A: Answers are evaluated on a 0-10 scale across four weighted criteria: Technical Correctness (35%), Relevance (25%), Completeness (20%), and Clarity (20%). The algorithm inspects key concept coverage against expected answer points, calculates match ratios, and generates actionable advice.*

6. **Q: How does the "Prepare for Interview" feature connect internships to interviews?**  
   *A: When a student clicks "Prepare for Interview" on an internship card, the internship's required role and technology are passed via query parameters to `/interview`. This pre-configures the simulation panel and attaches the `internship_id` to the created `Interview` record in SQLite.*

7. **Q: How are SQL injection vulnerabilities prevented?**  
   *A: All database operations use Flask-SQLAlchemy ORM. SQLAlchemy compiles high-level queries into parameterized SQL statements where parameters are safely escaped by the SQLite driver.*

---

## 9. Future Scope

- **Automated Resume Parsing**: Extract candidate skills directly from PDF resumes using OCR / NLP.
- **Video Emotion & Eye Contact Telemetry**: Integrate WebRTC face-mesh models to assess interview posture and eye contact.
- **Adaptive Question Difficulty**: Dynamically increase or decrease question complexity based on candidate performance on preceding questions.
- **Recruiter Dashboard**: Allow verified recruiters to review student interview scorecards and issue direct interview invites.
- **Multi-lingual Voice Assessment**: Expand speech recognition to support regional Indian languages.

---

## 10. Authors & Acknowledgments

- **Student Name**: Aditya Sharma (3rd Year Computer Science & Engineering)
- **Course**: Advanced Programming Concepts (APC)
- **Academic Year**: 2026
- **Guided by**: Department of Computer Science & Engineering
