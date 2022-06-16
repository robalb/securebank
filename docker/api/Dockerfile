FROM python:3.9
WORKDIR /code
COPY doker/api/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api/app /code/app
# use --proxy-headers in production behind TLS termination proxy
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
