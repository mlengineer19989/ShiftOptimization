from pydantic import BaseModel, Field
import typing as tp

class TaskBase(BaseModel):
    title:tp.Optional[str] = Field(None, example="クリーニングを取りに行く")

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id:int

    class Config:
        orm_mode = True

class Task(TaskBase):
    id:int
    done:bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
