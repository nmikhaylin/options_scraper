import tensorflow as tf
import datetime
import re
import os
import json
import pandas as pd

log = tf.logging
FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string(
    "pandas_msg_pack_file", None,
    "Serialized msgpack DataFrame for the current options data.")

def find_covered_calls(df):
  print(df.head())


def load_df_from_file():
  full_path = os.path.abspath(FLAGS.pandas_msg_pack_file)
  with open(full_path, 'r') as f:
    df = pd.read_msgpack(f)
    return df


def analyze_options_data():
  df = load_df_from_file()
  find_covered_calls(df)


def main(argv):
  analyze_options_data()


if __name__ == "__main__":
  pd.options.display.max_columns = 20
  tf.flags.mark_flag_as_required('pandas_msg_pack_file')
  tf.app.run()
