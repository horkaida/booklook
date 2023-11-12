FROM python:3.10.10-alpine
COPY . .
WORKDIR .

EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt