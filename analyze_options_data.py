import tensorflow as tf
import datetime
import re
import json
import pandas as pd

log = tf.logging
FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string(
    "pandas_msg_pack_file", None, "Serialized msgpack DataFrame for the current options data.")

def analyze_options_data():
  df = pd.read_msgpack(FLAGS.pandas_msg_pack_file)
  print(df)

def main(argv):
  analyze_options_data()

if __name__ == "__main__":
  tf.flags.mark_flag_as_required('pandas_msg_pack_file')
  tf.app.run()
