FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY sigaa_api /app/sigaa_api

EXPOSE $PORT

CMD uvicorn sigaa_api.main:app --host "0.0.0.0" --port "$PORT"