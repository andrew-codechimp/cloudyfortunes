from google.appengine.ext import endpoints
from apis import CloudyFortunesApi

# Use of endpoints.api_server is the same for APIs created with or without
# endpoints-proto-datastore.
api = endpoints.api_server([CloudyFortunesApi], restricted=False)
