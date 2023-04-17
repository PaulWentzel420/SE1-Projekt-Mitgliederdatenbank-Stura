from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasUser


class TestUser(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    # Tests
    def test_login_user(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can login as User and all sites are displayed correctly.
            But that you can not reach Admin-only content.
        """
        # Login as User
        loginAsLukasUser(self)

        """
            TODO: Check ob es ein User ist.
        """
        pass
