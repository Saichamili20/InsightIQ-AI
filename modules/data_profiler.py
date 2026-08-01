import shutil
import uuid
import os
import zipfile
import pandas as pd
def extract_zip(uploaded_file):

    base_path = "data"

    # Delete previous uploads completely
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    # Create fresh folder
    os.makedirs(base_path)


    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall(base_path)


    return base_path


def load_dataset(folder):

    datasets = {}

    for root, dirs, files in os.walk(folder):

        for file in files:

            if file.lower().endswith(".csv"):

                full_path = os.path.join(root,file)

                datasets[file] = full_path


    return datasets

import pandas as pd


def profile_dataset(df):

    if df is None:
        return {}


    profile = {

        "Rows": int(df.shape[0]),

        "Columns": int(df.shape[1]),


        "Missing Values":
            int(df.isna().sum().sum()),


        "Missing Percentage":
            round(
                (df.isna().sum().sum() /
                (df.shape[0] * df.shape[1])) * 100,
                2
            ),


        "Duplicates":
            int(df.duplicated().sum()),


        "Memory Usage":
            round(
                df.memory_usage(deep=True)
                .sum()
                /
                1024**2,
                2
            ),


        "Numeric Columns":
            len(
                df.select_dtypes(
                    include="number"
                ).columns
            ),


        "Categorical Columns":
            len(
                df.select_dtypes(
                    include="object"
                ).columns
            ),


        "Date Columns":
            len(
                [
                    col
                    for col in df.columns
                    if "date" in col.lower()
                ]
            )

    }


    return profile