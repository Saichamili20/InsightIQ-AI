from modules.semantic_model import build_semantic_model


def check_forecast_availability(df, dataset_type=None):

    semantic = build_semantic_model(df)

    date_col = semantic.get("date")

    target_col = (
        semantic.get("forecast_target")
        or semantic.get("revenue")
        or semantic.get("amount")
    )

    if date_col and target_col:

        return (
            True,
            f"Forecast can be generated for '{target_col}'"
        )

    missing = []

    if not date_col:
        missing.append("Date")

    if not target_col:
        missing.append("Forecast Metric")

    return (
        False,
        "Missing required columns: "
        + ", ".join(missing)
    )