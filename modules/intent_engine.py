def detect_intent(question):

    q = question.lower()


    # -----------------------------
    # Ranking
    # -----------------------------

    if any(word in q for word in [
        "top",
        "highest",
        "best",
        "best selling",
        "best seller",
        "most sold",
        "maximum"
    ]):


        if any(word in q for word in [
            "product",
            "products",
            "item",
            "items"
        ]):

            return {
                "type": "ranking",
                "dimension": "product"
            }


        if any(word in q for word in [
            "category",
            "categories"
        ]):

            return {
                "type": "ranking",
                "dimension": "category"
            }



    # -----------------------------
    # Aggregation
    # -----------------------------

    if any(word in q for word in [
        "quantity",
        "units sold",
        "how many sold"
    ]):

        return {
            "type": "aggregation",
            "metric": "quantity"
        }



    if any(word in q for word in [
        "sales",
        "revenue",
        "amount",
        "value"
    ]):

        return {
            "type": "aggregation",
            "metric": "value"
        }



    # -----------------------------
    # Fraud
    # -----------------------------

    if "fraud" in q:

        return {
            "type": "fraud"
        }



    # -----------------------------
    # Count
    # -----------------------------

    if any(word in q for word in [
        "records",
        "rows",
        "entries"
    ]):

        return {
            "type": "count"
        }



    return {
        "type": "unknown"
    }