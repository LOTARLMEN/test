set shell := ["powershell", "-Command"]


hello:
    echo "Привет!"


start:
    uv run uvicorn src.main:app --reload