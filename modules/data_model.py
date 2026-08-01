import pandas as pd


def build_business_dataset(datasets):

    tables = {name.lower(): path for name, path in datasets.items()}


    sales_tables = []


    # -----------------------------
    # Load Sales Tables
    # -----------------------------

    for name, path in tables.items():

        if "sales data" in name:

            df = pd.read_csv(
                path,
                encoding="latin1",
                low_memory=False
            )

            sales_tables.append(df)


    if not sales_tables:
        return None


    # Combine sales years

    sales = pd.concat(
        sales_tables,
        ignore_index=True
    )


    # -----------------------------
    # Load Lookup Tables
    # -----------------------------


    product = None
    customer = None
    territory = None
    category = None
    subcategory = None
    calendar = None



    for name,path in tables.items():

        if "product lookup" in name:

            product = pd.read_csv(
                path,
                encoding="latin1"
            )


        elif "customer lookup" in name:

            customer = pd.read_csv(
                path,
                encoding="latin1"
            )


        elif "territory lookup" in name:

            territory = pd.read_csv(
                path,
                encoding="latin1"
            )


        elif "product categories" in name:

            category = pd.read_csv(
                path,
                encoding="latin1"
            )


        elif "product subcategories" in name:

            subcategory = pd.read_csv(
                path,
                encoding="latin1"
            )


        elif "calendar lookup" in name:

            calendar = pd.read_csv(
                path,
                encoding="latin1"
            )
                # -----------------------------
    # Standardize Key Columns
    # -----------------------------

    key_columns = [
        "ProductKey",
        "CustomerKey",
        "TerritoryKey",
        "SalesTerritoryKey",
        "ProductSubcategoryKey",
        "ProductCategoryKey"
    ]


    for df in [
        sales,
        product,
        customer,
        territory,
        subcategory,
        category
    ]:

        if df is not None:

            for col in key_columns:

                if col in df.columns:

                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.strip()
                    )


    # -----------------------------
    # Merge Product
    # -----------------------------

    if product is not None:

        sales = sales.merge(
            product,
            on="ProductKey",
            how="left"
        )


    # -----------------------------
    # Merge Customer
    # -----------------------------

    if customer is not None:

        sales = sales.merge(
            customer,
            on="CustomerKey",
            how="left"
        )


    # -----------------------------
    # Merge Territory
    # -----------------------------

    if territory is not None:

        sales = sales.merge(
            territory,
            left_on="TerritoryKey",
            right_on="SalesTerritoryKey",
            how="left"
        )


    # -----------------------------
    # Merge Subcategory
    # -----------------------------

    if subcategory is not None:

        sales = sales.merge(
            subcategory,
            on="ProductSubcategoryKey",
            how="left"
        )


    # -----------------------------
    # Merge Category
    # -----------------------------

    if category is not None:

        sales = sales.merge(
            category,
            on="ProductCategoryKey",
            how="left"
        )


    return sales