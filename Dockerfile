FROM python:3.12-alpine

COPY . /code
WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 4040

CMD ["python3", "webhooks.py"] 


