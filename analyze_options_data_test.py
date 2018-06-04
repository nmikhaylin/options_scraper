import tensorflow as tf
import pandas as pd
import datetime

import analyze_options_data

test  = tf.test
log = tf.logging
FLAGS = tf.flags.FLAGS

DEFAULT_NUM_ROWS = 6
TEST_TIME = datetime.date(2018,1,1)


class AnalyzeOptionsDataTest(test.TestCase):
  def setUp(self):
    analyze_options_data.todays_date = TEST_TIME
    self._test_df = pd.DataFrame({
      "underlying_name": ["AAPL"] * DEFAULT_NUM_ROWS,
      "underlying_price": [100.0] * DEFAULT_NUM_ROWS,
      "bid": [1.00, 6.00, 21.0, 1.00, 6.00, 21.0],
      "ask": [1.02, 6.02, 21.02, 1.02, 6.02, 21.02],
      "last_price": [1.03, 6.03, 21.03, 1.03, 6.03, 21.03],
      "iv": [30.00] * DEFAULT_NUM_ROWS,
      "volume": [1, 10 ,100, 1, 10 ,100],
      "expiration_date": [datetime.date(2018,1,21)] * DEFAULT_NUM_ROWS,
      "strike": [100.00, 95.0, 80.0, 100.00, 105.0, 120.0],
      "is_call": [True, True, True, False, False, False]
    })
    analyze_options_data.post_process_df(self._test_df)

  def testPostProcess(self):
    with self.test_session():
      self.assertAllEqual([20] * DEFAULT_NUM_ROWS,
                          self._test_df["days_til_expiry"])
      self.assertAllClose([1.00] * DEFAULT_NUM_ROWS,
                          self._test_df["bid_premium"])
      self.assertAllClose([1.02] * DEFAULT_NUM_ROWS,
                          self._test_df["ask_premium"])
      self.assertAllClose([100.0, 95.0, 80.0] * 2,
                          self._test_df["loan_amount"])
      self.assertAllClose([0.18615 , 0.195947, 0.232687] * 2,
                          self._test_df["loan_apr"])

  def testFindCoveredCalls(self):
    with self.test_session():
      self.assertEqual(self._test_df["is_call"][0],
                       self._test_df["is_call"][1])


if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  test.main()
