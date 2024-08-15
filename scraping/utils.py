# scraping/utils.py
from decimal import Decimal

def calculate_difference(old_data, new_data):
    price_diff = ((new_data.price - old_data.price) / old_data.price) * 100
    stock_diff = ((new_data.stock - old_data.stock) / old_data.stock) * 100 if old_data.stock != 0 else 0
    
    from difflib import SequenceMatcher
    description_similarity = SequenceMatcher(None, old_data.description, new_data.description).ratio() * 100
    description_diff = 100 - description_similarity

    return {
        'price_diff': round(price_diff, 2),
        'stock_diff': round(stock_diff, 2),
        'description_diff': round(description_diff, 2)
    }