import fnmatch
import os
import posixpath
import tempfile
import typing

import pandas as pd
from mlflow.tracking import MlflowClient
from pydantic import BaseModel
from whylogs import DatasetProfile

from mlfoundry.dataset.types import Profiles, Schema
from mlfoundry.enums import FileFormat
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.log_types import TabularDatasetStats

DATASET_PREFIX = os.path.join("mlf", "tabular-dataset")


def _save_dataframe(
    local_dir: str,
    entity_name: str,
    dataframe: pd.DataFrame,
    file_format: FileFormat,
) -> str:
    file_name = f"{entity_name}.{file_format.value}"
    file_path = os.path.join(local_dir, file_name)

    if file_format is FileFormat.PARQUET:
        dataframe.to_parquet(file_path, index=False)
    elif file_format is FileFormat.CSV:
        dataframe.to_csv(file_path, index=False)
    else:
        raise MlFoundryException(f"cannot save dataframe in {file_format} file format")

    return file_path


def _load_dataframe(local_file_path: str) -> pd.DataFrame:
    _, file_ext = os.path.splitext(local_file_path)
    if len(file_ext) <= 1:
        raise MlFoundryException(
            f"cannot recognize file format, '{file_ext}' is not valid"
        )
    # ".csv" -> "csv"
    file_ext = file_ext[1:]
    file_format = FileFormat(file_ext)

    if file_format is FileFormat.CSV:
        return pd.read_csv(local_file_path)
    elif file_format is FileFormat.PARQUET:
        return pd.read_parquet(local_file_path)
    else:
        raise MlFoundryException(
            f"cannot load dataframe from {file_format} file format"
        )


def _save_series(
    local_dir: str,
    entity_name: str,
    series: pd.Series,
    file_format: FileFormat,
):
    dataframe = series.to_frame()
    return _save_dataframe(
        local_dir=local_dir,
        entity_name=entity_name,
        dataframe=dataframe,
        file_format=file_format,
    )


def _load_series(local_file_path: str) -> pd.Series:
    dataframe = _load_dataframe(local_file_path)
    return dataframe.iloc[:, 0]


def _save_pydantic_as_json(local_dir: str, file_name: str, model: BaseModel):
    with open(os.path.join(local_dir, file_name), "w") as fp:
        fp.write(model.json())


class TabularDatasetSerDe:
    _FEATURE_ENTITY_NAME = "features"
    _PREDICTIONS_ENTITY_NAME = "predictions"
    _ACTUALS_ENTITY_NAME = "actuals"
    _SCHEMA_FILE_NAME = "schema.json"
    _STATS_FILE_NAME = "stats.json"
    _FEATURES_PROFILE_FILE_NAME = "features_profile.pb.bin"
    _PREDICTIONS_PROFILE_FILE_NAME = "predictions_profile.pb.bin"
    _ACTUALS_PROFILE_FILE_NAME = "actuals_profile.pb.bin"

    def __init__(self, mlflow_client: MlflowClient):
        self.mlflow_client: MlflowClient = mlflow_client
        self.dataset_prefix = DATASET_PREFIX

    def _get_artifact_dir(self, dataset_name: str) -> str:
        return os.path.join(self.dataset_prefix, dataset_name)

    def _get_versioned_artifact_dir(self, dataset_name: str, version: str) -> str:
        return os.path.join(self._get_artifact_dir(dataset_name), version)

    def get_latest_version(self, run_id: str, dataset_name: str) -> str:
        dataset_artifact_dir = self._get_artifact_dir(dataset_name)
        number_of_versions_present = len(
            self.mlflow_client.list_artifacts(run_id=run_id, path=dataset_artifact_dir)
        )
        return str(number_of_versions_present)

    def _get_artifact_dir_new_version(
        self, run_id: str, dataset_name: str
    ) -> typing.Tuple[str, str]:
        last_version = self.get_latest_version(run_id=run_id, dataset_name=dataset_name)
        version = str(int(last_version) + 1)
        return (
            self._get_versioned_artifact_dir(dataset_name, version=version),
            version,
        )

    def _get_latest_dataset_artifact_dir(self, run_id: str, dataset_name: str) -> str:
        latest_version = self.get_latest_version(
            run_id=run_id, dataset_name=dataset_name
        )
        return self._get_versioned_artifact_dir(dataset_name, version=latest_version)

    def _list_artifacts_with_pattern(
        self, run_id: str, path: str, pattern: str
    ) -> typing.List:
        return [
            file_info
            for file_info in self.mlflow_client.list_artifacts(run_id=run_id, path=path)
            if fnmatch.fnmatch(file_info.path, pattern)
        ]

    def _save_profiles(self, local_dir, profiles: Profiles):
        features_profile_path = os.path.join(
            local_dir, TabularDatasetSerDe._FEATURES_PROFILE_FILE_NAME
        )
        profiles.features.write_protobuf(features_profile_path)

        if profiles.predictions is not None:
            predictions_profile_path = os.path.join(
                local_dir, TabularDatasetSerDe._PREDICTIONS_PROFILE_FILE_NAME
            )
            profiles.predictions.write_protobuf(predictions_profile_path)

        if profiles.actuals is not None:
            actuals_profile_path = os.path.join(
                local_dir, TabularDatasetSerDe._ACTUALS_PROFILE_FILE_NAME
            )
            profiles.actuals.write_protobuf(actuals_profile_path)

    def _load_file(
        self,
        run_id: str,
        dataset_name: str,
        version: str,
        file_name: str,
        deserializer: typing.Callable,
    ):
        dataset_artifact_dir = self._get_versioned_artifact_dir(
            dataset_name, version=version
        )
        file_path = os.path.join(dataset_artifact_dir, file_name)
        artifacts = self._list_artifacts_with_pattern(
            run_id=run_id, path=dataset_artifact_dir, pattern=file_path
        )
        if len(artifacts) == 0:
            return None
        artifact_path = artifacts[0].path
        with tempfile.TemporaryDirectory() as local_dir:
            local_path = self.mlflow_client.download_artifacts(
                run_id, artifact_path, local_dir
            )
            return deserializer(local_path)

    def _load_entity(
        self,
        run_id: str,
        dataset_name: str,
        entity_name: str,
        version: str,
        deserializer: typing.Callable,
    ):
        dataset_artifact_dir = self._get_versioned_artifact_dir(
            dataset_name, version=version
        )
        # for features, predictions, actuals we may either save it as parquet
        # or CSV. Either feature.csv or feature.parquet.
        # So here we just search a pattern like `feature.*` to
        # get the artifact, then deserializer will take care of the rest
        pattern = posixpath.join(dataset_artifact_dir, f"{entity_name}.*")
        artifacts = self._list_artifacts_with_pattern(
            run_id=run_id, path=dataset_artifact_dir, pattern=pattern
        )
        if len(artifacts) == 0:
            return None

        artifact_path = artifacts[0].path
        with tempfile.TemporaryDirectory() as local_dir:
            local_path = self.mlflow_client.download_artifacts(
                run_id, artifact_path, local_dir
            )
            return deserializer(local_path)

    def save_dataset(
        self,
        run_id: str,
        dataset_name: str,
        features: pd.DataFrame,
        predictions: typing.Optional[pd.Series],
        actuals: typing.Optional[pd.Series],
        schema: Schema,
        stats: TabularDatasetStats,
        profiles: Profiles,
        file_format: FileFormat,
        only_stats: bool,
    ) -> str:
        with tempfile.TemporaryDirectory() as local_dir:
            if not only_stats:
                _save_dataframe(
                    local_dir=local_dir,
                    entity_name=TabularDatasetSerDe._FEATURE_ENTITY_NAME,
                    dataframe=features,
                    file_format=file_format,
                )

                if predictions is not None:
                    _save_series(
                        local_dir=local_dir,
                        entity_name=TabularDatasetSerDe._PREDICTIONS_ENTITY_NAME,
                        series=predictions,
                        file_format=file_format,
                    )
                if actuals is not None:
                    _save_series(
                        local_dir=local_dir,
                        entity_name=TabularDatasetSerDe._ACTUALS_ENTITY_NAME,
                        series=actuals,
                        file_format=file_format,
                    )

            _save_pydantic_as_json(
                local_dir=local_dir,
                file_name=TabularDatasetSerDe._SCHEMA_FILE_NAME,
                model=schema,
            )
            _save_pydantic_as_json(
                local_dir=local_dir,
                file_name=TabularDatasetSerDe._STATS_FILE_NAME,
                model=stats,
            )
            self._save_profiles(local_dir=local_dir, profiles=profiles)

            artifact_path, version = self._get_artifact_dir_new_version(
                run_id=run_id, dataset_name=dataset_name
            )
            self.mlflow_client.log_artifacts(
                run_id=run_id, local_dir=local_dir, artifact_path=artifact_path
            )
            return version

    def load_schema(self, run_id: str, dataset_name: str, version: str) -> Schema:
        return self._load_file(
            run_id=run_id,
            dataset_name=dataset_name,
            version=version,
            file_name=TabularDatasetSerDe._SCHEMA_FILE_NAME,
            deserializer=Schema.parse_file,
        )

    def load_stats(
        self, run_id: str, dataset_name: str, version: str
    ) -> TabularDatasetStats:
        return self._load_file(
            run_id=run_id,
            dataset_name=dataset_name,
            version=version,
            file_name=TabularDatasetSerDe._STATS_FILE_NAME,
            deserializer=TabularDatasetStats.parse_file,
        )

    def load_profiles(self, run_id: str, dataset_name: str, version: str) -> Profiles:
        features_profile = self._load_file(
            run_id=run_id,
            dataset_name=dataset_name,
            version=version,
            file_name=TabularDatasetSerDe._FEATURES_PROFILE_FILE_NAME,
            deserializer=DatasetProfile.read_protobuf,
        )
        actuals_profile = self._load_file(
            run_id=run_id,
            dataset_name=dataset_name,
            version=version,
            file_name=TabularDatasetSerDe._ACTUALS_PROFILE_FILE_NAME,
            deserializer=DatasetProfile.read_protobuf,
        )
        predictions_profile = self._load_file(
            run_id=run_id,
            dataset_name=dataset_name,
            version=version,
            file_name=TabularDatasetSerDe._PREDICTIONS_PROFILE_FILE_NAME,
            deserializer=DatasetProfile.read_protobuf,
        )
        return Profiles(
            features=features_profile,
            actuals=actuals_profile,
            predictions=predictions_profile,
        )

    def load_features(
        self, run_id: str, dataset_name: str, version: str
    ) -> typing.Optional[pd.DataFrame]:
        return self._load_entity(
            run_id=run_id,
            dataset_name=dataset_name,
            entity_name=TabularDatasetSerDe._FEATURE_ENTITY_NAME,
            deserializer=_load_dataframe,
            version=version,
        )

    def load_actuals(
        self, run_id: str, dataset_name: str, version: str
    ) -> typing.Optional[pd.DataFrame]:
        return self._load_entity(
            run_id=run_id,
            dataset_name=dataset_name,
            entity_name=TabularDatasetSerDe._ACTUALS_ENTITY_NAME,
            deserializer=_load_series,
            version=version,
        )

    def load_predictions(
        self, run_id: str, dataset_name: str, version: str
    ) -> typing.Optional[pd.DataFrame]:
        return self._load_entity(
            run_id=run_id,
            dataset_name=dataset_name,
            entity_name=TabularDatasetSerDe._PREDICTIONS_ENTITY_NAME,
            deserializer=_load_series,
            version=version,
        )
