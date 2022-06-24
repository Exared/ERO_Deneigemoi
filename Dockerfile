FROM gboeing/osmnx

WORKDIR /src
COPY montreal.py ./

ENTRYPOINT ["python", "montreal.py"]
