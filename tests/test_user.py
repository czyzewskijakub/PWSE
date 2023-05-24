import json
import random
import string
from flask_testing import TestCase
from backend import app


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
class UserTest(TestCase):
    token = ""
    def create_app(self):
        main_app = app.create_app()
        main_app.config["TESTING"] = True

        return main_app

    def test_01_register(self):
        response = self.client.post("/users/register", json=request_body, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_02_register(self):
        response = self.client.post("/users/register", json=request_body, content_type="application/json")
        self.assertEqual(response.status_code, 409)

    def test_03_login(self):
        response = self.client.post("/users/login", json=request_body, content_type="application/json")
        self.token = json.loads(response.data)["token"]
        self.assertEqual(202, response.status_code)

    def test_04_save_history(self):
        hds = {
            "Authorization": f'Bearer {self.token}'
        }
        prediction_body = {
            "channel_video_count": 33,
            "channel_view_count": 162137793,
            "channel_comment_count": 140,
            "channel_elapsed_time": 70920,
            "channel_subscriber_count": 153256,
            "video_category_id": 10,
            "video_published": "2009-10-03",
            "likes": 70973,
            "dislikes": 2433,
            "comments": 3473,
            "elapsed_time": 70176,
            "predicted_views": 14696828,
            "user_id": 1,
        }
        response = self.client.post("/users/history/save", headers=hds,
                                    json=prediction_body, content_type="application/json")
        self.assertEqual(201, response.status_code)

    def test_05_get_history(self):
        hds = {
            "Authorization": f'Bearer {self.token}'
        }
        response = self.client.get(f'/users/history/get?user_id={1}', headers=hds, content_type="application/json")
        self.assertEqual(200, response.status_code)
