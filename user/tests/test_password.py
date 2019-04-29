from user.tests.base_app import SetUpTest
from user.models import User
from user.tests.base_data import USER_DATA_DICT
from utils.security.secure import Session


class PasswordTest(SetUpTest):

    def test_forgotten_password_link(self):

        self._enter_site()
        email = USER_DATA_DICT.get("email")

        rv = self.app.post("/forgotten/password", data=dict(email=email))

        user = User.objects.first()
        password_reset_code = user.change_configuration.get("password_reset_code")
        username = USER_DATA_DICT.get("username")

        assert password_reset_code is not None

        # try wrong username
        rv = self.app.get("/password/reset/username_does_exists/" + password_reset_code)
        assert rv.status_code == 404

        # try wrong password reset code
        rv = self.app.get("/password/reset/" + username + "/bad_code")
        assert rv.status_code == 404

        # do right password reset code
        rv = self.app.post("/password/reset/" + username + "/" + password_reset_code,
                           data=dict(password="newpassword", confirm="newpassword"), follow_redirects=True)

        assert "Your password has been updated" in str(rv.data)

        user = User.objects.first()
        assert user.change_configuration == {}

        # try logging in with new password
        rv = self.app.post("/login", data=dict(
            username=username,
            password="newpassword"
        ))

        # check the session is set
        with self.app as context:
            rv = context.get("/")
            assert Session.get_session_by_name("username").lower() == username.lower()

    # def test_if_user_can_change_password(self):
    #
    #     self._enter_site()
    #
    #     rv = self.app.post("/login", data=dict(username=USER_DATA_DICT.get("username"),
    #                                            password=USER_DATA_DICT.get("passsword")))
    #
    #     rv = self.app.post("/password/new", data=dict(
    #         current_password="newpassword",#USER_DATA_DICT.get("password"),
    #         password="newpassword",
    #         confirm="newpassword"
    #     ), follow_redirects=True)
    #
    #     rv = self.app.get("/password/changed_password_successful")
    #     assert "You have successfully changed your password" in str(rv.data)

    def _enter_site(self):

        self.register_data()
        self.login()
