
FROM python:3.9.5-slim-buster
COPY . /deploy-app
WORKDIR /deploy-app
# RUN pip3 install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
# EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "app.py"]