import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from utils import calculate_carbon, ai_suggestion

st.set_page_config(page_title="AI Carbon Dashboard", layout="wide")

st.title("🌍 AI Carbon Footprint Dashboard")
st.markdown("Calculate, Analyze & Get AI Voice Guidance")

# Sidebar
st.sidebar.header("Enter Daily Usage")

transport_km = st.sidebar.slider("🚗 Travel Distance (km/day)", 0, 300, 20)
electricity_kwh = st.sidebar.slider("⚡ Electricity Usage (kWh/day)", 0, 50, 5)
meat_meals = st.sidebar.slider("🍖 Meat-based Meals/day", 0, 5, 1)

# Calculate
emissions = calculate_carbon(transport_km, electricity_kwh, meat_meals)

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Transport", f"{emissions['Transport']:.2f} kg")
col2.metric("Electricity", f"{emissions['Electricity']:.2f} kg")
col3.metric("Food", f"{emissions['Food']:.2f} kg")
col4.metric("Total", f"{emissions['Total']:.2f} kg")

st.divider()

# Charts
df = pd.DataFrame({
    "Category": ["Transport", "Electricity", "Food"],
    "Emissions": [
        emissions["Transport"],
        emissions["Electricity"],
        emissions["Food"]
    ]
})

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(px.bar(df, x="Category", y="Emissions", color="Category"),
                    use_container_width=True)

with col6:
    st.plotly_chart(px.pie(df, values="Emissions", names="Category"),
                    use_container_width=True)

st.divider()

# Rating
st.subheader("Sustainability Rating")

if emissions["Total"] < 10:
    st.success("Low Carbon Footprint 🌱")
elif emissions["Total"] < 25:
    st.warning("Moderate Emissions ⚠️")
else:
    st.error("High Carbon Footprint 🚨")

st.divider()

# CSV Upload
st.subheader("Upload CSV for Analysis")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

    if {"Transport", "Electricity", "Food"}.issubset(data.columns):
        data["Total"] = data["Transport"] + data["Electricity"] + data["Food"]
        st.plotly_chart(px.line(data, y="Total", title="Uploaded Emission Trend"),
                        use_container_width=True)
    else:
        st.warning("CSV must contain: Transport, Electricity, Food columns")

st.divider()

# ---------------- AI Assistant ----------------
st.subheader("🤖 AI Voice Assistant")

ai_response = ai_suggestion(emissions)

st.info(ai_response)

# Voice + Conversational Interface
voice_html = f"""
<button onclick="startRecognition()">🎤 Ask AI</button>
<p id="speechText"></p>

<script>
function startRecognition() {{
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {{
        var speech = event.results[0][0].transcript;
        document.getElementById("speechText").innerHTML = "You said: " + speech;

        var response = "{ai_response}";
        var utterance = new SpeechSynthesisUtterance(response);
        speechSynthesis.speak(utterance);
    }};
}}
</script>
"""

components.html(voice_html, height=150)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | AI without API")

