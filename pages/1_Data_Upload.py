import streamlit as st
import pandas as pd

from modules.data_profiler import (
    extract_zip,
    load_dataset
)

from modules.table_detector import detect_table_roles
from modules.business_model import build_business_model

from utils.session_manager import (
    save_dataset,
    save_business_data,
    save_data,
    clear_data
)

st.title("📂 Data Upload")

st.markdown(
    """
Upload your business dataset.

Supported formats:

- 📦 ZIP 
- 📄 CSV
- 📊 Excel (.xlsx)
"""
)

uploaded_file = st.file_uploader(
    "Choose Dataset",
    type=["zip", "csv", "xlsx"]
)

if uploaded_file:

    # Avoid rebuilding if same file
    if (
        "last_uploaded" not in st.session_state
        or st.session_state["last_uploaded"] != uploaded_file.name
    ):

        clear_data()

        st.session_state["last_uploaded"] = uploaded_file.name

    file_name = uploaded_file.name.lower()

    # ====================================================
    # ZIP DATASET
    # ====================================================

    if file_name.endswith(".zip"):

        st.success(f"Uploaded : {uploaded_file.name}")

        with st.spinner("Extracting dataset..."):

            folder = extract_zip(uploaded_file)

        st.success("Extraction completed")

        with st.spinner("Finding tables..."):

            datasets = load_dataset(folder)

        if datasets:

            save_dataset(datasets)

            st.success(f"{len(datasets)} tables detected")

            st.subheader("🧠 Table Understanding")

            table_info = detect_table_roles(
                datasets
            )

            st.write(table_info)

            with st.spinner("Building Business Model..."):

                business_df = build_business_model(
                    datasets,
                    table_info
                )

            if business_df is not None:

                save_data(
                    business_df
                )

                save_business_data(
                    business_df
                )
                st.session_state["uploaded"] = True

                st.success("✅ Business Model Created")

                st.subheader("🏢 Business Model")

                st.write("Shape:", business_df.shape)

                st.write("Columns:")

                st.write(
                    business_df.columns.tolist()
                )

                st.dataframe(
                    business_df.head(),
                    use_container_width=True
                )

            else:

                st.error(
                    "Business model creation failed."
                )

            st.subheader("📄 Available Tables")

            for table in datasets.keys():

                st.write("📄", table)

        else:

            st.error(
                "No CSV files found inside ZIP."
            )

    # ====================================================
    # CSV DATASET
    # ====================================================

    elif file_name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        save_data(df)
        save_business_data(df)
        save_dataset({
    uploaded_file.name: uploaded_file.name
})


        st.success("✅ CSV Uploaded Successfully")

        st.write("Shape:", df.shape)

        st.write("Columns:")

        st.write(df.columns.tolist())

        st.dataframe(
            df.head(),
            use_container_width=True
        )

    # ====================================================
    # EXCEL DATASET
    # ====================================================

    elif file_name.endswith(".xlsx"):

        df = pd.read_excel(uploaded_file)

        save_data(df)
        save_business_data(df)
        save_dataset({
    uploaded_file.name: uploaded_file.name
})


        st.success("✅ Excel Uploaded Successfully")

        st.write("Shape:", df.shape)

        st.write("Columns:")

        st.write(df.columns.tolist())

        st.dataframe(
            df.head(),
            use_container_width=True
        )