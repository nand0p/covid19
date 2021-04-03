FROM python:3.8-slim-buster

MAINTAINER "nando" <nando@hex7.com>

ARG DATE
ARG REVISION

COPY . .
RUN pip install -r requirements.txt --no-cache-dir
RUN pip list

WORKDIR /app
RUN mkdir -pv reports
RUN cat make_state.py
RUN python make_state.py

RUN sed -i "s|SEDME|$REVISION -- $DATE|g" index.py
RUN cat index.py
ENV FLASK_APP index.py
ENV FLASK_ENV production
ENV FLASK_DEBUG 1
CMD ["flask", "run", "--host=0.0.0.0"]
