#python3.11のイメージをダウンロード
FROM python:3.11-buster

#pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

# m1対応
#RUN apt-get install -y wget bash git gcc g++ gfortran  liblapack-dev libamd2 libcholmod3 libmetis-dev libsuitesparse-dev libnauty2-dev
RUN wget -nH https://raw.githubusercontent.com/coin-or/coinbrew/master/coinbrew
RUN chmod u+x coinbrew
RUN bash coinbrew fetch Cbc@master
RUN bash coinbrew build Cbc@master --no-prompt --prefix=/usr/local --tests=none --enable-cbc-parallel
# ENV PMIP_CBC_LIBRARY="/usr/local/lib/libCbc.so"
# ENV LD_LIBRARY_PATH="/home/haroldo/prog/lib"

#poetryの定義ファイルをコピー（存在する場合）
COPY pyproject.toml* poetry.lock* ./

#poetryのライブラリをインストール（pyproject.tomlが既にある場合）
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]