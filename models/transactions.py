import datetime

from sqlalchemy import (
    Column, Float, String,
    DateTime, UniqueConstraint
)

from models import db


class Transactions(db.Model):
    """
    Transactions
    """
    __tablename__ = 'transactions'
    __table_args__ = (
        UniqueConstraint('transaction_id'),
        {'mysql_engine': 'InnoDB'}
    )

    transaction_id = Column(String(256), primary_key=True)
    order_id = Column(String(256), nullable=False)
    product_name = Column(String(2000), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    register_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    @property
    def serialize(self):
        return {
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'product_name': self.product_name,
            'amount': self.amount,
            'currency': self.currency,
            'register_date': self.register_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
