def detect_dataset(df):

    if df is None:
        return "generic"


    columns = [
        col.lower()
        .replace(" ","")
        for col in df.columns
    ]


    # SALES FIRST
    if (
    any("orderdate" in c for c in columns)
    and
    any(
        "quantity" in c
        for c in columns
    )
):
        return "sales"



    # FRAUD

    if (
        "isfraud" in columns
        or "oldbalanceorg" in columns
    ):
        return "fraud"



    # HR

    if (
        "employeeid" in columns
        or "department" in columns
        or "salary" in columns
    ):
        return "hr"



    # CUSTOMER

    if (
        "customerkey" in columns
        or "firstname" in columns
    ):
        return "customer"



    # PRODUCT

    if (
        "productkey" in columns
        or "productcost" in columns
    ):
        return "product"



    return "generic"