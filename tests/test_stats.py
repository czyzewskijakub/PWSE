import json
import os
import random
import string
import sys
from unittest import TestCase
from urllib.parse import urlencode

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


class TestStats(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.post("/users/register", json=request_body, content_type="application/json")
        response = self.client.post("/users/login", json=request_body, content_type="application/json")
        self.headers = {'Authorization': f'Bearer {json.loads(response.data)["token"]}'}

    def test_returns_stats_for_music_category(self):
        params = {'videoCategoryId': 10}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req, headers=self.headers).json

        self.assertEqual(res['videoViewCount']['mean'], 101311.82430352402)
        self.assertEqual(res['videoViewCount']['std'], 1875953.9900374322)
        self.assertEqual(res['videoLikeCount']['max'], 1240473.0)

    def test_should_filter_music_comments_in_range(self):
        params = {'videoCategoryId': 10, 'minVideoCommentCount': 20, 'maxVideoCommentCount': 30}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req, headers=self.headers).json

        self.assertEqual(res['VideoCommentCount']['min'], 20)
        self.assertEqual(res['VideoCommentCount']['max'], 30)

    def test_should_return_ok_on_stats(self):
        req = '/ai/statistics/describe'
        self.assertEqual(self.client.get(req, headers=self.headers).status_code, 200)
