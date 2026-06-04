import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random

# =========================
# CONFIG
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## 🩺 MediAssist AI")

    dark_mode = st.toggle("🌙 Dark Mode")

    page = st.radio(
        "Navigation",
        [
            "💬 AI Chat",
            "🩺 Symptom Checker",
            "💊 Medicine Info",
            "⚖️ BMI Calculator",
            "❤️ Health Tips",
            "🚨 Emergency Help"
        ]
    )

    st.divider()

    st.subheader("🕒 Chat History")

    if len(st.session_state.chat_history) == 0:
        st.caption("No chat history yet")
    else:
        for item in reversed(st.session_state.chat_history[-10:]):
            st.caption(item[:50])

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# =========================
# DARK MODE
# =========================

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color:#0e1117;
            color:white;
        }

        section[data-testid="stSidebar"] {
            background-color:#161b22;
        }

        .card {
            background:#1f2937;
            padding:20px;
            border-radius:15px;
            margin-bottom:10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .card {
            background:#f5f7fa;
            padding:20px;
            border-radius:15px;
            margin-bottom:10px;
            border:1px solid #ddd;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================
# HEADER
# =========================

st.markdown(
    """
    <h1 style='text-align:center;color:#2E86C1'>
    🩺 MediAssist AI
    </h1>
    <p style='text-align:center'>
    Your Smart Medical Assistant
    </p>
    """,
    unsafe_allow_html=True
)

st.warning(
    "⚠️ This AI provides educational health information only and does not replace a licensed doctor."
)

# =========================
# DASHBOARD CARDS
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("💬 AI Chat")

with c2:
    st.info("⚖️ BMI")

with c3:
    st.info("💊 Medicine")

with c4:
    st.info("🚨 Emergency")

st.divider()

# =========================
# HEALTH TIPS DATA
# =========================

health_tips = [
    "Drink at least 8 glasses of water daily.",
    "Sleep 7-8 hours every night.",
    "Exercise at least 30 minutes daily.",
    "Reduce processed foods.",
    "Eat more fruits and vegetables.",
    "Manage stress with meditation.",
    "Avoid smoking and excessive alcohol.",
    "Get regular health checkups."
]

# =========================
# EMERGENCY WORDS
# =========================

emergency_words = [
    "chest pain",
    "heart attack",
    "stroke",
    "difficulty breathing",
    "can't breathe",
    "unconscious",
    "severe bleeding",
    "seizure"
]
# =========================
# AI CHAT
# =========================

if page == "💬 AI Chat":

    st.subheader("💬 AI Medical Chat")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Describe symptoms or ask a medical question..."
    )

    if prompt:

        st.session_state.chat_history.append(prompt)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Emergency Detection
        if any(
            word in prompt.lower()
            for word in emergency_words
        ):
            st.error(
                "🚨 Possible Medical Emergency Detected. "
                "Please contact emergency services or seek immediate medical attention."
            )

        try:

            with st.spinner("Analyzing..."):

                response = model.generate_content(
                    f"""
You are MediAssist AI.

Rules:
- You are NOT a doctor.
- Provide educational health information only.
- Never provide a final diagnosis.
- Recommend professional medical advice when necessary.
- If symptoms appear severe, advise emergency care.

User Question:
{prompt}
"""
                )

                reply = response.text

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            with st.chat_message("assistant"):
                st.markdown(reply)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# SYMPTOM CHECKER
# =========================

elif page == "🩺 Symptom Checker":

    st.subheader("🩺 Symptom Checker")

    symptom = st.selectbox(
        "Select a symptom",
        [
            "Fever",
            "Headache",
            "Cough",
            "Fatigue",
            "Stomach Pain",
            "Back Pain",
            "Sore Throat",
            "Dizziness"
        ]
    )

    if st.button("Analyze Symptom"):

        with st.spinner("Checking symptom..."):

            try:

                response = model.generate_content(
                    f"""
Explain the following symptom:

{symptom}

Include:
1. Possible causes
2. When to see a doctor
3. Self-care tips

Keep it simple.
"""
                )

                st.success(response.text)

            except Exception as e:
                st.error(str(e))

# =========================
# MEDICINE INFO
# =========================

elif page == "💊 Medicine Info":

    st.subheader("💊 Medicine Information")

    medicine = st.text_input(
        "Enter medicine name"
    )

    if st.button("Get Medicine Information"):

        if medicine:

            try:

                with st.spinner("Fetching information..."):

                    response = model.generate_content(
                        f"""
Explain medicine:

{medicine}

Include:
- Uses
- Side effects
- Precautions
- Important warnings

Simple language.
"""
                    )

                    st.success(response.text)

            except Exception as e:
                st.error(str(e))

# =========================
# BMI CALCULATOR
# =========================

elif page == "⚖️ BMI Calculator":

    st.subheader("⚖️ BMI Calculator")

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0
    )

    height_cm = st.number_input(
        "Height (cm)",
        min_value=1.0
    )

    if st.button("Calculate BMI"):

        height_m = height_cm / 100

        bmi = weight / (height_m ** 2)

        st.metric(
            "BMI",
            f"{bmi:.2f}"
        )

        if bmi < 18.5:
            st.warning("Underweight")
        elif bmi < 25:
            st.success("Normal Weight")
        elif bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

# =========================
# HEALTH TIPS
# =========================

elif page == "❤️ Health Tips":

    st.subheader("❤️ Daily Health Tips")

    st.success(
        random.choice(health_tips)
    )

    if st.button("Get Another Tip"):
        st.rerun()

    st.markdown("### Healthy Lifestyle")

    st.write(
        """
✅ Drink plenty of water

✅ Exercise regularly

✅ Sleep 7-8 hours

✅ Eat fruits and vegetables

✅ Reduce stress

✅ Avoid smoking
"""
    )

# =========================
# EMERGENCY HELP
# =========================

elif page == "🚨 Emergency Help":

    st.subheader("🚨 Emergency Warning Signs")

    st.error(
        """
Seek immediate medical help if you experience:

• Chest pain

• Difficulty breathing

• Stroke symptoms

• Severe bleeding

• Loss of consciousness

• Seizures

• Serious allergic reactions
"""
    )

    st.warning(
        "This tool cannot replace emergency medical services."
    )

# =========================
# DOWNLOAD CHAT
# =========================

if len(st.session_state.chat_history) > 0:

    st.divider()

    chat_text = "\n".join(
        st.session_state.chat_history
    )

    st.download_button(
        "📄 Download Chat History",
        chat_text,
        file_name="mediassist_chat.txt",
        mime="text/plain"
    )