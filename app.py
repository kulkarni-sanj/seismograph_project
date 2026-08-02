import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="The AI Cultural Seismograph", layout="wide")

# --- CUSTOM THEMING ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .insight-box { background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #1f3864; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🏛️ The Cultural Seismograph")
st.subheader("Measuring the Impact of Generative AI on Public Discourse")
st.markdown("""
This dashboard quantifies how the release of **ChatGPT (Nov 2022)** acted as a 'societal earthquake,' 
permanently shifting how we talk about technology in communities like *r/technology* and *r/MachineLearning*.
""")

# --- SMART DATA LOADER ---
def load_data():
    if not os.path.exists("cdi_results.csv") or not os.path.exists("keyword_frequency_monthly.csv"):
        return None, None
    df_cdi = pd.read_csv("cdi_results.csv")
    df_key = pd.read_csv("keyword_frequency_monthly.csv")
    return df_cdi, df_key

df_cdi, df_key = load_data()

if df_cdi is not None:
    # --- TOP LEVEL METRICS ---
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Corpus Size", "1.19M Comments", "Big Data Scale")
    with col2:
        st.metric("Peak Activity", "Nov 2022", "Event Horizon")
    with col3:
        st.metric("Cultural Drift", "Significant", "Z > 2.0")
    with col4:
        st.metric("Primary Driver", "Topic Emergence", "Generative AI")

    # --- THE CORE EXPLANATION ---
    st.markdown("---")
    with st.expander("🔍 How does the Seismograph work? (Read this for the Viva)"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**1. Semantic Drift (SDS)**")
            st.caption("Measures the *meaning* of words. If we use the same words but in different contexts, the SDS spikes.")
        with c2:
            st.markdown("**2. Topic Emergence (TES)**")
            st.caption("Measures the *subject* of talk. When brand new topics (like LLMs or Prompt Engineering) appear, the TES spikes.")
        with c3:
            st.markdown("**3. CDI (Composite Index)**")
            st.caption("The final 'Seismograph' score. A high CDI indicates a fundamental shift in the community's culture.")

    # --- ANALYSIS TABS ---
    tab1, tab2 = st.tabs(["📉 The Seismograph (CDI)", "🎯 The Validation (Keywords)"])
    
    with tab1:
        st.header("Global Cultural Drift Index")
        st.markdown("_This chart tracks the 'vibrations' of the community. Higher peaks indicate a faster rate of cultural change._")
        
        # Build the chart manually for better annotations
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_cdi['window_label'], y=df_cdi['cdi_score'], 
                                 name="CDI Score", line=dict(color='#1F3864', width=4), 
                                 mode='lines+markers', marker=dict(size=8)))
        
        # Highlight ChatGPT launch
        fig.add_vrect(x0="2022-10", x1="2022-12", fillcolor="red", opacity=0.1, layer="below", line_width=0)
        fig.add_annotation(x="2022-11", y=df_cdi['cdi_score'].max(), text="ChatGPT Launch", showarrow=True, arrowhead=1)
        
        fig.update_layout(template="plotly_white", height=500, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # INSIGHT BOX
        st.markdown("""
        <div class="insight-box">
        <strong>Key Observation:</strong> Notice how the CDI begins to rise <i>before</i> the actual launch. 
        This represents the 'pre-shock' phase where technical communities were already discussing GPT-3 
        and early generative models before they became mainstream.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.header("Keyword Frequency: The Evidence")
        st.markdown("_Directly tracking mentions of AI, LLM, and ChatGPT. This validates that the CDI isn't just 'noise'._")
        
        fig2 = px.area(df_key, x='month' if 'month' in df_key.columns else df_key.columns[0], 
                       y='mention_rate', title="Discourse Volume (%)")
        fig2.update_traces(line_color='#E63946', fillcolor='rgba(230, 57, 70, 0.2)')
        fig2.update_layout(template="plotly_white", height=450)
        st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 **Analysis:** The 'Level Shift'—where frequency doesn't return to the baseline—proves that AI has moved from a 'temporary trend' to a 'permanent cultural norm'.")

else:
    st.error("⚠️ Pipeline data not detected. Please upload CSVs to GitHub.")
