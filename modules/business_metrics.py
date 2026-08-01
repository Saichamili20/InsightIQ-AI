import pandas as pd


def generate_business_metrics(df):

    metrics = {}

    # -----------------------------
    # Total Records
    # -----------------------------
    metrics["Total Records"] = len(df)

    # -----------------------------
    # Revenue
    # -----------------------------
    if "Revenue" in df.columns:

        metrics["Total Revenue"] = round(
            df["Revenue"].sum(),
            2
        )

    # -----------------------------
    # Orders
    # -----------------------------
    if "OrderNumber" in df.columns:

        metrics["Total Orders"] = df["OrderNumber"].nunique()

    # -----------------------------
    # Customers
    # -----------------------------
    if "CustomerKey" in df.columns:

        metrics["Customers"] = df["CustomerKey"].nunique()

    # -----------------------------
    # Products
    # -----------------------------
    if "ProductKey" in df.columns:

        metrics["Products"] = df["ProductKey"].nunique()

    # -----------------------------
    # Average Order Value
    # -----------------------------
    if (
        "Revenue" in df.columns
        and "OrderNumber" in df.columns
    ):

        orders = df["OrderNumber"].nunique()

        if orders > 0:

            metrics["Avg Order Value"] = round(
                df["Revenue"].sum() / orders,
                2
            )

    # -----------------------------
    # Top Region
    # -----------------------------
    if (
        "Region" in df.columns
        and "Revenue" in df.columns
    ):

        metrics["Top Region"] = (
            df.groupby("Region")["Revenue"]
            .sum()
            .idxmax()
        )

    # -----------------------------
    # Top Category
    # -----------------------------
    if (
        "CategoryName" in df.columns
        and "Revenue" in df.columns
    ):

        metrics["Top Category"] = (
            df.groupby("CategoryName")["Revenue"]
            .sum()
            .idxmax()
        )

    # -----------------------------
    # Best Product
    # -----------------------------
    if (
        "ProductName" in df.columns
        and "Revenue" in df.columns
    ):

        metrics["Best Product"] = (
            df.groupby("ProductName")["Revenue"]
            .sum()
            .idxmax()
        )

    return metrics