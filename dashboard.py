import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Momentum Intelligence Platform")

# -----------------------------
# Mock Data
# -----------------------------
data = [
    {
        "name": "YouTube",
        "trajectory": [12, 18, 25],
        "current_score": 25,
        "change": 7,
        "signals": [
            {"signal": "github_spike", "date": "2026-03-11"},
            {"signal": "beta_launch", "date": "2026-03-12"},
            {"signal": "hiring_surge", "date": "2026-03-12"}
        ]
    },
    {
        "name": "NovaAI",
        "trajectory": [10, 15, 20],
        "current_score": 20,
        "change": 5,
        "signals": [
            {"signal": "domain_registration", "date": "2026-02-10"},
            {"signal": "social_buzz", "date": "2026-02-15"}
        ]
    },
    {
        "name": "QuantumForge",
        "trajectory": [8, 14, 21],
        "current_score": 21,
        "change": 7,
        "signals": [
            {"signal": "github_spike", "date": "2026-01-20"},
            {"signal": "media_mention", "date": "2026-01-25"}
        ]
    }
]

df = pd.DataFrame(data)

# -----------------------------
# Helper Functions
# -----------------------------
def momentum_to_temperature(score):
    if score < 8:
        return "❄️ Cold"
    elif score < 15:
        return "🌤 Getting Warm"
    elif score < 21:
        return "🔥 Warmer"
    else:
        return "🚀 Hot"

signal_emoji = {
    "github_spike": "🔥",
    "beta_launch": "🚀",
    "hiring_surge": "💼",
    "domain_registration": "📄",
    "social_buzz": "📢",
    "media_mention": "📰"
}

colors = {
    "YouTube": "gold",
    "NovaAI": "green",
    "QuantumForge": "lime"
}

# -----------------------------
# Leader Detection
# -----------------------------
top_companies = df.sort_values("current_score", ascending=False)
today_leader = top_companies.iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Today's Leader", f"{today_leader['name']}", today_leader["current_score"])
col2.metric("Weekly Leader", f"{top_companies.iloc[0]['name']}", sum(top_companies.iloc[0]["trajectory"]))
col3.metric("Biggest Jump", f"{top_companies.iloc[0]['name']}", top_companies.iloc[0]["change"])

st.divider()

# -----------------------------
# Plotly Chart
# -----------------------------
fig = go.Figure()

for idx, row in df.iterrows():
    x_values = [0, 1, 2]  # Q1, Q2, Q3
    y_values = row["trajectory"]

    hover_text = "<br>".join([f"{signal_emoji.get(s['signal'], '')} {s['signal'].replace('_', ' ').title()}: {s['date']}" for s in row["signals"]])

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode="lines+markers",
        name=row["name"],
        line=dict(color=colors.get(row["name"], "white"), width=4 if idx == 0 else 2),
        hovertemplate=f"<b>{row['name']}</b><br>Momentum: %{y}<br>{hover_text}<extra></extra>"
    ))

fig.update_xaxes(tickvals=[0, 1, 2], ticktext=['Q1', 'Q2', 'Q3'])
fig.update_layout(
    height=600,
    template="plotly_dark",
    title="Startup Momentum Field",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Leaderboard Panel
# -----------------------------
st.subheader("Top Momentum Startups")
for idx, row in top_companies.iterrows():
    temp = momentum_to_temperature(row["current_score"])
    leader_emoji = "🏆" if idx == 0 else ""
    st.write(f"{leader_emoji} {idx + 1}. {row['name']} | CS={row['current_score']} | Δ={row['change']} | {temp}")

# -----------------------------
# Emerging Signals / Newly Detected
# -----------------------------
emerging_signals = [
    {"name": "QuantumForge", "signal": "Media Mention", "date": "2026-01-25"},
    {"name": "NovaAI", "signal": "Social Buzz", "date": "2026-02-15"}
]

newly_detected = [
    {"name": "NovaAI", "date": "2026-02-10"},
    {"name": "YouTube", "date": "2026-03-11"}
]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Emerging Signals")
    for company in emerging_signals:
        st.write(f"{company['name']} | {company['signal']} | {company['date']}")

with col2:
    st.subheader("Newly Detected Startups")
    for company in newly_detected:
        st.write(f"{company['name']} | Detected on {company['date']}")
