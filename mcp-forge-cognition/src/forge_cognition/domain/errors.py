"""Domain errors mapped to non-revealing MCP responses."""


class CognitionError(Exception):
    code = "cognition_error"


class AccessDeniedError(CognitionError):
    code = "not_found"


class NotFoundError(CognitionError):
    code = "not_found"


class ConflictError(CognitionError):
    code = "conflict"

    def __init__(self, message: str, current_hash: str | None = None) -> None:
        super().__init__(message)
        self.current_hash = current_hash


class IdempotencyConflictError(CognitionError):
    code = "idempotency_conflict"


class ValidationError(CognitionError):
    code = "validation_error"


class ImmutableEntityError(CognitionError):
    code = "immutable_entity"
