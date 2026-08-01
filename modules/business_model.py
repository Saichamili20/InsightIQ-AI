import pandas as pd


def load_csv(path):

    return pd.read_csv(
        path,
        encoding="latin1",
        low_memory=False
    )


def load_file(path):

    if path.lower().endswith(".csv"):
        return load_csv(path)

    elif path.lower().endswith(".xlsx"):
        return pd.read_excel(path)

    return None



def merge_dimension(fact, dim, key):

    if (
        key not in fact.columns
        or
        key not in dim.columns
    ):
        return fact


    fact[key] = fact[key].astype(str)
    dim[key] = dim[key].astype(str)


    merged = fact.merge(
        dim,
        on=key,
        how="left",
        suffixes=("", "_dup")
    )


    duplicate_cols = [
        c for c in merged.columns
        if c.endswith("_dup")
    ]


    merged.drop(
        columns=duplicate_cols,
        inplace=True
    )


    return merged




def build_business_model(datasets, table_info=None):


    # -------------------------------
    # Single file mode
    # -------------------------------

    if len(datasets) == 1:

        file = list(datasets.values())[0]

        return load_file(file)



    # -------------------------------
    # ZIP mode
    # -------------------------------

    if table_info is None:

        return None



    fact_tables = table_info.get(
        "fact_tables",
        []
    )


    if not fact_tables:

        return None



    # Only sales tables

    sales_tables = [

        table

        for table in fact_tables

        if "sales" in table.lower()

    ]


    if not sales_tables:

        return None



    # Combine sales years

    frames = []


    for table in sales_tables:

        frames.append(
            load_csv(
                datasets[table]
            )
        )


    business_df = pd.concat(
        frames,
        ignore_index=True
    )



    lookup_keys = [

        "ProductKey",
        "CustomerKey",
        "TerritoryKey",
        "ProductSubcategoryKey",
        "ProductCategoryKey"

    ]



    # -------------------------------
    # Merge dimensions
    # -------------------------------

    for table, path in datasets.items():


        if table in sales_tables:

            continue



        if "return" in table.lower():

            print(
                "Skipping returns table"
            )

            continue



        try:


            dim = load_csv(path)



            for key in lookup_keys:


                if (
                    key in business_df.columns
                    and
                    key in dim.columns
                ):


                    print(
                        f"Merging {table} on {key}"
                    )


                    business_df = merge_dimension(
                        business_df,
                        dim,
                        key
                    )


                    print(
                        "After merge shape:",
                        business_df.shape
                    )


                    break



        except Exception as e:


            print(
                table,
                e
            )



    return business_df