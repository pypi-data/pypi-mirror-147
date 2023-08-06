from json import dumps

def raise_not_implemented_error():
  raise not NotImplementedError('django is currently required to use geometry_helper modules. These should be changed to use pandas or similar')
try:
  from django.contrib.gis.geos import GeometryCollection, GEOSGeometry, Polygon

except ImportError:
  GeometryCollection = raise_not_implemented_error
  GEOSGeometry = raise_not_implemented_error
  Polygon = raise_not_implemented_error

def geometry_from_geojson(geojson):
    """
    Converts gejson to GEOSGeometry
    :param geojson:
    :return:
    """
    str = dumps(geojson)
    return GEOSGeometry(str)

def geometry_from_feature(feature):
    """
        Extracts the geometry property from the feature
    :param feature:
    :return:
    """
    return geometry_from_geojson(feature['geometry'])


def ewkt_from_feature(feature):
    return geometry_from_feature(feature).ewkt


# https://gis.stackexchange.com/questions/177254/create-a-geosgeometry-from-a-featurecollection-in-geodango
def geometrycollection_from_feature_collection(feature_collection):
    return GeometryCollection(tuple(R.map(geometry_from_feature, feature_collection['features'])))


def ewkt_from_feature_collection(feature_collection):
    """
        Like geometrycollection_from_featurecollection but calls ewkt to get the ewkt
        string.
    :param feature_collection:
    :return:
    """
    return geometrycollection_from_feature_collection(feature_collection).ewkt

