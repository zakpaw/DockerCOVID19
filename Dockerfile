FROM python=3.8.5:

RUN apt-get update -y && apt-get install -y python3-pip

COPY requirements.txt

RUN pip install -r requirements.txt