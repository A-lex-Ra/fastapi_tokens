FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install poetry
RUN POETRY_VIRTUALENVS_CREATE=false poetry install

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80
