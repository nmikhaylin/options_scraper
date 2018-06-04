import tensorflow as tf
import pandas as pd
import datetime

import analyze_options_data

test  = tf.test
log = tf.logging
FLAGS = tf.flags.FLAGS

DEFAULT_NUM_ROWS = 3
TEST_TIME = datetime.date(2018,1,1)


class AnalyzeOptionsDataTest(test.TestCase):
  def setUp(self):
    self._test_df = pd.DataFrame({
      "underlying_name": ["AAPL"] * DEFAULT_NUM_ROWS,
      "underlying_price": [100.0] * DEFAULT_NUM_ROWS,
      "bid": [1.00, 6.00, 21.0],
      "ask": [1.02, 6.02, 21.2],
      "last_price": [1.03, 6.03, 21.3],
      "iv": [30.00] * DEFAULT_NUM_ROWS,
      "volume": [1, 10 ,100],
      "expiration_date": [datetime.date(2018,1,21)] * DEFAULT_NUM_ROWS,
      "strikes": [100.00, 95.0, 80.0],
      "is_call": [True] * DEFAULT_NUM_ROWS
    })

  def testFindCoveredCalls(self):
    with self.test_session():
      self.assertEqual(self._test_df["is_call"][0],
                       self._test_df["is_call"][1])
      self.assertEqual(self._test_df["strikes"][0],
                       self._test_df["strikes"][1])


if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  test.main()
