import streamlit as st
from modules.forecast_checker import check_forecast_availability
from utils.session_manager import get_business_data
from modules.forecast_engine import generate_forecast
from modules.semantic_model import build_semantic_model
from modules.dataset_detector import detect_dataset
from modules.forecast_analyzer import analyze_forecast
import plotly.graph_objects as go
from modules.ai_engine import ask_gemini

st.title("📈 Business Forecasting")


df = get_business_data()


if df is None:

    st.warning(
        "Please upload dataset first."
    )

    st.stop()



dataset_type = detect_dataset(df)

st.subheader("📊 Forecast Capability")

st.success("Forecast Available")


st.info(
    f"Detected Dataset: {dataset_type.upper()}"
)



historical, future = generate_forecast(df)

semantic = build_semantic_model(df)

metric_name = "ForecastValue"

metric_display = semantic.get(
    "forecast_target",
    "Business Metric"
)

if historical is None:

    st.info(
        "Forecast unavailable. Dataset does not contain required date and metric columns."
    )

    st.stop()



st.subheader(
    f"📈 {metric_display} Forecast"
)



fig = go.Figure()



fig.add_trace(
    go.Scatter(
        x=historical["Date"],
        y=historical[metric_name],
        mode="lines+markers",
        name="Historical"
    )
)



fig.add_trace(
    go.Scatter(
        x=future["Date"],
        y=future[metric_name],
        mode="lines+markers",
        name="Forecast"
    )
)



st.plotly_chart(
    fig,
    use_container_width=True
)

forecast_summary = analyze_forecast(
    historical,
    future,
    metric_name
)

forecast_context = f"""

You are a business intelligence analyst.

Dataset Type:
{dataset_type}


Forecast Metric:
{metric_name}


Historical Last Value:
{forecast_summary["last_actual"]}


Future Predicted Value:
{forecast_summary["future_value"]}


Expected Change:
{forecast_summary["change_percent"]}%


Trend:
{forecast_summary["trend"]}


Rules:
- Use only provided forecast information.
- Do not invent reasons for changes.
- Clearly separate observations and assumptions.
- Mention if external factors are unavailable.


Generate a short business forecast explanation.

Include:

1. Forecast Observation
2. Trend Explanation
3. Assumptions and Limitations

"""


if forecast_summary:


    st.subheader(
        "📌 Forecast Summary"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Current Value",
        forecast_summary["last_actual"]
    )


    col2.metric(
        "Future Prediction",
        forecast_summary["future_value"]
    )


    col3.metric(
        "Expected Change",
        f'{forecast_summary["change_percent"]}%'
    )


    st.info(
        f"""
        Forecast trend:
        {forecast_summary["trend"]}
        """
    )

    with st.spinner(
    "Generating AI forecast explanation..."
):
        forecast_ai = ask_gemini(
        forecast_context
    )


st.subheader(
    "🤖 AI Forecast Explanation"
)


st.write(
    forecast_ai
)



st.subheader(
    "🔮 Future Prediction"
)



st.dataframe(
    future,
    use_container_width=True
)