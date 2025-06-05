import pandas as pd
import random
import time

def generate_order_data(num_orders):
    data = {
        'order_id': [i for i in range(1, num_orders + 1)],
        'timestamp': [time.time() + i for i in range(num_orders)],
        'symbol': [random.choice(['AAPL', 'GOOG', 'MSFT', 'AMZN']) for _ in range(num_orders)],
        'quantity': [random.randint(1, 1000) for _ in range(num_orders)],
        'price': [random.uniform(100, 500) for _ in range(num_orders)],
        'side': [random.choice(['buy', 'sell']) for _ in range(num_orders)]
    }
    return pd.DataFrame(data)
