import streamlit as st
import os

# Toggle between mock and real OpenAI
USE_MOCK = True  

def get_ai_response(user_input):
    if USE_MOCK:
        # Mocked response for local testing
        return f"(Mock) I understand you said: '{user_input}'. This is a placeholder AI reply."
    else:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a supportive assistant for youth wellness."},
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message["content"]

# ------------------- Streamlit UI -------------------

st.set_page_config(page_title="Youth Wellness Chatbot", page_icon="💬")

st.title("💬 Youth Wellness Chatbot")
st.write("A confidential AI-powered space to share your thoughts.")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
if user_input := st.chat_input("How are you feeling today?"):
    # Store user input
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user input
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    ai_reply = get_ai_response(user_input)

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_reply)
