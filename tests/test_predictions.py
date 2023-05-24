import json
import os
import random
import string
import sys
from unittest import TestCase

sys.path.append(os.getcwd() + '/..')
from backend.app import create_app


def random_chars(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


random_email = random_chars(15) + "@" + random_chars(5) + "." + random_chars(2)
request_body = {
    "name": "example",
    "email": random_email.lower(),
    "password": "14km77So9x!",
    "profile_picture_url": "https://i.pinimg.com/550x/ee/f5/a8/eef5a896701a544d1b3da168956eca44.jpg"
}
token = ""


class TestPredictions(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.post("/users/register", json=request_body, content_type="application/json")
        response = self.client.post("/users/login", json=request_body, content_type="application/json")
        self.headers = {'Authorization': f'Bearer {json.loads(response.data)["token"]}'}

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
        self.assertEqual(self.client.post(req, json=request_body, headers=self.headers).status_code, 200)

    def test_should_return_unauthorized_on_prediction(self):
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
        self.assertEqual(self.client.post(req, json=request_body).status_code, 401)

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
        self.assertIsInstance(self.client.post(req, json=request_body, headers=self.headers).json['views'], int)
