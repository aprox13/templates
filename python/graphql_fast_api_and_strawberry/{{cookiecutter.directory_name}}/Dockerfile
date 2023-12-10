FROM python:{{cookiecutter.pythonMajor}}.{{cookiecutter.pythonMinor}}

WORKDIR /app/backend

COPY . ./

RUN apt update

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/backend/requirements.txt

CMD python3.9 -m uvicorn main:app --host 0.0.0.0 --workers $WORKERS_COUNT --port $_DEPLOY_PORT
