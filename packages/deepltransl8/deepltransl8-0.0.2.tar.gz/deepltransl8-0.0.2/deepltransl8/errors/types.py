class DeepLException(Exception):
    pass


class InvalidLanguageException(DeepLException):
	pass


class ReadTheDocsException(DeepLException):
	pass


class InvalidResponseException(DeepLException):
	pass
