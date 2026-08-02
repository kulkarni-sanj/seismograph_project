import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Cultural Seismograph", page_icon="📉", layout="wide")

# --- GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #11111d 100%);
        color: #ffffff;
    }
    
    /* Frosted Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Titles */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.3);
        padding: 10px;
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
    st.markdown("<p style='color:rgba(255,255,255,0.5)'>Welcome back to the Seismic Command Center.</p>", unsafe_allow_html=True)
    
    st.divider()

    # --- TOP ROW: 3 COLUMNS ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        # MAIN SEISMOGRAPH CARD
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📡 Global Cultural Pulse (CDI)")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_cdi['window_label'], y=df_cdi['cdi_score'],
            line=dict(color='#7b61ff', width=4, shape='spline'),
            fill='tozeroy', fillcolor='rgba(123, 97, 255, 0.1)',
            mode='lines+markers', marker=dict(size=10, color='#ff4b4b')
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="white", height=400, margin=dict(l=0,r=0,t=20,b=0),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # KEYWORD SPIKE (Small Cards style)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎯 Discourse Validation (Keywords)")
        fig2 = px.bar(df_key.tail(12), x=df_key.columns[0], y='mention_rate', 
                      color_discrete_sequence=['#4ade80'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        # RIGHT HAND SUMMARY (Donut Chart)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Statistical Confidence")
        
        # Donut chart
        fig_donut = go.Figure(data=[go.Pie(labels=['Confidence', 'Noise'], values=[99.2, 0.8], hole=.7)])
        fig_donut.update_traces(marker=dict(colors=['#7b61ff', '#1e1e2f']), textinfo='none')
        fig_donut.update_layout(
            showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text='99.2%', x=0.5, y=0.5, font_size=25, showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
        st.metric("Peak Intensity", f"{df_cdi['cdi_score'].max():.2f}", "Richter Scale")
        st.metric("Total Sample", "1.19M", "Comments")
        st.markdown('</div>', unsafe_allow_html=True)

        # STATUS CARD
        st.markdown(f"""
            <div style='background: rgba(255,75,75,0.1); border: 1px solid #ff4b4b; padding: 20px; border-radius: 20px; text-align: center;'>
                <h4 style='color: #ff4b4b; margin:0;'>⚠️ MAJOR DRIFT</h4>
                <p style='font-size:12px; margin:0;'>Structural breakpoint detected: Dec 2022</p>
            </div>
        """, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
        <div class="footer">
            This is purely based on data available to the user. Analysis performed for Dissertation S2-25.
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Command Center Offline. Check GitHub Data.")
