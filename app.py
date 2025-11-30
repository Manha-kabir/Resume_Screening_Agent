# resume_screening_agent.py
# GROQ DIRECT API - AI Resume Screening Agent
# NO LANGCHAIN - ZERO DEPENDENCY CONFLICTS
# Created for 48h AI Challenge

# ============================================
# IMPORTS (ONLY WHAT WE NEED)
# ============================================
import streamlit as st
import os
from PyPDF2 import PdfReader
import pandas as pd
from dotenv import load_dotenv
from groq import Groq  # Direct Groq SDK, no LangChain!

# Load API keys
load_dotenv()

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="AI Resume Screening Agent (Groq)",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
#st.markdown("""
#<style>
#    .stApp {
 #       background-color: #f5f7fa;
  #  }
   # .resume-card {
    #    background-color: white;
     #   border-radius: 12px;
      #  padding: 16px;
       # margin: 8px 0;
        #box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        #transition: transform 0.2s;
    #}
    #.resume-card:hover {
     #   transform: translateY(-2px);
      #  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    #}
    #.match-score {
     #   font-size: 24px;
      #  font-weight: bold;
       # padding: 8px 16px;
        #border-radius: 8px;
        #display: inline-block;
   # }
    #.high-score {
     #   background-color: #e8f5e9;
      #  color: #2e7d32;
    #}
    #.medium-score {
     #   background-color: #fff3e0;
      #  color: #ef6c00;
    #}
    #.low-score {
     #   background-color: #ffebee;
      #  color: #c62828;
    #}
  #  .section-header {
   #     color: #1a73e8;
    #    font-size: 18px;
     #   font-weight: 600;
      #  margin: 12px 0 8px 0;
#    }
 #   .gap-item {
  #      color: #d32f2f;
   #     font-weight: 500;
   # }
    #.match-item {
     #   color: #2e7d32;
      #  font-weight: 500;
    #}
#</style>
#""", unsafe_allow_html=True)

# ============================================
# INITIALIZE GROQ CLIENT (DIRECT CONNECTION)
# ============================================
@st.cache_resource
def init_groq_client():
    """Direct connection to Groq's Llama 3.1 model (no LangChain!)"""
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            st.sidebar.error("❌ Groq API key not found! Add to .env file")
            return None
        
        client = Groq(api_key=groq_api_key)
        st.sidebar.success("✅ Connected to Groq Llama 3.1 (FREE)")
        return client
    
    except Exception as e:
        st.sidebar.error(f"❌ Failed to connect to Groq: {str(e)}")
        return None

groq_client = init_groq_client()

# ============================================
# RESUME PARSING FUNCTION
# ============================================
def parse_resume(pdf_file):
    """Extract clean text from PDF resume"""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        resume_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text
        
        # Clean up messy PDF text
        resume_text = resume_text.replace("\n", " ").replace("\t", " ").strip()
        resume_text = " ".join(resume_text.split())  # Remove extra spaces
        return resume_text
    
    except Exception as e:
        st.error(f"❌ Failed to parse {pdf_file.name}: {str(e)}")
        return None

# ============================================
# GROQ DIRECT RESUME SCORING (NO LANGCHAIN!)
# ============================================
def score_resume(job_description, resume_text):
    """Score resume using Groq's Llama 3.1 model (direct API call)"""
    if not groq_client:
        return 0, "❌ No Groq connection available", [], []
    
    # Simple, clear prompt that Llama 3.1 follows perfectly
    system_prompt = """
    You are a senior HR recruiter with 10+ years of experience.
    Follow these instructions EXACTLY:
    1. Give a MATCH SCORE from 0-100% (whole number only)
    2. List 3-5 KEY MATCHES (start with "MATCH: ")
    3. List 2-3 KEY GAPS (start with "GAP: ")
    FORMAT YOUR RESPONSE LIKE THIS:
    SCORE: [NUMBER]%
    MATCHES:
    - MATCH: [Skill 1]
    - MATCH: [Skill 2]
    GAPS:
    - GAP: [Missing Skill 1]
    - GAP: [Missing Skill 2]
    """

    try:
        # Direct Groq API call (no LangChain!)
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"JOB DESCRIPTION: {job_description}\nRESUME: {resume_text}"}
            ],
            temperature=0.1,
            max_tokens=1000
        )

        response_text = response.choices[0].message.content.strip()
        score = 0
        matches = []
        gaps = []

        # Parse Groq's structured output
        lines = [line.strip() for line in response_text.split("\n") if line.strip()]
        
        # Extract score
        for line in lines:
            if line.startswith("SCORE:"):
                try:
                    score = int(line.replace("SCORE:", "").replace("%", "").strip())
                except:
                    score = 0
                break
        
        # Extract matches and gaps
        matches_start = next((i for i, line in enumerate(lines) if line == "MATCHES:"), -1)
        gaps_start = next((i for i, line in enumerate(lines) if line == "GAPS:"), -1)
        
        if matches_start != -1 and gaps_start != -1:
            matches = [line for line in lines[matches_start+1:gaps_start] if line.startswith("- MATCH:")]
        
        if gaps_start != -1:
            gaps = [line for line in lines[gaps_start+1:] if line.startswith("- GAP:")]

        return score, response_text, matches, gaps

    except Exception as e:
        st.error(f"❌ Failed to score resume: {str(e)}")
        return 0, f"Error: {str(e)}", [], []

# ============================================
# MAIN APP INTERFACE
# ============================================
def main():
    # Header
    st.title("📄 AI Resume Screening Agent (Groq)")
    st.caption("100% No LangChain | Fast, Free Resume Screening")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Job Description Input
        st.subheader("📋 Job Description")
        job_desc = st.text_area(
            "Paste job description here:",
            height=200,
            placeholder="e.g., 'Looking for a Python developer with 3+ years experience in Django, REST APIs, and cloud deployment...'"
        )

        # Resume Upload
        st.subheader("📥 Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload PDF resumes (multiple allowed):",
            type=["pdf"],
            accept_multiple_files=True
        )

        # Action Buttons
        st.subheader("🚀 Actions")
        run_screening = st.button("Start Screening", use_container_width=True, type="primary")
        export_results = st.button("Export Results to CSV", use_container_width=True)

        # Groq Info
        st.divider()
        st.info("""
        🎯 **Powered by Groq Llama 3.1**
        - Fastest open-source LLM (sub-1 second responses)
        - 1M free tokens/month (no credit card needed)
        - No LangChain = No dependency conflicts!
        """)

    # Initialize session state for results
    if "screening_results" not in st.session_state:
        st.session_state.screening_results = []

    # Run Screening
    if run_screening and job_desc and uploaded_files:
        with st.spinner("🔍 Screening resumes with Groq Llama 3.1..."):
            results = []
            
            for file in uploaded_files:
                # Parse resume
                resume_text = parse_resume(file)
                if not resume_text:
                    continue
                
                # Score resume with direct Groq call
                score, full_response, matches, gaps = score_resume(job_desc, resume_text)
                
                # Store result
                results.append({
                    "filename": file.name,
                    "score": score,
                    "matches": matches,
                    "gaps": gaps,
                    "full_analysis": full_response
                })
            
            # Sort results by score (highest first)
            st.session_state.screening_results = sorted(results, key=lambda x: x["score"], reverse=True)
            st.success(f"✅ Screening complete! Processed {len(results)} resumes in seconds.")

    # Display Results
    if st.session_state.screening_results:
        st.header("🏆 Ranked Resumes (Highest Match First)")
        
        # Create results dataframe for export
        results_df = pd.DataFrame(st.session_state.screening_results)
        results_df = results_df[["filename", "score", "matches", "gaps"]]

        # Export to CSV
        if export_results:
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="resume_screening_results.csv",
                mime="text/csv"
            )

        # Display each resume card
        for idx, resume in enumerate(st.session_state.screening_results):
            with st.container():
                st.markdown(f'<div class="resume-card">', unsafe_allow_html=True)
                
                # Score and filename
                col1, col2 = st.columns([1, 4])
                with col1:
                    # Score styling
                    if resume["score"] >= 70:
                        score_class = "high-score"
                    elif resume["score"] >= 40:
                        score_class = "medium-score"
                    else:
                        score_class = "low-score"
                    
                    st.markdown(f'<div class="match-score {score_class}">{resume["score"]}%</div>', unsafe_allow_html=True)
                
                with col2:
                    st.subheader(f"Resume #{idx+1}: {resume['filename']}")

                # Matches
                if resume["matches"]:
                    st.markdown('<div class="section-header">✅ Key Matches</div>', unsafe_allow_html=True)
                    for match in resume["matches"]:
                        st.markdown(f'<div class="match-item">{match.replace("- MATCH:", "")}</div>', unsafe_allow_html=True)

                # Gaps
                if resume["gaps"]:
                    st.markdown('<div class="section-header">⚠️ Key Gaps</div>', unsafe_allow_html=True)
                    for gap in resume["gaps"]:
                        st.markdown(f'<div class="gap-item">{gap.replace("- GAP:", "")}</div>', unsafe_allow_html=True)

                # Full analysis
                with st.expander("📝 Full Groq AI Analysis"):
                    st.text(resume["full_analysis"])
                
                st.markdown('</div>', unsafe_allow_html=True)

    # Empty state
    else:
        st.markdown("""
        ### 🎯 Get Started
        1. **Paste your job description** in the sidebar
        2. **Upload resume PDFs** (multiple allowed)
        3. Click **"Start Screening"** to see ranked results in seconds!
        """)

    # Footer
    st.divider()
    st.caption("🤖 Built for 48h AI Challenge | Groq Direct API")
    st.caption("⚠️ This agent provides recommendations only - final hiring decisions should be made by HR professionals.")

# ============================================
# RUN APP
# ============================================
if __name__ == "__main__":

    main()
