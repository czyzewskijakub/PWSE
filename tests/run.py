import unittest

from tests.test_predictions import TestPredictions
from tests.test_stats import TestStats
from tests.test_user import UserTest

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(UserTest("test_01_register"))
    suite.addTest(UserTest("test_02_register"))
    suite.addTest(UserTest("test_03_login"))
    suite.addTest(UserTest("test_04_save_history"))
    suite.addTest(UserTest("test_05_get_history"))

    suite.addTest(TestStats("test_returns_stats_for_music_category"))
    suite.addTest(TestStats("test_should_filter_music_comments_in_range"))
    suite.addTest(TestStats("test_should_return_ok_on_stats"))
    suite.addTest(TestStats("test_should_return_unauthorized_on_stats"))

    suite.addTest(TestPredictions("test_should_return_ok_on_prediction"))
    suite.addTest(TestPredictions("test_should_return_unauthorized_on_prediction"))
    suite.addTest(TestPredictions("test_should_return_predictions_as_number"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
