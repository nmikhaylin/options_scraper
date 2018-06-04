py_binary(
  name = "convert_to_pandas",
  srcs = ["convert_to_pandas.py"],
  data = [":option_price_data"],
  deps = []
)

py_binary(
  name = "analyze_options_data",
  srcs = ["analyze_options_data.py"],
  data = [":option_price_data"],
  deps = []
)

py_test(
  name = "analyze_options_data_test",
  srcs = ["analyze_options_data_test.py"],
  deps = [":analyze_options_data"]
)

py_library(
  name = "scrape",
  srcs = ["scrape.py"],
  deps = []
)

filegroup(
  name = "option_price_data",
  srcs = glob(["data/*"])
)

py_test(
  name = "scrape_test",
  srcs = ["scrape_test.py"],
  deps = [":scrape",]
)
