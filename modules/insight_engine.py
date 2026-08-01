import pandas as pd



def analyze_dataset(df):

    analysis = {}


    # --------------------------------
    # Basic Information
    # --------------------------------

    analysis["rows"] = df.shape[0]

    analysis["columns"] = df.shape[1]



    # --------------------------------
    # Column Type Detection
    # --------------------------------

    analysis["numeric_columns"] = (
        df.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )


    analysis["categorical_columns"] = (
        df.select_dtypes(
            include="object"
        )
        .columns
        .tolist()
    )



    # --------------------------------
    # Date Detection
    # --------------------------------

    date_columns = []


    for col in df.columns:

        name = col.lower()


        # Column name based detection

        if (
            "date" in name
            or "time" in name
            or "year" in name
        ):

            date_columns.append(col)

            continue



        # Only check object columns
        # Avoid converting numbers into dates

        if df[col].dtype == "object":

            try:

                converted = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )


                ratio = (
                    converted.notna()
                    .mean()
                )


                if ratio > 0.8:

                    date_columns.append(col)


            except:

                pass



    analysis["date_columns"] = date_columns




    # --------------------------------
    # Binary Columns
    # --------------------------------

    binary_columns = []


    for col in df.columns:

        unique_values = (
            df[col]
            .dropna()
            .unique()
        )


        if len(unique_values) == 2:

            binary_columns.append(col)


    analysis["binary_columns"] = binary_columns




    # --------------------------------
    # ID Detection
    # --------------------------------

    id_columns = []


    for col in df.columns:

        name = col.lower()


        # Skip dates

        if col in date_columns:

            continue



        if (
            "id" in name
            or "key" in name
        ):

            id_columns.append(col)



        # High uniqueness columns
        # Only object columns

        elif df[col].dtype == "object":


            unique_ratio = (
                df[col].nunique()
                /
                len(df)
            )


            if unique_ratio > 0.95:

                id_columns.append(col)



    analysis["id_columns"] = id_columns




    # --------------------------------
    # Measure Detection
    # --------------------------------

    measures = []


    for col in analysis["numeric_columns"]:


        name = col.lower()



        if col in id_columns:

            continue



        # Remove flags / labels

        if (
            "flag" in name
            or "fraud" in name
            or "status" in name
            or name.startswith("is")
        ):

            continue
            if (
                "step" in name
                or "year" in name
                or "month" in name
    ):
                continue



        unique_ratio = (
            df[col]
            .nunique()
            /
            len(df)
        )



        if unique_ratio < 0.95:

            measures.append(col)



    analysis["measure_columns"] = measures




    # --------------------------------
    # Dimension Detection
    # --------------------------------

    dimensions = []


    for col in analysis["categorical_columns"]:


        if col in id_columns:

            continue



        unique_count = (
            df[col]
            .nunique()
        )



        if unique_count < 100:

            dimensions.append(col)



    analysis["dimension_columns"] = dimensions



    return analysis