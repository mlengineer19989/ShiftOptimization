# poetryによるパッケージ管理
- docker imageのbuild時に、poetryをpip installする。
- 以下のコマンドを実行する。
```
docker compose run \
--entrypoint "poetry init \
    --name demo-app \
    --dependency [ライブラリ1] \
    --dependency [ライブラリ2] \
    ...
demo-app
```
例えば、以下のようにする。
```
docker compose run \
--entrypoint "poetry init \
    --name demo-app \
    --dependency fastapi \
    --dependency uvicorn[standard] \
    --dependency pulp \
    --dependency pandas \
    --dependency numpy \
    --dependency python-multipart" \
demo-app
```


```
docker compose run --entrypoint "poetry install --no-root" demo-app
```


```
docker compose up
```