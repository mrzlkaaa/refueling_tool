FROM python:3.10
WORKDIR /python
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8890"]