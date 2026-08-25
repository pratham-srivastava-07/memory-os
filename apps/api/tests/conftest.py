"""Shared pytest configuration.

Adds the repo root to sys.path so `apps.*` imports resolve regardless of
where pytest is invoked from, and provides the database gate used by the
integration suite.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Modules read CONFIG.yml and data/documents by relative path, so the tests
# have to run with the repo root as cwd.
import os
os.chdir(REPO_ROOT)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "db: requires a running PostgreSQL with the chunks table"
    )
    config.addinivalue_line(
        "markers", "slow: loads the sentence-transformers model"
    )


def _database_reachable() -> bool:
    try:
        from apps.api.app.db import get_connection
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False


DB_AVAILABLE = _database_reachable()

requires_db = pytest.mark.skipif(
    not DB_AVAILABLE,
    reason="PostgreSQL not reachable (start the container in infra/)",
)


@pytest.fixture(scope="session")
def db_conn():
    """A live connection, or skip the test."""
    if not DB_AVAILABLE:
        pytest.skip("PostgreSQL not reachable")
    from apps.api.app.db import get_connection
    conn = get_connection()
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def sample_embedding() -> list[float]:
    """A 384-dim vector matching the chunks.embedding column."""
    return [0.01] * 384
