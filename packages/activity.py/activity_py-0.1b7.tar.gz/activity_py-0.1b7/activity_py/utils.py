from collections import defaultdict
from math import asin, cos, radians, sin, sqrt

AVG_EARTH_RADIUS = 6371  # in km


def format_mins_seconds(d):
    d = int(d)
    minutes, seconds = divmod(d, 60)
    return f"{minutes:02}:{seconds:02}"


def semicircle_to_degrees(semicircles):
    """Convert a number in semicricles to degrees"""
    return semicircles * (180.0 / 2.0**31)


def etree_to_dict_no_namespaces(t):
    tag = t.tag.split("}")[-1]
    d = {tag: {} if t.attrib else None}

    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict_no_namespaces, children):
            for k, v in dc.items():
                dd[k.split("}")[-1]].append(v)
        d = {tag: {k.split("}")[-1]: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[tag]["#text"] = text
        else:
            d[tag] = text
    return d


def haversine(point1, point2):
    """Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance between the two points.
    """
    # unpack latitude/longitude
    lat1, lng1 = point1[0], point1[1]
    lat2, lng2 = point2[0], point2[1]

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))

    return h  # in kilometers
