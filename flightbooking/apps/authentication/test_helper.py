from faker import Faker

from django.urls import reverse

from flightbooking.apps.authentication.models import User

fake = Faker()
test_client = None


def set_test_client(client):
    """
    Set the test client used by your tests. This should be called in the
    setUp() method of your test class. It is not necessary for methods
    that don't require a test client.
    :param client: Client
    """
    global test_client
    test_client = client


def check_client():
    """
    Checks if the test client is set. If it is not it raises an exception
    indicating that the client is required.
    """
    if test_client is None:
        raise ValueError('A test client must be set to use this helper method.')


def login(user=None, verified=False, admin=False, overrides=None, return_field=None):
    """
    Logs in user and returns the User object. If a user object is not specified,
    one is randomly generated. The user object is force authenticated on the
    DRF API client. If the return_field is specified it returns the field
    instead of the entire user object. The verified, admin and overrides fields
    are only applied when a user object is not specified.
    :param admin: bool
    :param user: User
    :param overrides: dict
    :param return_field: str
    :param verified: bool
    :return: User
    """
    check_client()
    if user is None:
        user = create_user(verified=verified, admin=admin, overrides=overrides)

    # force authenticate
    test_client.force_authenticate(user)

    if return_field is not None:
        return getattr(user, return_field)

    return user


def logout():
    check_client()
    test_client.force_authenticate(None)


def create_user(verified=False, admin=False, overrides=None, return_field=None):
    """
    Creates and registers a random user. If verified is set to True the user will
    be verified. If admin is set to True the user will be a superuser. Overrides
    should be a dictionary that specifies fields to
    override from the auto-generated ones. If the return_field is
    specified it returns the field instead of the entire user
    object. This method triggers creation of the user profile.
    :param admin: bool
    :param return_field: str
    :param verified: bool
    :param overrides: dict
    :return: User
    """
    check_client()
    attributes = make_user(overrides)

    # register via api to ensure that the user profile is created
    test_client.post(reverse("authentication:user-register"), data={"user": attributes}, format="json")

    # get the model of the just created user
    user = User.objects.get(email=attributes['email'])
    user.is_verified = verified
    user.is_staff = admin
    user.save()

    if return_field is not None:
        return getattr(user, return_field)

    return user


def make_user(overrides=None):
    """
    Creates a dictionary containing random attributes of a user. Overrides
    should be a dictionary that specifies fields to override from
    the auto-generated ones.
    :param overrides: dict
    :return:
    """
    attributes = {
        'username': fake.profile()['username'],
        'email': fake.email(),
        'password': fake.password()
    }

    if overrides is not None:
        override_fields = overrides.keys()
        for field in ['username', 'email', 'password']:
            if field in override_fields:
                attributes[field] = overrides.get(field)

    return attributes
