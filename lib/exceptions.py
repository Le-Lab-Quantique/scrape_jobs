class NoLLQJWTTokenException(Exception):
    """
    Raised when we cannot get JWT token wit LLQ REST API
    """

    pass


class PostJobToLLQException(Exception):
    """
    Raise when we cannot post a job in LLQ website via REST API
    """
