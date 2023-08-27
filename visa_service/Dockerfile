#build docker file for main.py 

FROM python:3.10-alpine

WORKDIR /app

RUN pip install fastapi uvicorn

COPY visa.py /app

EXPOSE 8000

CMD ["python", "visa.py"]

