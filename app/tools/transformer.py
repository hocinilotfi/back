from typing import List, Optional
import pandas
import os
from joblib import load, dump
import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


# scale function
def scale_score(score: int, max_score: int, scale: int) -> int:
    """fonction de mise en echelle

    Args:
        score (int): score actuel
        max_score (int): score max définit à partir des seuils
        scale (int): échelle

    Returns:
        int: score mis à échele
    """
    return round((score * scale) / max_score)


# grade into score function
def grade_into_score(
    grade: float, thresholds: List[float], scale: Optional[int] = None
) -> int:
    """
    Convertit une note en un score d'accompagnement en fonction
    des seuils donnés et d'un facteur de mise à l'échelle (facultatif).

    Args:
    - score (int): La note de l'étudiant.
    - thresholds (List[float]): est une liste de  seuils , par exp, [5, 10], on aura alors 3 groupes:
        [0-5], [5,10] et [10,20]
    - Plus la note est petite, plus le score est grand et vice versa.
    - scale (Optional[int]): Facteur de mise à l'échelle facultatif pour ajuster le score.

    Returns:
    - score (int): Le score accompagnement calculé.
    """

    # la liste des threshols doit contenir au moins un élement
    if thresholds == []:
        thresholds.append(10)

    # Éliminer 0 et 20 de la liste des seuils
    if 0 in thresholds or 20 in thresholds:
        thresholds = [x for x in thresholds if x not in [0, 20]]

    # Éliminer les élements redondants
    thresholds = list(set(thresholds))

    sorted_thresholds = sorted(thresholds)
    sorted_thresholds.append(20)
    number_of_groups = len(sorted_thresholds)
    if scale != None:
        if scale < number_of_groups:
            scale = None

    for i in range(0, number_of_groups):
        if i == 0:
            if grade <= sorted_thresholds[0]:
                score = number_of_groups - i - 1
                if scale != None:
                    return scale_score(
                        score=score, max_score=number_of_groups - 1, scale=scale
                    )
                return score
        else:
            if sorted_thresholds[i - 1] < grade <= sorted_thresholds[i]:
                score = number_of_groups - i - 1
                if scale != None:
                    return scale_score(
                        score=score, max_score=number_of_groups - 1, scale=scale
                    )
                return score


# automatic binary categorical feature encoder
def encode_binary_categorical_features(df_original: pandas.DataFrame) -> pd.DataFrame:
    # Binary feature encoder
    df = df_original.copy()

    for column in df.columns:
        num_values = df[column].nunique()
        first_value = df[column].unique()[0]
        second_value = df[column].unique()[1]
        a = 1
        b = 0
        if first_value == "yes" or first_value == 1:
            a = 1
            b = 0
        else:
            a = 0
            b = 1
        if num_values == 2:
            df[column].replace({first_value: a, second_value: b}, inplace=True)
    return df


# automatic binary categorical feature encoder code generatore and saver
def encode_binary_categorical_features_code_generator(
    df_original: pandas.DataFrame, output_file=None
) -> None:
    # Binary feature encoder code generator
    df = df_original.copy()
    for column in df.columns:
        num_values = df[column].nunique()
        first_value = df[column].unique()[0]
        second_value = df[column].unique()[1]
        a = 1
        b = 0
        if first_value == "yes" or first_value == 1:
            a = 1
            b = 0
        else:
            a = 0
            b = 1
        if num_values == 2:
            print(
                f"{column}_mapping = {{ '{first_value}': {a}, '{second_value}': {b} }}"
            )
            print(f"df['{column}'] = df['{column}'].replace({column}_mapping)")
            if output_file != None:
                with open(output_file, "a") as f:
                    f.write(
                        f"{column}_mapping = {{ '{first_value}': {a}, '{second_value}': {b} }}\n"
                    )
                    f.write(
                        f"df['{column}'] = df['{column}'].replace({column}_mapping)\n"
                    )


# automatic categorical features encoder and saver
def encode_categorical_features_onehot(
    df_original: pandas.DataFrame, output_file
) -> pd.DataFrame:
    df = df_original.copy()
    from sklearn.preprocessing import OneHotEncoder

    catigorical_columns_to_encode = []
    for column in df.columns:
        if df[column].dtype == "object" and df[column].nunique() > 2:
            catigorical_columns_to_encode.append(column)
    # Separate categorical and numerical columns
    # categorical_cols = ['sex','smoker' , 'region']
    numerical_cols = [
        col for col in df.columns if col not in catigorical_columns_to_encode
    ]

    # One-hot encode categorical columns
    encoder = OneHotEncoder()
    encoder.fit(df[catigorical_columns_to_encode])
    if output_file != None:

        dump(encoder, output_file)
    encoded_categorical = encoder.transform(df[catigorical_columns_to_encode]).toarray()

    # Create a DataFrame for the encoded categorical columns
    encoded_categorical_df = pd.DataFrame(
        encoded_categorical,
        columns=encoder.get_feature_names_out(catigorical_columns_to_encode),
        index=df.index,
    )

    # Combine encoded categorical columns with numerical columns
    encoded_df = pd.concat([encoded_categorical_df, df[numerical_cols]], axis=1)
    return encoded_df
