import scrapy
import re
import json
import pprint

BASE_URL = "https://finance.yahoo.com/quote/{underlying}/options"
DATED_URL = "https://finance.yahoo.com/quote/{underlying}/options?date={option_date}"
STOCKS = ["OEX.X", "AAPL", "TWTR", "CSCO", "CHGG", "GRUB", "AMZN", "SPY", "GOOG", "GS", "BAC", "BA", "C", "CAT"]
# STOCKS = ["AAPL"]

def extract_dict(body, start_pos):
  bracket_itr = re.finditer("[{}]", body[start_pos:])
  match_beg = None
  match_end = None
  bracket_count = 0
  for m in bracket_itr:
    if (m.group(0) == "{"):
      if match_beg == None:
        match_beg = m.span()[0]
      bracket_count += 1
      continue
    bracket_count -= 1
    if bracket_count == 0:
      match_end = m.span()[1]
      break
  return body[start_pos + match_beg:start_pos + match_end]

def find_key(d, key):
  if key in d:
    return [key]
  ret = []
  for (k,v) in d.items():
    if type(v) != dict:
      continue
    rec = find_key(v,key)
    if rec:
      ret.extend([k + ":" + r for r in rec])
  return ret

class OptionsScraper(scrapy.Spider):
  name = "options_scraper"
  start_urls = [BASE_URL.format(underlying=s) for s in STOCKS]

  def parse(self, response):
    underlying_name = response.css("h1.D\(ib\)::text").extract_first()
    stock_name = underlying_name.split(" ")[0]
    contract_names = response.css(".data-col0 a::text").extract()
    strikes = [float(x.replace(",","")) for x in response.css(".data-col2 a::text").extract()]
    last_prices = [float(x.replace(",","")) for x in response.css(".data-col3::text").extract()]
    bids = [float(x.replace(",","")) for x in response.css(".data-col4::text").extract()]
    asks = [float(x.replace(",","")) for x in response.css(".data-col5::text").extract()]
    volumes = [int(x.replace(",","")) for x in response.css(".data-col8::text").extract()]
    open_ints = [int(x.replace(",","")) for x in response.css(".data-col9::text").extract()]
    ivs = [float(x.replace(",","")[0:-1]) for x in response.css(".data-col10::text").extract()]
    expiration_match = re.search( "\"expirationDates\":(\[[\w,]+\])", response.body)
    actual_price = re.findall( "\"regularMarketPrice\":(\{[^}]+\})", response.body)
    data_dict_beg = re.search("root.App.main ", response.body).span()[1]
    dict_string = extract_dict(response.body, data_dict_beg)
    data_dict = json.loads(dict_string)
    underlying_price = float(
        data_dict["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
          ["price"]["regularMarketPrice"]["raw"])

    if expiration_match:
      expiration_dates = json.loads(expiration_match.group(1))

    for exp_date in expiration_dates:
      yield scrapy.Request(DATED_URL.format(underlying=stock_name, option_date=exp_date))

    yield {
      "underlying_name": underlying_name,
      "stock_name": stock_name,
      "contract_names": contract_names,
      "strikes": strikes,
      "last_prices": last_prices,
      "bids": bids,
      "asks": asks,
      "volumes": volumes,
      "open_ints": open_ints,
      "ivs": ivs,
      "underlying_price": underlying_price
    }
