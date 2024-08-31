FROM python:latest

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt 

EXPOSE 7000 

ENV FILE  /app/.env

ENV PYTHONPATH /src

CMD ["python3","app/app.py"]