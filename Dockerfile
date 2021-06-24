FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /werecord
COPY requirements.txt /werecord/
RUN pip install -r requirements.txt
COPY . /werecord/