FROM python:3.9.10

WORKDIR /tmp/git/INF8808_Project

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD [ "python", "./app.py"]