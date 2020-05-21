FROM python:buster

ARG DATE
ARG REVISION

COPY . .
WORKDIR /app
RUN pip install -r requirements.txt

RUN sed -i "s|SEDME|$REVISION -- $DATE|g" index.py
RUN python make_state.py

ENV FLASK_APP index.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
CMD ["flask", "run", "--host=0.0.0.0"]
