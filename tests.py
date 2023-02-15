import unittest

import requests
import requests_mock
import validators

from process_sat_data import fetch_scene, compute_mean

JSON = 'satellite_geometry.json'


class TestProcessSatData(unittest.TestCase):

    def test_fetch_scene(self):
        """
        Assert that output exists and is correct format
        """
        scene = fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        self.assertNotIsInstance(scene, requests.exceptions.HTTPError), "Scene not found"
        self.assertIsInstance(scene, dict), "Output format is incorrect"

    def test_fetch_scene_with_http_error(self):
        """
        Mock a failed response from search endpoint and assert HTTP error is raised
        """
        with requests_mock.Mocker() as m:
            m.post('https://earth-search.aws.element84.com/v0/search', text='Bad Request', status_code=400)
            scene = fetch_scene(geometry_json='satellite_geometry.json', cloud_cover_limit=40)
            self.assertRaises(requests.exceptions.HTTPError)

    def test_tif_in_url(self):
        """
        Assert that dict index reaches a url with 'TCI.tif' to verify correct image is retrieved
        """
        scene = fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        raster_url = scene["features"][1]["assets"]["visual"]["href"]
        self.assertTrue(validators.url(raster_url))
        self.assertIn('TCI.tif', raster_url)

    def test_compute_mean_invalid_data(self):
        """
        Assert that if the scene json dict is empty, an IndexError will be raised
        """
        scene = {'features': []}
        mean_value = compute_mean(scene=scene)
        self.assertRaises(IndexError)

    def test_compute_mean_value(self):
        """
        Assert that computing the mean value will return a non-zero value
        """
        scene = fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        mean = compute_mean(scene=scene)
        self.assertNotEqual(mean, 0)


if __name__ == '__main__':
    unittest.main()
