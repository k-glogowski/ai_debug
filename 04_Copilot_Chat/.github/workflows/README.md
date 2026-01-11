# GitHub Actions CI/CD Pipeline

## Konfiguracja

Pipeline używa **GitHub Container Registry (GHCR)** - nie wymaga dodatkowych secrets! Używa wbudowanego `GITHUB_TOKEN`.

### Wymagania:

1. **Uprawnienia do pakietów** - workflow automatycznie otrzymuje uprawnienia przez `permissions: packages: write`
2. **Publiczne/prywatne pakiety** - domyślnie obrazy są prywatne, możesz zmienić to w ustawieniach pakietu

## Jak działa Pipeline

### Job 1: Test
- Uruchamia się przy każdym push i pull request
- Instaluje zależności Python
- Uruchamia testy pytest z katalogu `test/`

### Job 2: Build and Push
- Uruchamia się **TYLKO** po pomyślnym zakończeniu testów
- Uruchamia się **TYLKO** przy push do brancha `main`
- Loguje się do GitHub Container Registry
- Buduje obraz Docker
- Taguje obraz z:
  - SHA commita (pełny hash)
  - Tag `latest`
- Pushuje oba tagi do GHCR

## Struktura tagów obrazów

```
ghcr.io/[OWNER]/[REPO]:latest
ghcr.io/[OWNER]/[REPO]:[COMMIT_SHA]
```

Przykład:
```
ghcr.io/username/ai_debug-1:latest
ghcr.io/username/ai_debug-1:a1b2c3d4e5f6...
```

## Pobieranie obrazu

```bash
# Zaloguj się do GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pobierz obraz
docker pull ghcr.io/username/repo:latest
```

## Dostosowanie

Możesz zmienić:
- Branch triggery w sekcji `on:`
- Wersję Python w job `test`
- Tagi obrazu w `docker/metadata-action`
