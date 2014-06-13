import webapp2
import endpoints
from apis import CloudyFortunesApi
from views import MainPage

# Use of endpoints.api_server is the same for APIs created with or without
# endpoints-proto-datastore.
api = endpoints.api_server([CloudyFortunesApi], restricted=False)
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
