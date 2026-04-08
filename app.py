import streamlit as st

# ✅ Page config FIRST
st.set_page_config(page_title="Outbreak Detection", layout="wide")

# ✅ SAFE UI DESIGN (works in light + dark)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111 !important;
    }

    /* Cards */
    [data-testid="metric-container"], .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import pandas as pd
import matplotlib.pyplot as plt
import base64

# 🔊 Sound function
def play_alert_sound():
    with open("alert.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

        md = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# 🦠 Title
st.title("🦠 Disease Outbreak Detection System")
st.caption("AI-powered early detection and monitoring system")

# 📂 Load data
data = pd.read_csv("data.csv")

# 🎛 Sidebar
st.sidebar.title("⚙️ Controls")

# 📍 Location
location = st.sidebar.selectbox(
    "📍 Select Location",
    data["Location"].unique()
)

# 🦠 Disease
disease = st.sidebar.selectbox(
    "🦠 Select Symptom",
    ["Fever", "Cough", "Flu"]
)

# 📅 Day Range
day_range = st.sidebar.slider(
    "📅 Select Day Range",
    int(data["Day"].min()),
    int(data["Day"].max()),
    (1, 5)
)

# 🔊 Sound toggle
sound_on = st.sidebar.checkbox("🔊 Enable Alert Sound", value=True)

# 🔍 Filter data
filtered_data = data[
    (data["Location"].str.lower() == location.lower()) &
    (data["Day"] >= day_range[0]) &
    (data["Day"] <= day_range[1])
]

filtered_data = filtered_data.reset_index(drop=True)

# ❗ No data check
if filtered_data.empty:
    st.error("No data available for selected filters")
    st.stop()

# 📊 Metrics
colA, colB, colC = st.columns(3)

with colA:
    st.metric("Average", round(filtered_data[disease].mean(), 2))

with colB:
    st.metric("Maximum", filtered_data[disease].max())

with colC:
    st.metric("Minimum", filtered_data[disease].min())

st.divider()

# 📊 Graph + Alerts
col1, col2 = st.columns([2, 1])

# 📈 Graph
with col1:
    st.subheader(f"📊 {disease} Trend")

    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(filtered_data["Day"], filtered_data[disease], marker='o')

    ax.set_xticks(filtered_data["Day"])
    ax.set_xlabel("Day")
    ax.set_ylabel(f"{disease} Cases")
    ax.set_title(f"{disease} Trend Over Days")

    st.pyplot(fig)

# 🚨 Alerts
with col2:
    st.subheader("🚨 Alerts")

    for i in range(len(filtered_data)):
        value = filtered_data[disease][i]

        if value >= 20:
            st.error(f"🔴 Day {filtered_data['Day'][i]}: {value} cases")
        elif value >= 12:
            st.warning(f"🟠 Day {filtered_data['Day'][i]}: {value} cases")
        else:
            st.success(f"🟢 Day {filtered_data['Day'][i]}: {value} cases")

st.divider()

# 🤖 AI Analysis
st.subheader("🤖 AI Analysis")

high_cases = sum(filtered_data[disease] >= 20)

if high_cases >= 2:
    st.error("🚨 High outbreak probability detected!")
    if sound_on:
        play_alert_sound()

elif high_cases == 1:
    st.warning("⚠️ Moderate risk detected. Monitoring required.")
else:
    st.success("✅ Situation is under control.")

# 📌 Insights
st.subheader("📌 Insights")

st.write(f"📍 Location: **{location}**")
st.write(f"🦠 Symptom: **{disease}**")
st.write(f"📅 Days: {day_range[0]} to {day_range[1]}")
st.write(f"📊 Records: {len(filtered_data)}")