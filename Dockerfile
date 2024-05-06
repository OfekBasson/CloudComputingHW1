FROM python:alpine3.17

WORKDIR /app.

COPY . .

RUN  pip install flask

RUN pip install flask_restful

EXPOSE 8000

CMD ["python3", "main.py"]