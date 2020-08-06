
class GraphQLException(Exception):
    """
    Base class for GraphQL exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    default_detail = "A server error occurred."
    default_code = "error"

    def __init__(self, detail=None, code=None):
        self.detail = detail
        if detail is None:
            self.detail = self.default_detail
        self.code = code
        if code is None:
            self.code = self.default_code

    def __str__(self):
        return str(self.detail)
