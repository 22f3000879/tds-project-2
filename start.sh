#!/bin/bash

# Install Playwright browsers
python3 -m playwright install --with-deps chromium

# Start FastAPI app
uvicorn app.main:app --host 0.0.0.0 --port $PORT
