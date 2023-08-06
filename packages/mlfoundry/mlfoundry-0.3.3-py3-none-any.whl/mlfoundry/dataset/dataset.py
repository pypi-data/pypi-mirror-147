import typing

import pandas as pd
from mlflow.tracking import MlflowClient

from mlfoundry.dataset.schema import build_schema
from mlfoundry.dataset.serde import TabularDatasetSerDe
from mlfoundry.dataset.stats import build_stats
from mlfoundry.dataset.types import DataSet, Profiles, Schema
from mlfoundry.dataset.validation import validate_dataset, validate_dataset_name
from mlfoundry.enums import FileFormat
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.log_types import TabularDatasetStats


def pre_process_features(features) -> pd.DataFrame:
    try:
        return pd.DataFrame(features).reset_index(drop=True)
    except Exception as ex:
        raise MlFoundryException("could not convert features to a DataFrame") from ex


def pre_process_actuals(actuals) -> pd.Series:
    try:
        return pd.Series(actuals).reset_index(drop=True)
    except Exception as ex:
        raise MlFoundryException("could not convert actuals to a Series") from ex


def pre_process_predictions(predictions) -> pd.Series:
    try:
        return pd.Series(predictions).reset_index(drop=True)
    except Exception as ex:
        raise MlFoundryException("could not convert predictions to a Series") from ex


class TabularDataset:
    def __init__(self, mlflow_client: MlflowClient):
        self.mlflow_client: MlflowClient = mlflow_client
        self.serde: TabularDatasetSerDe = TabularDatasetSerDe(self.mlflow_client)

    def log_dataset(
        self,
        run_id: str,
        dataset_name: str,
        features,
        predictions=None,
        actuals=None,
        only_stats: bool = False,
        file_format: FileFormat = FileFormat.PARQUET,
    ) -> str:
        validate_dataset_name(dataset_name)

        features = pre_process_features(features)
        predictions = (
            predictions if predictions is None else pre_process_predictions(predictions)
        )
        actuals = actuals if actuals is None else pre_process_actuals(actuals)

        schema = build_schema(
            features=features, predictions=predictions, actuals=actuals
        )
        validate_dataset(
            features=features, predictions=predictions, actuals=actuals, schema=schema
        )
        dataset_stats, profiles = build_stats(
            features=features, predictions=predictions, actuals=actuals
        )
        return self.serde.save_dataset(
            run_id=run_id,
            dataset_name=dataset_name,
            features=features,
            predictions=predictions,
            actuals=actuals,
            schema=schema,
            stats=dataset_stats,
            profiles=profiles,
            file_format=file_format,
            only_stats=only_stats,
        )

    def get_dataset(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> DataSet:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return DataSet(
            features=self.get_features(run_id, dataset_name, version=version),
            actuals=self.get_actuals(run_id, dataset_name, version=version),
            predictions=self.get_predictions(run_id, dataset_name, version=version),
        )

    def get_features(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> typing.Optional[pd.DataFrame]:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_features(
            run_id=run_id, dataset_name=dataset_name, version=version
        )

    def get_predictions(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> typing.Optional[pd.Series]:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_predictions(
            run_id=run_id, dataset_name=dataset_name, version=version
        )

    def get_actuals(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> typing.Optional[pd.Series]:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_actuals(
            run_id=run_id, dataset_name=dataset_name, version=version
        )

    def get_schema(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> Schema:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_schema(
            run_id=run_id, dataset_name=dataset_name, version=version
        )

    def get_stats(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> TabularDatasetStats:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_stats(
            run_id=run_id, dataset_name=dataset_name, version=version
        )

    def get_profiles(
        self, run_id: str, dataset_name: str, version: typing.Optional[str] = None
    ) -> Profiles:
        version = version or self.serde.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self.serde.load_profiles(
            run_id=run_id, dataset_name=dataset_name, version=version
        )


if __name__ == "__main__":
    import random

    import mlfoundry

    client = mlfoundry.get_client()
    # client = mlfoundry.get_client("http://localhost:5000")
    run = client.create_run("dataset-test")

    data = pd.DataFrame()
    num_rows = 10000
    data["a"] = [random.randint(-100, 100) for _ in range(num_rows)] + [None] * (
        num_rows // 4
    )
    data["b"] = [random.randint(-5, 5) for _ in range(num_rows)] + [None] * (
        num_rows // 4
    )

    data["c"] = [random.uniform(-100, 100) for _ in range(num_rows)] + [None] * (
        num_rows // 4
    )

    data["d"] = [random.choice([True, False]) for _ in range(num_rows)] + [None] * (
        num_rows // 4
    )

    data["e"] = [random.choice(["high", "low", "medium"]) for _ in range(num_rows)] + [
        None
    ] * (num_rows // 4)

    data["f"] = None
    # data.drop(data.index, inplace=True)

    dataset = TabularDataset(run.mlflow_client)
    print(
        dataset.log_dataset(
            run_id=run.run_id,
            dataset_name="my-dataset",
            features=data,
            actuals=data["a"],
            predictions=data["b"],
        )
    )
    print(
        dataset.log_dataset(
            run_id=run.run_id,
            dataset_name="my-dataset",
            features=data,
            actuals=data["a"],
            predictions=None,
        )
    )
    print(dataset.get_dataset(run_id=run.run_id, dataset_name="my-dataset"))
    print(dataset.get_schema(run_id=run.run_id, dataset_name="my-dataset"))
    print(dataset.get_stats(run_id=run.run_id, dataset_name="my-dataset"))
    print(dataset.get_profiles(run_id=run.run_id, dataset_name="my-dataset"))
