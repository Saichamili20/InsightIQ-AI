import plotly.express as px
import pandas as pd


def generate_dashboard(df, analysis):

    charts = []


    dates = analysis.get(
        "date_columns",
        []
    )


    measures = analysis.get(
        "measure_columns",
        []
    )


    dimensions = analysis.get(
        "dimension_columns",
        []
    )


    # ---------------------------------
    # Revenue / Numeric Trend
    # ---------------------------------

    if dates and measures:
        date_col = dates[0]


    revenue_candidates = [

        "revenue",
        "sales",
        "salesamount",
        "amount",
        "totalprice",
        "productprice",
        "unitprice"

    ]


    measure_col = None


    for col in measures:

        clean = col.lower().replace(
            " ",
            ""
        )


        if any(
            x in clean
            for x in revenue_candidates
        ):

            measure_col = col
            break



    if measure_col is None:

        measure_col = measures[0]
        temp = df.copy()


        temp[date_col] = pd.to_datetime(
            temp[date_col],
            errors="coerce"
        )


        temp = (
            temp
            .groupby(
                date_col
            )[measure_col]
            .sum()
            .reset_index()
        )


        fig = px.line(
            temp,
            x=date_col,
            y=measure_col,
            title=f"{measure_col} Trend"
        )


        charts.append(fig)



    # ---------------------------------
    # Category Analysis
    # ---------------------------------

    for col in dimensions:


        if (
            df[col].nunique() > 1
            and
            df[col].nunique() < 15
        ):


            temp = (
                df[col]
                .value_counts()
                .reset_index()
            )


            temp.columns = [
                col,
                "Count"
            ]


            fig = px.bar(
                temp,
                x=col,
                y="Count",
                title=f"{col} Distribution"
            )


            charts.append(fig)



    # ---------------------------------
    # Numeric KPI Distribution
    # ---------------------------------

    for col in measures[:3]:


        fig = px.histogram(
            df,
            x=col,
            title=f"{col} Distribution"
        )


        charts.append(fig)



    return charts