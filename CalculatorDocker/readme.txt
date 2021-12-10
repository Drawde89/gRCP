Same calculator app except it utilizes docker. The Server is put into the docker container and clients can be launched to interact with it.

When launching the server on Docker use: $ docker run -p 127.0.0.1:50051:50051/tcp <IMAGE>
