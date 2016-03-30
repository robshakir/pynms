
class PyNMSGRPCClientException(Exception):
  pass

class PyNMSConfigOperation(object):
  def __init__(self, path, obj, operation):
    self.path = path
    self.content = obj
    self.operation = operation

  def __str__(self):
    return "%s -> %s" % (self.path, self.content.get(filter=True))