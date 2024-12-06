"""Models representing a log entry."""

from __future__ import annotations

import os
from typing import Any, Self

import pydantic


class Application(pydantic.BaseModel):
    """Contains information about the application."""

    name: str
    version: str
    service_name: str
    commit_hash: str

    @classmethod
    def from_env(cls) -> Self:
        """Load application details from the environment."""
        return cls(
            name=os.environ["LDR_APPLICATION_NAME"],
            version=os.environ["LDR_APPLICATION_VERSION"],
            service_name=os.environ["LDR_APPLICATION_SERVICE_NAME"],
            commit_hash=os.environ["LDR_APPLICATION_COMMIT_HASH"],
        )


class Entry(pydantic.BaseModel):
    """Standardised log entry for Louder projects."""

    client: str
    message: str
    app: Application = pydantic.Field(default_factory=Application.from_env)
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)

    def __str__(self) -> str:
        """Serialize the log as a string."""
        return self.model_dump_json()
