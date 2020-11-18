FROM python:3.8

EXPOSE 5000

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip install cryptography

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY get_data.py /app

CMD python get_data.py