import streamlit as st
from modules.dataset_detector import detect_dataset
from modules.kpi_engine import generate_kpis
from modules.dashboard_engine import generate_dashboard
from modules.insight_engine import analyze_dataset
from utils.session_manager import (
    get_business_data
)


st.title("📊 Business Dashboard")


# -----------------------------------
# Get Dataset
# -----------------------------------

df = get_business_data()

if df is None:

    st.warning(
        "⚠️ Please upload a dataset first from Data Upload page."
    )

    st.stop()
# Detect dataset type
dataset_type = detect_dataset(df)


st.info(
    f"Detected Dataset Type: {dataset_type.upper()}"
)


# Debug section

st.subheader("🔎 Dashboard Data Check")

st.write(
    "Shape:",
    df.shape
)

st.write(
    "Columns:",
    df.columns.tolist()
)



# -----------------------------------
# Business KPIs
# -----------------------------------

st.divider()

st.subheader("📈 Business KPIs")


analysis = analyze_dataset(df)

kpis = generate_kpis(df,dataset_type)






cols = st.columns(4)


for index, (key, value) in enumerate(kpis.items()):

    # Convert numpy values
    if hasattr(value, "item"):
        value = value.item()


    cols[index % 4].metric(
        key,
        value
    )

# -----------------------------------
# Automatic Dashboard
# -----------------------------------



st.subheader("📊 Business Visualizations")


charts = generate_dashboard(
    df,
    analysis
)


if len(charts) == 0:

    st.info(
        "No suitable visualizations found for this dataset."
    )


else:

    for chart in charts:

        st.plotly_chart(
            chart,
            use_container_width=True
        )