import sys
import os
from pynms_grpc.common import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindJSONEncoder, pybindIETFJSONEncoder, pybindJSONDecoder
from pyangbind.lib.xpathhelper import YANGPathHelperException
from pyangbind.lib.yangtypes import safe_name
import json

class PyNMSServerGRPCMethods(object):

  @staticmethod
  def get_encoded_object_set(path_helper, path, encoding, logger, select_filter=False):
    # TODO: filtering

    generate_element = False
    if encoding == 'JSON_IETF':
      encoder = pybindIETFJSONEncoder
      generate_element = True
    elif encoding == 'JSON_PYBIND':
      encoder = pybindJSONEncoder

    logger.debug("Getting objects at %s..." % path)
    objects = path_helper.get(path)
    logger.debug("Objects returned were: %s" % objects)

    logger.debug("Generate element was %s" % generate_element)

    if generate_element is True:
      try:
        tmp_obj = [pybindIETFJSONEncoder.generate_element(i, flt=True) for i in objects]
      except Exception as e:
        logger.debug("Received an exception whilst generating elements: %s: %s" % (type(e), str(e)))
        raise Exception(str(e))
      objects = tmp_obj
    else:
      tmp_obj = [i.get(filter=True) for i in objects]
      objects = tmp_obj

    logger.debug("Objects are %s" % objects)
    logger.debug("Objects length is %d" % len(objects))

    if len(objects) > 1:
      try:
        ret_obj = [json.dumps(i, cls=encoder) for i in objects]
      except Exception as e:
        logger.debug("Received an exception whilst encoding(multi-obj): %s" % str(e))
        raise Exception(str(e))
    elif len(objects) == 0:
      ret_obj = ""
    else:
      try:
        ret_obj = json.dumps(objects[0], cls=encoder)
      except Exception as e:
        logger.debug("Received an exception whilst encoding (one object): %s" % str(e))
        raise Exception(str(e))

    logger.debug("returned object is %s" % ret_obj)

    return ret_obj

  @staticmethod
  def service_get_request(request, path_helper, logger):
    response_msg = pynms_rpc_pb2.GetResponse(request_id=request.request_id)

    prefix = request.prefix if len(request.prefix) else None
    data_type = request.data_type
    encoding = pynms_rpc_pb2.EncodingType.Name(request.encoding)

    logger.debug("Prefix: %s, DataType: %s, Encoding: %s" % (prefix, data_type, encoding))

    if not encoding in ["JSON_IETF", "JSON_PYBIND"]:
      response_msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
      response_msg.message = "PyNMS only supports JSON encodings currently."
      return response_msg

    logger.debug("Handling %s" % request.path)

    for path in request.path:
      logger.debug("Looking at path: %s" % path)
      msg = response_msg.response.add()
      if prefix is not None:
        # TODO: what should be done if a prefix is specified, should the
        # absolute path be used, or the path that corresponds to the prefix?
        msg.path = request.path + "/" + path
      else:
        msg.path = path

      logger.debug("Getting object at %s" % msg.path)
      obj = PyNMSServerGRPCMethods.get_encoded_object_set(path_helper, path, encoding, logger)
      logger.debug("Got object %s" % str(obj))
      # TODO: get that has filtered output based on type (data_type is ignored)
      msg.value = unicode(obj)

    return response_msg

  @staticmethod
  def service_set_request(request, path_helper, logger):

    response_msg = pynms_rpc_pb2.SetResponse(request_id=request.request_id)
    prefix = request.prefix if len(request.prefix) else None

    logger.debug("Starting set routine with input message as %s" % request)

    if pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_IETF':
      decoder = pybindJSONDecoder.load_ietf_json
    elif pynms_rpc_pb2.EncodingType.Name(request.encoding) == 'JSON_PYBIND':
      decoder = pybindJSONDecoder.load_json
    else:
      response_msg.response_code = pynms_rpc_pb2.UNSUPPORTED_ENCODING
      response_msg.message = "Unsupported encoding"
      return response_msg

    logger.debug("Determind the encoding to be %s from message" % request.encoding)

    logger.debug("Starting checkpointing...")
    checkpoint = {}
    encoder = pybindJSONEncoder()
    for operation in request.operation:
      logger.debug("Looking for %s" % str(operation))
      path = operation.path if prefix is None else prefix + "/" + operation.path
      logger.debug("Trying to checkpoint %s" % path)
      # TODO: do we assume that the request.operation dataset is ordered
      # for us?
      chk_objects = path_helper.get(path)
      checkpoint[operation.path] = PyNMSServerGRPCMethods.get_encoded_object_set(path_helper, path, "JSON_PYBIND", logger)
      logger.debug("Checkpointed %s successfully" % operation.path)

    error_paths = []
    completed_paths = []
    for operation in request.operation:
      try:
        existing_obj = path_helper.get_unique(operation.path)
      except YANGPathHelperException as m:
        logger.debug("Hit a YANGPathException when getting %s" % operation.path)

        error_paths.append({
                            'path': path,
                            'error': pynms_rpc_pb2.INVALID_PATH,
                            'message': 'Invalid Path'
                            })
        break

      if pynms_rpc_pb2.SetDataCommand.Name(operation.opcode) in ['UPDATE_CONFIG', 'REPLACE_CONFIG']:
        logger.debug("Running parsing for %s with method %s" % (operation.path, pynms_rpc_pb2.SetDataCommand.Name(operation.opcode)))

        try:
          parsed_json = json.loads(operation.value)
        except ValueError as m:
          logger.debug("Hit an exception when loading the JSON for %s -> %s" % (operation.path, str(m)))
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid JSON'
                              })
          break
        except Exception as e:
          logger.debug("Hit unknown exception %s @ %s:152" % (str(e), __file__))
          break

        overwrite = True if pynms_rpc_pb2.SetDataCommand.Name(operation.opcode) == 'REPLACE_CONFIG' else False

        try:
          decoder(parsed_json, None, None, obj=existing_obj, path_helper=path_helper, overwrite=overwrite)
        except ValueError as e:
          logger.debug("Hit a ValueError when loading the JSON for %s (specified to %s)" % (operation.path, existing_obj._path()))
          logger.debug("ValueError: %s" % str(msg))
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid configuration'
                              })
          break
        except AttributeError as msg:
          logger.debug("Hit a AttributeError when loading the JSON for %s (specified to %s)" % (operation.path, existing_obj._path()))
          logger.debug("AttributeError: %s" % str(msg))
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Invalid configuration'
                              })
          break
        except KeyError as msg:
          logger.debug("Hit a KeyError when loading the JSON for %s" % (operation.path))
          error_paths.append({
                                'path': operation.path,
                                'error': pynms_rpc_pb2.INVALID_CONFIGURATION,
                                'message': 'Attempted to update an existing leaf entry',
            })
        except Exception as e:
          logger.debug("Hit unknown exception %s @ %s:152" % (str(e), __file__))
          break

      elif pynms_rpc_pb2.SetDataCommand.Name(operation.opcode) in ['DELETE_CONFIG']:
        if "[" in existing_obj._path()[-1]:
          path = existing_obj._path()[:-1]
          containing_obj = path_helper.get_unique(path)
          parent = getattr(containing_obj,existing_obj._path()[-1].split("[")[0])
        else:
          parent = existing_obj._parent

        if hasattr(parent, "delete"):
          keyval = parent._extract_key(existing_obj)
          # todo, error handling
          if hasattr(keyval, "_get_ptr"):
            keyval = keyval._get_ptr()
          parent.delete(keyval)
        else:
          # if the value is not a list entry
          unset_method = getattr(parent, "_unset_%s" % safe_name(operation.path.split("/")[-1]), None)
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



