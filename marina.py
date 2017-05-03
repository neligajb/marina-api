import boatHandlers
import slipHandlers


class MainPage(boatHandlers.webapp2.RequestHandler):
    def get(self):
        self.response.write("hey sailor")


# Enable PATCH
allowed_methods = boatHandlers.webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
boatHandlers.webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = boatHandlers.webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boats', boatHandlers.BoatsHandler),
    ('/boats/(.*)', boatHandlers.BoatsHandler),
    ('/slips', slipHandlers.SlipsHandler),
    ('/slips/(.*)/arrival/(.*)', slipHandlers.ArrivalsHandler),
    ('/slips/(.*)/departure/(.*)', slipHandlers.DeparturesHandler),
    ('/slips/(.*)/boat', slipHandlers.SlipBoatHandler),
    ('/slips/(.*)', slipHandlers.SlipsHandler)
], debug=True)
