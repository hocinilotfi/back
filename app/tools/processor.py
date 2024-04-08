# dataframe encoder
from joblib import load
import os
import pandas as pd


class DataProcessor:
    def __init__(self) -> None:
        encoder_dir = os.path.dirname(__file__)
        encoder_path = os.path.join(encoder_dir, "encoders", "encoder.enc")
        self.encoder = load(encoder_path)

    def prepare_data_frame(self, df_to_prepare: pd.DataFrame) -> pd.DataFrame:
        df = df_to_prepare.copy()

        columns_to_drop = [
            "StudentID",
            "FirstName",
            "FamilyName",
        ]
        columns_to_drop_list = []
        for column in columns_to_drop:
            if column in df.columns:
                df.drop(columns=[column], inplace=True)
        #         columns_to_drop_list.append(column)
        # if len(columns_to_drop_list) > 0:
        #     df.drop(columns=columns_to_drop_list, inplace=True)

        sex_mapping = {"F": 0, "M": 1}
        df["sex"] = df["sex"].replace(sex_mapping)
        address_mapping = {"U": 0, "R": 1}
        df["address"] = df["address"].replace(address_mapping)
        famsize_mapping = {"GT3": 0, "LE3": 1}
        df["famsize"] = df["famsize"].replace(famsize_mapping)
        Pstatus_mapping = {"A": 0, "T": 1}
        df["Pstatus"] = df["Pstatus"].replace(Pstatus_mapping)
        schoolsup_mapping = {"yes": 1, "no": 0}
        df["schoolsup"] = df["schoolsup"].replace(schoolsup_mapping)
        famsup_mapping = {"no": 0, "yes": 1}
        df["famsup"] = df["famsup"].replace(famsup_mapping)
        paid_mapping = {"no": 0, "yes": 1}
        df["paid"] = df["paid"].replace(paid_mapping)
        activities_mapping = {"no": 0, "yes": 1}
        df["activities"] = df["activities"].replace(activities_mapping)
        nursery_mapping = {"yes": 1, "no": 0}
        df["nursery"] = df["nursery"].replace(nursery_mapping)
        higher_mapping = {"yes": 1, "no": 0}
        df["higher"] = df["higher"].replace(higher_mapping)
        internet_mapping = {"no": 0, "yes": 1}
        df["internet"] = df["internet"].replace(internet_mapping)
        romantic_mapping = {"no": 0, "yes": 1}
        df["romantic"] = df["romantic"].replace(romantic_mapping)

        catigorical_columns_to_encode = ["Mjob", "Fjob", "reason", "guardian"]
        numerical_cols = [
            col for col in df.columns if col not in catigorical_columns_to_encode
        ]

        encoded_categorical = self.encoder.transform(
            df[catigorical_columns_to_encode]
        ).toarray()

        # Create a DataFrame for the encoded categorical columns and drop encoded
        encoded_categorical_df = pd.DataFrame(
            encoded_categorical,
            columns=self.encoder.get_feature_names_out(catigorical_columns_to_encode),
            index=df.index,
        )

        # Combine encoded categorical columns with numerical columns
        encoded_df = pd.concat([encoded_categorical_df, df[numerical_cols]], axis=1)

        return encoded_df
