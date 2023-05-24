import unittest

from tests.test_user import UserTest
from tests.test_stats import TestStats

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(UserTest("test_01_register"))
    suite.addTest(UserTest("test_02_register"))
    suite.addTest(UserTest("test_03_login"))
    suite.addTest(UserTest("test_04_save_history"))
    suite.addTest(UserTest("test_05_get_history"))

    suite.addTest(TestStats("test_returns_stats_for_music_category"))
    suite.addTest(TestStats("test_should_filter_music_comments_in_range"))

    runner = unittest.TextTestRunner()
    runner.run(suite)