# https://github.com/whylabs/whylogs/blob/04f3c31baf0abd727f360805cfc6a2a1e5f53835/proto/src/summaries.proto

import enum
import typing

from pydantic import BaseModel, Field


class UniqueCountSummary(BaseModel):
    estimate: typing.Optional[float] = None
    upper: typing.Optional[float] = None
    lower: typing.Optional[float] = None


class FrequentStringItem(BaseModel):
    value: str
    estimate: str


class FrequentStringsSummary(BaseModel):
    items: typing.List[FrequentStringItem]


class FrequentDoubleItem(BaseModel):
    estimate: int
    value: float
    rank: int


class FrequentLongItem(BaseModel):
    estimate: int
    value: int
    rank: int


class FrequentNumbersSummary(BaseModel):
    doubles: typing.List[FrequentDoubleItem]
    longs: typing.List[FrequentLongItem]


class FrequentItem(BaseModel):
    estimate: int
    json_value: str


class FrequentItemsSummary(BaseModel):
    items: typing.List[FrequentItem]


@enum.unique
class InferredTypeEnum(enum.Enum):
    UNKNOWN = "UNKNOWN"
    NULL = "NULL"
    FRACTIONAL = "FRACTIONAL"
    INTEGRAL = "INTEGRAL"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"


class InferredType(BaseModel):
    type: InferredTypeEnum
    ratio: float


class SchemaSummary(BaseModel):
    inferred_type: InferredType
    type_counts: typing.Dict[str, int]


class HistogramSummary(BaseModel):
    start: typing.Optional[float] = None
    end: typing.Optional[float] = None
    width: typing.Optional[float] = None
    counts: typing.List[int]

    max: typing.Optional[float] = None
    min: typing.Optional[float] = None
    bins: typing.List[float]
    n: int


class QuantileSummary(BaseModel):
    quantiles: typing.List[float]
    quantile_values: typing.List[float]


class NumberSummary(BaseModel):
    count: int
    min: typing.Optional[float] = None
    max: typing.Optional[float] = None
    mean: typing.Optional[float] = None
    stddev: typing.Optional[float] = None

    histogram: HistogramSummary
    unique_count: UniqueCountSummary
    quantiles: QuantileSummary
    frequent_numbers: typing.Optional[FrequentNumbersSummary] = None

    is_discrete: typing.Optional[bool] = None


class CharPosSummary(BaseModel):
    character_list: str
    char_pos_map: typing.Dict[str, NumberSummary]


class StringsSummary(BaseModel):
    unique_count: UniqueCountSummary
    frequent: FrequentStringsSummary
    length: NumberSummary
    token_length: NumberSummary
    # char_pos_tracker: CharPosSummary


class Counters(BaseModel):
    count: int
    true_count: typing.Optional[int] = None
    null_count: typing.Optional[int] = None


class ColumnSummary(BaseModel):
    counters: Counters
    schema_summary: SchemaSummary = Field(alias="schema")
    number_summary: typing.Optional[NumberSummary] = None
    string_summary: typing.Optional[StringsSummary] = None
    frequent_items: typing.Optional[FrequentItemsSummary] = None
    unique_count: typing.Optional[UniqueCountSummary] = None

    class Config:
        allow_population_by_field_name = True


class DataFrameSummary(BaseModel):
    columns: typing.Dict[str, ColumnSummary] = Field(default_factory=dict)
