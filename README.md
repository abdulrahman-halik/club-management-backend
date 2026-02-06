# FastAPI MongoDB Project

This is a FastAPI backend project with MongoDB integration.

## Project Structure

The project follows a layered architecture:

- `app/main.py`: Entry point of the application.
- `app/config.py`: Configuration settings.
- `app/routes/`: API route definitions.
- `app/models/`: Pydantic models.
- `app/schemas/`: Request/Response schemas.
- `app/services/`: Business logic.
- `app/repositories/`: Database interactions.

## Setup

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

## Docker

Run with Docker Compose:

```bash
docker-compose up --build
```
