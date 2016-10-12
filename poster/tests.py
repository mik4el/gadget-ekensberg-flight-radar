import unittest
from post_serial_data import DataPosterWorker
import queue


class TestDataPosterWorker(unittest.TestCase):
	def setUp(self):
		self.token = 'eyJaaGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjasLCJ1c2VybmFtZSI6Im1pazRlbCIsImVtYWlsIjoibWlrNGVsLjRuZGVyc3NvbkBnbWFpbC5jb20iLCJleHAiOjE0NjkwODkxMjIsIm9yaWdfaWF0IjoxNDY3ODc5NTIyfQ.ekFnrBFR5DosdDvwNf5u3-shOMtNFkQWTTAvCINd3pY'
		base_url = 'https://m4bd.se'
		self.data = '[{"hex":"47a41b", "flight":"NAX817  ", "lat":59.502457, "lon":17.815247, "altitude":10950, "track":283, "speed":290},{"hex":"478690", "flight":"SAS163  ", "lat":59.457275, "lon":17.710693, "altitude":12300, "track":261, "speed":322},{"hex":"4ac8b8", "flight":"SAS109  ", "lat":59.192148, "lon":17.283388, "altitude":24825, "track":218, "speed":391},{"hex":"478536", "flight":"NAX4162 ", "lat":59.304703, "lon":18.264130, "altitude":12125, "track":3, "speed":264},{"hex":"407003", "flight":"SK082   ", "lat":59.428024, "lon":18.206177, "altitude":10275, "track":359, "speed":261}]'
		self.status_queue = queue.Queue()
		self.data_poster = DataPosterWorker(self.token, base_url, self.data, self.status_queue)

	def test_values_set(self):
		self.assertEqual(self.data_poster.post_url, 'https://m4bd.se/api/v1/gadgets/ekensberg-flight-radar/data/')
		self.assertEqual(self.data_poster.headers['Authorization'], 'Bearer '+ self.token)
		self.assertEqual(self.data_poster.data_string, self.data)