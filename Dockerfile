FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN python3 /code/app/parser.py

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]
