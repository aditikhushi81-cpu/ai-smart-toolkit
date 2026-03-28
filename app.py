from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import speech_recognition as sr

from collections import Counter

from modules.scam_detector import detect_scam
from modules.code_debugger import debug_code
from modules.statement_analyzer import analyze_statement
from modules.text_analyzer import analyze_text
#from modules.body_language import analyze_body_language

# 🔥 Page config
st.set_page_config(page_title="AI Smart Toolkit", layout="wide")

# 🎨 Modern UI
st.markdown("""
<style>
body {
    background-color: #0f1117;
}
.title {
    font-size: 42px;
    text-align: center;
    color: white;
    font-weight: bold;
}
.card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🚀 Title
st.markdown('<div class="title">🚀 AI Smart Toolkit</div>', unsafe_allow_html=True)

# 📌 Sidebar
st.sidebar.title("🧠 Toolkit Panel")

option = st.sidebar.selectbox(
    "Choose Tool",
    ["Scam Detector", "Code Debugger", "Statement Analyzer", "Text Analyzer"]
)

# 🗑 Clear history
if st.sidebar.button("🗑 Clear History"):
    st.session_state.messages = []
    st.session_state.history = []

# 📜 History
st.sidebar.subheader("📜 History")
if "history" not in st.session_state:
    st.session_state.history = []

for item in st.session_state.history[-5:]:
    st.sidebar.write(f"• {item[0]}")

# 📊 SIDEBAR ANALYTICS
st.sidebar.markdown("## 📊 Usage Analytics")

total_queries = len(st.session_state.history)
tool_counts = Counter([item[0] for item in st.session_state.history])

st.sidebar.write(f"Total Queries: {total_queries}")

if tool_counts:
    most_used = tool_counts.most_common(1)[0][0]
    st.sidebar.write(f"Most Used: {most_used}")

# 🎤 Voice Input
def voice_input():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Speak now...")
            audio = r.listen(source)
        return r.recognize_google(audio)
    except:
        return "❌ Voice not supported"

# 💎 TOP DASHBOARD CARDS
colA, colB, colC = st.columns(3)

with colA:
    st.markdown(f'<div class="card">📊 Total Queries<br><h2>{total_queries}</h2></div>', unsafe_allow_html=True)

with colB:
    st.markdown(f'<div class="card">🛠 Active Tool<br><h2>{option}</h2></div>', unsafe_allow_html=True)

with colC:
    last_conf = "0%"
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        last_msg = st.session_state.messages[-1]
        if isinstance(last_msg[1], dict):
            last_conf = last_msg[1].get("Confidence", "0%")

    st.markdown(f'<div class="card">🎯 Last Confidence<br><h2>{last_conf}</h2></div>', unsafe_allow_html=True)

# 💬 CHAT SYSTEM
if True:

    if "messages" not in st.session_state:
        st.session_state.messages = []

    col1, col2 = st.columns([5,1])

    with col1:
        user_input = st.chat_input("💬 Type your message...")

    with col2:
        if st.button("🎤"):
            user_input = voice_input()

    if user_input:

        st.session_state.messages.append(("user", user_input))

        with st.spinner("🤖 AI is thinking..."):

            if option == "Scam Detector":
                result = detect_scam(user_input)

            elif option == "Code Debugger":
                result = debug_code(user_input)

            elif option == "Statement Analyzer":
                result = analyze_statement(user_input)

            elif option == "Text Analyzer":
                result = analyze_text(user_input)

        st.session_state.messages.append(("assistant", result))
        st.session_state.history.append((option, user_input))

    # 💬 DISPLAY CHAT
    for i, (role, msg) in enumerate(st.session_state.messages):

        with st.chat_message(role):

            if isinstance(msg, dict):

                st.markdown("## 🤖 AI Analysis Dashboard")

                result = msg.get("Result", "")
                reason = msg.get("Reason", "")
                confidence = msg.get("Confidence", "0%")

                confidence_value = int(confidence.replace("%", ""))

                if "Unrealistic" in result:
                    st.error(f"❌ {result}")
                else:
                    st.success(f"✅ {result}")

                st.markdown(f"🧠 **Reason:** {reason}")

                progress_bar = st.progress(0)
                for i in range(confidence_value + 1):
                    progress_bar.progress(i)

                st.markdown(f"📊 **Confidence:** {confidence}")

                # 🎯 Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=confidence_value,
                    title={'text': "AI Confidence"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "green" if confidence_value > 70 else "red"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ff4d4d"},
                            {'range': [50, 80], 'color': "#ffd11a"},
                            {'range': [80, 100], 'color': "#33cc33"}
                        ]
                    }
                ))

                st.plotly_chart(fig, use_container_width=True, key=f"gauge_{role}_{id(msg)}")

            else:
                st.write(msg)

# 📊 TEXT ANALYZER CHART
if option == "Text Analyzer" and len(st.session_state.messages) > 0:

    last_msg = st.session_state.messages[-1]

    if last_msg[0] == "assistant" and isinstance(last_msg[1], dict):

        sentiment = last_msg[1].get("Sentiment Score", 0)
        subjectivity = last_msg[1].get("Subjectivity", 0)

        data = {
            "Metric": ["Sentiment", "Subjectivity"],
            "Score": [sentiment, subjectivity]
        }

        fig = px.bar(
            data,
            x="Metric",
            y="Score",
            color="Metric",
            title="📊 AI Text Analysis Dashboard",
            text="Score"
        )

        st.plotly_chart(fig, use_container_width=True, key="text_chart")
# 📈 TOOL USAGE CHART
if tool_counts:
    st.markdown("## 📈 Tool Usage Overview")

    tools = list(tool_counts.keys())
    counts = list(tool_counts.values())

    fig = px.pie(
        names=tools,
        values=counts,
        title="Tool Usage Distribution"
    )

    st.plotly_chart(fig, use_container_width=True, key=str(id(fig)))

