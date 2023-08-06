import typing

from pydantic import BaseModel

from mlfoundry.log_types.whylogs_types.summary import DataFrameSummary


class TabularDatasetStats(BaseModel):
    features: DataFrameSummary
    actuals: typing.Optional[DataFrameSummary] = None
    predictions: typing.Optional[DataFrameSummary] = None

    @property
    def log_type(self) -> str:
        return "dataset-summary-v1"
