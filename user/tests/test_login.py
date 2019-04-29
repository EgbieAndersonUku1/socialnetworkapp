from user.tests.base_data import USER_DATA_DICT
from utils.security.secure import Session
from user.tests.base_app import SetUpTest


class UserLoginTest(SetUpTest):

    def test_login_user(self):
        """test the application to check if the user can login"""

        self.register_data()
        self._confirm_email()
        self.login()

        with self.app as context:
            s = context.get("/")

            assert Session.get_session_by_name("username") == USER_DATA_DICT.get("username").lower()
