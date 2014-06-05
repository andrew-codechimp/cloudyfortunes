import endpoints
import random
import settings

from models import Quote
from google.appengine.ext import ndb
from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel

@endpoints.api(name='cloudyfortunes', version='v1', description='Cloudy Fortunes')
class CloudyFortunesApi(remote.Service):

  @Quote.method(user_required=True, path='quotes', http_method='POST', name='quote.insert')
  def QuoteInsert(self, my_quote):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    if not endpoints.get_current_user().email() == settings.ADMIN_USER_EMAIL:
      raise endpoints.UnauthorizedException('Invalid user id.')      
    my_quote.put()
    return my_quote

  @Quote.method(user_required=True, path='quotes/{id}', http_method='PUT', name='quote.update')
  def QuoteUpdate(self, my_quote):
    if not endpoints.get_current_user().email() == settings.ADMIN_USER_EMAIL:
      raise endpoints.UnauthorizedException('Invalid user id.')      
    my_quote.put()
    return my_quote

  @Quote.method(user_required=True, request_fields=('id',), path='quotes/{id}', http_method='DELETE', name='quote.delete')
  def QuoteDelete(self, my_quote):
    if not endpoints.get_current_user().email() == settings.ADMIN_USER_EMAIL:    
      raise endpoints.UnauthorizedException('Invalid user id.')      
    if not my_quote.from_datastore:
      raise endpoints.NotFoundException('Quote not found.')
    my_quote._key.delete()
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

  @Quote.query_method(query_fields=('limit', 'order', 'pageToken'), path='quotes', http_method='GET', name='quote.list')
  def QuoteList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    return query
    
  @Quote.method(path='quotes/random', http_method='GET', name='quote.random')
  def QuoteRandom(self, query):
    keys = Quote.query().fetch(keys_only=True)
    key = random.sample(keys, 1)[0]
    return key.get()
