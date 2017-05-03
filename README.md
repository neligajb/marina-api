## Intro
This REST API mangages boats and slip assignment in a "marina". It is built on Google App Engine, using the **webapp2** framework.
## https://marina-rest-api.appspot.com/
## Endpoints (required data in **bold**)

### Boats

* POST /boats

    * Add a boat

    * Data

        * { **"name": “SS Example”**, type: “schooner”, “length”: 21 }

    * Response

        * ```{"name": "SS Leisure", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw", "at_sea": true, "length": 32, "current_slip": null, "type": "schooner", "id": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw"}```

* PATCH /boats/**{boat_key}**

    * Modify a boat

    * Data

        * { **"name": “SS Leisure”,** type: “schooner”, “length”: 21 }

    * Response

        * ```{"name": "SS Leisure", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw", "at_sea": true, "length": 21, "current_slip": null, "type": "schooner", "id": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw"}```

* GET /boats

    * Get all boats

    * Response

        * ```[ {"name": "SS Leisure", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw", "at_sea": true, "length": 32, "current_slip": null, "type": "schooner"}, … ]```

* GET /boats/{boat_key}

    * Get single boat

    * Response

        * ```{"name": "SS Leisure", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw", "at_sea": true, "length": 32, "current_slip": null, "type": "schooner"}```

* PUT /boats/**{boat_key}**

    * Replace a boat

    * Data

        * { "**name": “SS Fergie”**, type: “yacht”, “length”: 130 }

    * Response

        * ```{"name": "SS Fergie", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICAgICACgw", "at_sea": true, "length": 130, "current_slip": null, "type": "yacht"}```

* DELETE /boats/**{boat_key}**

    * Response

        * 200 Deleted

### Slips

* POST /slips

    * Add a slip

    * Data

        * { **"number": 5 **}

    * Response

        * ```{"arrival_date": null, "departure_history": [], "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICAvKGCCgw", "number": 1, "current_boat": null, "id": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICAvKGCCgw"}```

* PATCH /slips/**{slip_key}**

    * Modify a slip

    * Data

        * { **"number": 3 **}

    * Response

        * ```{"departure_history": [], "current_boat": null, "arrival_date": null, "number": 3, "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICAvKGCCgw"}```

* GET /slips/{slip_key}

    * Get a slip

    * Response

        * ```{"departure_history": [], "current_boat": null, "arrival_date": null, "number": 3, "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICAvKGCCgw"}```

* GET /slips

    * Get all slips

    * Response

        * ```[{"departure_history": [], "current_boat": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICA2uOGCgw", "arrival_date": "04/30/2017", "number": 5, "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA3pCBCgw"}, {"departure_history": [{"departure_date": "04/30/2017", "departed_boat": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICA-MKECgw"}], "current_boat": null, "arrival_date": null, "number": 1, "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA-JaVCgw"}]```

* GET /slips/**{slip_key}**/boat

    * Get the boat in current slip

    * Response

        * ```{"name": "SS n00b2", "self": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICA2uOGCgw", "at_sea": false, "length": 6, "current_slip": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA3pCBCgw", "type": "dinghy"}```

    * Unoccupied slip returns *null*

* PUT /slips/**{slip_key}**

    * Replace a slip

    * Data

        * { **"number": 10 }**

    * Response

        * ```{"departure_history": [], "current_boat": null, "arrival_date": null, "number": 10, "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICAvKGCCgw"}```

* DELETE /slips/**{slip_key}**

    * 200 Deleted

### Arrivals

* PUT /slips/**{slip_key}**/arrival/**{boat_key}**

    * Move a boat from At Sea to a specified slip

    * Data

        * None

    * Response

        * ```{"arrival_date": "04/30/2017", "departure_history": [], "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA-JaVCgw", "number": 1, "current_boat": "/boats/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICA-MKECgw", "id": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA-JaVCgw"}```

### Departures

* PUT /slips/**{slip_key}**/departure/**{boat_key}**

    * Move a boat from a slip to At Sea

    * Data

        * None

    * Response

        * ```{"arrival_date": null, "departure_history": [{"departure_date": "04/30/2017", "departed_boat": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEQm9hdBiAgICA-MKECgw"}], "self": "/slips/ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA-JaVCgw", "number": 1, "current_boat": null, "id": "ahFwfm1hcmluYS1yZXN0LWFwaXIRCxIEU2xpcBiAgICA-JaVCgw"}```

