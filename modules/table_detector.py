import pandas as pd


def detect_table_roles(datasets):

    result = {

        "fact_tables": [],

        "dimension_tables": [],

        "dataset_type": "generic"

    }


    for name, path in datasets.items():

        try:

            df = pd.read_csv(
                path,
                encoding="latin1",
                low_memory=False,
                nrows=100
            )


            columns = [
                c.lower().replace(" ","")
                for c in df.columns
            ]


            score = 0


            if any(
                "order" in c
                for c in columns
            ):
                score += 3


            if any(
                "orderquantity" in c
                for c in columns
            ):
                score += 3

            if any(
                "product" in c
                for c in columns
            ):
                score += 2


            if any(
                "customer" in c
                for c in columns
            ):
                score += 2

            if any(
                "return" in c
                for c in columns
            ):
                score -= 5



            if score >= 5:

                result["fact_tables"].append(
                    name
                )

            else:

                result["dimension_tables"].append(
                    name
                )



        except Exception as e:

            print(e)



    if result["fact_tables"]:

        result["dataset_type"]="sales"



    return result