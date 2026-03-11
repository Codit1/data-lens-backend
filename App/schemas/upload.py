from typing import List, Optional
from pydantic import BaseModel

class DataSetDescription(BaseModel):
    name: str
    columns_names: List[str]
    table: List
    no_rows: int
    no_columns: int
    no_nulls_values: int
    no_nulls_values_columns: int
    no_duplicates_values: int
    no_unique_values: int
    percentage_null_values: float
    percentage_duplicates_values: float
    percentage_unique_values: float
    total_number_data: int

