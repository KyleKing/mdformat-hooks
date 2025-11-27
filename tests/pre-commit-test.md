# Test file

This file contains code examples for testing mdformat-hooks with mdsf integration.

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

## JavaScript / TypeScript

```javascript
const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
};

function processArray(items) {
    return items
        .filter((item) => item.active)
        .map((item) => ({
            id: item.id,
            name: item.name,
            timestamp: Date.now(),
        }));
}

export { fetchData, processArray };
```

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    role: "admin" | "user" | "guest";
}

class UserManager {
    private users: Map<number, User> = new Map();

    addUser(user: User): void {
        this.users.set(user.id, user);
    }

    getUser(id: number): User | undefined {
        return this.users.get(id);
    }

    filterByRole(role: User["role"]): User[] {
        return Array.from(this.users.values()).filter(
            (user) => user.role === role,
        );
    }
}

export { UserManager, type User };
```

## Go

```go
package main

import (
    "context"
    "fmt"
    "time"
)

type Config struct {
    Host string
    Port int
    Timeout time.Duration
}

func NewConfig(host string, port int) *Config {
    return &Config{
        Host: host,
        Port: port,
        Timeout: 30 * time.Second,
    }
}

func (c *Config) String() string {
    return fmt.Sprintf("%s:%d", c.Host, c.Port)
}

func ProcessData(ctx context.Context, data []string) ([]string, error) {
    result := make([]string, 0, len(data))

    for _, item := range data {
        select {
        case <-ctx.Done():
            return nil, ctx.Err()
        default:
            if len(item) > 0 {
                result = append(result, item)
            }
        }
    }

    return result, nil
}
```

## Rust

```rust
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::Read;
use std::path::Path;

#[derive(Debug, Clone)]
pub struct Config {
    pub name: String,
    pub version: String,
    pub enabled: bool,
}

impl Config {
    pub fn new(name: String, version: String) -> Self {
        Self {
            name,
            version,
            enabled: true,
        }
    }
}

pub fn read_file(path: &Path) -> Result<String, Box<dyn Error>> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

pub fn process_map(data: &HashMap<String, i32>, threshold: i32) -> Vec<String> {
    data.iter()
        .filter(|(_, &value)| value > threshold)
        .map(|(key, _)| key.clone())
        .collect()
}
```

## Shell / Bash

```shell
#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CONFIG_FILE="${SCRIPT_DIR}/config.json"

log_info() {
    echo "[INFO] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

cleanup() {
    log_info "Cleaning up temporary files..."
    rm -f /tmp/temp_*.log
}

trap cleanup EXIT

process_files() {
    local input_dir="$1"
    local output_dir="$2"

    if [[ ! -d "$input_dir" ]]; then
        log_error "Input directory does not exist: $input_dir"
        return 1
    fi

    mkdir -p "$output_dir"

    find "$input_dir" -name "*.txt" -type f | while IFS= read -r file; do
        local basename
        basename=$(basename "$file")
        log_info "Processing $basename"
        cp "$file" "$output_dir/$basename"
    done
}

main() {
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <input_dir> <output_dir>"
        exit 1
    fi

    process_files "$1" "$2"
}

main "$@"
```

## Ruby

```ruby
require "json"
require "fileutils"

class DataProcessor
  attr_reader :name, :version

  def initialize(name, version)
    @name = name
    @version = version
    @cache = {}
  end

  def process(data, threshold = 100)
    data.select { |key, value| value > threshold }
        .transform_values { |value| value * 2 }
  end

  def load_config(path)
    return nil unless File.exist?(path)

    file_content = File.read(path)
    JSON.parse(file_content)
  rescue JSON::ParserError => e
    warn "Failed to parse JSON: #{e.message}"
    nil
  end

  def self.create_default
    new("default", "1.0.0")
  end
end

module Utils
  def self.ensure_directory(path)
    FileUtils.mkdir_p(path) unless Dir.exist?(path)
  end

  def self.clean_string(str)
    str.strip.downcase.gsub(/\s+/, "_")
  end
end
```

## Java

```java
package com.example.app;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class DataProcessor {
    private final String name;
    private final String version;
    private final Map<String, Object> cache;

    public DataProcessor(String name, String version) {
        this.name = name;
        this.version = version;
        this.cache = new java.util.HashMap<>();
    }

    public List<String> processData(List<String> data, int threshold) {
        return data.stream()
                .filter(item -> item.length() > threshold)
                .map(String::toUpperCase)
                .collect(Collectors.toList());
    }

    public String readFile(Path path) throws IOException {
        if (!Files.exists(path)) {
            throw new IOException("File not found: " + path);
        }
        return Files.readString(path);
    }

    public static class Builder {
        private String name = "default";
        private String version = "1.0.0";

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder version(String version) {
            this.version = version;
            return this;
        }

        public DataProcessor build() {
            return new DataProcessor(name, version);
        }
    }
}
```

## C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int version;
    int enabled;
} Config;

Config *config_create(const char *name, int version) {
    Config *config = (Config *)malloc(sizeof(Config));
    if (config == NULL) {
        return NULL;
    }

    config->name = strdup(name);
    config->version = version;
    config->enabled = 1;

    return config;
}

void config_destroy(Config *config) {
    if (config != NULL) {
        free(config->name);
        free(config);
    }
}

int process_array(int *data, int size, int threshold) {
    int count = 0;

    for (int i = 0; i < size; i++) {
        if (data[i] > threshold) {
            count++;
        }
    }

    return count;
}

char *read_file(const char *path) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        perror("Error opening file");
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *buffer = (char *)malloc(length + 1);
    if (buffer == NULL) {
        fclose(file);
        return NULL;
    }

    fread(buffer, 1, length, file);
    buffer[length] = '\0';

    fclose(file);
    return buffer;
}
```

## C++

```cpp
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <vector>

class Config {
public:
    Config(std::string name, std::string version)
        : name_(std::move(name)), version_(std::move(version)), enabled_(true) {}

    const std::string& name() const { return name_; }
    const std::string& version() const { return version_; }
    bool enabled() const { return enabled_; }

    void set_enabled(bool enabled) { enabled_ = enabled; }

private:
    std::string name_;
    std::string version_;
    bool enabled_;
};

template <typename T>
class DataProcessor {
public:
    explicit DataProcessor(int threshold) : threshold_(threshold) {}

    std::vector<T> process(const std::vector<T>& data) const {
        std::vector<T> result;
        std::copy_if(data.begin(), data.end(), std::back_inserter(result),
                     [this](const T& item) { return item > threshold_; });
        return result;
    }

private:
    int threshold_;
};

std::unique_ptr<std::string> read_file(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        return nullptr;
    }

    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());

    return std::make_unique<std::string>(std::move(content));
}
```

## C\#

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace Example.App
{
    public class Config
    {
        public string Name { get; set; }
        public string Version { get; set; }
        public bool Enabled { get; set; } = true;

        public Config(string name, string version)
        {
            Name = name;
            Version = version;
        }
    }

    public class DataProcessor
    {
        private readonly int _threshold;
        private readonly Dictionary<string, object> _cache;

        public DataProcessor(int threshold)
        {
            _threshold = threshold;
            _cache = new Dictionary<string, object>();
        }

        public List<string> ProcessData(List<string> data)
        {
            return data
                .Where(item => item.Length > _threshold)
                .Select(item => item.ToUpper())
                .ToList();
        }

        public async Task<string> ReadFileAsync(string path)
        {
            if (!File.Exists(path))
            {
                throw new FileNotFoundException($"File not found: {path}");
            }

            return await File.ReadAllTextAsync(path);
        }

        public static DataProcessor CreateDefault()
        {
            return new DataProcessor(100);
        }
    }
}
```

## JSON

```json
{
    "name": "example-config",
    "version": "1.0.0",
    "enabled": true,
    "settings": {
        "timeout": 30,
        "retries": 3,
        "endpoints": ["https://api.example.com", "https://backup.example.com"]
    },
    "features": {
        "logging": true,
        "monitoring": false,
        "caching": {
            "enabled": true,
            "ttl": 3600
        }
    }
}
```

## YAML

```yaml
name: example-workflow
version: 1.0.0
enabled: true

settings:
    timeout: 30
    retries: 3
    endpoints:
        - https://api.example.com
        - https://backup.example.com

features:
    logging: true
    monitoring: false
    caching:
        enabled: true
        ttl: 3600

jobs:
    - name: build
      steps:
          - checkout
          - install-deps
          - run-tests
    - name: deploy
      steps:
          - build-image
          - push-image
          - update-service
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
