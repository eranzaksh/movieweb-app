FROM python:3.11-slim
WORKDIR ./web_app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5005
CMD [ "gunicorn", "--bind", "0.0.0.0:5005", "wsgi:app" ]