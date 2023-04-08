FROM python:latest

WORKDIR /tmp/git/INF8808_Project

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py"]