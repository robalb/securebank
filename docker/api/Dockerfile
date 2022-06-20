# Production api Dockerfile
FROM python:3.9
WORKDIR /code
COPY docker/api/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api/app /code/app
# Use --proxy-headers if in production behind TLS termination proxy.
# This production Dockerfile is designed to be behind the nginx webservice proxy
# if you are using the docker-compose deployment, or behind an ingress if you
# are using the k8s deployment
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
