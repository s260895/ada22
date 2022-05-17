import ccxt
from flask import jsonify
from datetime import datetime


def price_fetcher(request):
    """Fetch the latest price for every stock.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a Response object using `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    content_type = request.headers["content-type"]
    if "application/json" in content_type:
        stocks = request.get_json(silent=True)
        if not stocks:
            raise ValueError("JSON is invalid.")
    else:
        raise ValueError(f"Invalid content type: {content_type}")

    # Parameters
    candles = 5
    interval = "5m"
    exchange = ccxt.binance({
        "apiKey": "INH9JYsd4Cu3kMPoONiCVHP3KlACsg3F4ehDN1cburoKohsARMpZGcq4PnQoqzyF",
        "secret": "FSVMXANswsGOj3B4Oi4NSDOlX5fsvWOJ3s56DQsWvJTjLhSuPyq1aFLbFEWoOrMt",
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
        "hedgeMode": True})
    last_incomplete_candle = False

    # Store the fetched Price Values and Datetimes
    for stock in stocks:
        if not last_incomplete_candle:
            closes = [
                [datetime.utcfromtimestamp(float(elem[0]) / 1000.), elem[4]]
                for elem in exchange.fapiPublic_get_klines({"symbol": stock["ticker"], "interval": interval})
            ][-candles:-1]
        if last_incomplete_candle:
            closes = [
                [datetime.utcfromtimestamp(float(elem[0]) / 1000.), elem[4]]
                for elem in exchange.fapiPublic_get_klines({"symbol": stock["ticker"], "interval": interval})
            ][-(candles - 1):]
        stock["prices"] = [float(elem[1]) for elem in closes]

    return jsonify(stocks)
