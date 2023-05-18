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
        params = {'videoCategoryId': 10}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req).json

        self.assertEqual(res['videoViewCount']['mean'], 101311.82430352402)
        self.assertEqual(res['videoViewCount']['std'], 1875953.9900374322)
        self.assertEqual(res['videoLikeCount']['max'], 1240473.0)

    def test_should_filter_music_comments_in_range(self):
        params = {'videoCategoryId': 10, 'minVideoCommentCount': 20, 'maxVideoCommentCount': 30}
        req = '/ai/statistics/describe?' + urlencode(params)
        res = self.client.get(req).json

        self.assertEqual(res['VideoCommentCount']['min'], 20)
        self.assertEqual(res['VideoCommentCount']['max'], 30)
