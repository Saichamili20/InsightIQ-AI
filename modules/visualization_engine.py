import plotly.express as px


def create_visualization(response):


    if not isinstance(response, dict):

        return None



    if response["type"] != "table":

        return None



    df = response["data"]



    columns = df.columns.tolist()



    # -------------------------
    # Product chart
    # -------------------------

    if (
        "Product" in columns
        and
        "OrderQuantity" in columns
    ):


        fig = px.bar(
            df,
            x="Product",
            y="OrderQuantity",
            title=response["title"]
        )


        return fig



    # -------------------------
    # Category chart
    # -------------------------

    if (
        "Category" in columns
        and
        "Count" in columns
    ):


        fig = px.bar(
            df,
            x="Category",
            y="Count",
            title=response["title"]
        )


        return fig



    return None