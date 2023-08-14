from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
from pathlib import Path

from optimizer import ScheduleOptimizer

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/optimize/")
async def optimize(n_member_day:int, upload_file: UploadFile = File(...)):
    df_request_table = pd.read_csv(upload_file.file, index_col=0, header=0)

    #最適化実行
    opt = ScheduleOptimizer(df_request_table, n_member_day)
    solution_df:pd.DataFrame = opt.optimize()

    # TODO :データの保存先をどうするかは要検討
    csv_path:Path = Path(__file__).parent / "data/uploaded_file/optimized_shift.csv"
    solution_df.to_csv(csv_path)
    response = FileResponse(
                            path=csv_path,
                            filename="optimized_shift.csv"
                            )
    return response

if __name__ == "__main__":
    #本pyファイルの実行または、コマンド"uvicorn main:app --reload"でも実行可能。
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)