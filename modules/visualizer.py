import plotly.express as px


def generate_visualizations(df):

    charts = []

    # -----------------------------
    # Numeric Columns
    # -----------------------------
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        fig = px.histogram(
            df,
            x=col,
            title=f"Distribution of {col}"
        )

        charts.append(fig)

    # -----------------------------
    # Categorical Columns
    # -----------------------------
    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:

        if df[col].nunique() <= 20:

            counts = df[col].value_counts().reset_index()

            counts.columns = [col, "Count"]

            fig = px.bar(
                counts,
                x=col,
                y="Count",
                title=f"{col} Distribution"
            )

            charts.append(fig)

    return charts