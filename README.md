📄 AI Resume Screening Agent (48h AI Challenge - HR Category)
A fast, free, and dependency-free AI agent that automates resume screening for HR teams, eliminating 80% of manual resume review work. Built with Groq's Llama 3.1 model (no LangChain, zero dependency conflicts).

🎯 Overview
The Problem
HR teams spend 50+ hours/month manually screening resumes against job descriptions, wasting valuable time on administrative work instead of connecting with top talent. Small to mid-sized companies often lack access to expensive Applicant Tracking Systems (ATS) to automate this process.

The Solution
This AI Resume Screening Agent:

Parses PDF resumes to extract clean, readable text
Uses Groq's ultra-fast Llama 3.1 model to score resumes 0-100% based on job fit
Highlights key matching skills and critical gaps for each candidate
Ranks candidates by match score and exports results to CSV for HR review
Operates on Groq's free tier (1M tokens/month, no credit card required)

✨ Features & Limitations
Key Features

Feature	Benefit

📥 Multi-Resume Upload	Process 1-100+ PDF resumes in a single batch
🎯 AI Match Scoring	0-100% fit score based on job requirements (skills, experience, education)
🔍 Matches & Gaps Visualization	Clear breakdown of candidate strengths and missing qualifications
📤 CSV Export	Download ranked results for HR record-keeping and follow-up
⚡ Ultra-Fast Performance	Sub-1 second response per resume (powered by Groq's Llama 3.1)
🆓 Free Tier Access	1M free tokens/month (no credit card required)
🧠 Bias-Mitigated Scoring	Strictly evaluates job-relevant criteria only (no demographic data used)
🚫 Zero Dependency Conflicts	Direct Groq API integration (no LangChain, no messy library conflicts)

Known Limitations

PDF-Only Support: Currently only parses standard PDF resumes (no Word/docx files)
No OCR for Complex Resumes: Cannot extract text from image-based or heavily designed resumes (e.g., resumes with graphics/tables)
No ATS Integration: Does not connect to existing HR Applicant Tracking Systems yet
Authenticity Verification: Cannot verify the truthfulness of resume claims (HR must perform final verification)
Requires Clear Job Descriptions: Scoring accuracy depends on detailed, well-written job descriptions

🛠️ Techstack & APIs Used

Component	Tool/Library	Purpose
Frontend UI	Streamlit 1.36.0	Professional, user-friendly interface for resume upload and result display
AI Model	Groq Llama 3.1 8b	Fast, free LLM for resume scoring and match/gap analysis
Document Parsing	PyPDF2 3.0.1	Extract clean text from PDF resumes
Data Export	Pandas 2.2.2	Generate CSV reports of ranked candidates
Environment Management	python-dotenv 1.0.1	Securely store API keys (no hardcoding)

🚀 Setup & Run Instructions

Prerequisites

Python 3.8+ installed on your system
A free Groq API key (get one from Groq Console)
Step 1: Clone the Repository
Bash
git clone https://github.com/your-username/ResumeScreeningAgent.git
cd ResumeScreeningAgent

Step 2: Install Dependencies
Bash
# Install all required packages (conflict-free!)
pip install -r requirements.txt

Step 3: Configure API Key
Create a file named .env in the project folder
Add your Groq API key to the file:
env

# Groq API Key (free tier available)
GROQ_API_KEY=your_groq_api_key_here

Step 4: Run the App
Bash : 
streamlit run resume_screening_agent.py

Step 5: Use the Agent
Open the URL shown in your terminal (usually http://localhost:8501)
Paste your job description in the sidebar
Upload 1+ PDF resumes
Click "Start Screening" to see ranked results in seconds!

🚀 Potential Improvements
Short-Term (1-2 Weeks):
Add support for Word/docx resumes using python-docx
Integrate OCR (Optical Character Recognition) using pytesseract for image-based resumes
Add resume authenticity checks via LinkedIn profile verification
Implement bulk resume upload from cloud storage (Google Drive, Dropbox)

Long-Term (1-3 Months):
Integrate with popular ATS platforms (Greenhouse, Lever, BambooHR)
Add bias detection for job descriptions to ensure inclusive hiring practices
Build team collaboration features (share results, add HR notes)
Auto-schedule top candidates for interviews via Google Calendar/Calendly API
Add multi-language support for global hiring teams
Build a dashboard for historical hiring trend analysis

🏗️ Architecture
AI Resume Screening Agent Architecture 
![architecture](assets/agent_architecture.png)

End-to-End Workflow: 

HR User: Uploads resumes and inputs job description
Streamlit UI: Handles user interaction and displays results
Resume Parser: Extracts clean text from PDF resumes
Groq Llama 3.1: Scores resumes and identifies matches/gaps
CSV Export: Saves ranked results for HR review

📱 Demo Link
Live Streamlit Demo

