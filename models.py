from typing import List

from manage import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import insert


class ExchangeRate(db.Model):
    __tablename__ = "exchange_rates"

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(255), nullable=False)
    currency_abr = db.Column(db.String(20), nullable=False, unique=True)
    new_rate = db.Column(db.Float(10), nullable=False)
    old_rate = db.Column(db.Float(10), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, currency, currency_abr, new_rate):
        self.currency = currency
        self.currency_abr = currency_abr
        self.new_rate = new_rate

    def to_json(self):
        return {
            "id": self.id,
            "currency": self.currency,
            "currency_abr": self.currency_abr,
            "rate": self.new_rate,
            "created_at": self.created_at,
            "updated": self.updated,
        }

    def to_json_comparison(self):
        return {
            "currency": self.currency,
            "currency_abr": self.currency_abr,
            "rate_today": self.new_rate,
            "rate_yesterday": self.old_rate,
            "updated": self.updated,
        }

    @staticmethod
    def bulk_update():
        from utils import get_rate_and_currency

        currency_id_rate_mapping = get_rate_and_currency()
        db.session.bulk_update_mappings(ExchangeRate, currency_id_rate_mapping)
        db.session.commit()

    @staticmethod
    def upsert(exchange_rate: List):
        ExchangeRate.bulk_update()
        stmt = insert(ExchangeRate).values(exchange_rate)
        stmt = stmt.on_conflict_do_update(
            constraint="exchange_rates_currency_abr_key",
            set_={
                "currency": stmt.excluded.currency,
                "currency_abr": stmt.excluded.currency_abr,
                "new_rate": stmt.excluded.new_rate,
                "updated": func.now(),
            }
        )
        db.session.execute(stmt)
        db.session.commit()
