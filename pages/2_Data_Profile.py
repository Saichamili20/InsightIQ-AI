import streamlit as st
import pandas as pd

from modules.data_understanding import understand_dataset
from modules.metric_engine import generate_metrics
from modules.data_profiler import profile_dataset
from modules.insight_engine import analyze_dataset
from modules.semantic_model import build_semantic_model

from utils.session_manager import get_data, save_data


st.title("🔍 Data Profile")


# Get uploaded dataframe

df = get_data()


if df is None:

    st.warning(
        "⚠️ Please upload a dataset first from Data Upload page."
    )

    st.stop()



try:


    # -----------------------------
    # Dataset Understanding
    # -----------------------------

    st.subheader("🧠 Dataset Understanding")


    analysis = understand_dataset(df)


    st.write(analysis)



    # -----------------------------
    # Semantic Model
    # -----------------------------

    semantic = build_semantic_model(df)


    st.subheader("🔎 Semantic Model")


    st.json(semantic)



    # -----------------------------
    # Generated Metrics
    # -----------------------------

    st.subheader("📈 Generated Metrics")


    metrics = generate_metrics(
        df,
        analysis
    )


    st.write(metrics)



    # -----------------------------
    # Save Dataset
    # -----------------------------

    save_data(df)



    # -----------------------------
    # Dataset Intelligence
    # -----------------------------

    analysis_result = analyze_dataset(df)


    st.subheader(
        "🧠 Dataset Intelligence"
    )


    st.write(
        analysis_result
    )



    st.success(
        "Dataset loaded successfully"
    )



    # -----------------------------
    # Preview
    # -----------------------------

    st.subheader("Preview")


    st.dataframe(
        df.head(),
        use_container_width=True
    )



    # -----------------------------
    # Dataset Profile
    # -----------------------------

    st.subheader(
        "📊 Dataset Profile"
    )


    profile = profile_dataset(df)



    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Rows",
        profile["Rows"]
    )


    col2.metric(
        "Columns",
        profile["Columns"]
    )


    col3.metric(
        "Missing Values",
        profile["Missing Values"]
    )


    col4.metric(
        "Duplicates",
        profile["Duplicates"]
    )



    col5, col6, col7, col8 = st.columns(4)


    col5.metric(
        "Memory (MB)",
        profile["Memory Usage"]
    )


    col6.metric(
        "Numeric Columns",
        profile["Numeric Columns"]
    )


    col7.metric(
        "Categorical Columns",
        profile["Categorical Columns"]
    )


    col8.metric(
        "Date Columns",
        profile["Date Columns"]
    )



    # -----------------------------
    # Column Information
    # -----------------------------

    st.subheader(
        "📋 Column Information"
    )


    column_info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing Values": df.isnull().sum().values,

        "Unique Values": df.nunique().values

    })


    st.dataframe(
        column_info,
        use_container_width=True
    )



    # -----------------------------
    # Summary
    # -----------------------------

    st.subheader(
        "📑 Dataset Summary"
    )


    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )



    # -----------------------------
    # Missing Values
    # -----------------------------

    st.subheader(
        "🚨 Missing Values"
    )


    missing = df.isnull().sum()

    missing = missing[missing > 0]


    if len(missing) == 0:

        st.success(
            "No missing values found."
        )

    else:

        st.dataframe(
            missing
        )



except Exception as e:


    st.error(
        f"Error loading dataset: {e}"
    )