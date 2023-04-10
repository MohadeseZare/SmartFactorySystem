FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code

EXPOSE 7000

CMD ["python", "manage.py", "runserver", "127.0.0.1:7000"]