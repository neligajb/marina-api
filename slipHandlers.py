import json
import webapp2
import time

import models


class SlipsHandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
        if 'number' not in slip_data:
            self.response.set_status(400)
            self.response.write("400 Bad request")
            return
        new_slip = models.Slip(number=slip_data['number'])
        new_slip.put()
        slip_dict = new_slip.to_dict()
        slip_dict['id'] = new_slip.key.urlsafe()
        slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
        self.response.write(json.dumps(slip_dict))

    def put(self, id=None):
        if id:
            slip_data = json.loads(self.request.body)
            if 'number' not in slip_data:
                self.response.set_status(400)
                self.response.write("400 Bad request")
                return

            try:
                slip = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return

            slip.number = slip_data['number']

            # check if there is a boat in this slip
            if slip.current_boat:
                boat = models.ndb.Key(slip.current_boat).get()
                boat.at_sea = True
            slip.current_boat = None
            slip.arrival_date = None
            del slip.departure_history[:]

            slip.put()
            slip_dict = slip.to_dict()
            slip_dict['self'] = '/slips/' + id
            self.response.write(json.dumps(slip_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")

    def get(self, id=None):
        if id:
            try:
                slip = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            slip_dict = slip.to_dict()
            if slip_dict['current_boat'] is not None:
                boat_key = slip_dict['current_boat']
                slip_dict['current_boat'] = '/boats/' + boat_key.urlsafe()
            slip_dict['self'] = '/slips/' + id
            self.response.write(json.dumps(slip_dict))
        else:
            slip_list = models.Slip.query().fetch()
            slip_arr = []
            for slip in slip_list:
                slip_dict = slip.to_dict()
                slip_dict['self'] = '/slips/' + slip.key.urlsafe()
                if slip_dict['current_boat'] is not None:
                    boat_key = slip_dict['current_boat']
                    slip_dict['current_boat'] = '/boats/' + boat_key.urlsafe()
                slip_arr.append(slip_dict)
            self.response.write(json.dumps(slip_arr))

    def patch(self, id=None):
        if id:
            try:
                slip = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            slip_data = json.loads(self.request.body)

            if 'number' in slip_data:
                slip.number = slip_data['number']

            slip.put()
            slip_dict = slip.to_dict()
            slip_dict['self'] = '/slips/' + id
            self.response.write(json.dumps(slip_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")

    def delete(self, id=None):
        if id:
            try:
                slip = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            if slip.current_boat is not None:
                boat = slip.current_boat.get()
                boat.current_slip = None
                boat.at_sea = True
                boat.put()
            models.ndb.Key(urlsafe=id).delete()
            self.response.set_status(200)
            self.response.write("200 Deleted")
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")


class ArrivalsHandler(webapp2.RequestHandler):
    def put(self, slipId=None, boatId=None):
        if slipId and boatId:
            try:
                slip = models.ndb.Key(urlsafe=slipId).get()
                boat = models.ndb.Key(urlsafe=boatId).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            if slip.current_boat is not None:
                self.response.set_status(403)
                self.response.write("403 Forbidden")
                return
            boat.at_sea = False
            boat.current_slip = slip.key
            boat.put()
            slip.arrival_date = time.strftime("%m/%d/%Y")
            slip.current_boat = boat.key
            slip.put()
            slip_dict = slip.to_dict()
            slip_dict['id'] = slip.key.urlsafe()
            slip_dict['self'] = '/slips/' + slip.key.urlsafe()
            boat_key = slip_dict['current_boat']
            slip_dict['current_boat'] = '/boats/' + boat_key.urlsafe()
            self.response.write(json.dumps(slip_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")


class DeparturesHandler(webapp2.RequestHandler):
    def put(self, slipId=None, boatId=None):
        if slipId and boatId:
            try:
                slip = models.ndb.Key(urlsafe=slipId).get()
                boat = models.ndb.Key(urlsafe=boatId).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            boat.at_sea = True
            boat.put()
            slip.arrival_date = None
            slip.current_boat = None
            boat.current_slip = None
            log = slip.departure_history
            this_departure = {'departure_date': time.strftime("%m/%d/%Y"), 'departed_boat': boat.key.urlsafe()}
            if log is not None:
                log.append(this_departure)
            else:
                log = this_departure
            slip.departure_history = log
            slip.put()
            slip_dict = slip.to_dict()
            slip_dict['id'] = slip.key.urlsafe()
            slip_dict['self'] = '/slips/' + slip.key.urlsafe()
            self.response.write(json.dumps(slip_dict))
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")


class SlipBoatHandler(webapp2.RequestHandler):
    def get(self, id=None):
        if id:
            try:
                slip = models.ndb.Key(urlsafe=id).get()
            except:
                self.response.set_status(404)
                self.response.write("404 not found")
                return
            if slip.current_boat is not None:
                boat = slip.current_boat.get()
                boat_dict = boat.to_dict()
                boat_dict['self'] = '/boats/' + boat.key.urlsafe()
                boat_dict['current_slip'] = '/slips/' + id
                self.response.write(json.dumps(boat_dict))
            else:
                self.response.write("null")
        else:
            self.response.set_status(400)
            self.response.write("400 Bad request")
