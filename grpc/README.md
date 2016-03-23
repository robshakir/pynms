
* Currently gRPC doesn't run on OS X, see https://github.com/grpc/grpc/issues/995.
* Preferred development environment in Debian Jessie, with the following backports repo added:
    ```
deb http://http.debian.net/debian jessie-backports main
    ```

* Install gRPC and create a virtualenv. The virtualenv is required because there are likely to be conflicts in dependencies between pip and other pkg managers:
```
# apt-get install libgrpc-dev
# pip install virtualenv
# virtualenv dev
# source dev/bin/activate
# pip install grpcio pyangbind
```



