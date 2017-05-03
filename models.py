from google.appengine.ext import ndb


class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(default=None)
    length = ndb.IntegerProperty(default=None)
    at_sea = ndb.BooleanProperty(default=True)
    current_slip = ndb.KeyProperty(default=None)


class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.KeyProperty(default=None)
    arrival_date = ndb.StringProperty(default=None)
    departure_history = ndb.JsonProperty(default=None, repeated=True)
