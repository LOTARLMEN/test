app_module := "src.main:app"


start:
    uv run uvicorn {{app_module}} --reload --host 127.0.0.1 --port 8000


db_status:
    uv run alembic current


db_migrate msg:
    uv run alembic revision --autogenerate -m "{{msg}}"


db_up:
    uv run alembic upgrade head


db_down:
    uv run alembic downgrade -1


check:
    uv run mypy src
    uv run pytest