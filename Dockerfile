FROM python:3.9.13-alpine

WORKDIR /app.

COPY . .

RUN  pip install flask
RUN  pip install flask_restful
RUN  pip install google-generativeai
RUN  pip install dependency-injector
RUN  pip install requests
RUN  pip install uuid
RUN  pip install datetime

EXPOSE 8000

ENV API_KEY="AIzaSyDZ-DCljJFFfiKF7gKJIZIvOQg4NijXY4k"

CMD ["python3", "main.py"]