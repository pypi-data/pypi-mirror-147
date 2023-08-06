# Written by Gabe Banks 2022 <https://gabebanks.net>

import os
import sys
import random
import requests
import numpy as np
from .parse import *

def translate(x: float, l1: float, h1: float, l2: float, h2: float) -> float:
    """
    Translate from one range to another.
    
        Parameters:
            x (float) - number to translate in range 1.
            l1 (float) - lower bound of range 1.
            h1 (float) - upper bound of range 1.
            l2 (float) - lower bound of range 2.
            h2 (float) - upper bound of range 2.

        Returns:
            y (float) - x mapped to range 2.
    """
    try:
        return (((x - l1) / (h1 - l1)) * (h2 - l2)) + l2
    except ZeroDivisionError:
        print("Error: Price in this timeframe has not changed by more than $0.00001. This is more specific than the API can keep track.")
        sys.exit(1)


def get_api_key() -> str:
    """Gets the API key from the environment variable ALPHAVANTAGE_API_KEY, raises an error if not found."""
    if os.getenv('ALPHAVANTAGE_API_KEY') == None:
        print("error: API key not detected! Follow these instructions to get your API Key working:\n" + \
        "- Make a free AlphaVantage API account at https://www.alphavantage.co/support/#api-key\n" + \
        "- After creating the account, you will see your free API key\n" + \
        "- Run \"export ALPHAVANTAGE_API_KEY=<your access key>\"." + \
        "You can make this permanent by adding this line to your .bashrc\n")
        sys.exit(1)
    else:
        return os.getenv('ALPHAVANTAGE_API_KEY')


def print_search(opts: dict):
    """Full script for the -s option."""
    ticker = opts["ticker"]
    apikey = get_api_key()
    verbose = opts["verbose"]
    request_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={apikey}'
    if verbose:
        print(f"API Key: {apikey}\nRequest URL: {request_url}")

    # Try to make a HTTP request. If this fails, there is probably no internet.
    try:
        r = requests.get(request_url).json()
    except:
        print("An error occured while making an HTTP request. Are you connected to the internet?")
        sys.exit(1)
    # If the API responds with 'Error Message', report it and exit.
    if 'Error Message' in list(r.keys()):
        print(f"error: The API returned the following error:\n{r}")
        sys.exit(1)
    # Try to parse the incoming JSON data. If it fails, then the API does that weird thing where it returns an empty JSON object {}
    try:
        data = list(r.values())[0]
    except IndexError:
        print("Error: The API did not return data.")
        sys.exit(1)
    
    print("The search returned the following results:")
    for i in data:
        print(f"\x1b[35;1m{i['1. symbol']} \x1b[32;1m({i['2. name']})\x1b[0m")
        print(f"\tReigon:\t\t\x1b[36m{i['4. region']}\x1b[0m")
        print(f"\tType:\t\t\x1b[36m{i['3. type']}\x1b[0m")
        print(f"\tCurrency:\t\x1b[36m{i['8. currency']}\x1b[0m")


def print_short(opts: dict):
    """Full script for the --short option."""
    ticker = opts["ticker"]
    asset_class = opts["asset_class"]
    apikey = get_api_key()
    verbose = opts["verbose"]
    currency = opts["currency"]
    currency_symbol = opts["currency_symbol"]
    
    # Vary request url depending on the asset class
    if asset_class == "stock":
        request_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={apikey}'

    elif asset_class == "crypto":
        request_url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={ticker}&apikey={apikey}&to_currency={currency}'

    elif asset_class == "forex":
        ticker = ticker.split("/")
        from_currency = ticker[0]
        to_currency = ticker[1]
        request_url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={apikey}'
    if verbose:
        print(f"API Key: {apikey}\nRequest URL: {request_url}")

    # Try to make a HTTP request. If this fails, there is probably no internet.
    try:
        r = requests.get(request_url).json()
    except:
        print("An error occured while making an HTTP request. Are you connected to the internet?")
        sys.exit(1)
    # If the API responds with 'Error Message', report it and exit.
    if 'Error Message' in list(r.keys()):
        print(f"error: The API returned the following error:\n{r}")
        sys.exit(1)
    # Try to parse the incoming JSON data. If it fails, then the API does that weird thing where it returns an empty JSON object {}
    try:
        data = list(r.values())[0]
    except IndexError:
        print("Error: The API did not return data.")
        sys.exit(1)
    if not bool(data):
        print("Error: The API did not return data.")
        sys.exit(1)
    
    # Output the data. Stocks pretty much never matter on the interval of below one penny, but crypto and forex can
    if asset_class == "stock":
        print(currency_symbol + "{:,.2f}".format(float(data["05. price"])))
    elif asset_class == "crypto" or asset_class == "forex":
        price = float(data["5. Exchange Rate"])
        if price < 0.01:
            print(currency_symbol + "{:,.5f}".format(price))
        else:
            print(currency_symbol + "{:,.2f}".format(price))


def get_request_url(opts: dict):
    """Generates an API request URL based off of options."""
    interval = opts["interval"]
    ticker = opts["ticker"]
    asset_class = opts["asset_class"]
    intervals_back = opts['intervals_back']
    apikey = get_api_key()
    full = "full" if intervals_back > 100 else "compact"
    intraday = 'min' in interval
    verbose = opts["verbose"]
    currency = opts["currency"]
    
    # Builds different request_urls corresponding to the endpoints of the API, depending on which asset class is specified.
    if asset_class == "stock":
        if interval == 'day':
            api_function = 'TIME_SERIES_DAILY'
        elif interval == 'week':
            api_function = 'TIME_SERIES_WEEKLY'
        elif interval == 'month':
            api_function = 'TIME_SERIES_MONTHLY'
        elif intraday:
            api_function = 'TIME_SERIES_INTRADAY'
    
        request_url = f'https://www.alphavantage.co/query?function={api_function}&symbol={ticker}&apikey={apikey}&outputsize={full}'

        if intraday:
            request_url += f"&interval={interval}"

    elif asset_class == "crypto":
        if interval == 'day':
            api_function = 'DIGITAL_CURRENCY_DAILY'
        elif interval == 'week':
            api_function = 'DIGITAL_CURRENCY_WEEKLY'
        elif interval == 'month':
            api_function = 'DIGITAL_CURRENCY_MONTHLY'
        elif intraday:
            api_function = 'CRYPTO_INTRADAY'
        request_url = f'https://www.alphavantage.co/query?function={api_function}&symbol={ticker}&apikey={apikey}&market={currency}'
        if intraday:
            request_url += f"&interval={interval}&outputsize={full}"

    elif asset_class == "forex":
        ticker = ticker.split("/")
        from_currency = ticker[0]
        to_currency = ticker[1]
        if interval == 'day':
            api_function = 'FX_DAILY'
        elif interval == 'week':
            api_function = 'FX_WEEKLY'
        elif interval == 'month':
            api_function = 'FX_MONTHLY'
        elif intraday:
            api_function = 'FX_INTRADAY'
        request_url = f'https://www.alphavantage.co/query?function={api_function}&from_symbol={from_currency}&to_symbol={to_currency}&apikey={apikey}'
        if interval == 'day' or intraday:
            request_url += f"&outputsize={full}"
        if intraday:
            request_url += f"&interval={interval}"

    if verbose:
        print(f"API Key: {apikey}\nRequest URL: {request_url}")
    return request_url

# It would be nice if when the candlesticks are drawn, additional detail could be had by utilizing quarter-blocks and eighth-blocks.
# Not sure if this is possible though.
def get_candlesticks(opts: dict) -> list:
    """Creates a list of candlesticks of the shape [O, H, L, C, D]."""
    interval = opts["interval"]
    intervals_back = opts['intervals_back']
    asset_class = opts['asset_class']
    intraday = 'min' in interval

    # Try to send HTTP request
    request_url = get_request_url(opts)
    try:
        r = requests.get(request_url).json()
    except:
        print("An error occured while making an HTTP request. Are you connected to the internet?")
        sys.exit(1)
    if 'Error Message' in list(r.keys()):
        print(f"error: The API returned the following error:\n{r}")
        sys.exit(1)

    try:
        data = list(r.values())[1]
    except IndexError:
        print("Error: The API did not return data.")
        sys.exit(1)

    # Parse API data
    candlesticks = []
    if asset_class == "stock":
        for k, v in data.items():
            candlesticks.append([
                float(v['1. open']),
                float(v['2. high']),
                float(v['3. low']),
                float(v['4. close']), -1
            ])
            if interval in ['day', 'week']:
                candlesticks[-1][4] = int(k[8:])
            elif interval == 'month':
                candlesticks[-1][4] = int(k[5:7])
            elif interval in ['1min', '5min']:
                candlesticks[-1][4] = int(k[14:16])
            elif interval in ['15min', '30min', '60min']:
                candlesticks[-1][4] = int(k[11:13])
            if len(candlesticks) == intervals_back:
                break
    elif asset_class == "crypto":
        for k, v in data.items():
            prices = [ float(price) for name, price in v.items() ]
            if intraday:
                candlesticks.append([
                    float(prices[0]),
                    float(prices[1]),
                    float(prices[2]),
                    float(prices[3]), -1
                ])
            else:
                candlesticks.append([
                    float(prices[0]),
                    float(prices[2]),
                    float(prices[4]),
                    float(prices[6]), -1
                ])
            if interval in ['day', 'week']:
                candlesticks[-1][4] = int(k[8:])
            elif interval == 'month':
                candlesticks[-1][4] = int(k[5:7])
            elif interval in ['1min', '5min']:
                candlesticks[-1][4] = int(k[14:16])
            elif interval in ['15min', '30min', '60min']:
                candlesticks[-1][4] = int(k[11:13])
            if len(candlesticks) == intervals_back:
                break
    elif asset_class == "forex":
        for k, v in data.items():
            prices = [ float(price) for name, price in v.items() ]
            candlesticks.append([
                float(prices[0]),
                float(prices[1]),
                float(prices[2]),
                float(prices[3]), -1
            ])
            if interval in ['day', 'week']:
                candlesticks[-1][4] = int(k[8:])
            elif interval == 'month':
                candlesticks[-1][4] = int(k[5:7])
            elif interval in ['1min', '5min']:
                candlesticks[-1][4] = int(k[14:16])
            elif interval in ['15min', '30min', '60min']:
                candlesticks[-1][4] = int(k[11:13])
            if len(candlesticks) == intervals_back:
                break

    candlesticks = list(reversed(candlesticks))

    return candlesticks


def draw_graph(opts: dict):
    """Main tstock script body."""

    if opts['short']:
        print_short(opts)
        return(0)

    if opts['search']:
        print_search(opts)
        return(0)

    ticker = opts["ticker"]
    interval = opts["interval"]
    intervals_back = opts["intervals_back"]
    max_y = opts["max_y"]
    pad_x = opts["pad_x"]
    pad_y = opts["pad_y"]
    wisdom = opts["wisdom"]
    chart_only = opts["chart_only"]
    currency_symbol = opts['currency_symbol']
    intraday = 'min' in interval
    candlesticks = get_candlesticks(opts)
    nocolor = opts["nocolor"]
    upcolor = opts["upcolor"]
    downcolor = opts["downcolor"]

    ANSI_colors = {"green" : "\x1b[32m",
                    "red" : "\x1b[31m",
                    "blue" : "\x1b[34m"}

    max_x = len(candlesticks) + pad_x * 2 + 2

    # Create the chart
    chart = np.full((max_y, max_x), " ")
    column_colors = ["\x1b[0m" for x in range(max_x)]  # Stores ANSI escape sequences for printing color
    # Draw borders
    chart[0, :] = "─"
    chart[-1, :] = "─"
    chart[:, 0] = "│"
    chart[:, -1] = "│"
    chart[0, 0] = "┌"
    chart[0, -1] = "┐"
    chart[-1, 0] = "└"
    chart[-1, -1] = "┘"

    spacer = "x" if intraday else " "
    # Draw graph title, if there are there enough worth of data to contain it
    title = f"┤  {intervals_back}{spacer}{interval.capitalize()} Price for ${ticker.upper()}  ├"
    if max_x >= len(title) + 2:
        for i, c in enumerate(title):
            chart[0, i + 1] = c
    # Find all time high and all time low
    ath = 0
    atl = 99999999
    for c in candlesticks:
        if c[1] > ath:
            ath = c[1]
        if c[2] < atl:
            atl = c[2]
    extra_decimals = ath - atl < 0.1
    # Draw candlesticks
    start_i = 1 + pad_x
    end_i = max_x - 1 - pad_x
    y_axis_low = pad_y
    y_axis_high = max_y - pad_y
    for i, c in enumerate(candlesticks):
        shifted_i = i + start_i
        # Stuff gets a little confusing here because the graph has to be y-inverted. "high" is referring to a high price, but needs to be flipped to a low index.
        translated_open = int(
            translate(c[0], atl, ath, y_axis_high, y_axis_low))
        translated_high = int(
            translate(c[1], atl, ath, y_axis_high, y_axis_low))
        translated_low = int(translate(c[2], atl, ath, y_axis_high,
                                       y_axis_low))
        translated_close = int(
            translate(c[3], atl, ath, y_axis_high, y_axis_low))
        # Draw high/low
        for y in range(translated_high, translated_low + 1):
            chart[y, shifted_i] = "│"
        # Draw open/close
        # Positive day, stock went up
        if c[0] < c[3]:
            column_colors[shifted_i] = ANSI_colors[upcolor]
            tmp = translated_low
            translated_low = translated_high
            translated_high = tmp
            for y in range(translated_close, translated_open + 1):
                chart[y, shifted_i] = "█"
        # Negative day, stock went down
        else:
            column_colors[shifted_i] = ANSI_colors[downcolor]
            for y in range(translated_open, translated_close + 1):
                chart[y, shifted_i] = "█"

    # Setup x-axis labels
    x_axis_labels = " " * (1 + pad_x)
    for i in range(start_i, end_i):
        shifted_i = i - start_i
        if (shifted_i) % 5 == 0:
            chart[-1, i] = "┼"
            if int(candlesticks[shifted_i][4]) >= 10:
                x_axis_labels += f"{candlesticks[shifted_i][4]}   "
            else:
                x_axis_labels += f"{int(candlesticks[shifted_i][4])}    "
    x_axis_labels += " " * (max_x - len(x_axis_labels))

    # Setup y-axis labels
    y_axis_labels = []
    if extra_decimals:
        margin = len( currency_symbol + "{:,.5f}".format(ath))
    else:
        margin = len( currency_symbol + "{:,.2f}".format(ath))
    for i in range(max_y):
        if i >= y_axis_low and i <= y_axis_high:
            shifted_i = y_axis_high - i
            if shifted_i % 4 == 0:
                chart[i, 0] = "┼"
                if extra_decimals:
                    label = currency_symbol + "{:,.5f}".format(translate(shifted_i, y_axis_low, y_axis_high, atl, ath))
                else:
                    label = currency_symbol + "{:,.2f}".format(translate(shifted_i, y_axis_low, y_axis_high, atl, ath))
                y_axis_labels.append(" " * (margin - len(label)) + f"{label}")
            else:
                y_axis_labels.append(" " * margin)
        else:
            y_axis_labels.append(" " * margin)

    # Print out the chart
    for y, row in enumerate(chart):
        out = ""
        out += y_axis_labels[y]
        for x, char in enumerate(row):
            if y >= y_axis_low and y <= y_axis_high and not nocolor:
                out += column_colors[x]
            out += char
        print(out)
    # Print x axis labels
    print(y_axis_labels[0] + x_axis_labels)
    if interval in ['day', 'week']:
        x_axis_title = "Day"
    elif interval == 'month':
        x_axis_title = "Month"
    elif interval in ['1min', '5min']:
        x_axis_title = "Minute"
    elif interval in ['15min', '30min', '60min']:
        x_axis_title = "Hour"
    print(y_axis_labels[0] + " " * int((len(x_axis_labels)-len(x_axis_title)) / 2) + x_axis_title)
    print()

    if not chart_only:
        #Print additional info
        if extra_decimals:
            label = currency_symbol + "{:,.5f}".format(candlesticks[-1][3])
        else:
            label = currency_symbol + "{:,.2f}".format(candlesticks[-1][3])
        print("Last price:\t" + label)
        print(
            f"% change:\t{round(100*(candlesticks[-1][3]-candlesticks[0][0])/candlesticks[0][3],2)}%"
        )
        if wisdom:
            if candlesticks[-1][3] > candlesticks[0][0]:
                print(
                    random.choice([
                        f"${ticker.upper()} to the moon! 🚀🚀🚀",
                        "Apes alone weak. Apes together strong 🦍🦍🦍",
                        f"${ticker.upper()} primary bull thesis: I like the stock. 🚀🚀🚀",
                        "Stocks can only go down 100% but can go up infinite %. Stocks can literally only go up. Q.E.D. 📈📈📈",
                    ]))
            else:
                print(
                    random.choice([
                        "Losses aren't real 'till you sell 💎🙌",
                        "Literally cannot go tits up 💎🙌",
                        "GUH.",
                        "Short squeeze any time now 💎🙌",
                        "Are you sufficiently leveraged for your Personal Risk Tolerance?",
                    ]))


def main():
    parser = get_args()
    parse_args_exit(parser)

    opts = parse_args(parser)
    draw_graph(opts)