FROM python:3
# WORKDIR .
COPY . .
# COPY ./requirements.txt /python/requirements.txt

# COPY ./app.py /python/app.py
# COPY ./APP /python/APP
# COPY ./input /python/input
# COPY ./output /python/output
# COPY ./static /python/static
# COPY ./templates /python/templates
# COPY ./.env /python/.env
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:5000 -w 3 app:application