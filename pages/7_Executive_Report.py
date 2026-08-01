import streamlit as st

from utils.session_manager import get_business_data
from modules.semantic_model import build_semantic_model
from modules.kpi_engine import generate_kpis
from modules.dataset_detector import detect_dataset
from modules.ai_engine import ask_gemini
from modules.forecast_engine import (forecast_sales,forecast_hr,forecast_fraud,generate_forecast)

import plotly.graph_objects as go


st.title("📄 Executive Business Report")


# -----------------------------
# Load Business Data
# -----------------------------

df = get_business_data()


if df is None:

    st.warning(
        "Please upload dataset first."
    )

    st.stop()



# -----------------------------
# Detect Dataset Type
# -----------------------------

dataset_type = detect_dataset(df)


st.info(
    f"Detected Dataset Type: {dataset_type.upper()}"
)



# -----------------------------
# KPIs
# -----------------------------

st.subheader(
    "📊 Business Overview"
)


kpis = generate_kpis(
    df,
    dataset_type
)


cols = st.columns(4)


for index, (key, value) in enumerate(kpis.items()):

    if hasattr(value, "item"):

        value = value.item()


    cols[index % 4].metric(
        key,
        value
    )



# -----------------------------
# Gemini Executive Summary
# -----------------------------

st.divider()


st.subheader(
    "🤖 Executive Summary"
)
columns = df.columns.tolist()

sample_rows = df.head(5).to_string()


context = f"""

You are a senior business intelligence analyst.

The dataset belongs to this business domain:

{dataset_type.upper()}


IMPORTANT RULE:
Do not assume this is a sales dataset.

Generate the report based only on the dataset type and available KPIs.

Dataset Type:
{dataset_type}


Dataset Columns:

{columns}


Sample Data:

{sample_rows}


Available KPIs:

{kpis}


Dataset Information:

Rows:
{len(df)}

Columns:
{len(df.columns)}


Create an executive report containing:


1. Overall business performance

2. Key trends and patterns

3. Major risks or concerns

4. Strategic recommendations



Use terminology appropriate for the domain:


SALES:
- revenue
- customers
- products
- orders
- sales performance


FRAUD:
- transactions
- fraud cases
- fraud rate
- risk patterns


HR:
- employees
- departments
- attrition
- workforce trends



Write the report for business leadership.

Avoid calling every dataset a sales dataset.

IMPORTANT ANALYTICAL RULES:

1. Use only metrics provided.
2. Do not invent business facts.
3. If information is unavailable, explicitly state "Not available in dataset".
4. Do not calculate financial impact unless the required column exists.
5. Separate observed facts from assumptions.
6. Avoid industry assumptions unless supported by dataset columns.
7. Do not describe possible scenarios as facts.
8. Clearly label assumptions as "Possible interpretation".
9. Do not mention industries (banking, retail, healthcare etc.) unless dataset columns prove it.
10. If trends cannot be calculated because dates are unavailable, state that time-based analysis is unavailable.

"""



# Refresh AI response when dataset changes
dataset_key = (
    dataset_type,
    df.shape,
    tuple(df.columns)
)

if (
    "executive_summary" not in st.session_state
    or
    st.session_state.get("dataset_key")
    != dataset_key
):


    with st.spinner(
        "Generating executive summary..."
    ):

        st.session_state.executive_summary = ask_gemini(
            context
        )


        st.session_state.dataset_key = dataset_key



summary = st.session_state.executive_summary


st.write(summary)

# -----------------------------
# Forecasting
# -----------------------------

historical, future = generate_forecast(df)


semantic = build_semantic_model(df)

st.write("SEMANTIC CHECK")
st.write(semantic)

forecast_metric = semantic.get(
    "forecast_target",
    "Business Metric"
)

title = f"📈 Forecast: {forecast_metric}"


if historical is not None:

    metric_name = "ForecastValue"

else:

    metric_name = None
    title = None

if historical is not None:


    st.subheader(title)


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


    st.subheader(
        "🔮 Future Prediction"
    )


    st.dataframe(
        future[
            [
                "Date",
                metric_name
            ]
        ],
        use_container_width=True
    )


else:

    st.info(
        "Forecast unavailable. Required date and metric columns are missing."
    )