FROM python:3.9

WORKDIR /app
ENV DEBIAN_FRONTEND="noninteractive"

RUN pip3 install pipenv

COPY . .

RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "/app/main.py"]
