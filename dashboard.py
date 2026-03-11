import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Momentum Intelligence Platform", layout="wide")

st.title("Momentum Intelligence Platform")

# Connect to database
conn = sqlite3.connect("live.db")
df = pd.read_sql_query("SELECT * FROM startups", conn)

# Convert trajectory string to list
df["trajectory"] = df["trajectory"].apply(eval)

# Calculate metrics
df["current_score"] = df["trajectory"].apply(lambda x: x[-1])
df["previous_score"] = df["trajectory"].apply(lambda x: x[-2] if len(x) > 1 else x[-1])
df["change"] = df["current_score"] - df["previous_score"]

# Leader detection
today_leader = df.sort_values("current_score", ascending=False).iloc[0]
weekly_leader = df.assign(weekly=df["trajectory"].apply(sum)).sort_values("weekly", ascending=False).iloc[0]
biggest_jump = df.sort_values("change", ascending=False).iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Today's Leader", f"{today_leader['name']}", today_leader["current_score"])
col2.metric("Weekly Leader", f"{weekly_leader['name']}", sum(weekly_leader["trajectory"]))
col3.metric("Biggest Jump", f"{biggest_jump['name']}", biggest_jump["change"])

st.divider()

# Momentum chart
fig = go.Figure()

for _, row in df.iterrows():

    trajectory = row["trajectory"]

    color = "blue"

    if row["name"] == today_leader["name"]:
        color = "gold"
    elif row["change"] > 0:
        color = "green"
    elif row["change"] < 0:
        color = "red"

    fig.add_trace(
        go.Scatter(
            y=trajectory,
            mode="lines",
            name=row["name"],
            line=dict(color=color, width=3)
        )
    )

fig.update_layout(
    height=600,
    template="plotly_dark",
    title="Startup Momentum Field"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Momentum Startups")

leaderboard = df.sort_values("current_score", ascending=False)[["name", "current_score", "change"]]
leaderboard.index = range(1, len(leaderboard) + 1)

st.dataframe(leaderboard)
