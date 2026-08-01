from modules.semantic_model import build_semantic_model



def analyze(df, intent, question):


    semantic = build_semantic_model(df)


    intent_type = intent.get(
        "type"
    )

    metric = intent.get(
        "metric"
    )

    dimension = intent.get(
        "dimension"
    )


    q = question.lower()



    # -----------------------------
    # Total Records
    # -----------------------------

    if (
        "record" in q
        or "row" in q
    ):

        return (
            f"The dataset contains {len(df):,} records."
        )



    # -----------------------------
    # Aggregation
    # -----------------------------

    if intent_type == "aggregation":


        if metric == "quantity":


            quantity_col = semantic.get(
                "quantity"
            )


            if quantity_col:


                total = (
                    df[quantity_col]
                    .sum()
                )


                return (
                    f"Total {quantity_col}: "
                    f"{total:,.0f}"
                )



        if metric == "value":


            value_col = semantic.get(
                "value"
            )


            if value_col:


                total = (
                    df[value_col]
                    .sum()
                )


                return (
                    f"Total {value_col}: "
                    f"{total:,.2f}"
                )



    # -----------------------------
    # Fraud
    # -----------------------------

    if intent_type == "fraud":


        fraud_col = semantic.get(
            "fraud"
        )


        if fraud_col:


            fraud_cases = (
                df[fraud_col]
                .sum()
            )


            rate = (
                fraud_cases /
                len(df)
            ) * 100


            return (
                f"Fraud Cases: {fraud_cases:,.0f}\n\n"
                f"Fraud Rate: {rate:.2f}%"
            )



    # -----------------------------
    # Ranking
    # -----------------------------

    if intent_type == "ranking":



        # Product Ranking

        if dimension == "product":


            product_col = semantic.get(
                "product"
            )


            quantity_col = semantic.get(
                "quantity"
            )


            if product_col and quantity_col:


                cleaned_product = (
                    df[product_col]
                    .astype(str)
                    .str.replace(
                        r",\s*\d+$",
                        "",
                        regex=True
                    )
                )


                top = (
                    df.assign(
                        CleanProduct=cleaned_product
                    )
                    .groupby(
                        "CleanProduct"
                    )[quantity_col]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .head(5)
                )


                return {

                    "title":
                    "Top Products by Quantity",

                    "type":
                    "table",

                    "data":
                    top.rename_axis(
                        "Product"
                    )
                    .reset_index()

                }



        # Category Ranking

        if dimension == "category":


            category_col = semantic.get(
                "category"
            )


            if category_col:


                top = (
                    df[category_col]
                    .value_counts()
                    .head(5)
                )


                return {

                    "title":
                    "Top Categories",

                    "type":
                    "table",

                    "data":
                    top.rename_axis(
                        "Category"
                    )
                    .reset_index(
                        name="Count"
                    )

                }




    # -----------------------------
    # Unknown
    # -----------------------------

    return (
        "I couldn't understand the question yet. "
        "Try asking about products, quantity, sales, categories, or fraud."
    )