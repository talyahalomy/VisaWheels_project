#build docker file for main.py 

FROM python:3.10-alpine

WORKDIR /app

RUN pip install fastapi uvicorn pymongo

COPY visa.py /app

EXPOSE 9010

CMD ["python", "visa.py"]

