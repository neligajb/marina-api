import json
import webapp2

import models


class BoatsHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body)
        if 'name' not in boat_data:
            self.response.set_status(400)
            self.response.write("400 Bad request")
            return
        new_boat = models.Boat(name=boat_data['name'])
        new_boat.type = boat_data["type"]
        new_boat.length = boat_data["length"]
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['id'] = new_boat.key.urlsafe()
        boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
        self.response.write(json.dumps(boat_dict))

    def put(self, id=None):
        if id:
            boat_data = json.loads(self.request.body)
            if 'name' not in boat_data:
                self.response.set_status(400)
                self.response.write("400 Bad request")
                return

            try:
                boat = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return

            boat.name = boat_data['name']
            if 'type' in boat_data:
                boat.type = boat_data['type']
            else:
                boat.type = None
            if 'length' in boat_data:
                boat.length = boat_data['length']
            else:
                boat.length = None

            # boat.at_sea defaults to the previous boat's state

            boat.put()
            boat_dict = boat.to_dict()
            boat_dict['self'] = '/boats/' + id
            self.response.write(json.dumps(boat_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")

    def get(self, id=None):
        if id:
            try:
                boat = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            boat_dict = boat.to_dict()
            boat_dict['self'] = '/boats/' + id
            if boat_dict['current_slip'] is not None:
                slip_key = boat_dict['current_slip']
                boat_dict['current_slip'] = '/slips/' + slip_key.urlsafe()
            self.response.write(json.dumps(boat_dict))
        else:
            boat_list = models.Boat.query().fetch()
            boat_arr = []
            for boat in boat_list:
                boat_dict = boat.to_dict()
                boat_dict['self'] = '/boats/' + boat.key.urlsafe()
                if boat_dict['current_slip'] is not None:
                    slip_key = boat_dict['current_slip']
                    boat_dict['current_slip'] = '/slips/' + slip_key.urlsafe()
                boat_arr.append(boat_dict)
            self.response.write(json.dumps(boat_arr))

    def patch(self, id=None):
        if id:
            try:
                boat = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            boat_data = json.loads(self.request.body)

            if 'name' in boat_data:
                boat.name = boat_data['name']
            if 'type' in boat_data:
                boat.type = boat_data['type']
            if 'length' in boat_data:
                boat.length = boat_data['length']

            boat.put()
            boat_dict = boat.to_dict()
            boat_dict['self'] = '/boats/' + id
            self.response.write(json.dumps(boat_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")

    def delete(self, id=None):
        if id:
            try:
                boat = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return

            if boat.current_slip is not None:
                slip = boat.current_slip.get()
                slip.current_boat = None
                slip.arrival_date = None
                slip.put()
            models.ndb.Key(urlsafe=id).delete()
            self.response.set_status(200, "Deleted")
            self.response.write("200 Deleted")
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")
