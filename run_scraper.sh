set -e
PWD=$(pwd)
TIMESTAMP=$(date +%s)
JSON_FILENAME=$PWD/data/option_prices_$TIMESTAMP.json
PANDAS_FILENAME=$PWD/data/option_prices_$TIMESTAMP.msgpack
echo $TIMESTAMP
scrapy runspider scrape.py -o $JSON_FILENAME
echo $JSON_FILENAME
rm $PWD/data/option_prices_latest.json
ln -s $JSON_FILENAME $PWD/data/option_prices_latest.json
echo "Converting to pandas."
bazel run -- :convert_to_pandas --json_option_price_file=$JSON_FILENAME \
    --output_pandas_msg_pack_file=$PANDAS_FILENAME
rm $PWD/data/option_prices_latest.msgpack
ln -s $PANDAS_FILENAME $PWD/data/option_prices_latest.msgpack
echo $PANDAS_FILENAME
bazel run -- :analyze_options_data --pandas_msg_pack_file=$PANDAS_FILENAME --output_df_csv=/tmp/analyze_options_data_out.csv
