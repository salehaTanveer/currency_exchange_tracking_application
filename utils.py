from models import ExchangeRate


def get_rate_and_currency():
    exchange_rates = ExchangeRate.query.with_entities(ExchangeRate.id, ExchangeRate.new_rate).all()
    return [{"id": exchange_rate.id, "old_rate": exchange_rate.new_rate} for exchange_rate in exchange_rates]
