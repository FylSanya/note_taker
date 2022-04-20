FROM python:3.10

ENV POETRY_VERSION 1.1.13
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false && poetry install
COPY . /app/

RUN chmod 755 /app/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
