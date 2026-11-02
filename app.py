
import streamlit as st
import os
from openai import OpenAI

# ---------------- SETTINGS ----------------
st.set_page_config(
    page_title="Youth Mental Wellness",
    page_icon="🌱",
    layout="centered"
)

# Load API Key from Streamlit Secrets or environment
try:
    API_KEY = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize OpenAI client only if API key exists
client = OpenAI(api_key=API_KEY) if API_KEY else None

# Crisis words for emergency response
CRISIS_WORDS = [
    "suicide",
    "self-harm",
    "self harm",
    "kill myself",
    "end my life",
    "want to die",
    "hurt myself",
    "hopeless"
]

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "📌 Navigate",
    ["Home", "Chat with AI", "Resources", "Emergency Help", "About"]
)

# ---------------- HOME ----------------
if page == "Home":

    st.title("🌱 Youth Mental Wellness")

    st.subheader(
        "A safe, supportive, and empathetic space for young minds 💙"
    )

    st.write(
        "👉 Use the sidebar to navigate. "
        "Start chatting with AI or explore mental wellness resources."
    )

    st.info(
        "Your mental health matters. "
        "You are not alone, and asking for help is a strength."
    )

# ---------------- CHAT ----------------
elif page == "Chat with AI":

    st.title("🗨️ Confidential AI Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a kind, empathetic, and supportive mental "
                    "wellness guide for young people. Listen carefully, "
                    "respond without judgment, encourage healthy coping "
                    "strategies, and recommend professional support when "
                    "appropriate. Never diagnose or prescribe medication. "
                    "If someone may be in immediate danger, encourage "
                    "them to contact emergency services and a trusted person."
                )
            }
        ]

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:

        st.chat_message("user").write(user_input)

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        # Crisis detection
        if any(word in user_input.lower() for word in CRISIS_WORDS):

            ai_reply = (
                "💙 I'm really sorry you're going through this. "
                "You deserve support, and you don't have to face this alone.\n\n"
                "Please consider these steps:\n"
                "- Contact someone you trust and stay with them.\n"
                "- India: Call Tele-MANAS at 14416 for free mental "
                "health support (24/7).\n"
                "- If you are in immediate danger, call 112 or go "
                "to the nearest hospital emergency department.\n\n"
                "Are you safe right now?"
            )

        elif client is None:

            ai_reply = (
                "⚠️ OpenAI API key is missing. "
                "Please configure OPENAI_API_KEY in Streamlit Secrets."
            )

        else:

            # Call OpenAI API
            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=500
                )

                ai_reply = response.choices[0].message.content

                if not ai_reply:
                    ai_reply = "I'm here to listen. Could you tell me more?"

            except Exception:
                ai_reply = (
                    "Sorry, something went wrong while connecting "
                    "to the AI service. Please try again later."
                )

        # Display AI reply
        with st.chat_message("assistant"):
            st.write(ai_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

# ---------------- RESOURCES ----------------
elif page == "Resources":

    st.title("📚 Resources for Mental Wellness")

    st.markdown("""
    - 🌿 [Headspace: Mindfulness & Meditation](https://www.headspace.com/)

    - 💙 [NAMI: Mental Health Resources](https://www.nami.org/)

    - 🌍 [WHO: Mental Health](https://www.who.int/health-topics/mental-health)

    - 🎥 [TED Talks on Mental Health](https://www.ted.com/topics/mental-health)

    - 💚 [Tele-MANAS India](https://telemanas.mohfw.gov.in/)
    """)

# ---------------- EMERGENCY HELP ----------------
elif page == "Emergency Help":

    st.title("🚨 Emergency Help")

    st.warning(
        "If you are experiencing a mental health crisis, "
        "please reach out for immediate support."
    )

    st.markdown("""
    ### 🇮🇳 India

    - 📞 **112** – National Emergency Number
    - 📞 **14416** – Tele-MANAS Mental Health Helpline (24/7)
    - 📞 **1800-891-4416** – Tele-MANAS alternate number

    ### 🇺🇸 USA

    - 📞 **988** – Suicide & Crisis Lifeline

    ### 🇬🇧 UK & Ireland

    - 📞 **116 123** – Samaritans

    """)

    st.info(
        "If you are in immediate danger, contact emergency services "
        "and reach out to a trusted person nearby."
    )

# ---------------- ABOUT ----------------
elif page == "About":

    st.title("ℹ️ About This Platform")

    st.write("""
    This is an **AI-powered Youth Mental Wellness Platform**
    built using Python, Streamlit and Generative AI.

    ### Features

    ✅ AI-powered mental wellness chatbot

    ✅ Helpful mental health resources

    ✅ Emergency contact information

    ✅ Crisis keyword detection

    ✅ Supportive and stigma-free environment

    ### Technologies Used

    - Python
    - Streamlit
    - OpenAI API
    - Generative AI

    ⚠️ **Disclaimer:**

    This application provides general emotional support and
    educational information. It is not a substitute for
    professional mental health care, diagnosis or treatment.

    Please avoid sharing sensitive personal information.
    """)

