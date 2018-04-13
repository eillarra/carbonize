from math import radians, cos, sin, sqrt, atan2

from .typing import Point, Km


def great_circle(a: Point, b: Point) -> Km:
    """Calculates the great circle distance between two points on Earth.
    Source: https://github.com/geopy/geopy/blob/master/geopy/distance.py"""
    lat1, lng1, lat2, lng2 = map(radians, [a.latitude, a.longitude, b.latitude, b.longitude])
    sin_lat1, sin_lat2 = map(sin, [lat1, lat2])
    cos_lat1, cos_lat2 = map(cos, [lat1, lat2])
    delta_lng = lng2 - lng1
    cos_delta_lng, sin_delta_lng = cos(delta_lng), sin(delta_lng)

    d = atan2(
        sqrt((cos_lat2 * sin_delta_lng) ** 2 + (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
        sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng
    )

    return 6371.009 * d  # Radius of earth in kilometers is 6371
