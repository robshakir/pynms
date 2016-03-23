import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "common"))
import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindJSONEncoder
import json

class grpc_PyNMS_methods(object):
  @staticmethod
  def service_get_request(request, path_helper):
    response_msg = pynms_rpc_pb2.GetResponse(request_id=request.request_id)
    for operation in request.get_request:
      msg = response_msg.response.add()
      msg.operation_id = operation.operation_id
      msg.path = operation.path

      if pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_IETF':
        mode = "ietf"
      elif pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_PYBIND':
        mode = "default"
      else:
        msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
        msg.message = "No encodings other than JSON currently supported."
        break

      objects = path_helper.get(msg.path)
      if len(objects) > 1:
        ret_obj = [pybindJSONEncoder().encode(i) for i in objects]
      elif len(objects) == 0:
        ret_obj = ""
      else:
        ret_obj = pybindJSONEncoder().encode(objects[0])

      msg.value = unicode(ret_obj)

    return response_msg
