import geopandas as gpd
import fiona

from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import requests

import math

def get_key():
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close()
    return api_key


def get_image(base_url, lat, lon, maptype, zoom):
    custom_url = base_url.replace("LAT", str(lat))
    custom_url = custom_url.replace("LON", str(lon))
    custom_url = custom_url.replace("ZOOM", str(zoom))
    custom_url = custom_url.replace("MAPTYPE", maptype)
    custom_url = custom_url.replace("YOUR_API_KEY", get_key())
    buffer = BytesIO(requests.get(custom_url).content)
    image = Image.open(buffer)
    opencv_image = np.array(image.convert('RGB'))
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
    return opencv_image


def deg_to_rad(arc):
    return math.pi*arc/180.0


# https://www.movable-type.co.uk/scripts/latlong.html
def distance_from_coordinates(lat1, lon1, lat2, lon2):
    r = 6371e3
    phi1 = deg_to_rad(lat1)
    phi2 = deg_to_rad(lat2)
    delta_phi = deg_to_rad(lat2-lat1)
    delta_lambda = deg_to_rad(lon2-lon1)
    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) * \
        math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c


def test_distance_calc():
    err = distance_from_coordinates(-20.315146, -40.288799, -20.314758, -40.289660) - 99.6116927217669
    if math.fabs(err) > 0.01:
        print("Error at distance_from_coordinates function")
        exit(0)


def main():
    print(get_key())
    test_distance_calc()

    lat = -20.3152889
    lon = -40.2889104
    zoom = 20
    maptype = "satellite"
    base_url = """
        https://maps.googleapis.com/maps/api/staticmap?center=LAT,LON&zoom=ZOOM&size=
        1024x1024&maptype=MAPTYPE&key=YOUR_API_KEY"""
    opencv_image = get_image(base_url, lat, lon, maptype, zoom)
    cv2.imshow('original image', opencv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    exit(0)
    fiona.drvsupport.supported_drivers['kml'] = 'rw'  # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw'  # enable KML support which is disabled by default

    geo_data = gpd.read_file("./data/Edificacoes.kml")


if __name__ == "__main__":
    main()
