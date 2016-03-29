---
layout: doc
title: About Py<b>NMS</b>
subtitle: Network management components in Python.
permalink: /about/
---

## What is Py**NMS**?

Py**NMS** is a collection of libraries and tooling - written in Python - that is intended to allow those working on network automation - be they network administrators, network architects or engineers, software developers or "NetDevOps" - to adopt emerging technologies as part of their NMS components.

Primarily, this effort is focused around driving the adoption of model-driven management interfaces, and managing and receiving streaming telemetry data from network elements. Put more simply... you should be able to use PyNMS components to push configuration data to your device,and parse operational state data that comes back - via either query/response or streaming interfaces.

Py**NMS** is intended for use primarily with [OpenConfig](https://www.openconfig.net) models, and the RPCs and implementation associated with them. This is where the majority of implementation and testing amongst the initial contributors is likely to be. The toolset follows the same ethos as OpenConfig - to provide the functionality considered most operationally relevant to real-world network deployments. It is not intended to provide unlimited flexibility for testing environments, nor to be feature complete.

<hr>
## Components of Py**NMS**

 * [PyangBind](/pyangbind) - is a plugin for [Pyang](https://github.com/mbj4668/pyang) that generates Python bindings for a YANG model.  
  &nbsp;
  
Additional components that are under development:

 * gRPC client and server conforming to the OpenConfig RPC specification. The client within this bundle is intended to be able to interact with 3rd party network components.