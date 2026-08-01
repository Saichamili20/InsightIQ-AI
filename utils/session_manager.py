import streamlit as st



def save_dataset(datasets):

    st.session_state["datasets"] = datasets



def get_dataset():

    return st.session_state.get(
        "datasets"
    )



def save_data(df):

    st.session_state["dataframe"] = df



def get_data():

    return st.session_state.get(
        "dataframe"
    )



def save_business_data(df):

    st.session_state["business_df"] = df

    # keep both synced
    st.session_state["dataframe"] = df



def get_business_data():

    return st.session_state.get(
        "business_df"
    )



def clear_data():

    keys = [
        "datasets",
        "dataframe",
        "business_df"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]