import pandas as pd

from typing import Tuple, Union, List

class DelayModel:

    FEATURES_COLS = [
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air",
    ]

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self._feature_columns = self.FEATURES_COLS.copy()

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union(Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        features = features.reindex(columns=self._feature_columns, fill_value=0)

        if target_column is None:
            return features

        if target_column in data.columns:
            target = data[[target_column]].copy()
            return features, target

        if target_column == "delay":
            scheduled_date = pd.to_datetime(data["Fecha-I"], errors="coerce")
            operation_date = pd.to_datetime(data["Fecha-O"], errors="coerce")
            minutes_difference = (operation_date - scheduled_date).dt.total_seconds() / 60
            target = pd.DataFrame({target_column: (minutes_difference > 15).astype(int)})
            return features, target

        raise ValueError(f"Target column '{target_column}' is not available in input data.")

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return
