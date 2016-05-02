# PyNMS gRPC Client + Server

The Dockerfiles within this directory create packaged instances of:
  * PyNMS gRPC Client - an example gRPC client implementing the OpenConfig RPC specification.
  * PyNMS gRPC Server - an example gRPC server which uses PyangBind as the backend in-memory storage for data models.

## Running the example...

Run `docker-compose up` in the `docker` directory of this project. This launches two containers:

 * `pynms/grpc_client` - a container which has the gRPC client installed within it.
 * `pynms/grpc_server` - a container running the gRPC server under `supervisord`.

To interact with the client - run `docker exec -ti pynms-grpc-client /bin/bash` - where the example client code can be interacted with. Example scripts are included in the `/opt/pynms_client` directory. These send gRPC requests to the grpc server data instance.

There is no need to rebuild the Docker images from the `Dockerfiles` in this directory to run the pre-existing examples - however, they may be useful if more bindings are required to be installed. Currently the examples utilise the `egbindings` that are provided under the main PyNMS repository (see [this directory](https://github.com/robshakir/pynms/tree/master/egbindings)).

