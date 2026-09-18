"""Stable errors shared by public service and command boundaries."""


class CoreError(Exception):
    """An actionable failure without private inputs or subprocess output."""

    def __init__(self, code: str, message: str, remedy: str) -> None:
        super().__init__(message)
        self.code = code
        self.remedy = remedy

    def as_dict(self) -> dict[str, str]:
        return {
            "outcome": "failure",
            "code": self.code,
            "message": str(self),
            "remedy": self.remedy,
        }
