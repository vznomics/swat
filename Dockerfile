FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y samba samba-common && \
    apt-get clean

WORKDIR /app
COPY ./app /app/app

RUN pip install fastapi uvicorn jinja2 python-multipart passlib[bcrypt]

EXPOSE 8000 445 139
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
