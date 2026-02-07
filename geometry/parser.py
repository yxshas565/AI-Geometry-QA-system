# geometry/parser.py

from shapely import wkt

def load_geometry(wkt_string):
    """
    Load WKT string into a Shapely geometry
    """
    try:
        geom = wkt.loads(wkt_string)
        return geom
    except Exception as e:
        raise ValueError(f"Invalid WKT input: {e}")
