import endpoints

from google.appengine.ext import ndb
from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel

class Quote(EndpointsModel):  
  _message_fields_schema = ('id', 'content', 'created')
  content = ndb.StringProperty(indexed=False)  
  created = ndb.DateTimeProperty(auto_now_add=True)
