from user.tests.base_app import SetUpTest

from utils.security.secure import Session


from user.tests.base_data import USER_DATA_DICT
from user.models import User
from relationship.models import Relationship


class RelationshipTest(SetUpTest):

    def user2_dict(self):

        user2 = USER_DATA_DICT.copy()
        user2["first_name"] = "Username_test2"
        user2["email"] = "email@example.com"
        return user2

    def test_friends(self):

        rv = self.register_data()
        assert User.objects.filter(username=USER_DATA_DICT.get("username")).count() == 1

        rv = self.register_data(register_data=self.user2_dict())
        assert User.objects.filter(username=self.user2_dict().get("username")).count() == 1

        rv = self.login(email=USER_DATA_DICT.get("email"), password=USER_DATA_DICT.get("password"))

        rv = self.app.get("/friends/add/" + self.user2_dict().get("username"), follow_redirects=True)

        assert "relationship-friends-requested" in str(rv.data)

        rel_count = Relationship.ojects.count()
        assert rel_count

        rv = self.login(email=self.user2_dict().get("email"), password=self.user2_dict().get("password"))

        rv = self.app.get("/" + USER_DATA_DICT.get("username"))
        assert "relationship-reverse-friends-requested" in str(rv.data)







