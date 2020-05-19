FROM python:alpine3.7

COPY . .
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python make_state.py
RUN python freshen_reports.py

ENV FLASK_APP index.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
CMD ["flask", "run", "--host=0.0.0.0"]
