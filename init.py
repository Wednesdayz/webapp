from routes import app
from model import Customer, connect_to_db, db

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()