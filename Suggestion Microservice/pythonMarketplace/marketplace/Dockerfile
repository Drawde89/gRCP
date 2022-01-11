FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs
COPY marketplace/ /service/marketplace
WORKDIR /service/marketplace
RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 5000
#sets the environment variable FLASK_APP in the image
ENV FLASK_APP=marketplace.py 
#Entry point runs each command in "" but we can read it as: flask run --host=0.0.0.0
#--host=0.0.0.0 allows flask to have connections outside the localhost
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]