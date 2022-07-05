polygon = api.model('PolygonGeometry', {
    'type': fields.String(required=True, default="Polygon"),
    'coordinates': fields.List(fields.List(fields.Float, required=True, type="Array"),
                               required=True, type="Array")
})


poly2 = Polygon(data['features']["geometry"]['coordinates'])