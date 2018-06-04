import tensorflow as tf
import datetime
import re
import json
import pandas as pd

log = tf.logging
FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string(
    "json_option_price_file", None, "File that contains current option price data"
    " as JSON.")
tf.flags.DEFINE_string(
    "output_pandas_msg_pack_file", None, "File that the serialized msgpack of "
    "the pandas options data.")

cur_time = datetime.date.today()

def generate_data_frame(option_prices):
  regex = re.compile("(\d{6})([PC])")
  underlying_names = []
  underlying_prices = []
  bids = []
  asks = []
  last_prices = []
  ivs = []
  volumes = []
  expiration_dates = []
  strikes = []
  is_calls = []

  for option in option_prices:
    num_contracts = len(option["contract_names"])
    if not num_contracts:
      continue
    underlying_names.extend([option["underlying_name"]] * num_contracts)
    underlying_prices.extend([option["underlying_price"]] * num_contracts)
    bids.extend(option["bids"])
    asks.extend(option["asks"])
    last_prices.extend(option["last_prices"])
    strikes.extend(option["strikes"])
    ivs.extend(option["ivs"])
    volumes.extend(option["volumes"])
    # Assume the expiration is always the same.
    for contract_name in option["contract_names"]:
      match = regex.search(contract_name)
      expiration_date = datetime.datetime.strptime(match.group(1), "%y%m%d")
      expiration_dates.append(expiration_date)
      is_calls.append(True if (match.group(2) == "C") else False)
  assert(len(underlying_names) == len(underlying_prices))
  assert(len(underlying_names) == len(bids))
  assert(len(underlying_names) == len(asks))
  assert(len(underlying_names) == len(last_prices))
  assert(len(underlying_names) == len(ivs))
  assert(len(underlying_names) == len(volumes))
  assert(len(underlying_names) == len(expiration_dates))
  assert(len(underlying_names) == len(strikes))
  assert(len(underlying_names) == len(is_calls))
  df = pd.DataFrame({
      "underlying_name": underlying_names,
      "underlying_price": underlying_prices,
      "bid": bids,
      "ask": asks,
      "last_price": last_prices,
      "iv": ivs,
      "volume": volumes,
      "expiration_date": expiration_dates,
      "strike": strikes,
      "is_call": is_calls
  })
  df.to_msgpack(FLAGS.output_pandas_msg_pack_file)
  print(df)

def main(argv):
  with open(FLAGS.json_option_price_file) as f:
    option_data = json.load(f)
  df = generate_data_frame(option_data)
  print(len(option_data))

if __name__ == "__main__":
  tf.flags.mark_flag_as_required('json_option_price_file')
  tf.flags.mark_flag_as_required('output_pandas_msg_pack_file')
  tf.app.run()
