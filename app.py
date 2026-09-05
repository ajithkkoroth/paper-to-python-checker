import streamlit as st
from PIL import Image
from google import genai

# Page configuration for mobile devices
st.set_page_config(page_title="Flowchart & Pseudocode Evaluator | GCE Kannur", page_icon="📝", layout="centered")

# Custom Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 700px; }
    .header-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-card h3 { color: #ffffff !important; margin-bottom: 0.2rem; font-size: 1.25rem; font-weight: 600; }
    .header-card p { color: #e2e8f0; font-size: 0.9rem; margin-bottom: 0; }
    h1 { color: #0f172a; font-weight: 700; font-size: 1.8rem !important; margin-top: 1rem; }
    .course-badge {
        background-color: #f1f5f9; color: #334155; padding: 0.4rem 0.8rem;
        border-radius: 6px; font-weight: 500; font-size: 0.85rem; display: inline-block;
        margin-bottom: 1rem; border: 1px solid #e2e8f0;
    }
    .stButton > button {
        width: 100%; border-radius: 8px; font-weight: 600; background-color: #2563eb;
        color: white; padding: 0.6rem; border: none;
    }
    .stButton > button:hover { background-color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-card">
    <h3>Government College of Engineering Kannur</h3>
    <p>Dr. Ajith K K;|&nbsp;Dept. of Electronics and Communication Engineering &nbsp </p>
</div>
""", unsafe_allow_html=True)

st.title("📝 Flowchart & Pseudocode Evaluator")
st.markdown('<div class="course-badge">Course: Algorithmic Thinking with Python (UCEST105)</div>', unsafe_allow_html=True)
st.write("Scan or upload a photo of your handwritten flowchart or pseudocode to grade your submission against the rubric and view the reference implementation.")

uploaded_file = st.file_uploader("Upload or snap a photo of your work", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Resize image to optimize payload size and avoid memory bottlenecks
    image.thumbnail((1024, 1024))
    st.image(image, caption="Your Hand-Drawn Work", use_container_width=True)
    
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Gemini API Key is missing or not detected in Streamlit Secrets.")
    else:
        if st.button("Grade Submission & Generate Code", type="primary"):
            with st.spinner("Grading your uploaded submission against the rubric..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    prompt = """
                    You are Dr. Ajith K K, an expert computer science professor for course UCEST105 Algorithmic Thinking with Python. Grade strictly and exclusively the student's uploaded handwritten submission (their flowchart or pseudocode).
                    
                    Grade the submission using the following 10-mark Rubric:
                    1. Algorithmic Logic & Correctness (Out of 4 marks)
                    2. Structural Notation & Flow (Out of 3 marks)
                    3. Python Translation Readiness (Out of 3 marks)

                    Format your response strictly with the following sections using Markdown headings:
                    ## 📊 Submission Rubric Scorecard
                    - **Logic & Correctness:** [X]/4
                    - **Notation & Flow:** [X]/3
                    - **Python Translation Readiness:** [X]/3
                    - **Total Score:** **[X]/10**

                    ## 💡 Detailed Critique & Feedback
                    - Provide 2-3 concise bullet points highlighting structural strengths or specific logic flaws.

                    ## 🐍 Generated Python Code (Reference Implementation)
                    - Provide clean, idiomatic Python code corresponding to the problem depicted in the submission.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, prompt]
                    )
                    
                    st.success("Grading & Generation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str:
                        st.error("⏳ API rate limit or daily free tier quota reached. Please wait a moment or try again later.")
                    else:
                        st.error(f"An error occurred during evaluation: {e}")
