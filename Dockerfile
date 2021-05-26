#build: docker build -t img-webserv-ecg:alpine .
#run development:
#docker run --rm --name webserv-ecg -p 5000:5000 --mount "type=bind,source=$(pwd)/src,target=/app" img-webserv-ecg:alpine


# first stage
FROM python:3.7-slim AS Builder

ENV DEBIAN_FRONTEND=noninteractive

#install build dependencies
#RUN apt-get update && apt-get -y install xauth firefox

#install python dependencies to virtual env
RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


FROM python:3.7-slim AS App

COPY --from=Builder /opt/venv /opt/venv
#COPY ./src .
RUN mkdir ./app


#entry
#RUN adduser --disabled-password appuser
#USER appuser
RUN useradd appuser
USER appuser
CMD . /opt/venv/bin/activate && exec python app/main.py
