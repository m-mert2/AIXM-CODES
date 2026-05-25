# AIXM PDA Validator
# Her feature için PDA geçiş kuralları tanımlıdır.
# Yapı: { durum: { etiket: (yeni_durum, yığın_işlemi) } }
# Yığın işlemi: "push:X", "pop", "none", "reject"

PDA_RULES = {

    "Airspace": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Airspace": ("q1", "push:Airspace")},
            "q1": {
                "gml:identifier": ("q2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q2": {
                "aixm:timeSlice": ("q3", "none"),
                "gml:boundedBy": ("q_bounded", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_bounded": {
                "aixm:timeSlice": ("q3", "none"),
                "__other__": ("q_reject", "none")
            },
            "q3": {
                "/aixm:Airspace": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AirspaceLayer": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AirspaceLayer": ("q1", "push:AirspaceLayer")},
            "q1": {
                "aixm:discreteLevelSeries": ("q_discrete", "none"),
                "aixm:lowerLimit": ("q_lower1", "none"),
                "aixm:upperLimit": ("q_upper1", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_discrete": {
                "/aixm:AirspaceLayer": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_lower1": {
                "aixm:lowerLimitReference": ("q_lower2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_lower2": {
                "aixm:altitudeInterpretation": ("q_alt_interp", "none"),
                "/aixm:AirspaceLayer": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_upper1": {
                "aixm:upperLimitReference": ("q_upper2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_upper2": {
                "aixm:lowerLimit": ("q_upper3", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_upper3": {
                "aixm:lowerLimitReference": ("q_upper4", "none"),
                "aixm:altitudeInterpretation": ("q_alt_interp", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_upper4": {
                "aixm:altitudeInterpretation": ("q_alt_interp", "none"),
                "__other__": ("q_reject", "none")
            },
            "q_alt_interp": {
                "/aixm:AirspaceLayer": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AirportHeliport": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AirportHeliport": ("q1", "push:AirportHeliport")},
            "q1": {
                "gml:identifier": ("q2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q2": {
                "aixm:timeSlice": ("q3", "none"),
                "__other__": ("q_reject", "none")
            },
            "q3": {
                "/aixm:AirportHeliport": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Runway": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Runway": ("q1", "push:Runway")},
            "q1": {
                "gml:identifier": ("q2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q2": {
                "aixm:timeSlice": ("q3", "none"),
                "__other__": ("q_reject", "none")
            },
            "q3": {
                "aixm:designator": ("q_body", "none"),
                "/aixm:Runway": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:nominalLength": ("q_body", "none"),
                "aixm:lengthAccuracy": ("q_body", "none"),
                "aixm:nominalWidth": ("q_body", "none"),
                "aixm:widthAccuracy": ("q_body", "none"),
                "aixm:lengthStrip": ("q_body", "none"),
                "aixm:widthStrip": ("q_body", "none"),
                "aixm:surfaceProperties": ("q_body", "none"),
                "aixm:associatedAirportHeliport": ("q_body", "none"),
                "/aixm:Runway": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RunwayDirection": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RunwayDirection": ("q1", "push:RunwayDirection")},
            "q1": {
                "gml:identifier": ("q2", "none"),
                "__other__": ("q_reject", "none")
            },
            "q2": {
                "aixm:timeSlice": ("q3", "none"),
                "__other__": ("q_reject", "none")
            },
            "q3": {
                "aixm:designator": ("q_body", "none"),
                "/aixm:RunwayDirection": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_body": {
                "aixm:trueBearing": ("q_body", "none"),
                "aixm:trueBearingAccuracy": ("q_body", "none"),
                "aixm:elevationTDZ": ("q_body", "none"),
                "aixm:usedRunway": ("q_body", "none"),
                "/aixm:RunwayDirection": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RunwayElement": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RunwayElement": ("q1", "push:RunwayElement")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RunwayElement": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {
                "aixm:designator": ("q_body", "none"),
                "aixm:type": ("q_body", "none"),
                "/aixm:RunwayElement": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:extent": ("q_body", "none"),
                "aixm:associatedRunway": ("q_body", "none"),
                "/aixm:RunwayElement": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RunwayMarking": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RunwayMarking": ("q1", "push:RunwayMarking")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RunwayMarking": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {
                "aixm:type": ("q_body", "none"),
                "/aixm:RunwayMarking": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_body": {
                "aixm:condition": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:RunwayMarking": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RunwayCentrelinePoint": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RunwayCentrelinePoint": ("q1", "push:RunwayCentrelinePoint")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RunwayCentrelinePoint": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {
                "aixm:role": ("q_body", "none"),
                "/aixm:RunwayCentrelinePoint": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
            "q_body": {
                "aixm:location": ("q_body", "none"),
                "aixm:usedRunway": ("q_body", "none"),
                "/aixm:RunwayCentrelinePoint": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Navaid": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Navaid": ("q1", "push:Navaid")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Navaid": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:Navaid": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:designator": ("q_body", "none"),
                "aixm:name": ("q_body", "none"),
                "aixm:navaidEquipment": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "aixm:servedAirport": ("q_body", "none"),
                "aixm:signalPerformance": ("q_body", "none"),
                "aixm:runwayDirection": ("q_body", "none"),
                "/aixm:Navaid": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "VOR": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:VOR": ("q1", "push:VOR")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:VOR": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:frequency": ("q_body", "none"), "/aixm:VOR": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:magneticVariation": ("q_body", "none"),
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "/aixm:VOR": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "NDB": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:NDB": ("q1", "push:NDB")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:NDB": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:frequency": ("q_body", "none"), "/aixm:NDB": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "/aixm:NDB": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "DME": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:DME": ("q1", "push:DME")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:DME": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:channel": ("q_body", "none"), "/aixm:DME": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:location": ("q_body", "none"),
                "aixm:ghostFrequency": ("q_body", "none"),
                "/aixm:DME": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "TACAN": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:TACAN": ("q1", "push:TACAN")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:TACAN": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:channel": ("q_body", "none"), "/aixm:TACAN": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:location": ("q_body", "none"),
                "/aixm:TACAN": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Localizer": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Localizer": ("q1", "push:Localizer")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Localizer": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:frequency": ("q_body", "none"), "/aixm:Localizer": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:course": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:Localizer": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Glidepath": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Glidepath": ("q1", "push:Glidepath")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Glidepath": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:angle": ("q_body", "none"), "/aixm:Glidepath": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:rdh": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:Glidepath": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "MarkerBeacon": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:MarkerBeacon": ("q1", "push:MarkerBeacon")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:MarkerBeacon": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:MarkerBeacon": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:location": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:MarkerBeacon": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "VerticalStructure": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:VerticalStructure": ("q1", "push:VerticalStructure")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:VerticalStructure": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:name": ("q_body", "none"), "/aixm:VerticalStructure": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:lighted": ("q_body", "none"),
                "aixm:group": ("q_body", "none"),
                "aixm:length": ("q_body", "none"),
                "aixm:width": ("q_body", "none"),
                "aixm:radius": ("q_body", "none"),
                "aixm:part": ("q_body", "none"),
                "aixm:annotation": ("q_body", "none"),
                "/aixm:VerticalStructure": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "ObstacleArea": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:ObstacleArea": ("q1", "push:ObstacleArea")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:ObstacleArea": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:ObstacleArea": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:reference_ownerAirport": ("q_body", "none"),
                "aixm:reference_ownerRunway": ("q_body", "none"),
                "aixm:reference_ownerOrganisation": ("q_body", "none"),
                "aixm:surfaceExtent": ("q_body", "none"),
                "aixm:obstacle": ("q_body", "none"),
                "aixm:annotation": ("q_body", "none"),
                "/aixm:ObstacleArea": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Apron": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Apron": ("q1", "push:Apron")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Apron": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:name": ("q_body", "none"), "/aixm:Apron": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:associatedAirportHeliport": ("q_body", "none"),
                "/aixm:Apron": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "ApronElement": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:ApronElement": ("q1", "push:ApronElement")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:ApronElement": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:ApronElement": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:extent": ("q_body", "none"),
                "aixm:associatedApron": ("q_body", "none"),
                "/aixm:ApronElement": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AircraftStand": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AircraftStand": ("q1", "push:AircraftStand")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:AircraftStand": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:AircraftStand": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "aixm:apronLocation": ("q_body", "none"),
                "aixm:availability": ("q_body", "none"),
                "/aixm:AircraftStand": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Taxiway": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Taxiway": ("q1", "push:Taxiway")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Taxiway": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:Taxiway": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:associatedAirportHeliport": ("q_body", "none"),
                "/aixm:Taxiway": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "TaxiwayElement": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:TaxiwayElement": ("q1", "push:TaxiwayElement")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:TaxiwayElement": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:TaxiwayElement": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:extent": ("q_body", "none"),
                "aixm:associatedTaxiway": ("q_body", "none"),
                "/aixm:TaxiwayElement": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "TaxiHoldingPosition": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:TaxiHoldingPosition": ("q1", "push:TaxiHoldingPosition")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:TaxiHoldingPosition": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:TaxiHoldingPosition": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "/aixm:TaxiHoldingPosition": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "TaxiHoldingPositionMarking": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:TaxiHoldingPositionMarking": ("q1", "push:TaxiHoldingPositionMarking")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:TaxiHoldingPositionMarking": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:TaxiHoldingPositionMarking": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:condition": ("q_body", "none"),
                "aixm:servedTaxiHoldingPosition": ("q_body", "none"),
                "/aixm:TaxiHoldingPositionMarking": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "GuidanceLine": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:GuidanceLine": ("q1", "push:GuidanceLine")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:GuidanceLine": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:GuidanceLine": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:extent": ("q_body", "none"),
                "aixm:associatedTaxiway": ("q_body", "none"),
                "/aixm:GuidanceLine": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "GuidanceLineMarking": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:GuidanceLineMarking": ("q1", "push:GuidanceLineMarking")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:GuidanceLineMarking": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:GuidanceLineMarking": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:condition": ("q_body", "none"),
                "aixm:servedGuidanceLine": ("q_body", "none"),
                "/aixm:GuidanceLineMarking": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "TouchDownLiftOff": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:TouchDownLiftOff": ("q1", "push:TouchDownLiftOff")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:TouchDownLiftOff": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:TouchDownLiftOff": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "aixm:associatedAirportHeliport": ("q_body", "none"),
                "/aixm:TouchDownLiftOff": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "HoldingPattern": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:HoldingPattern": ("q1", "push:HoldingPattern")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:HoldingPattern": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:inboundCourse": ("q_body", "none"), "/aixm:HoldingPattern": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:turnDirection": ("q_body", "none"),
                "aixm:fix": ("q_body", "none"),
                "/aixm:HoldingPattern": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Route": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Route": ("q1", "push:Route")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Route": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:Route": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:flightRule": ("q_body", "none"),
                "/aixm:Route": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RouteSegment": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RouteSegment": ("q1", "push:RouteSegment")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RouteSegment": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:level": ("q_body", "none"), "/aixm:RouteSegment": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:start": ("q_body", "none"),
                "aixm:end": ("q_body", "none"),
                "aixm:routeFormed": ("q_body", "none"),
                "/aixm:RouteSegment": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "DesignatedPoint": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:DesignatedPoint": ("q1", "push:DesignatedPoint")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:DesignatedPoint": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:designator": ("q_body", "none"), "/aixm:DesignatedPoint": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "/aixm:DesignatedPoint": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "ChangeOverPoint": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:ChangeOverPoint": ("q1", "push:ChangeOverPoint")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:ChangeOverPoint": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:distance": ("q_body", "none"), "/aixm:ChangeOverPoint": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:routeSegment": ("q_body", "none"),
                "/aixm:ChangeOverPoint": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AirTrafficControlService": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AirTrafficControlService": ("q1", "push:AirTrafficControlService")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:AirTrafficControlService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:serviceProvider": ("q_body", "none"), "/aixm:AirTrafficControlService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:call_sign": ("q_body", "none"),
                "aixm:radioCommunication": ("q_body", "none"),
                "aixm:type": ("q_body", "none"),
                "aixm:clientAirspace": ("q_body", "none"),
                "/aixm:AirTrafficControlService": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "InformationService": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:InformationService": ("q1", "push:InformationService")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:InformationService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:serviceProvider": ("q_body", "none"), "/aixm:InformationService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:radioCommunication": ("q_body", "none"),
                "/aixm:InformationService": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "SearchRescueService": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:SearchRescueService": ("q1", "push:SearchRescueService")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:SearchRescueService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:serviceProvider": ("q_body", "none"), "/aixm:SearchRescueService": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "/aixm:SearchRescueService": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RadioCommunicationChannel": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RadioCommunicationChannel": ("q1", "push:RadioCommunicationChannel")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RadioCommunicationChannel": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:frequencyTransmission": ("q_body", "none"), "/aixm:RadioCommunicationChannel": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:frequencyReception": ("q_body", "none"),
                "aixm:type": ("q_body", "none"),
                "/aixm:RadioCommunicationChannel": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RadioFrequencyArea": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RadioFrequencyArea": ("q1", "push:RadioFrequencyArea")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RadioFrequencyArea": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:RadioFrequencyArea": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:extent": ("q_body", "none"),
                "/aixm:RadioFrequencyArea": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "GeoBorder": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:GeoBorder": ("q1", "push:GeoBorder")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:GeoBorder": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:GeoBorder": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:extent": ("q_body", "none"),
                "/aixm:GeoBorder": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "OrganisationAuthority": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:OrganisationAuthority": ("q1", "push:OrganisationAuthority")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:OrganisationAuthority": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:name": ("q_body", "none"), "/aixm:OrganisationAuthority": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:designator": ("q_body", "none"),
                "/aixm:OrganisationAuthority": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AuthorityForAirspace": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AuthorityForAirspace": ("q1", "push:AuthorityForAirspace")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:AuthorityForAirspace": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:AuthorityForAirspace": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:theAirspace": ("q_body", "none"),
                "aixm:theUnit": ("q_body", "none"),
                "/aixm:AuthorityForAirspace": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "Unit": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:Unit": ("q1", "push:Unit")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:Unit": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:name": ("q_body", "none"), "/aixm:Unit": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:designator": ("q_body", "none"),
                "/aixm:Unit": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "SpecialDate": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:SpecialDate": ("q1", "push:SpecialDate")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:SpecialDate": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:timeSlice": ("q3", "none"), "aixm:dateYear": ("q_body", "none"), "/aixm:SpecialDate": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:dateMonth": ("q_body", "none"),
                "aixm:dateDay": ("q_body", "none"),
                "aixm:type": ("q_body", "none"),
                "/aixm:SpecialDate": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AeronauticalGroundLight": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AeronauticalGroundLight": ("q1", "push:AeronauticalGroundLight")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:AeronauticalGroundLight": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:name": ("q_body", "none"), "/aixm:AeronauticalGroundLight": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:type": ("q_body", "none"),
                "aixm:colour": ("q_body", "none"),
                "aixm:flashing": ("q_body", "none"),
                "aixm:location": ("q_body", "none"),
                "/aixm:AeronauticalGroundLight": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "ApproachLightingSystem": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:ApproachLightingSystem": ("q1", "push:ApproachLightingSystem")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:ApproachLightingSystem": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:ApproachLightingSystem": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:classICAO": ("q_body", "none"),
                "aixm:length": ("q_body", "none"),
                "aixm:element": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:ApproachLightingSystem": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "RunwayDirectionLightSystem": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:RunwayDirectionLightSystem": ("q1", "push:RunwayDirectionLightSystem")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:RunwayDirectionLightSystem": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:RunwayDirectionLightSystem": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:RunwayDirectionLightSystem": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "VisualGlideSlopeIndicator": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:VisualGlideSlopeIndicator": ("q1", "push:VisualGlideSlopeIndicator")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:VisualGlideSlopeIndicator": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:type": ("q_body", "none"), "/aixm:VisualGlideSlopeIndicator": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:angle": ("q_body", "none"),
                "aixm:servedRunwayDirection": ("q_body", "none"),
                "/aixm:VisualGlideSlopeIndicator": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "AngleIndication": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:AngleIndication": ("q1", "push:AngleIndication")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:AngleIndication": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:angle": ("q_body", "none"), "/aixm:AngleIndication": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:angleType": ("q_body", "none"),
                "aixm:indicationDirection": ("q_body", "none"),
                "aixm:fix": ("q_body", "none"),
                "/aixm:AngleIndication": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },

    "DistanceIndication": {
        "start": "q0",
        "accept": ["q_accept"],
        "transitions": {
            "q0": {"aixm:DistanceIndication": ("q1", "push:DistanceIndication")},
            "q1": {"gml:identifier": ("q2", "none"), "__other__": ("q_reject", "none")},
            "q2": {"aixm:timeSlice": ("q3", "none"), "/aixm:DistanceIndication": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q3": {"aixm:distance": ("q_body", "none"), "/aixm:DistanceIndication": ("q_accept", "pop"), "__other__": ("q_reject", "none")},
            "q_body": {
                "aixm:fix": ("q_body", "none"),
                "aixm:pointChoice_navaidSystem": ("q_body", "none"),
                "/aixm:DistanceIndication": ("q_accept", "pop"),
                "__other__": ("q_reject", "none")
            },
        }
    },
}


def run_pda(feature_name, tokens):
    """
    PDA simülasyonu çalıştırır.
    tokens: liste halinde etiketler
    Döndürür: { accepted, steps, stack_history, error_token }
    """
    if feature_name not in PDA_RULES:
        return {"accepted": False, "steps": [], "error": f"{feature_name} için PDA kuralı bulunamadı."}

    rules = PDA_RULES[feature_name]
    state = rules["start"]
    stack = ["Z0"]
    steps = []
    stack_history = [list(stack)]

    for token in tokens:
        transitions = rules["transitions"].get(state, {})

        if token in transitions:
            next_state, stack_op = transitions[token]
        elif "__other__" in transitions:
            next_state, stack_op = transitions["__other__"]
        else:
            steps.append({
                "from": state,
                "token": token,
                "to": "q_reject",
                "stack_op": "none",
                "stack": list(stack)
            })
            return {
                "accepted": False,
                "steps": steps,
                "stack_history": stack_history,
                "error_token": token
            }

        # Yığın işlemi
        if stack_op.startswith("push:"):
            symbol = stack_op.split(":")[1]
            stack.append(symbol)
        elif stack_op == "pop":
            if len(stack) > 1:
                stack.pop()

        steps.append({
            "from": state,
            "token": token,
            "to": next_state,
            "stack_op": stack_op,
            "stack": list(stack)
        })
        stack_history.append(list(stack))
        state = next_state

        if state == "q_reject":
            return {
                "accepted": False,
                "steps": steps,
                "stack_history": stack_history,
                "error_token": token
            }

    accepted = state in rules["accept"] and stack == ["Z0"]
    return {
        "accepted": accepted,
        "steps": steps,
        "stack_history": stack_history,
        "error_token": None
    }
