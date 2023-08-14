import pandas as pd
from pydantic import BaseModel as PydanticBaseModel
from pydantic.dataclasses import dataclass

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Entity(BaseModel):
    df_request_table:pd.DataFrame
    n_member_day:int