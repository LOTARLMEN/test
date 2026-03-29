

start:
    uv run uvicorn src.main:app --reload


status:
    alembic current


migrate msg:
    alembic revision --autogenerate -m "{{msg}}"
    alembic upgrade head