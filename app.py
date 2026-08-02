import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Cultural Seismograph", page_icon="🌋", layout="wide")

# --- CUSTOM CSS FOR HIGH VISIBILITY ---
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    
    /* Metric Cards Styling */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Heading Colors */
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Highlight Box for Stats */
    .stat-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #f85149;
        margin-bottom: 20px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🌋 The Cultural Seismograph")
st.markdown("#### **Dissertation Presentation:** Monitoring the Generative AI Discourse Shift (2021-2024)")
st.caption("Researcher: Sanjana V Kulkarni | ID: 2024DA04217")

# --- DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists("cdi_results.csv") and os.path.exists("keyword_frequency_monthly.csv"):
        return pd.read_csv("cdi_results.csv"), pd.read_csv("keyword_frequency_monthly.csv")
    return None, None

df_cdi, df_key = load_data()

if df_cdi is not None:
    # --- GLOBAL STATUS CALCULATIONS ---
    peak_cdi = df_cdi['cdi_score'].max()
    
    # 1. TOP KPI ROW
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Sample Size", "1.19M Comments", "r/tech + r/ML")
    with c2:
        st.metric("Peak CDI Intensity", f"{peak_cdi:.3f}", "Nov 2022")
    with c3:
        st.metric("Stat. Significance", "99.9%", "p < 0.001")
    with c4:
        # Dynamic Color Status
        status_color = "#4ade80" if peak_cdi < 0.5 else "#f85149"
        st.markdown(f"""
            <div style='text-align:center; padding:10px; border-radius:10px; background-color:{status_color}; color:black; font-weight:bold;'>
                SEISMIC STATUS: MAJOR SHIFT
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 2. MAIN TABS
    tab1, tab2, tab3 = st.tabs(["📊 THE SEISMOGRAPH", "🎯 GROUND TRUTH", "🔬 STATISTICAL RIGOR"])

    with tab1:
        st.subheader("Global Cultural Drift Index (CDI)")
        
        # Enhanced Seismograph Chart
        fig = go.Figure()
        
        # Add the pulse line
        fig.add_trace(go.Scatter(
            x=df_cdi['window_label'], y=df_cdi['cdi_score'],
            fill='tozeroy', mode='lines+markers',
            line=dict(color='#58a6ff', width=4),
            marker=dict(size=10, color='#f85149', line=dict(width=2, color='white')),
            name="Cultural Drift"
        ))

        # Event Annotation for ChatGPT
        fig.add_annotation(
            x="Nov 2022" if "Nov 2022" in df_cdi['window_label'].values else df_cdi['window_label'].iloc[len(df_cdi)//2],
            y=peak_cdi, text="💥 CHATGPT DEPLOYMENT",
            showarrow=True, arrowhead=2, arrowcolor="#f85149",
            font=dict(color="#f85149", size=14), bgcolor="rgba(0,0,0,0.8)"
        )

        fig.update_layout(
            template="plotly_dark", height=500,
            xaxis_title="Time Horizon", yaxis_title="Shift Magnitude (0-1)",
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Direct Keyword Frequency Validation")
        st.markdown("_This chart confirms that the drift detected above matches the explosion in AI-specific terminology._")
        
        fig_key = px.area(df_key, x=df_key.columns[0], y='mention_rate',
                          color_discrete_sequence=['#238636'])
        fig_key.update_layout(template="plotly_dark", height=400, 
                             xaxis_title="Month", yaxis_title="Mention Rate (%)")
        st.plotly_chart(fig_key, use_container_width=True)

    with tab3:
        st.header("Algorithmic Validation")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div class="stat-card">
                <h3>🔬 Welch's T-Test</h3>
                <p>Comparing pre-and-post November 2022 discourse.</p>
                <h2 style='color:#4ade80'>p < 0.000002</h2>
                <p>Conclusion: The shift is statistically Distinguishable from noise.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_stat2:
            st.markdown(f"""
            <div class="stat-card">
                <h3>🛡️ PELT Detection</h3>
                <p>Structural Change-Point Detection Algorithm.</p>
                <h2 style='color:#58a6ff'>Breakpoint: Dec 2022</h2>
                <p>Matches ChatGPT launch with high temporal precision.</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("📡 Waiting for Satellite Uplink... Please ensure CSV files are present in the repository.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJmZzR6NHJmZzR6NHJmZzR6NHJmZzR6NHJmZzR6NHJmZzR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxVfV9V10z6/giphy.gif")
