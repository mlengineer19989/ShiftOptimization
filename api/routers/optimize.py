#標準ライブラリ
from pathlib import Path
import platform

#追加ライブラリ
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd

#自作モジュール
import api.schemas.optimize as optimize_schema
from ..optimizers.optimizer import ScheduleOptimizer

router = APIRouter()

@router.post("/optimize/")
async def optimize(n_member_day:int, upload_file: UploadFile = File(...)):

    #現状、１回のリクエストで、ファイル情報と他の入力情報をFastAPIの機能で１度にvalidationすることはできない。
    #また、UploadFileとpydantic.BaseModelの両方を引数にするとエラーとなるため、現状このような実装としている。
    #詳細は、docs参照。
    optimize_body = optimize_schema.RequestedSchedule(n_member_day=n_member_day, upload_file=upload_file)

    # TODO :CPUがarmかつosがLinuxの場合、最適化ソルバが実行できないため現状このように実装する。詳細はdocs参照。
    if platform.system()=="Linux":
        return {"message": "This os is Linux. We cannot use solver."}
    else:
        #最適化実行
        opt:ScheduleOptimizer = ScheduleOptimizer.generate_optimizer(optimize_body=optimize_body)
        solution_df:pd.DataFrame = opt.optimize()

        # TODO :データの保存先をどうするかは要検討
        csv_path:Path = Path(__file__).parent.parent / "data/uploaded_file/optimized_shift.csv"
        solution_df.to_csv(csv_path)
        response = FileResponse(
                                path=csv_path,
                                filename="optimized_shift.csv"
                                )
        return response


# TODO :デコレータのresponse_modelをFileResponseで指定するとエラーとなる。以下の実装のようにresponse_classなら、うまく動き、戻り値の型が異なるとエラーとなるが使い方は合っているか？
# @router.post("/optimize/", response_class=FileResponse)
# async def optimize(n_member_day:int, upload_file: UploadFile = File(...)):
#     df_request_table = pd.read_csv(upload_file.file, index_col=0, header=0)

#     #最適化実行
#     if platform.system()=="Linux":
#         return {"message": "This os is Linux. We cannot use solver."}
#     opt = ScheduleOptimizer(df_request_table, n_member_day)
#     solution_df:pd.DataFrame = opt.optimize()

#     # TODO :データの保存先をどうするかは要検討
#     csv_path:Path = Path(__file__).parent.parent / "data/uploaded_file/optimized_shift.csv"
#     solution_df.to_csv(csv_path)
#     response = FileResponse(
#                             path=csv_path,
#                             filename="optimized_shift.csv"
#                             )
#     return response