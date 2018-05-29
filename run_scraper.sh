set -e
TIMESTAMP=$(date +%s)
JSON_FILENAME=data/option_prices_$TIMESTAMP.json
PANDAS_FILENAME=data/option_prices_$TIMESTAMP.msgpack
echo $TIMESTAMP
scrapy runspider scrape.py -o $JSON_FILENAME
echo $JSON_FILENAME
echo "Converting to pandas."
bazel run -- :convert_to_pandas --json_option_price_file=$JSON_FILENAME \
    --output_pandas_msg_pack_file=$PANDAS_FILENAME
echo $PANDAS_FILENAME
bazel run -- :analyze_options_data --pandas_msg_pack_file=$PANDAS_FILENAME
