# PyNMS gRPC Client + Server

The Dockerfiles within this directory create packaged instances of:
  * PyNMS gRPC Client - an example gRPC client implementing the OpenConfig RPC specification.
  * PyNMS gRPC Server - an example gRPC server which uses PyangBind as the backend in-memory storage for data models.

## Running the example...

Run `docker-compose up` in the `docker` directory of this project. This launches two containers:

 * `pynms-grpc-client` - a container which has the gRPC client installed within it.
 * `pynms-grpc-server` - a container running the gRPC server under `supervisord`.

To interact with the client - run `docker exec -ti pynms-grpc-client /bin/bash` - where the example client code can be interacted with. Example scripts are included in the `/opt/virtualenv/bin/` directory and are prefixed with `pynms_gprc.`.

There is no need to rebuild the Docker images from the `Dockerfiles` in this directory to run the pre-existing examples - however, they may be useful in cases where you would like to add more YANG modules to the example code. See the `build_yang.sh` script 

## Common YANG bindings are 
