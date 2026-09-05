import streamlit as st
from PIL import Image
from google import genai

# Page configuration for mobile devices
st.set_page_config(page_title="Paper-to-Python Evaluator & Rubric", page_icon="📝", layout="centered")

st.title("📝 Paper-to-Python Evaluator & Rubric")
st.write("Snap a photo of your handwritten flowchart or pseudocode to grade it against the rubric and convert it to Python.")

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
        if st.button("Grade Submission & Translate", type="primary"):
            with st.spinner("Grading handwriting against rubric and analyzing logic..."):
                try:
                    # Initialize the Google GenAI client
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    You are an expert computer science professor evaluating an engineering student's handwritten flowchart or pseudocode submission for exercise: {exercise_id}.
                    
                    Analyze the uploaded image and grade it using the following 10-mark Rubric:
                    1. Algorithmic Logic & Correctness (Out of 4 marks): Are the steps, conditions, and loops logically sound to solve the problem?
                    2. Structural Notation & Flow (Out of 3 marks): Proper use of structural flow (sequencing, selection, repetition, arrows/connectors).
                    3. Python Translation Quality (Out of 3 marks): Feasibility and accuracy of mapping the logic to clean Python syntax.

                    Format your response strictly with the following sections using Markdown headings:
                    ## 📊 Evaluation Rubric Scorecard
                    - **Logic & Correctness:** [X]/4
                    - **Notation & Flow:** [X]/3
                    - **Python Translation:** [X]/3
                    - **Total Score:** **[X]/10**

                    ## 💡 Detailed Critique & Feedback
                    - Provide 2-3 concise bullet points highlighting structural strengths or specific logic flaws.

                    ## 🐍 Generated Python Code
                    - Provide clean, idiomatic Python code matching the student's intention and exercise requirement.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, prompt]
                    )
                    
                    st.success("Grading & Evaluation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred during evaluation: {e}")
