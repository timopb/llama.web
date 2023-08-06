FROM python:3.10

WORKDIR /llama
RUN mkdir models
COPY ./requirements.txt /llama/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /llama/requirements.txt


COPY ./app /llama/app

WORKDIR /llama/app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8123"]
