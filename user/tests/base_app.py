from unittest import TestCase
from mongoengine.connection import _get_db

from user.models import User
from user.tests.base_data import USER_DATA_DICT
from app import create_app as _create_app_base


class SetUpTest(TestCase):

    def create_app_base(self):
        """Creates the basic setup needed for the application"""
        db_name = "social_network"

        return _create_app_base(
            MONGODB={"DB": db_name},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="SECRET_TESTING_KEY",
        )

    def setUp(self):
        """Creates the setup necessary for the database"""
        self.app_factory = self.create_app_base()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        """Tears the application by deleting all the data in database"""
        db = _get_db()
        db.connection.drop_database(db)

    def register_data(self, register_data=USER_DATA_DICT):
        """Gets the user registration details"""
        return self.app.post("/register", data=register_data, follow_redirects=True)

    def login(self, email=USER_DATA_DICT.get("email"), password=USER_DATA_DICT.get("password")):
        """"""
        self._confirm_email()
        return self.app.post("/login", data=dict(email=email, password=password))

    def get_app(self):
        return self.app

    def _confirm_email(self):
        """After the user has registered with the application. In order for the application to work the
           user needs to verify their email address. This method fakes that email address verification.
        """
        user = User.objects.filter(username=USER_DATA_DICT['username']).first()
        user.email_confirmed = True
        user.save()
