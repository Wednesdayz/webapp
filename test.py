from unittest import TestCase
import os
import sys

current = os.getcwd()
current = current.split("/")
current = "/".join(current[:-1])
sys.path.append(current)

from routes import app
from model import connect_to_db, db


class FlaskTests(TestCase):

    def setUp(self):
        """Before tests."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        print("connecting")
        connect_to_db(app, "postgresql:///Beyond")

        # Create tables and add sample data
        db.create_all()
    def tearDown(self):
        """For after test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    import unittest

    unittest.main()