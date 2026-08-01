import pandas as pd


def understand_dataset(df):

    columns = [
        col.lower()
        for col in df.columns
    ]


    result = {
        "type": "generic",
        "date_columns": [],
        "numeric_columns": [],
        "categorical_columns": []
    }


    # -----------------------------
    # Detect column types
    # -----------------------------

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            result["numeric_columns"].append(col)


        elif pd.api.types.is_datetime64_any_dtype(df[col]):

            result["date_columns"].append(col)


        else:

            result["categorical_columns"].append(col)



    # -----------------------------
    # Sales Detection
    # -----------------------------

    sales_keywords = [
        "sales",
        "revenue",
        "price",
        "amount",
        "quantity",
        "order"
    ]


    sales_score = sum(
        1
        for word in sales_keywords
        if any(word in col for col in columns)
    )


    # -----------------------------
    # Fraud Detection
    # -----------------------------

    fraud_keywords = [
        "fraud",
        "isfraud",
        "transaction",
        "risk"
    ]


    fraud_score = sum(
        1
        for word in fraud_keywords
        if any(word in col for col in columns)
    )


    # -----------------------------
    # HR Detection
    # -----------------------------

    hr_keywords = [
        "employee",
        "salary",
        "department",
        "attrition",
        "joining"
    ]


    hr_score = sum(
        1
        for word in hr_keywords
        if any(word in col for col in columns)
    )



    # -----------------------------
    # Decide Dataset Type
    # -----------------------------

    scores = {

        "sales": sales_score,

        "fraud": fraud_score,

        "hr": hr_score

    }


    best_match = max(
        scores,
        key=scores.get
    )


    if scores[best_match] > 0:

        result["type"] = best_match



    return result