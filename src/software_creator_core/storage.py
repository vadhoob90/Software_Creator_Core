"""Local SQLite snapshot journal with atomic compare-and-append and integrity checks."""

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from pydantic import ValidationError

from .contracts import Job
from .errors import CoreError
from .files import digest


def job_digest(job: Job) -> str:
    return digest(job.model_dump(mode="json"))


class Store:
    """The local operator owns the DB; digests detect corruption, not a hostile DB owner."""

    def __init__(self, path: Path) -> None:
        self.path = path

    @contextmanager
    def connection(self, *, create: bool = False) -> Iterator[sqlite3.Connection]:
        if self.path.is_symlink():
            raise CoreError(
                "unsafe-store",
                "Store must not be a symbolic link.",
                "Select an ordinary local database file.",
            )
        if not create and not self.path.is_file():
            raise CoreError("missing-store", "The job store does not exist.", "Create a job first.")
        try:
            with closing(sqlite3.connect(self.path, timeout=3)) as connection, connection:
                yield connection
        except sqlite3.Error as exc:
            raise CoreError(
                "store-failure",
                "The job transaction could not be committed.",
                "Check the database and retry from the last durable revision.",
            ) from exc

    def append(self, job: Job, expected_revision: int | None) -> None:
        """Commit one snapshot or fail without changing the previous revision."""
        with self.connection(create=True) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "CREATE TABLE IF NOT EXISTS snapshots ("
                "job_id TEXT, revision INTEGER, payload TEXT, digest TEXT, "
                "PRIMARY KEY (job_id, revision))"
            )
            latest = connection.execute(
                "SELECT MAX(revision) FROM snapshots WHERE job_id = ?", (job.spec.job_id,)
            ).fetchone()[0]
            next_revision = 0 if latest is None else latest + 1
            if latest != expected_revision or job.revision != next_revision:
                raise CoreError(
                    "revision-conflict",
                    "The job changed or already exists.",
                    "Reload the job; do not replay an old approval or contribution.",
                )
            connection.execute(
                "INSERT INTO snapshots VALUES (?, ?, ?, ?)",
                (job.spec.job_id, job.revision, job.model_dump_json(), job_digest(job)),
            )

    def load(self, job_id: str) -> Job:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT payload, digest FROM snapshots WHERE job_id = ? "
                "ORDER BY revision DESC LIMIT 1",
                (job_id,),
            ).fetchone()
        if row is None:
            raise CoreError("missing-job", "The requested job does not exist.", "Check the job ID.")
        try:
            job = Job.model_validate_json(row[0])
        except ValidationError as exc:
            raise CoreError(
                "corrupt-state",
                "The stored job violates its contract.",
                "Restore a verified database backup; do not overwrite this record.",
            ) from exc
        if job_digest(job) != row[1] or job.spec.job_id != job_id:
            raise CoreError(
                "corrupt-state",
                "The stored job digest or identity is invalid.",
                "Restore a verified backup and retain the corrupt file for investigation.",
            )
        return job
