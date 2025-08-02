import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# Set Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🧠 Audiogram Summary Generator (Gemini)")

# Step 1: Upload audiogram image
uploaded_file = st.file_uploader("Upload an audiogram image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Audiogram", use_column_width=True)

# Step 2: Manual input of thresholds
st.header("🎧 Enter Thresholds (in dB HL)")
freqs = ["250", "500", "1000", "2000", "4000", "8000"]
left_ear = {}
right_ear = {}

st.subheader("Left Ear")
for freq in freqs:
    left_ear[freq] = st.slider(f"Left {freq} Hz", 0, 120, 20)

st.subheader("Right Ear")
for freq in freqs:
    right_ear[freq] = st.slider(f"Right {freq} Hz", 0, 120, 20)

# Step 3: Generate clinical summary using Gemini
if st.button("📝 Generate Clinical Summary"):
    prompt = f"""
    Audiogram thresholds (in dB HL):
    Left ear: {left_ear}
    Right ear: {right_ear}

    Please summarize the type, degree, symmetry, and configuration of hearing loss using clinical language suitable for a hearing aid fitting report.
    """

    with st.spinner("Generating summary using Gemini..."):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        result = response.text

        st.success("Summary Generated!")
        st.markdown("### 🧾 Clinical Summary")
        st.write(result)
