import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Cultural Seismograph", page_icon="📈", layout="wide")

# --- MODERN SOFT-UI CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F8F9FB;
        color: #1F2937;
    }
    
    /* Card Styling */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #F1F5F9;
        margin-bottom: 20px;
    }

    /* Metric Numbers */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 10px 30px;
        font-weight: 600;
        color: #64748B;
        border: 1px solid #E2E8F0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B61FF !important;
        color: white !important;
        border: none !important;
    }

    /* Titles */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1F2937;
        font-weight: 800;
    }

    /* Footer Disclaimer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(248, 249, 251, 0.9);
        text-align: center;
        font-size: 11px;
        color: #94A3B8;
        padding: 10px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists("cdi_results.csv") and os.path.exists("keyword_frequency_monthly.csv"):
        return pd.read_csv("cdi_results.csv"), pd.read_csv("keyword_frequency_monthly.csv")
    return None, None

df_cdi, df_key = load_data()

if df_cdi is not None:
    # --- HEADER ---
    st.markdown("<h1>Hello👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:1.1rem; margin-top:-15px;'>Here is the latest seismic activity in AI discourse.(2021-2023)</p>", unsafe_allow_html=True)
    
    # --- TOP KPI ROW ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Corpus", "1.19M", "Comments")
    with c2:
        st.metric("Peak Drift", f"{df_cdi['cdi_score'].max():.2f}", "Nov 2022")
    with c3:
        st.metric("T-Test", "p < 0.001", "Significant")
    with c4:
        st.metric("Breakpoint", "Dec 2022", "PELT Detection")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- THREE TABS ---
    tab1, tab2, tab3 = st.tabs(["📉 Seismograph Index", "🎯 Keyword Validation", "🔬 Statistical Rigor"])

    with tab1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Global Cultural Drift Index")
        
        fig = go.Figure()
        # Smooth area chart with gradient-like look
        fig.add_trace(go.Scatter(
            x=df_cdi['window_label'], y=df_cdi['cdi_score'],
            line=dict(color='#7B61FF', width=5, shape='spline'),
            fill='tozeroy', fillcolor='rgba(123, 97, 255, 0.1)',
            mode='lines+markers', marker=dict(size=10, color='#FF4B8B', line=dict(width=2, color='white'))
        ))
        
        # Highlight ChatGPT
        fig.add_annotation(
            x="Jul 2022 - Dec 2022" if "Jul 2022 - Dec 2022" in df_cdi['window_label'].values else df_cdi['window_label'].iloc[len(df_cdi)//2],
            y=df_cdi['cdi_score'].max(), text="ChatGPT Launch",
            showarrow=True, arrowhead=2, arrowcolor="#FF4B8B", font=dict(color="#FF4B8B", size=14)
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=20,b=0), height=450,
            xaxis=dict(showgrid=False, color='#64748B'), 
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', color='#64748B')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Micro-Scale Keyword Frequency")
        
        # Boosto Style Bar chart
        fig2 = px.bar(df_key, x=df_key.columns[0], y='mention_rate',
                      color_discrete_sequence=['#FF4B8B'])
        
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=20,b=0), height=400,
            xaxis=dict(showgrid=False, title="Monthly Timeline"),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Mention Rate")
        )
        fig2.update_traces(marker_round=True) # Attempt rounding
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        col_s1, col_stat2 = st.columns(2)
        with col_s1:
            st.markdown("""
            <div class="metric-card">
                <h3 style='color:#FF4B8B'>Welch's T-Test</h3>
                <p style='color:#64748B'>Comparing pre-and-post November 2022 discourse.</p>
                <h1 style='font-size:3rem; margin:10px 0;'>p < 0.000002</h1>
                <p style='color:#4ade80; font-weight:600;'>Highly Statistically Significant</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_stat2:
            st.markdown("""
            <div class="metric-card">
                <h3 style='color:#7B61FF'>PELT Detection</h3>
                <p style='color:#64748B'>Structural change-point detection algorithm.</p>
                <h1 style='font-size:3rem; margin:10px 0;'>Dec 2022</h1>
                <p style='color:#7B61FF; font-weight:600;'>Algorithmic Breakpoint Confirmed</p>
            </div>
            """, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
        <div class="footer">
            This is purely based on data available to the user. Analysis performed for Dissertation S2-25.
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Data source not found. Please ensure cdi_results.csv is in your GitHub repository.")
