#!/usr/bin/env bash

set -e

echo "Running migrations"

alembic upgrade head

echo "migration done"

exec "$@"