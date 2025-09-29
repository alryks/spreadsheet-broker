## Spreadsheet Broker API

Simple FastAPI service that stores spreadsheet data in memory.

### Configuration

Create a `.env` file with your auth key:

```bash
echo 'AUTH_KEY=supersecret' > .env
```

Optionally set `UVICORN_WORKERS` in `.env`.

### Run with Docker Compose

```bash
docker compose up --build
```

Service will be available at `http://localhost:8000`.

### Endpoints

- `POST /add`

  Request body:
  ```json
  {
    "spreadsheet": "uniqueKey",
    "data": [["cell1", "cell2"], ["cell3", "cell4", "cell5"]]
  }
  ```

  Headers:
  - `Authorization: Bearer <AUTH_KEY>`

  Response:
  ```json
  { "status": "ok" }
  ```

- `GET /get?spreadsheet=uniqueKey&pop=true`

  Query params:
  - `spreadsheet` (required)
  - `pop` (optional, default false). If true, remove after reading.

  Headers:
  - `Authorization: Bearer <AUTH_KEY>`

  Response:
  ```json
  {
    "data": [["cell1", "cell2"], ["cell3", "cell4", "cell5"]]
  }
  ```

### Develop locally (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AUTH_KEY=supersecret
uvicorn app.main:app --reload
```


