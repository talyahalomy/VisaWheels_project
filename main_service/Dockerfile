#build docker file for main.py 

FROM python:3.10-alpine

WORKDIR /app

RUN pip install fastapi uvicorn requests pymongo

COPY main.py /app

EXPOSE 9000

CMD ["python", "main.py"]






