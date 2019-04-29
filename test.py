import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

# from user.tests.test_registration import UserRegistrationTest
# from user.tests.test_login import UserLoginTest
# #from user.tests.test_edit import EditProfileTest
# from user.tests.test_confirmation import ConfirmationTest
# from user.tests.test_password import PasswordTest
from user.tests.test_relationship import RelationshipTest

if __name__ == "__main__":
    unittest.main()