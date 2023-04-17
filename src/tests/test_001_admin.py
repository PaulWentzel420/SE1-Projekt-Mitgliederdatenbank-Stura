from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin


class TestAdmin(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    # Tests
    def test_login_superuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can login as Admin and all sites are displayed correctly.
        """
        # login
        loginAsLukasAdmin(self)

        """
            TODO: Check ob es ein Admin ist.
        """
        pass
