from user.models import User
from user.tests.base_data import USER_DATA_DICT
from user.tests.base_app import SetUpTest


class ConfirmationTest(SetUpTest):

    def test_if_user_is_able_to_confirm_code_after_registering__Should_return_true(self):
        self._enter_site()

        user = User.objects.get(username=USER_DATA_DICT['username'])
        code = user.change_configuration.get("confirmation_code")

        rv = self._get_confirmation_url(user, code)

        assert "Your email address has been confirmed" in str(rv.data)

        # try to confirm again should return a 404 because the user has already confirmed
        rv = self._get_confirmation_url(user, code)
        assert rv.status_code == 404

        # # Check if the code in the configuration object has been reset to empty dict
        # assert user.change_configuration.get("confirmation_code")

    def _enter_site(self):
        self.register_data()
        self.login()

    def _get_confirmation_url(self, user, code):
        return self.app.get("/confirm/" + user.username + "/" + code)