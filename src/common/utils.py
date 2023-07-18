from sqlalchemy import Float

from src.models.exchange_rate_model import ExchangeRate


def get_rate_and_currency():
    exchange_rates = ExchangeRate.query.with_entities(ExchangeRate.id, ExchangeRate.new_rate).all()
    return [{"id": exchange_rate.id, "old_rate": exchange_rate.new_rate} for exchange_rate in exchange_rates]


def generate_comparison_comments(old_rate: Float, new_rate: Float):
    if old_rate > new_rate:
        return "The currency value has declined."
    elif old_rate < new_rate:
        return "The currency value has improved."
    else:
        return "There is no change in currency value."
