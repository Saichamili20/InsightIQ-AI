import streamlit as st

st.set_page_config(
    page_title="InsightIQ AI",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <h1 style='text-align:center;color:#2E86DE;'>
        📊 InsightIQ AI
    </h1>
    <h3 style='text-align:center;color:gray;'>
        Autonomous Business Intelligence & Decision Support Platform
    </h3>
    <p style='text-align:center;font-size:18px;'>
        Transform raw business data into AI-powered insights, intelligent dashboards,
        predictive forecasts, and executive reports.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()
# ==========================================================
# FEATURE HIGHLIGHTS
# ==========================================================

st.subheader("🚀 Platform Highlights")

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        """
### 📈 Interactive Dashboards

- Dynamic KPI Cards
- Interactive Charts
- Business Performance Tracking
"""
    )

with c2:
    st.success(
        """
### 🤖 AI Business Analysis

- Executive Insights
- Trend Detection
- Business Recommendations
"""
    )

with c3:
    st.warning(
        """
### 🔮 Predictive Analytics

- Forecast Future Trends
- AI Executive Reports
- Decision Support
"""
    )

st.divider()

# ==========================================================
# WHY INSIGHTIQ AI
# ==========================================================

st.subheader("✨ Why InsightIQ AI?")

left, right = st.columns(2)

with left:

    st.markdown(
        """
✅ Supports Multiple Business Datasets

✅ Automatic Semantic Column Detection

✅ Intelligent KPI Generation

✅ AI-Powered Business Insights

"""
    )

with right:

    st.markdown(
        """
✅ Interactive Business Dashboards

✅ Predictive Forecasting

✅ Executive Decision Support

✅ Minimal Manual Configuration

"""
    )

st.divider()

# ==========================================================
# MODULES
# ==========================================================

st.subheader("📂 Explore the Platform")

col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        """
### 📂 Data Upload

Upload CSV or Excel datasets and let
InsightIQ AI automatically understand
your business data.
"""
    )

    st.success(
        """
### 🔍 Data Profiling

Explore missing values,
statistics, data quality,
and dataset structure.
"""
    )

with col2:

    st.info(
        """
### 📊 Business Dashboard

View KPIs,
interactive visualizations,
and business trends.
"""
    )

    st.info(
        """
### 🤖 AI Business Analyst

Generate business insights,
identify patterns,
and receive recommendations.
"""
    )

with col3:

    st.warning(
        """
### 📈 Forecasting

Predict future business
performance using
machine learning.
"""
    )

    st.warning(
        """
### 📄 Executive Report

Generate AI-powered
executive summaries
for business leaders.
"""
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "InsightIQ AI • Version 1.0 | Built with Streamlit • Python • Pandas • Plotly • Scikit-learn • Gemini AI"
)