FROM continuumio/anaconda3

RUN mkdir /src
WORKDIR /src
COPY montreal.py ./

RUN pip install osmnx

ENTRYPOINT ["python3", "montreal.py"]
