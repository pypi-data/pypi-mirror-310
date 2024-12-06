class WebscoutE(Exception):
    """Base exception class for search."""


class RatelimitE(Exception):
    """Raised for rate limit exceeded errors during API requests."""

class ConversationLimitException(Exception):
    """Raised for conversation limit exceeded errors during API requests."""
    pass
class TimeoutE(Exception):
    """Raised for timeout errors during API requests."""
    
class FailedToGenerateResponseError(Exception):
    
    """Provider failed to fetch response"""
class AllProvidersFailure(Exception):
    """None of the providers generated response successfully"""
    pass

class FacebookInvalidCredentialsException(Exception):
    pass


class FacebookRegionBlocked(Exception):
    pass

class ModelUnloadedException(Exception):
    pass