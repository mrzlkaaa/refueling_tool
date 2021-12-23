
FROM python:3.9.5-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
# EXPOSE 8080
# ENTRYPOINT [ "python" ]
CMD gunicorn --bind 0.0.0.0:5000 -w 3 app:application