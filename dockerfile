FROM python:latest

WORKDIR /tmp/git/INF8808_Project

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

CMD [ "python", "./app.py"]