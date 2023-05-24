import os
import sys
from unittest import TestCase
from urllib.parse import urlencode

sys.path.append(os.getcwd() + '/..')
from backend.app import create_app


class TestPredictions(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_should_return_ok_on_prediction(self):
        request_body = {
            "channel_view_count": 123,
            "channel_elapsed_time": 123,
            "channel_video_count": 123,
            "channel_subscriber_count": 123,
            "channel_comment_count": 123,
            "likes": 123,
            "video_categoryId": 1,
            "dislikes": 123,
            "comments": 123,
            "elapsed_time": 123,
            "video_published": "2023-06-04",
        }
        req = '/ai/predict'
        self.assertEqual(self.client.post(req, json=request_body).status_code, 200)

    def test_should_return_predictions_as_number(self):
        request_body = {
            "channel_view_count": 123,
            "channel_elapsed_time": 123,
            "channel_video_count": 123,
            "channel_subscriber_count": 123,
            "channel_comment_count": 123,
            "likes": 123,
            "video_categoryId": 1,
            "dislikes": 123,
            "comments": 123,
            "elapsed_time": 123,
            "video_published": "2023-06-04",
        }
        req = '/ai/predict'
        self.assertIsInstance(self.client.post(req, json=request_body).json['views'], int)
