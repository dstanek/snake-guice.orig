
class User(object):
    """An object representing a user."""


class UserProvider(object):

    def get(self):
        return User()


class RequestData(object):
    """Some some data generated for each request."""


class RequestDataProvider(object):

    def get(self):
        return RequestData()
