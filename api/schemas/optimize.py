from fastapi import UploadFile, File
from pydantic import Field, field_validator, conint
from pydantic import BaseModel as PydanticBaseModel
import typing as tp
import pandas as pd

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class RequestedSchedule(BaseModel):
    n_member_day:conint(strict=True, ge=1)
    upload_file: tp.Optional[UploadFile]

    # TODO :以下のように改めてコンストラクタでself.upload_fileを定義しないと、self.upload_fileがNoneになってしまう。できれば、以下のコンストラクタは無くしたい。
    def __init__(self, n_member_day, upload_file):
        super().__init__(n_member_day=n_member_day)
        self.upload_file = upload_file

    # TODO: upload_file.fileの形式がcsvであることもvalidationしたい。
    @field_validator("upload_file")
    def check_upload_file(cls, upload_file):
        pass

    def generate_df(self) -> pd.DataFrame:
        return pd.read_csv(self.upload_file.file, index_col=0, header=0)