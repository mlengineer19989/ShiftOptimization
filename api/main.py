#追加ライブラリ
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


#自作モジュール
from api.routers import task, done, optimize

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
app.include_router(optimize.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    #本pyファイルの実行または、コマンド"uvicorn main:app --reload"でも実行可能。
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)