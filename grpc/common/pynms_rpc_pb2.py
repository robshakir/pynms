# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pynms_rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pynms_rpc.proto',
  package='pynms_api',
  syntax='proto3',
  serialized_pb=_b('\n\x0fpynms_rpc.proto\x12\tpynms_api\x1a\x19google/protobuf/any.proto\"\x1a\n\nGetRequest\x12\x0c\n\x04path\x18\x03 \x01(\t\"\x1c\n\x0bGetResponse\x12\r\n\x05value\x18\x03 \x01(\t2?\n\x07OCPyNMS\x12\x34\n\x03Get\x12\x15.pynms_api.GetRequest\x1a\x16.pynms_api.GetResponseb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='pynms_api.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='pynms_api.GetRequest.path', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=83,
)


_GETRESPONSE = _descriptor.Descriptor(
  name='GetResponse',
  full_name='pynms_api.GetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='pynms_api.GetResponse.value', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=85,
  serialized_end=113,
)

DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetResponse'] = _GETRESPONSE

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETREQUEST,
  __module__ = 'pynms_rpc_pb2'
  # @@protoc_insertion_point(class_scope:pynms_api.GetRequest)
  ))
_sym_db.RegisterMessage(GetRequest)

GetResponse = _reflection.GeneratedProtocolMessageType('GetResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETRESPONSE,
  __module__ = 'pynms_rpc_pb2'
  # @@protoc_insertion_point(class_scope:pynms_api.GetResponse)
  ))
_sym_db.RegisterMessage(GetResponse)


import abc
from grpc.beta import implementations as beta_implementations
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

class BetaOCPyNMSServicer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Get(self, request, context):
    raise NotImplementedError()

class BetaOCPyNMSStub(object):
  """The interface to which stubs will conform."""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Get(self, request, timeout):
    raise NotImplementedError()
  Get.future = None

def beta_create_OCPyNMS_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import pynms_rpc_pb2
  import pynms_rpc_pb2
  request_deserializers = {
    ('pynms_api.OCPyNMS', 'Get'): pynms_rpc_pb2.GetRequest.FromString,
  }
  response_serializers = {
    ('pynms_api.OCPyNMS', 'Get'): pynms_rpc_pb2.GetResponse.SerializeToString,
  }
  method_implementations = {
    ('pynms_api.OCPyNMS', 'Get'): face_utilities.unary_unary_inline(servicer.Get),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

def beta_create_OCPyNMS_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  import pynms_rpc_pb2
  import pynms_rpc_pb2
  request_serializers = {
    ('pynms_api.OCPyNMS', 'Get'): pynms_rpc_pb2.GetRequest.SerializeToString,
  }
  response_deserializers = {
    ('pynms_api.OCPyNMS', 'Get'): pynms_rpc_pb2.GetResponse.FromString,
  }
  cardinalities = {
    'Get': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'pynms_api.OCPyNMS', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)
