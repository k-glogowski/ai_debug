# FastAPI Application

Prosta aplikacja FastAPI z testami pytest.

## Struktura projektu

```
04_Copilot_Chat/
├── main.py              # Główna aplikacja FastAPI
├── requirements.txt     # Zależności projektu
├── conftest.py         # Konfiguracja pytest
└── test/
    ├── __init__.py
    └── test_main.py    # Testy aplikacji
```

## Wymagania

- Python 3.8+
- FastAPI
- pytest
- httpx

## Instalacja

Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

## Uruchomienie aplikacji

### Tryb development

```bash
uvicorn main:app --reload
```

Aplikacja będzie dostępna pod adresem: `http://localhost:8000`

### Dokumentacja API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testy

### Uruchomienie testów

```bash
pytest
```

### Uruchomienie testów z większą ilością informacji

```bash
pytest -v
```

### Uruchomienie testów z pokryciem kodu

```bash
pytest --cov=. --cov-report=html
```

## Endpoints

### GET /

Zwraca prosty komunikat powitalny.

**Response:**
```json
{
    "Hello": "World"
}
```

**Status Code:** `200 OK`

## Przykład użycia

```bash
curl http://localhost:8000/
```

## Rozwój

Struktura testów znajduje się w katalogu `test/`. Każdy test używa `TestClient` z FastAPI do symulowania requestów HTTP.

### Dodawanie nowych testów

1. Utwórz nowy plik testowy w katalogu `test/` z prefiksem `test_`
2. Importuj `TestClient` i `app`
3. Napisz funkcje testowe z prefiksem `test_`

Przykład:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_example():
    response = client.get("/endpoint")
    assert response.status_code == 200
```
