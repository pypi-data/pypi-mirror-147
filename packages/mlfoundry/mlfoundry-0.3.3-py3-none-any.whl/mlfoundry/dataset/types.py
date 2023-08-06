import enum
import typing

import pandas as pd
from pydantic import BaseModel
from whylogs import DatasetProfile


class FieldType(enum.Enum):
    NUMERICAL = "NUMERICAL"
    CATEGORICAL = "CATEGORICAL"
    EMPTY = "EMPTY"


class InferredFieldType(BaseModel):
    field_type: typing.Optional[FieldType]
    pandas_inferred_dtype: str


class Schema(BaseModel):
    features: typing.Dict[str, InferredFieldType]

    # only supports scalar output at this point
    # we do not support multi-label
    actuals: typing.Optional[InferredFieldType] = None
    predictions: typing.Optional[InferredFieldType] = None


class Profiles(BaseModel):
    features: DatasetProfile
    actuals: typing.Optional[DatasetProfile] = None
    predictions: typing.Optional[DatasetProfile] = None

    class Config:
        arbitrary_types_allowed = True


class DataSet(BaseModel):
    features: pd.DataFrame
    actuals: typing.Optional[pd.Series] = None
    predictions: typing.Optional[pd.Series] = None

    class Config:
        arbitrary_types_allowed = True
