FROM python:alpine3.7

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python make_dates.py
RUN python make_states.py

EXPOSE 5000

ENV FLASK_APP covid-api.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
CMD ["flask", "run", "--host=0.0.0.0"]
