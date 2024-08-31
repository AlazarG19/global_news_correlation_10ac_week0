FROM python:latest

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt 

EXPOSE 5000 

ENV FILE  .env

ENV PYTHONPATH /src

CMD ["python3","app.py"]