class ArtifactoryException(Exception):
    '''General exception type for artifactory-API-related failures.'''
    pass


class NotFoundException(ArtifactoryException):
    '''A special exception to call out the case of receiving a 404.'''
    pass


class EmptyResponseException(ArtifactoryException):
    '''A special exception to call out the case receiving an empty response.'''
    pass


class BadHTTPException(ArtifactoryException):
    '''A special exception to call out the case of a broken HTTP response.'''
    pass


class TimeoutException(ArtifactoryException):
    '''A special exception to call out in the case of a socket timeout.'''
    pass
