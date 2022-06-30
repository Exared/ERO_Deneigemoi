FROM python:3

RUN pip install osmnx

WORKDIR /ero/

COPY . .

ENTRYPOINT [ "python3", "montreal.py" ]