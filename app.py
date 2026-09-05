import streamlit as st
from PIL import Image
from google import genai

# Page configuration for mobile devices
st.set_page_config(page_title="Algorithmic Thinking with Python | GCE Kannur", page_icon="📝", layout="centered")

# Custom Professional CSS Styling
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
    }

    /* Header Banner Styling */
    .header-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .header-card h3 {
        color: #ffffff !important;
        margin-bottom: 0.2rem;
        font-size: 1.25rem;
        font-weight: 600;
    }

    .header-card p {
        color: #e2e8f0;
        font-size: 0.9rem;
        margin-bottom: 0;
    }

    /* App Title Styling */
    h1 {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.8rem !important;
        margin-top: 1rem;
    }

    /* Subtext & Meta */
    .course-badge {
        background-color: #f1f5f9;
        color: #334155;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #2563eb;
        color: white;
        padding: 0.6rem;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* File Uploader styling box */
    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 10px;
        padding: 1rem;
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# Course Header & Branding Card
st.markdown("""
<div class="header-card">
    <h3>Government College of Engineering Kannur</h3>
    <p>Dr. Ajith K K |&nbsp;Dept. of Electronics and Communication Engineering &nbsp;</p>
</div>
""", unsafe_allow_html=True)

st.title("📝 Flowchart & Pseudocode Evaluator")
st.markdown('<div class="course-badge">Course: Algorithmic Thinking with Python (UCEST105)</div>', unsafe_allow_html=True)
st.write("Snap or upload a photo of your handwritten flowchart or pseudocode to grade your submission against the rubric and view the Python implementation.")

# Exercise mapping from URL query parameters
# exercise_id = st.query_params.get("ex", "general_exercise")
# st.info(f"📌 Active Exercise Context: **{exercise_id.upper()}**")

# Simple image file uploader
uploaded_file = st.file_uploader("Upload or snap a photo of your work", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Hand-Drawn Work", use_container_width=True)
    
    # Securely retrieve API key from Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Gemini API Key is missing or not detected in Streamlit Secrets. Please check your app settings on share.streamlit.io.")
    else:
        if st.button("Grade Submission & Generate Code", type="primary"):
            with st.spinner("Grading your uploaded submission against the rubric..."):
                try:
                    # Initialize the Google GenAI client
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    You are Dr. Ajith K K, an expert computer science professor for course UCEST105 Algorithmic Thinking with Python. Grade strictly and exclusively the student's uploaded handwritten submission (their flowchart or pseudocode). Evaluate only what the student drew or wrote on paper, not the generated code.
                    
                    Grade the submission using the following 10-mark Rubric:
                    1. Algorithmic Logic & Correctness (Out of 4 marks): Are the steps, conditions, and loops logically sound in the student's drawing?
                    2. Structural Notation & Flow (Out of 3 marks): Proper use of structural flow (sequencing, selection, repetition, arrows/connectors) in the paper work.
                    3. Python Translation Readiness (Out of 3 marks): How accurately and cleanly the student's handwritten logic can map to Python.

                    Format your response strictly with the following sections using Markdown headings:
                    ## 📊 Submission Rubric Scorecard
                    - **Logic & Correctness:** [X]/4
                    - **Notation & Flow:** [X]/3
                    - **Python Translation Readiness:** [X]/3
                    - **Total Score:** **[X]/10**

                    ## 💡 Detailed Critique & Feedback
                    - Provide 2-3 concise bullet points highlighting structural strengths or specific logic flaws found exclusively in the student's handwritten work.

                    ## 🐍 Generated Python Code
                    - Provide clean, idiomatic Python code corresponding to the exercise requirement.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, prompt]
                    )
                    
                    st.success("Grading & Generation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred during evaluation: {e}")
