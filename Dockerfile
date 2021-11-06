
FROM python:3.9.5-slim-buster
COPY . /deploy-app
WORKDIR /deploy-app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]