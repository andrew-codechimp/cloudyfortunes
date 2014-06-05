from apis import CloudyFortunesApi
import webapp2
import jinja2


class MainPage(webapp2.RequestHandler):
    def get(self):
        
        quote = CloudyFortunesApi.QuoteRandom()
        
        template_values = {
            'quote_content': quote.Content,
        }

        template = JINJA_ENVIRONMENT.get_template('static/index.html')
        self.response.write(template.render(template_values))