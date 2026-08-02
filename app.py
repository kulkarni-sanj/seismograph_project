import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cultural Seismograph", layout="wide")
st.title("📊 The Cultural Seismograph Dashboard")
st.caption("Dissertation Prototype | Sanjana V Kulkarni | 2024DA04217")

# --- SMART DATA LOADER ---
def load_data():
    if not os.path.exists("cdi_results.csv") or not os.path.exists("keyword_frequency_monthly.csv"):
        return None, None
    
    df_cdi = pd.read_csv("cdi_results.csv")
    df_key = pd.read_csv("keyword_frequency_monthly.csv")
    return df_cdi, df_key

df_cdi, df_key = load_data()

if df_cdi is not None:
    tab1, tab2 = st.tabs(["📉 CDI Seismograph", "🎯 Keyword Validation"])
    
    with tab1:
        st.subheader("Longitudinal Cultural Drift Index")
        # Automatically find the right columns for Tab 1
        x_col = 'window_label' if 'window_label' in df_cdi.columns else df_cdi.columns[0]
        y_col = 'cdi_score' if 'cdi_score' in df_cdi.columns else df_cdi.columns[-1]
        
        fig = px.line(df_cdi, x=x_col, y=y_col, title="CDI Score (Semantic + Topic Drift)", markers=True)
        fig.update_traces(line_color='#1F3864', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Keyword Frequency (Ground Truth)")
        # Automatically find the right columns for Tab 2
        # It looks for 'month' or 'window_key' for X, and 'rate' for Y
        x_col_k = 'month' if 'month' in df_key.columns else 'window_key'
        if x_col_k not in df_key.columns: x_col_k = df_key.columns[0]
        
        y_col_k = 'mention_rate' if 'mention_rate' in df_key.columns else [c for c in df_key.columns if 'rate' in c.lower()][0]

        fig2 = px.area(df_key, x=x_col_k, y=y_col_k, title="AI-Related Terms Mention Rate (%)")
        fig2.update_traces(line_color='#E63946', fillcolor='rgba(230, 57, 70, 0.3)')
        st.plotly_chart(fig2, use_container_width=True)
        
    st.success("Dashboard successfully synchronized with pipeline results.")
else:
    st.error("Data files (CSV) not found. Please ensure they are uploaded to the GitHub repository.")
    st.info("Check that 'cdi_results.csv' and 'keyword_frequency_monthly.csv' are in the main folder.")
