import pandas as pd


def add_revenue(df):

    df = df.copy()

    # Check required columns
    if (
        "ProductPrice" not in df.columns
        or "OrderQuantity" not in df.columns
    ):
        return df

    # Convert to numeric
    df["ProductPrice"] = pd.to_numeric(
        df["ProductPrice"],
        errors="coerce"
    )

    df["OrderQuantity"] = pd.to_numeric(
        df["OrderQuantity"],
        errors="coerce"
    )

    # Fill missing values
    df["ProductPrice"] = df["ProductPrice"].fillna(0)
    df["OrderQuantity"] = df["OrderQuantity"].fillna(0)

    # Revenue calculation
    df["Revenue"] = (
        df["ProductPrice"]
        * df["OrderQuantity"]
    )

    return df