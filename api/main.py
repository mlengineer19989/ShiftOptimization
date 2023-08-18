#追加ライブラリ
from fastapi import FastAPI
import uvicorn


#自作モジュール
from .routers import task, done, optimize

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
app.include_router(optimize.router)



if __name__ == "__main__":
    #本pyファイルの実行または、コマンド"uvicorn main:app --reload"でも実行可能。
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)