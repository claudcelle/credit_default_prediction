"""Dataset splitting and containers for features, targets and model splits."""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset_train_val_test(df, random_state=42, test_size=0.2, proportion = 'equal')-> tuple[pd.DataFrame]:

    if proportion == 'equal':
        df_full_train, df_test = train_test_split(df, test_size=test_size, random_state=random_state)
        test_size = (test_size)/(1-test_size)
        df_train, df_val = train_test_split(df_full_train, test_size=test_size, random_state=random_state)


    return df_train, df_val, df_test


def split_feature_target_columns(
    df, target_columns: list[str], training_columns: list[str] | None = None
):
    if training_columns is None:
        training_columns = [c for c in df.columns if c not in target_columns]

    S = IOData(df[training_columns], df[target_columns])
    return S


class IOData:
    def __init__(self, features, targets):
        self.features = features
        self.targets = targets
        # self.to_matrices()

    def __repr__(self):
        return f"Features: {self.features}\nTargets: {self.targets}"

    def to_matrices(self):
        self.X = self.features.to_numpy()
        self.y = self.targets.to_numpy()
        self.Xe = np.column_stack([np.ones(self.X.shape[0]), self.X])


class ModelData:
    def __init__(self, train, val, test):
        self.train = train
        self.val = val
        self.test = test

    def vectorize(self, *, sparse=True, fill_value=0):
        from sklearn.feature_extraction import DictVectorizer

        dv = DictVectorizer(sparse=sparse)

        train_dicts = (
            self.train.features
            .fillna(fill_value)
            .to_dict(orient="records")
        )
        self.train.X = dv.fit_transform(train_dicts)

        for split in (self.val, self.test):
            records = (
                split.features
                .fillna(fill_value)
                .to_dict(orient="records")
            )
            split.X = dv.transform(records)

        for split in (self.train, self.val, self.test):
            split.y = split.targets.to_numpy()

        return dv

    @classmethod
    def from_dataframe(
        cls,
        df,
        target_columns: list[str],
        training_columns: list[str] | None = None,
        random_state: int = 42,
        test_size: float = 0.2,
    ):
        if not 0 < test_size < 0.5:
            raise ValueError("test_size deve essere tra 0 e 0.5 esclusi")

        splits = split_dataset_train_val_test(df, random_state=random_state, test_size=test_size)

        train, val, test = (
            split_feature_target_columns(
                subset,
                target_columns=target_columns,
                training_columns=training_columns,
            )
            for subset in splits
        )

        return cls(train=train, val=val, test=test)
