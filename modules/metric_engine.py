import pandas as pd


def generate_metrics(df, dataset_info):

    metrics = {}

    dataset_type = dataset_info["type"]


    # -----------------------------
    # Sales Metrics
    # -----------------------------

    if dataset_type == "sales":

        metrics["Total Records"] = len(df)


        # Quantity
        quantity_columns = [
            col for col in df.columns
            if "quantity" in col.lower()
        ]

        if quantity_columns:

            metrics["Total Quantity"] = int(
                df[quantity_columns[0]].sum()
            )


        # Orders
        order_columns = [
            col for col in df.columns
            if "order" in col.lower()
        ]

        if order_columns:

            metrics["Total Orders"] = df[
                order_columns[0]
            ].nunique()


        # Customers
        customer_columns = [
            col for col in df.columns
            if "customer" in col.lower()
        ]

        if customer_columns:

            metrics["Customers"] = df[
                customer_columns[0]
            ].nunique()



    # -----------------------------
    # Fraud Metrics
    # -----------------------------

    elif dataset_type == "fraud":

        metrics["Total Transactions"] = len(df)


        fraud_columns = [
            col for col in df.columns
            if "fraud" in col.lower()
        ]


        if fraud_columns:

            fraud_col = fraud_columns[0]

            metrics["Fraud Cases"] = int(
                df[fraud_col].sum()
            )


            metrics["Fraud Rate %"] = round(
                df[fraud_col].mean()*100,
                2
            )



    # -----------------------------
    # HR Metrics
    # -----------------------------

    elif dataset_type == "hr":

        metrics["Total Employees"] = len(df)


        department_columns = [
            col for col in df.columns
            if "department" in col.lower()
        ]

        if department_columns:

            metrics["Departments"] = df[
                department_columns[0]
            ].nunique()



    # -----------------------------
    # Generic Dataset
    # -----------------------------

    else:

        metrics["Rows"] = df.shape[0]

        metrics["Columns"] = df.shape[1]


        numeric_columns = df.select_dtypes(
            include="number"
        ).columns


        metrics["Numeric Fields"] = len(
            numeric_columns
        )


    return metrics