import tensorflow as tf
import datetime
import math
import re
import os
import json
import pandas as pd

log = tf.logging
FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string(
    "pandas_msg_pack_file", None,
    "Serialized msgpack DataFrame for the current options data.")

todays_date = datetime.date.today()

def find_covered_calls(df):
  sorted_df = df.sort_values(by=["loan_apr"], ascending=False)
  print(sorted_df.head(30))


def load_df_from_file():
  full_path = os.path.abspath(FLAGS.pandas_msg_pack_file)
  with open(full_path, 'r') as f:
    df = pd.read_msgpack(f)
    return df


# Generates some extra columns for the DF that provide useful transformations.
def post_process_df(original_df):
  # Filter out no open interest options
  df = original_df[original_df["open_ints"] > 100]

  def duration_func(row):
    return (row["expiration_date"].to_pydatetime().date() - todays_date).days
  df["days_til_expiry"] = df.apply(duration_func, axis=1)

  def bid_premium_func(row):
    if row["is_call"]:
      intrinsic_value = max(0, row["underlying_price"] - row["strike"])
      return row["bid"] - intrinsic_value
    intrinsic_value = max(0, row["strike"] - row["underlying_price"])
    return row["bid"] - intrinsic_value
  df["bid_premium"] = df.apply(bid_premium_func, axis=1)
  def ask_premium_func(row):
    if row["is_call"]:
      intrinsic_value = max(0, row["underlying_price"] - row["strike"])
      return row["ask"] - intrinsic_value
    intrinsic_value = max(0, row["strike"] - row["underlying_price"])
    return row["ask"] - intrinsic_value
  df["ask_premium"] = df.apply(ask_premium_func, axis=1)

  def loan_amount_func(row):
    return row["underlying_price"] - (row["ask"] - row["ask_premium"])
  df["loan_amount"] = df.apply(loan_amount_func, axis=1)

  def loan_apr_func(row):
    percentage_cost = row["ask_premium"] / row["loan_amount"]
    return percentage_cost * (365.0 / row["days_til_expiry"])
  df["loan_apr"] = df.apply(loan_apr_func, axis=1)
  return df


def analyze_options_data():
  df = load_df_from_file()
  df = post_process_df(df)
  find_covered_calls(df)


def main(argv):
  analyze_options_data()


if __name__ == "__main__":
  pd.options.display.max_columns = 20
  tf.flags.mark_flag_as_required('pandas_msg_pack_file')
  tf.app.run()
