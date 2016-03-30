import sys
import os
import pynms_grpc.common.pynms_rpc_pb2
from pyangbind.lib.serialise import pybindJSONEncoder, pybindIETFJSONEncoder, pybindJSONDecoder
from pyangbind.lib.xpathhelper import YANGPathHelperException
from pyangbind.lib.yangtypes import safe_name
import json

class PyNMSGRPCMethods(object):

  @staticmethod
  def service_get_request(request, path_helper):
    response_msg = pynms_rpc_pb2.GetResponse(request_id=request.request_id)
    for operation in request.get_request:
      msg = response_msg.response.add()
      msg.operation_id = operation.operation_id
      msg.path = operation.path

      if pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_IETF':
        encoder = pybindIETFJSONEncoder()
      elif pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_PYBIND':
        encoder = pybindJSONEncoder()
      else:
        msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
        msg.message = "No encodings other than JSON currently supported."
        continue

      objects = path_helper.get(operation.path)
      if len(objects) > 1:
        ret_obj = [encoder.encode(i) for i in objects]
      elif len(objects) == 0:
        ret_obj = ""
      else:
        ret_obj = encoder.encode(objects[0])

      msg.value = unicode(ret_obj)

    return response_msg

  @staticmethod
  def service_set_request(request, path_helper):
    f = open("/tmp/called", 'w')
    f.write("called")
    f.flush()
    f.close()
    response_msg = pynms_rpc_pb2.SetResponse(request_id=request.request_id)
    for operation in request.config_operation:
      msg = response_msg.response.add()
      msg.operation_id = operation.operation_id

      if pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_IETF':
        decoder = pybindJSONDecoder.load_ietf_json
      elif pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_PYBIND':
        decoder = pybindJSONDecoder.load_json
      else:
        msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
        msg.message = "Unsupported encoding"
        continue

      # try and do the actual set
      # assume that the path can never be relative
      try:
        existing_obj = path_helper.get_unique(operation.path)
      except YANGPathHelperException as m:
        msg.response_code = pynms_rpc_pb2.INVALID_PATH
        msg.message = unicode(m)
        continue

      if pynms_rpc_pb2.SetDataCommand.Name(operation.operation) in ['UPDATE_CONFIG', 'REPLACE_CONFIG']:
        try:
          parsed_json = json.loads(operation.value)
        except ValueError as m:
          msg.response_code = pynms_rpc_pb2.INVALID_ENCODING
          msg.message = unicode(m)

        overwrite = True if pynms_rpc_pb2.SetDataCommand.Name(operation.operation) == 'REPLACE_CONFIG' else False

        try:
          decoder(parsed_json, None, None, obj=existing_obj, path_helper=path_helper, overwrite=overwrite)
        except ValueError as e:
          msg.reponse_code = pynms_rpc_pb2.INVALID_CONFIGURATION
          if len(e.args) and isinstance(e.args[0], dict):
            msg.message = unicode(e.args[0]['error-string'])
          else:
            msg.message = u"Invalid configuration"
          continue
        except AttributeError as msg:
          msg.response_code = pynms_rpc_pb2.INVALID_CONFIGURATION
          msg.message = u"Invalid JSON: " + unicode(msg)

      elif pynms_rpc_pb2.SetDataCommand.Name(operation.operation) in ['DELETE_CONFIG']:
        if hasattr("delete", existing_obj._parent):
          keyval = existing_obj._parent._extract_key(existing_obj)
          # error handling TODO
          existing_obj._parent.delete(keyval)
        else:
          # if the value is not alist entry
          unset_method = getattr(existing_obj._parent, "_unset_%s" % safe_name(operation.path.split("/")[-1]), None)
          if unset_method is None:
            msg.response_code = pynms_rpc_pb2.NOK
            msg.message = u"Could not delete " + unicode(operation.path)
            continue
          unset_method()

      msg.response_code = pynms_rpc_pb2.OK

    return response_msg

