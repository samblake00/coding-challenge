# encoding: utf-8

"""
RESTful API GeoAPI resources
--------------------------
"""

from functools import partial
from http import HTTPStatus

import geopy.distance
import pyproj
from app.modules.geoapi import GeoApiNamespace
from flask import request
from flask_restplus import Namespace, Resource, abort
from flask_restplus import fields
from http import HTTPStatus
from shapely.geometry import Polygon

from app.modules.geoapi import GeoApiNamespace

api = Namespace('geoapi', description=GeoApiNamespace.description)

# API modules
polygon = api.model('PolygonGeometry', {
    'type': fields.String(required=True, default="Polygon"),
    'coordinates': fields.List(fields.List(fields.Float, required=True, type="Array"),
                               required=True, type="Array")
})

polygon_feature = api.model('PolygonFeature', {
    'type': fields.String(default="Feature", require=True),
    'properties': fields.String(required=False),
    'geometry': fields.Nested(polygon, required=True)
})

polygon_collection = api.model('FeatureCollection', {
    'type': fields.String(default="Features", require=True),
    'features': fields.Nested(polygon_feature, required=True)
})

#API POST Method
@api.route('/polygon/intersect/')
class PolygonIntersect(Resource):
    """
    Return boolean value based on the intersection of two polygons
    """

    @api.expect(polygon_collection)
    @api.doc(id='polygon_intersect', validate=True)
    def post(self):
        """
        Return boolean value based on the intersection of two polygons
        """
        try:
            #geojson payload to json format
            data = request.get_json()

            #polygons being evaluated for intersection
            poly1 = Polygon(data['features'][0]['geometry']['coordinates'])
            poly2 = Polygon(data['features'][1]['geometry']['coordinates'])

            #print boolean result
            print(poly1.intersects(poly2))
        except Exception as err:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message="The GeoJSON polygon couldn't be processed.", error=err)

