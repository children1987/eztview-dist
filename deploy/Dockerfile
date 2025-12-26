FROM python:3.11
LABEL maintainer="Shihow Inc <public@shihow.cn>"

WORKDIR /workspace/mcq/backend

COPY backend/Pipfile ./
COPY backend/Pipfile.lock ./

RUN python -m pip install --upgrade pip setuptools wheel Cython -i https://pypi.doubanio.com/simple/
RUN python -m pip install -i https://pypi.doubanio.com/simple/ uwsgi pipenv
RUN pipenv requirements > requirements.txt && \
    pip install -r requirements.txt
