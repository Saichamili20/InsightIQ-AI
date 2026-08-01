def analyze_forecast(historical, future, metric):

    insights = {}


    if historical is None or future is None:
        return None



    last_actual = historical[metric].iloc[-1]

    first_prediction = future[metric].iloc[0]

    last_prediction = future[metric].iloc[-1]


    change = (
        (last_prediction - last_actual)
        /
        last_actual
        *
        100
    )


    insights["last_actual"] = round(
        last_actual,
        2
    )


    insights["future_value"] = round(
        last_prediction,
        2
    )


    insights["change_percent"] = round(
        change,
        2
    )


    if change > 0:

        insights["trend"] = "Increasing"

    elif change < 0:

        insights["trend"] = "Decreasing"

    else:

        insights["trend"] = "Stable"



    return insights