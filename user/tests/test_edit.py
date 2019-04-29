from user.models import User
from user.tests.base_data import USER_DATA_DICT
from user.tests.base_app import SetUpTest


class EditProfileTest(SetUpTest):

    def test_if_the_user_has_edit_button_in_their_profile_page__Should_return_true(self):
        """"""
        self._enter_site()
        rv = self.app.get("/" + USER_DATA_DICT.get("username").lower())
        assert "Edit profile" in str(rv.data)

    def test_if_the_user_can_edit_their_profile_page__Should_return_true(self):

        self._enter_site()

        user = USER_DATA_DICT.copy()
        user["first_name"] = "test_first_name_update"
        user["last_name"] = "test_last_name_update"
        user["username"] = "test_username_update"


        rv = self.app.post("/edit", data=user)

        assert "Profile updated" in str(rv.data)

        edited_user = User.objects.first()
        assert edited_user.username == "test_username_update"
        assert edited_user.first_name == "test_first_name_update"
        assert edited_user.last_name == "test_last_name_update"

    def _enter_site(self):
        self.register_data()
        self.login()

