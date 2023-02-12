import requests
import requests_mock
import unittest
import validators

import process_sat_data

JSON = 'satellite_geometry.json'


class TestProcessSatData(unittest.TestCase):

    def test_fetch_scene(self):
        scene = process_sat_data.fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        self.assertNotIsInstance(scene, requests.exceptions.HTTPError), "Scene not found"
        self.assertIsInstance(scene, dict), "Output format is incorrect"

    def test_fetch_scene_with_http_error(self):
        with requests_mock.Mocker() as m:
            # mock a failed response from the search endpoint
            m.post('https://earth-search.aws.element84.com/v0/search', text='Bad Request', status_code=400)

            with self.assertRaises(requests.exceptions.HTTPError):
                scene = process_sat_data.fetch_scene(geometry_json='satellite_geometry.json', cloud_cover_limit=40)

    def test_tif_in_url(self):
        scene = process_sat_data.fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        raster_url = scene["features"][1]["assets"]["visual"]["href"]
        self.assertTrue(validators.url(raster_url))
        self.assertIn('.tif', raster_url)

    def test_compute_mean_invalid_data(self):
        scene = {'features': []}
        mean_value = process_sat_data.compute_mean(scene=scene)
        self.assertRaises(IndexError)

    def test_compute_mean_value(self):
        scene = process_sat_data.fetch_scene(geometry_json=JSON, cloud_cover_limit=40)
        mean = process_sat_data.compute_mean(scene=scene)
        self.assertNotEqual(mean, 0)


if __name__ == '__main__':
    unittest.main()
