#syntax = docker/dockerfile:1

FROM python
WORKDIR /CalculatorGrcp

COPY calc_pb2.py .
COPY calc_pb2_grpc.py .
COPY calc_server.py .
COPY requirements.txt . 

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 50051
ENTRYPOINT [ "python3", "calc_server.py" ]




