FROM python:buster

COPY . .
WORKDIR /app

ARG DATE
ARG REVISION

RUN sed -i "s|SEDME|$REVISION $DATE|g" index.py
RUN pip install -r requirements.txt
RUN python make_state.py
RUN ls -la

ENV FLASK_APP index.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
CMD ["flask", "run", "--host=0.0.0.0"]
