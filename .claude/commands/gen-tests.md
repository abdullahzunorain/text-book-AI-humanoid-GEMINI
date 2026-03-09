# Generate Endpoint Tests

Autonomous skill to scaffold pytest test files for FastAPI endpoints.

## Input

Provide the endpoint path as argument, e.g., `/gen-tests POST /chat/`

## Steps

1. Read the endpoint's route handler from `backend/src/api/` to understand:
   - HTTP method and path
   - Request body schema (from `backend/src/schemas/`)
   - Response model
   - Dependencies (DB, Qdrant, auth)
2. Read `backend/tests/conftest.py` to understand available fixtures
3. Generate a test file in `backend/tests/` with:
   - **Happy path test**: Valid request returns expected response
   - **Edge case test**: Boundary values, optional fields, empty strings
   - **Error case test**: Missing required fields (422), invalid data, auth failures
4. Use `pytest.mark.asyncio`, `httpx.AsyncClient`, and `unittest.mock.patch` for external services
5. Write the test file and run `cd backend && uv run pytest <test_file> -v` to confirm tests are syntactically valid

## Test Template

```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_<endpoint>_happy_path(client):
    """<Method> <path> with valid data returns expected response."""
    ...

@pytest.mark.asyncio
async def test_<endpoint>_edge_case(client):
    """<Method> <path> edge case: <description>."""
    ...

@pytest.mark.asyncio
async def test_<endpoint>_error(client):
    """<Method> <path> with invalid data returns error."""
    ...
```

## Output

Report: file path, number of tests generated, pass/fail status after running pytest.
