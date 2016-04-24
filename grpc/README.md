# PyNMS GRPC
-- 

This directory contains an example implementation of a gRPC client and server which utilises [PyangBind](http://pynms.io/pyangbind) to ingest YANG modules.

The client has support for generating a transaction based on a set of changes that are to be made. Transactions can be directly generated from a PyangBind class hierarchy. 

The server utilises the PyangBind `YANGPathHelper` and in-memory storage of the modules. It has support for transactions.

The API between the client and server is generated based on Google's protobufs, the specification used for the API is a partial implementation of the OpenConfig RPC API, described in protobuf.

