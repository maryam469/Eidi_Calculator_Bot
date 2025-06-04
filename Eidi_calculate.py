import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load Groq API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

# Page settings
st.set_page_config(page_title="Eidi Calculator Bot", layout="centered")
st.balloons()
# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar inputs
with st.sidebar:
    st.title("Eidi Calculator Bot")
    st.markdown("Batao ab tak kis kis se Eidi mili:")

    known_people = st.number_input("Kitne logon se Eidi mili?", min_value=0, max_value=50, step=1)
    avg_amount = st.number_input("Average Eidi per person (Rs)", min_value=0, max_value=1000, step=10)

    st.markdown("---")
    st.markdown("Ab estimate karte hain:")

    age = st.number_input("Aap ki Umar", min_value=1, max_value=30, step=1)
    uncles_aunties = st.number_input("Uncles/Aunties abhi bache hain?", min_value=0, max_value=30, step=1)
    
    calc_btn = st.button("Final Eidi Prediction")

# Main Title
st.markdown("<h1 style='text-align:center; color:white;'>Eid Eidi Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Find out how much Eidi you might get this Eid!</p><hr>", unsafe_allow_html=True)

# Calculation and API Call
if calc_btn:
    # Basic calculations
    known_eidi = known_people * avg_amount
    estimated_remaining = (age * 50) + (uncles_aunties * 100)
    total_estimate = known_eidi + estimated_remaining

    # User prompt
    user_prompt = (
        f"Aik bacha {age} saal ka hai. Usay ab tak {known_people} logon se average {avg_amount} rupees ki Eidi mili hai "
        f"(total {known_eidi} rupees). Us ke {uncles_aunties} uncle/aunty abhi bache hain. "
        f"Tum batain ke usay Eid pe total kitni Eidi mil sakti hai — pyaar aur mazak se. Estimate total with short and clear answer: {total_estimate} rupees."
    )

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # API request to Groq
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": st.session_state.messages,
            "temperature": 0.7
        }
    )

    # Response Handling
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.success("🎉 Here's your Eidi prediction!")
        st.balloons()
        st.markdown(
            f"<div style='background-color:#f0f0f0;padding:10px;border-radius:10px;color:black;"
            f"font-family:ubuntu;font-weight:bold;font-size:15px;'><b>{reply}</b></div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Something went wrong! Please check your API key or try again.")


