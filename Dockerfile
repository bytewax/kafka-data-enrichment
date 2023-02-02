FROM bytewax/bytewax:latest-python3.10

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

RUN python utils/utils.py

ENTRYPOINT ["python", "dataflow.py"]
