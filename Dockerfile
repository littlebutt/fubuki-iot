FROM python:latest as requirements-stage
WORKDIR /tmp
COPY ./ /tmp/
RUN pip install -r requirements.txt
RUN mkdir resources
