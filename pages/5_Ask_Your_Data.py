import streamlit as st

from modules.visualization_engine import create_visualization
from utils.session_manager import get_data
from modules.query_engine import answer_query


st.title("🤖 Ask Your Data")


df = get_data()


if df is None:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()



question = st.text_input(
    "Ask a question about your data"
)



if question:

    with st.spinner("Analyzing..."):

        response = answer_query(
            df,
            question
        )
    



    # -----------------------------
    # TABLE RESPONSE
    # -----------------------------

    if isinstance(response, dict):

        response_type = response.get("type")


        if response_type == "table":

            st.subheader(
                response.get(
                    "title",
                    "Result"
                )
            )


            st.dataframe(
                response["data"],
                use_container_width=True
            )


            chart = create_visualization(
                response
            )


            if chart:

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )



        elif response_type == "text":

            st.success(
                response["data"]
            )



    # -----------------------------
    # NORMAL TEXT RESPONSE
    # -----------------------------

    elif isinstance(response, str):

        st.success(
            response
        )


    else:

        st.write(response)