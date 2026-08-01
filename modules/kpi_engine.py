import pandas as pd
from modules.semantic_model import build_semantic_model


def generate_kpis(df, dataset_type):
    
    dataset_type = dataset_type.lower()

    semantic = build_semantic_model(df)

    kpis = {}

    kpis["📄 Total Records"] = len(df)


    # ============================
    # SALES DATASET
    # ============================

    if dataset_type == "sales":

        qty = semantic.get("quantity")
        value = semantic.get("price") or semantic.get("revenue")
        customer = semantic.get("customer")
        product = semantic.get("product")

        revenue = None
        units = None


        if qty:

            df[qty] = pd.to_numeric(
                df[qty],
                errors="coerce"
            )

            units = df[qty].sum()

            kpis["📦 Units Sold"] = int(
                units
            )


        if value and qty:

            df[value] = pd.to_numeric(
                df[value],
                errors="coerce"
            )


            revenue = (
                df[value] *
                df[qty]
            ).sum()


            kpis["💰 Revenue"] = round(
                revenue,
                2
            )


        kpis["🛒 Orders"] = len(df)


        if revenue:

            kpis["💳 Average Order Value"] = round(
                revenue / len(df),
                2
            )


        if units:

            kpis["📊 Avg Units per Order"] = round(
                units / len(df),
                2
            )


        if customer:

            kpis["👥 Customers"] = (
                df[customer]
                .nunique()
            )


        if product:

            kpis["📦 Products"] = (
                df[product]
                .nunique()
            )



    # ============================
    # FRAUD DATASET
    # ============================

    elif dataset_type == "fraud":


        amount = (
            semantic.get("amount")
            or semantic.get("value")
            or semantic.get("revenue")
            or semantic.get("price")
        )

        fraud = semantic.get("fraud")

        total_amount = None


        if amount:

            df[amount] = pd.to_numeric(
                df[amount],
                errors="coerce"
            )


            total_amount = df[amount].sum()


            kpis["💰 Transaction Volume"] = round(
                total_amount,
                2
            )


            kpis["💳 Avg Transaction Value"] = round(
                total_amount / len(df),
                2
            )


        if fraud:

            fraud_cases = df[fraud].sum()


            kpis["🚨 Fraud Cases"] = int(
                fraud_cases
            )


            kpis["📈 Fraud Rate %"] = round(
                fraud_cases / len(df) * 100,
                2
            )


            kpis["✅ Legit Transactions"] = (
                len(df) - fraud_cases
            )



    # ============================
    # HR DATASET
    # ============================

    elif dataset_type == "hr":

        employee = semantic.get("employee")
        department = semantic.get("department")


        if employee:

            kpis["👥 Employees"] = (
                df[employee]
                .nunique()
            )


        if department:

            kpis["🏢 Departments"] = (
                df[department]
                .nunique()
            )


        if "Performance Score" in df.columns:
            performance = pd.to_numeric(
                df["Performance Score"],
                errors="coerce"
            )

            if performance.notna().sum() > 0:

                kpis["⭐ Avg Performance"] = round(
                    performance.mean(),
                    2
                )




        if "Satisfaction Score" in df.columns:

            satisfaction = pd.to_numeric(
                df["Satisfaction Score"],
                errors="coerce"
            )

            if satisfaction.notna().sum() > 0:

                kpis["😊 Avg Satisfaction"] = round(
                    satisfaction.mean(),
                    2
                )


        if "Engagement Score" in df.columns:

            engagement = pd.to_numeric(
                df["Engagement Score"],
                errors="coerce"
            )

            if engagement.notna().sum() > 0:

                kpis["🤝 Avg Engagement"] = round(
                    engagement.mean(),
                    2
                )
        if "Work-Life Balance Score" in df.columns:
            worklife = pd.to_numeric(
                df["Work-Life Balance Score"],errors="coerce"
                )
            kpis["⚖️ Avg Work-Life Balance"] = round(
                worklife.mean(),
                2
                )
        status = semantic.get("status")
        if status:
            active = (
        df[status]
        .astype(str)
        .str.lower()
        .eq("active")
        .sum()
        )
            kpis["✅ Active Employees"] = int(active)
        if "Training Program Name" in df.columns:
            kpis["📚 Training Programs"] = (
                df["Training Program Name"]
                .nunique()
                )
    # ============================
    # SEMANTIC GENERIC KPIs
    # ============================

    else:

        revenue = semantic.get("forecast_target") or semantic.get("revenue")

        quantity = semantic.get("quantity")

        distance = semantic.get("distance")

        customer_rating = semantic.get("customer_rating")

        driver_rating = semantic.get("driver_rating")

        price = semantic.get("price")


        if revenue:

            df[revenue] = pd.to_numeric(
                df[revenue],
                errors="coerce"
            )

            kpis["💰 Total Value"] = round(
                df[revenue].sum(),
                2
            )

            kpis["📊 Average Value"] = round(
                df[revenue].mean(),
                2
            )


        if quantity:

            df[quantity] = pd.to_numeric(
                df[quantity],
                errors="coerce"
            )

            kpis["📦 Total Quantity"] = int(
                df[quantity].sum()
            )


        if distance:

            df[distance] = pd.to_numeric(
                df[distance],
                errors="coerce"
            )

            kpis["🚖 Avg Ride Distance"] = round(
                df[distance].mean(),
                2
            )


        if customer_rating:

            df[customer_rating] = pd.to_numeric(
                df[customer_rating],
                errors="coerce"
            )

            kpis["⭐ Customer Rating"] = round(
                df[customer_rating].mean(),
                2
            )


        if driver_rating:

            df[driver_rating] = pd.to_numeric(
                df[driver_rating],
                errors="coerce"
            )

            kpis["👨‍✈️ Driver Rating"] = round(
                df[driver_rating].mean(),
                2
            )


        if price:

            df[price] = pd.to_numeric(
                df[price],
                errors="coerce"
            )

            kpis["💲 Average Price"] = round(
                df[price].mean(),
                2
            )


    # ============================
    # COMMON
    # ============================

    kpis["❌ Missing Values"] = int(
        df.isnull()
        .sum()
        .sum()
    )


    return kpis