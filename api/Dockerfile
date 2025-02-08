FROM python:3.10.15

RUN apt-get update && apt-get install --yes --no-install-recommends make

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["make", "start-prod"]
