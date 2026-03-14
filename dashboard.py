

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Momentum Intelligence Platform", layout="wide")

# -----------------------------
# MOCK DATA
# -----------------------------

startups = ["NovaAI", "StealthGen", "DevSync", "Ecospark", "FlexLab", "QuantumQ"]

x = ["Q1", "Q2", "Q3", "Q4"]

data = {
    s: np.cumsum(np.random.randint(5, 20, 4)) for s in startups
}

# -----------------------------
# HEADER
# -----------------------------

st.title("Momentum Intelligence Platform (MIp)")

# -----------------------------
# TOP MOMENTUM LEADER CARD
# -----------------------------

leader_container = st.container()

with leader_container:
    col1, col2, col3 = st.columns([1,4,1])

    with col2:
        st.markdown("### Top Momentum Leader Today")

        leader_cols = st.columns([1,4,2])

        with leader_cols[0]:
            st.image("https://cdn-icons-png.flaticon.com/512/906/906175.png", width=60)

        with leader_cols[1]:
            st.markdown("## NovaAI")
            st.markdown("Score: **85**  \n Rising")

        with leader_cols[2]:
            sparkline = go.Figure()
            sparkline.add_trace(go.Scatter(
                y=np.cumsum(np.random.randint(0,5,20)),
                mode="lines"
            ))

            sparkline.update_layout(
                height=80,
                margin=dict(l=0,r=0,t=0,b=0),
                xaxis_visible=False,
                yaxis_visible=False
            )

            st.plotly_chart(sparkline, use_container_width=True)


st.divider()

# -----------------------------
# TOP MOMENTUM STARTUPS PANEL
# -----------------------------

panel = st.container()

with panel:

    header_cols = st.columns([4,1,1])

    with header_cols[0]:
        st.subheader("Top Momentum Startups")

    with header_cols[1]:
        st.button("🔥 Trending Badge")

    with header_cols[2]:
        st.button("Share")

    layout = st.columns([1,4])

    # -----------------------------
    # FILTER SIDEBAR
    # -----------------------------

    with layout[0]:

        st.markdown("#### Filters")

        st.markdown("**Show**")
        st.radio("", ["All", "Top N", "Newly Detected"], label_visibility="collapsed")

        st.markdown("**Sector**")
        st.checkbox("AI")
        st.checkbox("Dev Tools")

        st.markdown("**Signals**")
        st.checkbox("GitHub")
        st.checkbox("Product Hunt")
        st.checkbox("X / Twitter")

    # -----------------------------
    # MOMENTUM CHART
    # -----------------------------

    with layout[1]:

        fig = go.Figure()

        for s in startups:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=data[s],
                    mode="lines+markers",
                    name=s
                )
            )

        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Signals Detected: GitHub spikes, media buzz, hiring growth"
        )

st.divider()

# -----------------------------
# LOWER PANELS
# -----------------------------

lower = st.columns(2)

# -----------------------------
# EMERGING SIGNALS
# -----------------------------

with lower[0]:

    st.subheader("Emerging Signals (Premium)")

    signals = [
        ("StealthGen", "Stealth launch seeing spikes in GitHub", "Surging"),
        ("NeuronForge", "Hot startup trending on X", "Surging"),
        ("AetherScale", "Gaining traction with investors", "Surging")
    ]

    for s in signals:

        row = st.columns([3,1,1])

        with row[0]:
            st.markdown(f"**{s[0]}**")
            st.caption(s[1])

        with row[1]:
            st.success(s[2])

        with row[2]:
            st.button("Chart", key=s[0])


# -----------------------------
# NEWLY DETECTED STARTUPS
# -----------------------------

with lower[1]:

    st.subheader("Newly Detected Startups (Premium)")

    new = [
        ("SkyLoom", "Added 1h ago"),
        ("Byteshift", "Added 2h ago"),
        ("EcoWave", "Added 2h ago")
    ]

    for n in new:

        row = st.columns([3,1])

        with row[0]:
            st.markdown(f"**{n[0]}**")
            st.caption(n[1])

        with row[1]:
            st.button("Chart", key=n[0])


st.divider()

# -----------------------------
# FOOTER METRICS BAR
# -----------------------------

footer = st.columns(3)

with footer[0]:
    st.metric("Tracked Startups", "1,254", "+23")

with footer[1]:
    st.metric("Avg Momentum Score", "62", "+5")

with footer[2]:
    st.metric("Top Movers This Week", "12", "🔥")

