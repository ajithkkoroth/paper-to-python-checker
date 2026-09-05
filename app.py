import streamlit as st
from PIL import Image
from google import genai

# Page configuration for mobile devices
st.set_page_config(page_title="Paper-to-Python Evaluator", page_icon="📝", layout="centered")

st.title("📝 Paper-to-Python Evaluator")
st.write("Snap a photo of your handwritten flowchart or pseudocode to check its logic and convert it to Python.")

# Exercise mapping or descriptions (You can customize based on your textbook chapters)
exercise_id = st.query_params.get("ex", "general_exercise")
st.info(f"Active Exercise Context: **{exercise_id.upper()}**")

# Image uploader (automatically triggers mobile camera on smartphones)
uploaded_file = st.file_uploader("Upload or snap a photo of your work", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Hand-Drawn Work", use_container_width=True)
    
# Securely retrieve API key from Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Gemini API Key is missing or not detected in Streamlit Secrets. Please check your app settings on share.streamlit.io.")
    else:
        if st.button("Evaluate and Translate Logic", type="primary"):
            with st.spinner("Analyzing your handwriting and logic structure..."):
                try:
                    # Initialize the Google GenAI client explicitly with the key
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    You are an expert computer science professor evaluating an engineering student's handwritten flowchart or pseudocode for exercise: {exercise_id}.
                    Analyze the uploaded image and perform three tasks:
                    1. LOGIC VERDICT: State clearly if the logic is correct, incomplete, or contains structural flaws (e.g., missing loop conditions, unclosed branches).
                    2. STRUCTURAL CRITIQUE: Provide 2-3 concise bullet points highlighting specific flaws or praising solid logic.
                    3. PYTHON TRANSLATION: Translate the validated logic into clean, idiomatic Python code matching this exercise requirement.
                    
                    Format your response clearly using markdown headings.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, prompt]
                    )
                    
                    st.success("Evaluation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred during evaluation: {e}")
