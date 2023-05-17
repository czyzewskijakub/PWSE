import os
import sys
from unittest import TestCase
from urllib.parse import urlencode

sys.path.append(os.getcwd() + '/..')
from backend.app import create_app


class TestStats(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_returns_stats_for_music_category(self):
        params = {'VCategory': 10}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req).json

        self.assertEqual(res['VViews']['mean'], 101076.14659525632)
        self.assertEqual(res['VViews']['std'], 1874283.3210626151)
        self.assertEqual(res['VLikes']['max'], 1240473.0)

    def test_should_filter_music_comments_in_range(self):
        params = {'VCategory': 10, 'minVComments': 20, 'maxVComments': 30}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req).json

        self.assertEqual(res['VComments']['min'], 20)
        self.assertEqual(res['VComments']['max'], 30)
