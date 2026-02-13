import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Everyday Carbon Savings Tracker", layout="wide")

# ===============================
# ECO THEME CSS
# ===============================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f3d2e, #14532d);
    color: white;
}
.metric-card {
    background-color: #1b4332;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}
.metric-card h3 { color: #74c69d; }
.metric-card h2 { color: white; font-weight: bold; }
.section-title {
    color: #95d5b2;
    font-size: 22px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# EMISSION FACTORS
# ===============================
EMISSION_FACTORS = {
    "Transportation": 2.3,
    "Food": 6,
    "Shopping": 25,
    "Utilities": 0.4,
    "Entertainment": 3,
    "Public Transport": 0.1
}

# ===============================
# SAMPLE DATA
# ===============================
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        ["Gasoline", "Transportation", 10],
        ["Restaurant", "Food", 1],
        ["Clothing", "Shopping", 1],
        ["Electricity Bill", "Utilities", 50],
        ["Movie", "Entertainment", 1],
        ["Bus Ride", "Public Transport", 15]
    ], columns=["Description", "Category", "Amount"])

# ===============================
# CALCULATION FUNCTION
# ===============================
def calculate_carbon(row):
    factor = EMISSION_FACTORS.get(row["Category"], 1)
    return row["Amount"] * factor

def generate_suggestion(category):
    suggestions = {
        "Transportation": "Consider carpooling, cycling, or electric vehicles.",
        "Food": "Choose plant-based meals or cook at home.",
        "Shopping": "Buy sustainable brands or second-hand items.",
        "Utilities": "Switch to LED lights and renewable energy.",
        "Entertainment": "Choose local outdoor activities.",
        "Public Transport": "Great choice! Continue using shared transport."
    }
    return suggestions.get(category, "Adopt eco-friendly habits.")

def conversational_ai(user_text, total):
    text = user_text.lower()
    if "reduce" in text:
        return "To reduce emissions, focus on transportation and shopping habits."
    elif "total" in text:
        return f"Your current total footprint is {total:.2f} kg CO2e."
    elif "food" in text:
        return "Reducing meat consumption significantly lowers footprint."
    elif "transport" in text:
        return "Switching to public transport reduces emissions drastically."
    else:
        return "Ask about reducing, total footprint, food, or transport."

# ===============================
# HEADER
# ===============================
st.title("🌍 Everyday Carbon Savings Tracker")
st.markdown("Supporting SDG 12 & SDG 13 – Responsible Consumption & Climate Action")

# ===============================
# ADD EXPENSE
# ===============================
st.markdown('<div class="section-title">➕ Add Expense</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

description = col1.text_input("Description")
category = col2.selectbox("Category", list(EMISSION_FACTORS.keys()))
amount = col3.number_input("Amount (units)", min_value=0.0)

if st.button("Add Expense"):
    new_row = pd.DataFrame([[description, category, amount]],
                           columns=["Description", "Category", "Amount"])
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_row], ignore_index=True
    )

# ===============================
# CALCULATE FOOTPRINT
# ===============================
df = st.session_state.expenses.copy()
df["Carbon (kg CO2e)"] = df.apply(calculate_carbon, axis=1)

total_carbon = df["Carbon (kg CO2e)"].sum()

# ===============================
# DASHBOARD METRICS
# ===============================
st.markdown('<div class="section-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)

colA, colB = st.columns(2)

colA.markdown(f"""
<div class="metric-card">
<h3>Total Carbon Footprint</h3>
<h2>{total_carbon:.2f} kg CO2e</h2>
</div>
""", unsafe_allow_html=True)

avg = 50
comparison = total_carbon - avg

colB.markdown(f"""
<div class="metric-card">
<h3>Comparison to Average</h3>
<h2>{comparison:.2f} kg</h2>
</div>
""", unsafe_allow_html=True)

# ===============================
# CHARTS
# ===============================
st.markdown('<div class="section-title">📈 Category Breakdown</div>', unsafe_allow_html=True)

category_summary = df.groupby("Category")["Carbon (kg CO2e)"].sum().reset_index()

colC, colD = st.columns(2)

colC.plotly_chart(px.pie(category_summary,
                         values="Carbon (kg CO2e)",
                         names="Category"),
                  use_container_width=True)

colD.plotly_chart(px.bar(category_summary,
                         x="Category",
                         y="Carbon (kg CO2e)",
                         color="Category"),
                  use_container_width=True)

# ===============================
# SUSTAINABLE ALTERNATIVES
# ===============================
st.markdown('<div class="section-title">🌱 Sustainable Alternatives</div>', unsafe_allow_html=True)

for cat in category_summary["Category"]:
    st.info(f"{cat}: {generate_suggestion(cat)}")

# ===============================
# VOICE ASSISTANT
# ===============================
st.markdown('<div class="section-title">🎙 AI Voice Assistant</div>', unsafe_allow_html=True)

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
    }};
}}
</script>
"""
components.html(voice_html, height=120)

user_input = st.text_input("Or type your question:")

if user_input:
    response = conversational_ai(user_input, total_carbon)
    st.success(response)
    components.html(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{response}");
    speechSynthesis.speak(msg);
    </script>
    """, height=0)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("🌿 Hackathon Ready | Clean UI | SDG Aligned | Deployable")
