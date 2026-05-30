#!/usr/bin/env sh
set -e

export PYTHONPATH="/app:${PYTHONPATH}"

if [ "${RUN_TESTS_ON_STARTUP:-1}" = "1" ]; then
  echo "Running tests with coverage..."
  pytest --cov=services --cov-report=term-missing
fi

exec uvicorn main:app --host 0.0.0.0 --port 8001
