import streamlit as st
from PIL import Image
from google import genai

# Page configuration for mobile devices
st.set_page_config(page_title="Algorithmic Thinking with Python | GCE Kannur", page_icon="📝", layout="centered")

# Course Header & Branding
st.subheader("Government College of Engineering Kannur")
st.caption("Dr. Ajith K K | Dept. of Electronics and Communication Engineering")
st.title("📝 Paper-to-Python Evaluator & Rubric")
st.markdown("**Course:** Algorithmic Thinking with Python (`UCEST105`)")
st.write("Snap a photo of your handwritten flowchart or pseudocode to grade your submission against the rubric and view the reference Python implementation.")

# Exercise mapping from URL query parameters
exercise_id = st.query_params.get("ex", "general_exercise")
st.info(f"Active Exercise Context: **{exercise_id.upper()}**")

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
                    You are Dr. Ajith K K, an expert computer science professor for course UCEST105 Algorithmic Thinking with Python. Grade strictly and exclusively the student's uploaded handwritten submission (their flowchart or pseudocode) for exercise: {exercise_id}. Evaluate only what the student drew or wrote on paper, not the generated code.
                    
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

                    ## 🐍 Generated Python Code (Reference Implementation)
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
