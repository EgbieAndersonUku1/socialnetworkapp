from user.tests.base_app import SetUpTest
from user.models import User
from user.tests.base_data import USER_DATA_DICT


class UserRegistrationTest(SetUpTest):

    def test_register_user(self):
        """Test if the user can successful log into the application"""
        self.register_data()
        assert User.objects.filter(username="test_username").count() == 1

    def test_if_the_user_can_register_with_an_invalid_username__Should_return_an_invalid_username(self):
        """"""
        invalid_user_data = USER_DATA_DICT.copy()
        invalid_user_data["username"] = "username with username"

        rv = self.register_data(register_data=invalid_user_data)
        assert "Invalid username" in str(rv.data)

    def test_if_a_user_can_register_with_an_invalid_email__Should_return_an_invalid_email(self):
        """"""
        invalid_user_data = USER_DATA_DICT.copy()
        invalid_user_data["email"] = "invalid_email"

        rv = self.register_data(register_data=dict(invalid_user_data))
        assert "Invalid email" in str(rv.data)


