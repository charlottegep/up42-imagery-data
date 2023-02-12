import json
import requests
import rasterio
import numpy as np


def fetch_scene(geometry_json, cloud_cover_limit):
    """
    Searches for and fetches the Sentinel-2 imagery that covers a given geometry.

    :param geometry_json: the json file with the geometry to be covered in the scene
    :param cloud_cover_limit: an integer representing the % limit of cloud cover
    :return: a json string of search results
    """

    with open(geometry_json) as f:
        geo = f.read()
    geometry = json.loads(geo)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/geo+json'
    }
    data = {
        "intersects": geometry,
        "limit": 1,
        "sorts": [
            {
                "field": "acquisition_date",
                "direction": "desc"
            }
        ],
        "filter": {
            "cloud_cover": {
                "lte": cloud_cover_limit
            }
        }
    }
    try:
        response = requests.post('https://earth-search.aws.element84.com/v0/search', params=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    scene = response.json()
    return scene


def compute_mean(scene):
    """
    Computes the mean value of the raster imagery scene.
    As there are several .tif images in the scene result, I have chosen to use the TCI (True Color Image)
    to focus on the visible light (RGB) bands. This function calculates the mean of each of the 3 color arrays,
    then the mean of the total.

    :param scene: the json string of scene search results
    :return: the mean value of the scene -> ndarray
    """

    raster_url = scene["features"][1]["assets"]["visual"]["href"]
    with rasterio.open(raster_url) as src:
        band_avg = []
        for i in range(1, src.count + 1):
            values = src.read(i)
            mean = np.mean(values)
            print(f'Mean of Band {i}: {mean}')
            band_avg.append(mean)
    mean_value = np.mean(band_avg)
    print(f'Mean: {mean_value}')
    return mean_value


if __name__ == '__main__':
    geometry_json = 'satellite_geometry.json'
    scene = fetch_scene(geometry_json=geometry_json, cloud_cover_limit=40)
    compute_mean(scene=scene)
