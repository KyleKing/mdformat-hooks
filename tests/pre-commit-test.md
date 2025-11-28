# Test file

This file contains code examples for testing mdformat-hooks with `mdsf` integration.

## Python

```python
from dataclasses import dataclass
from typing import Literal
from pathlib import Path
import json


@dataclass(frozen=True)
class Config:
    name: str
    version: str
    enabled: bool = True


def process_data(data: dict[str, int], threshold: int = 100) -> list[str]:
    """Process data and return filtered results."""
    return [key for key, value in data.items() if value > threshold]


def read_config(path: Path) -> Config | None:
    """Read configuration from file."""
    if not path.exists():
        return None

    with path.open() as f:
        data = json.load(f)

    return Config(**data)


Status = Literal["active", "inactive", "pending"]


class StatusManager:
    def __init__(self, initial_status: Status = "pending") -> None:
        self._status = initial_status

    def update(self, new_status: Status) -> None:
        self._status = new_status

    @property
    def current(self) -> Status:
        return self._status
```

## TOML

```toml
name = "example-config"
version = "1.0.0"
enabled = true

[settings]
timeout = 30
retries = 3
endpoints = ["https://api.example.com", "https://backup.example.com"]

[features]
logging = true
monitoring = false

[features.caching]
enabled = true
ttl = 3600

[[jobs]]
name = "build"
steps = ["checkout", "install-deps", "run-tests"]

[[jobs]]
name = "deploy"
steps = ["build-image", "push-image", "update-service"]
```

## SQL

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users (email);

CREATE INDEX idx_users_role ON users (role);

INSERT INTO
    users (name, email, role)
VALUES
    ('John Doe', 'john@example.com', 'admin'),
    ('Jane Smith', 'jane@example.com', 'user'),
    ('Bob Johnson', 'bob@example.com', 'user');

SELECT
    u.id,
    u.name,
    u.email,
    u.role,
    COUNT(o.id) AS order_count
FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
WHERE
    u.role IN ('admin', 'user')
    AND u.created_at >= NOW() - INTERVAL '30 days'
GROUP BY
    u.id,
    u.name,
    u.email,
    u.role
HAVING
    COUNT(o.id) > 0
ORDER BY order_count DESC, u.name ASC
LIMIT 100;

UPDATE users
SET
    updated_at = CURRENT_TIMESTAMP,
    role = 'premium'
WHERE
    id IN (
        SELECT user_id
        FROM subscriptions
        WHERE status = 'active'
    );
```
