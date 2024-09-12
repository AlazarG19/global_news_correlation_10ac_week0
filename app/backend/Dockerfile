FROM python:latest

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt 

EXPOSE 7000 

ENV FILE  .env

ENV PYTHONPATH /app

CMD ["python3","app.py"]