import os
import random
import webapp2
import jinja2

from google.appengine.ext import ndb
from apis import CloudyFortunesApi
from models import Quote

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
            
        # keys = Quote.query().fetch(keys_only=True)
        # key = random.sample(keys, 1)[0]
    	
        # template_values = {
        #     'quote':  key.get(),
        # }

        cf = CloudyFortunesApi()

        template_values = {
            'quote':  cf.QuoteRandom(None),
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))