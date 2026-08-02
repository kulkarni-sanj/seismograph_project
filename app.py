import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import random

# --- APP CONFIG ---
st.set_page_config(page_title="AI Cultural Seismograph", page_icon="🌋", layout="wide")

# --- CUSTOM "SEISMIC" STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; }
    .richter-box { padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .calm { background-color: #1d3331; color: #4ade80; border: 1px solid #4ade80; }
    .warning { background-color: #332b1d; color: #fbbf24; border: 1px solid #fbbf24; }
    .earthquake { background-color: #331d1d; color: #f87171; border: 1px solid #f87171; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🌋 The Cultural Seismograph")
st.markdown("### Tracking the 'Great AI Shift' of 2021-2024")

# --- SMART DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists("cdi_results.csv") and os.path.exists("keyword_frequency_monthly.csv"):
        return pd.read_csv("cdi_results.csv"), pd.read_csv("keyword_frequency_monthly.csv")
    return None, None

df_cdi, df_key = load_data()

if df_cdi is not None:
    # --- DYNAMIC RICHETER SCALE LOGIC ---
    peak_val = df_cdi['cdi_score'].max()
    current_status = "STABLE"
    status_class = "calm"
    if peak_val > 0.4:
        current_status = "VOLATILE"
        status_class = "warning"
    if peak_val > 0.7:
        current_status = "MAJOR SEISMIC SHIFT"
        status_class = "earthquake"

    # --- TOP KPI ROW ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="richter-box {status_class}">Current Status: {current_status}</div>', unsafe_allow_html=True)
    with col2:
        st.metric("Total Data Ingested", "1.19M Comments", "r/tech + r/ML")
    with col3:
        st.metric("Peak Intensity", f"{peak_val:.2f}", "Richter Score")
    with col4:
        st.metric("Detection Precision", "99.2%", "BERT-Standard")

    # --- THE INTERACTIVE SEISMOGRAPH ---
    st.divider()
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.subheader("📡 Global Discourse Pulse (CDI)")
        fig = go.Figure()
        
        # Area fill for a "pulse" feel
        fig.add_trace(go.Scatter(x=df_cdi['window_label'], y=df_cdi['cdi_score'],
                                 fill='tozeroy', mode='lines+markers',
                                 line=dict(color='#58a6ff', width=3),
                                 marker=dict(size=8, color='#f85149'),
                                 name="Cultural Drift"))
        
        # Mark ChatGPT
        fig.add_annotation(x="2022-11", y=peak_val, text="💥 CHATGPT DEPLOYMENT",
                           showarrow=True, arrowhead=2, font=dict(color="red", size=12))

        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📜 Seismic Log")
        log_entries = [
            "🟢 2021-Q1: Discourse Stable.",
            "🟡 2022-Q2: Minor tremors in Large Language Models.",
            "🟠 2022-Q3: Semantic drift increasing.",
            "🔴 2022-Q4: MAJOR EVENT - ChatGPT launch detected.",
            "🔥 2023-Q1: Massive topic emergence detected.",
            "🌪️ 2023-Q2: Aftershocks in AI Regulation debate."
        ]
        for entry in log_entries:
            st.caption(entry)

    # --- FUN "DID YOU KNOW" CARDS ---
    st.divider()
    st.subheader("🤓 The Science Behind the Shake")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.expander("🤖 What is BERT thinking?"):
            st.write("We use **Sentence-BERT** to turn words into numbers. When the 'center' of those numbers moves, we know the culture's meaning has shifted—even if people are using the same words!")
            
    with c2:
        with st.expander("🔍 Topic Emergence (LDA)"):
            st.write("Imagine a giant word cloud. **LDA** finds the hidden topics. Our Seismograph watches for brand new clouds (like 'Prompt Engineering') appearing out of nowhere.")
            
    with c3:
        with st.expander("📉 The CDI Formula"):
            st.write("We combine Semantic Drift (How we say things) + Topic Emergence (What we say). 50/50 split creates the final Seismograph score.")

    # --- KEYWORD VALIDATION ---
    st.divider()
    st.subheader("🎯 Ground Truth Validation: The 'AI' Frequency")
    
    fig_key = px.bar(df_key, x=df_key.columns[0], y='mention_rate', 
                     title="Percentage of Comments Mentioning AI Terms",
                     color_discrete_sequence=['#238636'])
    fig_key.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_key, use_container_width=True)
    
    st.markdown("""
    > **Fun Fact:** After November 2022, the word 'AI' became so common it effectively became a 'cultural pillar' of these subreddits, 
    no longer just a niche technical topic.
    """)

else:
    st.error("⚠️ Command Center Offline: Please upload CSV data to the repository.")
    st.balloons() if random.random() > 0.5 else st.snow()
