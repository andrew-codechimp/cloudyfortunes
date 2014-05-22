import endpoints
import random

from google.appengine.ext import ndb
from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel

class Quote(EndpointsModel):  
  _message_fields_schema = ('id', 'content', 'created')
  content = ndb.StringProperty(indexed=False)  
  created = ndb.DateTimeProperty(auto_now_add=True)

@endpoints.api(name='cloudyfortunesapi', version='v1', description='Cloudy Fortunes API')
class CloudyFortunesApi(remote.Service):

  @Quote.method(user_required=True, path='quotes', http_method='POST', name='quote.insert')
  def QuoteInsert(self, my_quote):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    if endpoints.get_current_user().email() == 'cubsta@gmail.com':
      my_quote.put()
    else:
      raise endpoints.UnauthorizedException('Invalid user id.')
    return my_quote
    
  @Quote.method(request_fields=('id',),
                  path='quotes/{id}', http_method='GET', name='quote.get')
  def QuoteGet(self, my_quote):
    # Since the field "id" is included, when it is set from the ProtoRPC
    # message, the decorator attempts to retrieve the entity by its ID. If the
    # entity was retrieved, the boolean from_datastore on the entity will be
    # True, otherwise it will be False. In this case, if the entity we attempted
    # to retrieve was not found, we return an HTTP 404 Not Found.

    # For more details on the behavior of setting "id", see the sample
    # custom_alias_properties/main.py.
    if not my_quote.from_datastore:
      raise endpoints.NotFoundException('Quote not found.')
    return my_quote

  # As Quote.method replaces a ProtoRPC request message to an entity of our
  # model, Quote.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in Quote.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with Quote.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @Quote.query_method(path='quotes', name='quote.list')
  def QuoteList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    return query
    
  @Quote.method(path='quotes/random', name='quote.random')
  def QuoteRandom(self, query):
    keys = Quote.query().fetch(keys_only=True)
    key = random.sample(keys, 1)[0]
    return key.get()

# Use of endpoints.api_server is the same for APIs created with or without
# endpoints-proto-datastore.
application = endpoints.api_server([CloudyFortunesApi], restricted=False)

