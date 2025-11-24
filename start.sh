#!/bin/bash

echo "Installing Playwright Chromium..."
python -m playwright install --with-deps chromium

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
