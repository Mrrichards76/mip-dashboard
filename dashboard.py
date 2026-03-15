import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import datetime

# -------------------------
# 1️⃣ Connect to the database and pull signals
# -------------------------
conn = sqlite3.connect("mip_live.db")
df_signals = pd.read_sql_query("SELECT * FROM signals", conn)
conn.close()

# -------------------------
# 2️⃣ Calculate momentum trajectories for each company
# -------------------------
momentum_data = []

for company in df_signals["company"].unique():
    company_signals = df_signals[df_signals["company"] == company].sort_values("timestamp")
    trajectory = company_signals["strength"].cumsum().tolist()
    current_score = trajectory[-1]
    change = trajectory[-1] - trajectory[0] if len(trajectory) > 1 else trajectory[0]

    momentum_data.append({
        "company": company,
        "trajectory": trajectory,
        "current_score": current_score,
        "change": change
    })

df_momentum = pd.DataFrame(momentum_data)

# -------------------------
# 3️⃣ Streamlit Dashboard Layout
# -------------------------
st.title("Momentum Intelligence Platform")

# Optional: Top metrics (Today’s Leader, Weekly Leader, Biggest Jump)
if not df_momentum.empty:
    today_leader = df_momentum.sort_values("current_score", ascending=False).iloc[0]
    biggest_jump = df_momentum.sort_values("change", ascending=False).iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Today's Leader", f"{today_leader['company']}", today_leader["current_score"])
    col2.metric("Biggest Jump", f"{biggest_jump['company']}", biggest_jump["change"])

st.divider()

# -------------------------
# 4️⃣ Jagged Lines Chart
# -------------------------
fig = go.Figure()

for idx, row in df_momentum.iterrows():
    x_values = list(range(len(row["trajectory"])))  # Q1, Q2, Q3, Q4
    y_values = row["trajectory"]

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode="lines+markers",
        name=row["company"],
        line=dict(width=3),
        hovertemplate=f"<b>{row['company']}</b><br>Momentum: %{{y}}<extra></extra>"
    ))

fig.update_xaxes(tickvals=[0,1,2,3], ticktext=["Q1","Q2","Q3","Q4"])
fig.update_layout(
    title="Startup Momentum Field",
    height=600,
    template="plotly_dark"
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# 5️⃣ Top Momentum Startups Table
# -------------------------
st.subheader("Top Momentum Startups")

df_top = df_momentum.sort_values("current_score", ascending=False).head(10)
st.table(df_top[["company", "current_score", "change"]])
