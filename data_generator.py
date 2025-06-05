import pandas as pd
import random
import time

def generate_order_data(intensity=0.3):
    data = []
    for _ in range(1000):
        order = {
            "timestamp": time.time(),
            "instrument": random.choice(["AAPL", "GOOG", "MSFT"]),
            "side": random.choice(["buy", "sell"]),
            "price": random.uniform(100, 500),
            "quantity": random.randint(1, 1000),
            "BaseCcyQty": random.uniform(1000, 1000000),
            "BaseCcyLeavesQty": random.uniform(0, 1000000),
            "CumulativeQty": random.uniform(0, 1000000),
            "BaseCcyValue": random.uniform(1000, 1000000),
            "event_type": random.choice(["Filled", "Partially Filled", "TN", "TR"]),
            "venue": random.choice(["NYSE", "NASDAQ", "LSE"]),
            "trade_inclusion": random.choice([True, False]),
            "severity": random.choice(["Low", "Medium", "High"])
        }
        if random.random() < intensity:
            order["price"] = 450  # Example to match the price spike rule
        data.append(order)
    return pd.DataFrame(data)
