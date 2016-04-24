import sys
import os
from pynms_grpc.common import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindJSONEncoder, pybindIETFJSONEncoder, pybindJSONDecoder
from pyangbind.lib.xpathhelper import YANGPathHelperException
from pyangbind.lib.yangtypes import safe_name
import json

class PyNMSServerGRPCMethods(object):

  @staticmethod
  def get_encoded_object_set(path_helper, path, encoding, select_filter=False, changed_filter=False):
    # TODO: filtering

    generate_element = False
    if encoding == 'JSON_IETF':
        encoder = pybindIETFJSONEncoder()
        generate_element = True
    elif encoding == 'JSON_PYBIND':
        encoder = pybindJSONEncoder()

    objects = path_helper.get(path)

    if changed_filter is True:
      tmp_obj = []
      for i in objects:
        if hasattr(i, "_changed"):
          if i._changed() is True:
            tmp_obj.append(i)
        else:
          tmp_obj.append(i)
        objects=  tmp_obj

    if generate_element is True:
      tmp_obj = [encoder.generate_element(i) if hasattr(i, "_pyangbind_elements") else i for i in objects]
      objects = tmp_obj

    if len(objects) > 1:
      ret_obj = [encoder.encode(i) for i in objects]
    elif len(objects) == 0:
      ret_obj = ""
    else:
      ret_obj = encoder.encode(objects[0])

    return ret_obj

  @staticmethod
  def service_get_request(request, path_helper):
    f = open("/tmp/foo3", 'w')
    f.write("hit this point\n")
    f.flush()
    f.close()
    response_msg = pynms_rpc_pb2.GetResponse(request_id=request.request_id)

    prefix = request.prefix if len(request.prefix) else None
    data_type = request.data_type
    encoding = pynms_rpc_pb2.EncodingType.Name(request.encoding)

    if not encoding in ["JSON_IETF", "JSON_PYBIND"]:
      response_msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
      response_msg.message = "PyNMS only supports JSON encodings currently."
      return response_msg

    for path in request.path:
      msg = response_msg.response.add()
      if prefix is not None:
        # TODO: what should be done if a prefix is specified, should the
        # absolute path be used, or the path that corresponds to the prefix?
        msg.path = request.path + "/" + path
      else:
        msg.path = path

      # TODO: get that has filtered output based on type (data_type is ignored)
      msg.value = unicode(PyNMSServerGRPCMethods.get_encoded_object_set(path_helper, path, encoding))

    return response_msg

  @staticmethod
  def service_set_request(request, path_helper):

    response_msg = pynms_rpc_pb2.SetResponse(request_id=request.request_id)
    prefix = request.prefix if len(request.prefix) else None

    if pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_IETF':
      decoder = pybindJSONDecoder.load_ietf_json
    elif pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_PYBIND':
      decoder = pybindJSONDecoder.load_json
    else:
      response_msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
      response_msg.message = "Unsupported encoding"
      return response_msg

    checkpoint = {}
    encoder = pybindJSONEncoder()
    for operation in request.operation:
      path = operation.path if prefix is None else prefix + "/" + operation.path
      # TODO: do we assume that the request.operation dataset is ordered
      # for us?
      chk_objects = path_helper.get(path)
      checkpoint[operation.path] = PyNMSServerGRPCMethods.get_encoded_object_set(path_helper, path, "JSON_PYBIND", encoder, changed_filter=True)

    error_paths = []
    completed_paths = []
    for operation in request.operation:
      try:
        existing_obj = path_helper.get_unique(operation.path)
      except YANGPathHelperException as m:
        error_paths.append({
                            'path': path,
                            'error': pynms_rpc_pb2.INVALID_PATH,
                            'message': 'Invalid Path'
                            })
        break

      if pynms_rpc_pb2.SetDataCommand.Name(operation.opcode) in ['UPDATE_CONFIG', 'REPLACE_CONFIG']:
        try:
          parsed_json = json.loads(operation.value)
        except ValueError as m:
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid JSON'
                              })
          break

        overwrite = True if pynms_rpc_pb2.SetDataCommand.Name(operation.opcode) == 'REPLACE_CONFIG' else False

        try:
          decoder(parsed_json, None, None, obj=existing_obj, path_helper=path_helper, overwrite=overwrite)
        except ValueError as e:
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid configuration'
                              })
          break
        except AttributeError as msg:
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid configuration'
                              })
          break

      elif pynms_rpc_pb2.SetDataCommand.Name(operation.operation) in ['DELETE_CONFIG']:
        if hasattr("delete", existing_obj._parent):
          keyval = existing_obj._parent._extract_key(existing_obj)
          # error handling TODO
          existing_obj._parent.delete(keyval)
        else:
          # if the value is not a list entry
          unset_method = getattr(existing_obj._parent, "_unset_%s" % safe_name(operation.path.split("/")[-1]), None)
          if unset_method is None:
            error_paths.append({
                                  'path': operation.path,
                                  'error': pynms_rpc_pb2.NOK,
                                  'message': "Could not delete %s" % path
                                })
            break
          unset_method()
      completed_paths.append(operation.path)

    if len(error_paths) == 0:
      response_msg.response_code = pynms_rpc_pb2.OK
      return response_msg

    # need to rollback
    #
    # We need to rollback by applying changes in reverse order to the transaction that
    # was specified.
    completed_paths.reverse()
    for path in completed_paths:
      original_content = checkpoint[path]
      existing_object = path_helper.get_unique(path)
      pybindJSONDecoder.load_json(original_content, None, None, obj=existing_object, path_helper=path_helper, overwrite=True)

    response_msg.response_code = error_paths[0]['error']
    response_msg.message = error_paths[0]['message']
    return response_msg


