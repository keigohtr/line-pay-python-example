from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(
    session_options={
        "autocommit": False,
        "autoflush": False
    }
)
db_url = 'sqlite:///db.sqlite3'


from models.transactions import Transactions
