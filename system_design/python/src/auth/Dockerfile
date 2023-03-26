FROM python:3.10-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirments.txt /app/
#Point to note here is that we are copying the req seperately so if the application code changes we can still use the cache for the reqs.txt
RUN pip install --no-cache-dir --requirement /app/requirments.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]
