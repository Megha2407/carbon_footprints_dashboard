import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Carbon Intelligence AI", layout="wide")

# -------------------- CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}
h1 { color: #1f4e79; }
</style>
""", unsafe_allow_html=True)

# -------------------- Logic --------------------
def calculate_carbon(t, e, m):
    transport = t * 0.21
    electricity = e * 0.82
    food = m * 2.5
    total = transport + electricity + food
    return transport, electricity, food, total

def conversational_ai(user_text, transport, electricity, food, total):
    text = user_text.lower()

    if "reduce" in text or "improve" in text:
        return "To reduce emissions, try lowering travel distance and reducing electricity usage."

    elif "transport" in text:
        return f"Your transport emission is {transport:.2f} kg. Consider public transport or carpooling."

    elif "electricity" in text:
        return f"Electricity contributes {electricity:.2f} kg. Switch to energy-efficient appliances."

    elif "food" in text or "meat" in text:
        return f"Food emission is {food:.2f} kg. Reducing meat meals can help lower this."

    elif "total" in text or "overall" in text:
        return f"Your total emission is {total:.2f} kg CO2 per day."

    elif "high" in text:
        if total > 25:
            return "Yes, your emissions are high. Major reduction is recommended."
        else:
            return "Your emissions are not critically high, but improvement is possible."

    else:
        return "I can help you analyze transport, electricity, food or total emissions. Please ask clearly."

# -------------------- UI --------------------
st.title("🌍 Carbon Intelligence Dashboard with AI Voice Assistant")

st.sidebar.header("Enter Daily Usage")

t = st.sidebar.slider("🚗 Travel (km/day)", 0, 300, 20)
e = st.sidebar.slider("⚡ Electricity (kWh/day)", 0, 50, 5)
m = st.sidebar.slider("🍖 Meat meals/day", 0, 5, 1)

transport, electricity, food, total = calculate_carbon(t, e, m)

# -------------------- Metrics --------------------
col1, col2, col3, col4 = st.columns(4)

for col, label, value in zip(
    [col1, col2, col3, col4],
    ["Transport", "Electricity", "Food", "Total"],
    [transport, electricity, food, total]
):
    col.markdown(f"""
    <div class="metric-card">
        <h3>{label}</h3>
        <h2>{value:.2f} kg</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -------------------- Charts --------------------
df = pd.DataFrame({
    "Category": ["Transport", "Electricity", "Food"],
    "Emissions": [transport, electricity, food]
})

col5, col6 = st.columns(2)
col5.plotly_chart(px.bar(df, x="Category", y="Emissions", color="Category"),
                  use_container_width=True)

col6.plotly_chart(px.pie(df, values="Emissions", names="Category", hole=0.4),
                  use_container_width=True)

st.divider()

# -------------------- Rating --------------------
if total < 10:
    st.success("Low Carbon Footprint 🌱")
elif total < 25:
    st.warning("Moderate Emissions ⚠️")
else:
    st.error("High Carbon Footprint 🚨")

st.divider()

# -------------------- Voice Conversational Assistant --------------------
st.subheader("🎙 Conversational AI Voice Assistant")

voice_html = f"""
<button onclick="startRecognition()">🎤 Speak</button>
<p id="userText"></p>

<script>
function startRecognition() {{
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {{
        var userSpeech = event.results[0][0].transcript;
        document.getElementById("userText").innerHTML = "You said: " + userSpeech;

        fetch('/?_user_query=' + userSpeech)
    }};
}}
</script>
"""

components.html(voice_html, height=120)

# Text-based fallback (important)
user_input = st.text_input("Or type your question:")

if user_input:
    response = conversational_ai(user_input, transport, electricity, food, total)
    st.info(response)

    components.html(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{response}");
    speechSynthesis.speak(msg);
    </script>
    """, height=0)
