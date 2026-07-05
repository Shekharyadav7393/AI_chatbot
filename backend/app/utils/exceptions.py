class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = "BAD_REQUEST"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")

class AuthorizationError(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")

class ValidationError(AppException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")

class ConflictError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409, error_code="CONFLICT")

class DocumentProcessingError(AppException):
    def __init__(self, message: str = "Error processing document"):
        super().__init__(message, status_code=500, error_code="DOCUMENT_PROCESSING_ERROR")

class RAGError(AppException):
    def __init__(self, message: str = "Error in AI generation"):
        super().__init__(message, status_code=500, error_code="RAG_ERROR")

class DatabaseError(AppException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")

class RateLimitError(AppException):
    def __init__(self, message: str = "Too many requests"):
        super().__init__(message, status_code=429, error_code="RATE_LIMIT_EXCEEDED")
