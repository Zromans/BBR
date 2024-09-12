from decimal import Decimal
from difflib import SequenceMatcher

def calculate_difference(old_data, new_data):
    differences = {}

    # Calculate price difference
    if old_data.price != new_data.price:
        price_diff = ((new_data.price - old_data.price) / old_data.price) * 100
        differences['price'] = {
            'old': str(old_data.price),
            'new': str(new_data.price),
            'diff': round(price_diff, 2)
        }

    # Calculate description difference
    if old_data.includes != new_data.includes:
        description_similarity = SequenceMatcher(None, old_data.includes, new_data.includes).ratio() * 100
        description_diff = 100 - description_similarity
        differences['description'] = {
            'old': old_data.includes,
            'new': new_data.includes,
            'diff': round(description_diff, 2)
        }

    # Calculate fitments difference
    if old_data.fitments != new_data.fitments:
        differences['fitments'] = {
            'old': old_data.fitments,
            'new': new_data.fitments
        }

    # Calculate brand difference
    if old_data.brand != new_data.brand:
        differences['brand'] = {
            'old': old_data.brand,
            'new': new_data.brand
        }

    # Calculate manufacturer_part_number difference
    if old_data.manufacturer_part_number != new_data.manufacturer_part_number:
        differences['manufacturer_part_number'] = {
            'old': old_data.manufacturer_part_number,
            'new': new_data.manufacturer_part_number
        }

    return differences
