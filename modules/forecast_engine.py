import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

from modules.semantic_model import build_semantic_model


# =====================================================
# GENERIC FORECAST DATA PREPARATION
# =====================================================

def prepare_forecast_data(df):

    semantic = build_semantic_model(df)

    date_col = semantic.get("date")

    target_col = (
        semantic.get("forecast_target")
        or semantic.get("revenue")
        or semantic.get("amount")
    )


    if date_col is None or target_col is None:
        return None



    data = df.copy()


    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce"
    )


    data[target_col] = pd.to_numeric(
        data[target_col],
        errors="coerce"
    )


    data = data.dropna(
        subset=[
            date_col,
            target_col
        ]
    )


    if len(data) == 0:
        return None



    monthly_data = (

        data

        .groupby(
            data[date_col]
            .dt
            .to_period("M")
        )[target_col]

        .sum()

        .reset_index()

    )


    monthly_data["Date"] = (
        monthly_data[date_col]
        .dt
        .to_timestamp()
    )


    monthly_data.rename(
        columns={
            target_col:"ForecastValue"
        },
        inplace=True
    )


    return monthly_data[
        [
            "Date",
            "ForecastValue"
        ]
    ]
# =====================================================
# SALES DATA PREPARATION
# =====================================================

def prepare_sales_data(df):

    semantic = build_semantic_model(df)

    date_col = semantic.get("date")
    quantity_col = semantic.get("quantity")
    price_col = (
        semantic.get("price")
        or semantic.get("revenue")
    )


    if (
        date_col is None
        or quantity_col is None
        or price_col is None
    ):
        return None



    data = df.copy()


    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce"
    )


    data[quantity_col] = pd.to_numeric(
        data[quantity_col],
        errors="coerce"
    )


    data[price_col] = pd.to_numeric(
        data[price_col],
        errors="coerce"
    )


    data["Revenue"] = (
        data[quantity_col]
        *
        data[price_col]
    )


    data = data.dropna(
        subset=[
            date_col,
            "Revenue"
        ]
    )


    if len(data) == 0:
        return None



    monthly_sales = (

        data

        .groupby(
            data[date_col]
            .dt
            .to_period("M")
        )["Revenue"]

        .sum()

        .reset_index()

    )


    monthly_sales["Date"] = (
        monthly_sales[date_col]
        .dt
        .to_timestamp()
    )


    return monthly_sales[
        [
            "Date",
            "Revenue"
        ]
    ]





# =====================================================
# HR DATA PREPARATION
# =====================================================

def prepare_hr_data(df):

    semantic = build_semantic_model(df)


    date_col = semantic.get("date")
    value_col = semantic.get("price")


    if (
        date_col is None
        or value_col is None
    ):
        return None



    data = df.copy()



    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce"
    )


    data[value_col] = pd.to_numeric(
        data[value_col],
        errors="coerce"
    )


    data = data.dropna(
        subset=[
            date_col,
            value_col
        ]
    )


    if len(data) == 0:
        return None



    monthly_hr = (

        data

        .groupby(
            data[date_col]
            .dt
            .to_period("M")
        )[value_col]

        .sum()

        .reset_index()

    )


    monthly_hr["Date"] = (
        monthly_hr[date_col]
        .dt
        .to_timestamp()
    )


    monthly_hr.rename(
        columns={
            value_col:"TrainingCost"
        },
        inplace=True
    )


    return monthly_hr[
        [
            "Date",
            "TrainingCost"
        ]
    ]





# =====================================================
# FRAUD DATA PREPARATION
# =====================================================

def prepare_fraud_data(df):

    semantic = build_semantic_model(df)

    date_col = semantic.get("date")
    amount_col = semantic.get("amount")


    if date_col is None or amount_col is None:
        return None


    data = df.copy()


    data[date_col] = pd.to_numeric(
        data[date_col],
        errors="coerce"
    )


    data[amount_col] = pd.to_numeric(
        data[amount_col],
        errors="coerce"
    )


    data = data.dropna(
        subset=[
            date_col,
            amount_col
        ]
    )


    if len(data) == 0:
        return None


    fraud_data = (

        data

        .groupby(date_col)[amount_col]

        .sum()

        .reset_index()

    )


    fraud_data.rename(
        columns={
            date_col: "Date",
            amount_col: "TransactionVolume"
        },
        inplace=True
    )


    return fraud_data[
        [
            "Date",
            "TransactionVolume"
        ]
    ]
# =====================================================
# GENERIC FORECAST ENGINE
# =====================================================

def run_forecast(data, value_column, periods=6):

    if data is None:
        return None, None

    if len(data) < 3:
        return None, None

    historical = data.copy()

    historical["TimeIndex"] = np.arange(len(historical))

    model = LinearRegression()

    model.fit(
        historical[["TimeIndex"]],
        historical[value_column]
    )

    future = pd.DataFrame({
        "TimeIndex": np.arange(
            len(historical),
            len(historical) + periods
        )
    })

    future[value_column] = model.predict(
        future[["TimeIndex"]]
    )

    return historical, future

# =====================================================
# GENERIC BUSINESS FORECAST
# =====================================================

def generate_forecast(df, months=6):

    print("FORECAST STARTED")

    data = prepare_forecast_data(df)

    print("FORECAST DATA")
    print(data)

    data = prepare_forecast_data(df)


    if data is None:
        return None, None


    historical, future = run_forecast(
        data,
        value_column="ForecastValue",
        periods=months
    )


    if historical is None:
        return None, None



    future["Date"] = pd.date_range(
        start=historical["Date"].max()
        +
        pd.DateOffset(months=1),

        periods=months,

        freq="MS"
    )


    return historical, future


# =====================================================
# SALES FORECAST
# =====================================================

def forecast_sales(df, months=6):

    sales = prepare_sales_data(df)

    if sales is None:
        return None, None

    historical, future = run_forecast(
        sales,
        value_column="Revenue",
        periods=months
    )

    if historical is None:
        return None, None

    future["Date"] = pd.date_range(
        start=historical["Date"].max() + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    return historical, future


# =====================================================
# HR FORECAST
# =====================================================

def forecast_hr(df, months=6):

    hr = prepare_hr_data(df)

    if hr is None:
        return None, None

    historical, future = run_forecast(
        hr,
        value_column="TrainingCost",
        periods=months
    )

    if historical is None:
        return None, None

    future["Date"] = pd.date_range(
        start=historical["Date"].max() + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    return historical, future


# =====================================================
# FRAUD FORECAST
# =====================================================

def forecast_fraud(df, months=6):

    fraud = prepare_fraud_data(df)

    if fraud is None:
        return None, None

    historical, future = run_forecast(
        fraud,
        value_column="TransactionVolume",
        periods=months
    )

    if historical is None:
        return None, None

    future["Date"] = np.arange(
        historical["Date"].max() + 1,
        historical["Date"].max() + months + 1
    )

    return historical, future
