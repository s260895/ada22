from flask import jsonify


def rule_evaluator(request):
    """Evaluates the rules for a set of stocks.
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

    signals = list()

    for stock in stocks:
        # Check if there are enough prices to compute signal
        if len(list(stock["prices"])) != 4:
            return f"Signal cannot be computed from {len(list(stock['prices']))} prices."

        # Convert stock prices to floats
        closes = [float(price) for price in stock["prices"]]

        # Compute signal (permissible values 1,-1,0)
        lower_bound = (sum(closes[:3]) / len(closes[:3])) * 0.99995
        upper_bound = (sum(closes[:3]) / len(closes[:3])) * 1.00005
        signal = -1 if closes[-1] <= lower_bound else 0 if closes[-1] < upper_bound else 1
        signals.append({"stock_id": stock["_id"], "signal": signal})

    return jsonify(signals)
