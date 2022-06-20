# Production api Dockerfile
FROM python:3.9
WORKDIR /code
COPY docker/api/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api/app /code/app
# Use --proxy-headers if in production behind TLS termination proxy
# Note that nginx is already configured to handle this.
# Adding both nginx Real-Ip directives and uvicorm --proxy-headers
# may lead to security issues
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

#TODO: copy app here
