
class Issue(object):
    def __init__(self, message, exception=None):
        self.message = message
        self.exception = exception

    def __str__(self):
        return self.message
