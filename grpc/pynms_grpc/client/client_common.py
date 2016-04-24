from pynms_grpc.common import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindJSONEncoder, pybindIETFJSONEncoder
import json

class PyNMSGRPCClientException(Exception):
  pass

class PyNMSConfigOperation(object):
  def __init__(self, obj, method='UPDATE_CONFIG'):
    self.path = obj._yang_path()
    self.content = obj
    self.method = method

  def __str__(self):
    return "%s -> %s" % (self.path, self.content.get(filter=True))

class PyNMSClientGRPCMethods(object):
  @staticmethod
  def generate_set_message(operations, request_id=0):
    try:
      msg_reqid = int(request_id)
    except ValueError:
      raise PyNMSGRPCClientException("request_id must be an integer")

    setreq = pynms_rpc_pb2.SetRequest(request_id=msg_reqid, encoding=pynms_rpc_pb2.JSON_IETF)

    req = 0
    for operation in operations:
      if not isinstance(operation, PyNMSConfigOperation):
        raise PyNMSGRPCClientException("operations must be PyNMSConfigOperation instances")
      setop = setreq.operation.add()
      if operation == 'UPDATE_CONFIG':
        setop.opcode = pynms_rpc_pb2.UPDATE_CONFIG
      else:
        # only support sending UPDATE_CONFIG right now
        setop.opcode = pynms_rpc_pb2.UPDATE_CONFIG
      setop.path = operation.path

      # always use IETF JSON for now
      if hasattr(operation.content, "_pyangbind_elements"):
        tree = pybindIETFJSONEncoder.generate_element(operation.content, flt=True)
      else:
        tree = operation.content

      encoder = pybindIETFJSONEncoder
      setop.value = json.dumps(tree, cls=encoder)

    return setreq

  @staticmethod
  def generate_get_message(paths, request_id, data_type='ALL', prefix=None):
    try:
      msg_reqid = int(request_id)
    except ValueError:
      raise PyNMSGRPCClientException("request_id must be an integer")

    getreq = pynms_rpc_pb2.GetRequest(request_id=msg_reqid,
                                    encoding=pynms_rpc_pb2.JSON_IETF)

    if prefix is not None:
      getreq.prefix = prefix

    # only support GET_ALL currently
    if data_type == 'ALL':
      getreq.data_type = pynms_rpc_pb2.GET_ALL
    else:
      getreq.data_type = pynms_rpc_pb2.GET_ALL

    getreq.path.extend(paths)

    return getreq
