import endpoints

from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel


# Transitioning an existing model is as easy as replacing ndb.Model with
# EndpointsModel. Since EndpointsModel inherits from ndb.Model, you will have
# the same behavior and more functionality.
class Quote(EndpointsModel):
  # By default, the ProtoRPC message schema corresponding to this model will
  # have three string fields: attr1, attr2 and created
  # in an arbitrary order (the ordering of properties in a dictionary is not
  # guaranteed).
  content = ndb.StringProperty(indexed=False)  
  created = ndb.DateTimeProperty(auto_now_add=True)


# Use of this decorator is the same for APIs created with or without
# endpoints-proto-datastore.
@endpoints.api(name='cloudyfortunesapi', version='v1', description='Cloudy Fortunes API')
class CloudyFortunesApi(remote.Service):

  # Instead of the endpoints.method decorator, we can use MyModel.method to
  # define a new endpoints method. Instead of having to convert a
  # ProtoRPC request message into an entity of our model and back again, we
  # start out with a MyModel entity and simply have to return one.
  # Since no overrides for the schema are specified in this decorator, the
  # request and response ProtoRPC message definition will have the three string
  # fields attr1, attr2 and created.
  @Quote.method(path='quote', http_method='POST', name='quote.insert')
  def QuoteInsert(self, my_quote):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    my_quote.put()
    return my_quote
    
  @Quote.method(request_fields=('id',),
                  path='quote/{id}', http_method='GET', name='quote.get')
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

  # As MyModel.method replaces a ProtoRPC request message to an entity of our
  # model, MyModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in MyModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with MyModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @Quote.query_method(path='quotes', name='quote.list')
  def QuoteList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    return query
    
  @Quote.method(path='quotes/random', http_method='GET', name='quote.random')
  def QuoteRandom(self, query):
    keys = Quotes.query().fetch(keys_only=True)
    key = random.sample(keys, 1)[0]
    return key.get()

# Use of endpoints.api_server is the same for APIs created with or without
# endpoints-proto-datastore.
application = endpoints.api_server([CloudyFortunesApi], restricted=False)
