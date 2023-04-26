FROM python:latest

WORKDIR /usr/src/app

COPY src /usr/src/app/src
COPY Makefile requirements.txt requirements-tests.txt setup.cfg /usr/src/app/

# tzdata for timzone
# RUN apt-get update -y
# RUN apt-get install -y tzdata
 
# timezone env with default
# ENV TZ=Europe/Madrid

RUN make venv


CMD ["make", "run"]