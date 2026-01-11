---
name: Helm Chart dla Adresowo Scraper
overview: ""
todos: []
---

# Helm Chart dla Adresowo Scraper

## Przegląd

Konwersja istniejących manifestów Kubernetes do Helm chart z templatami, które eliminują duplikację kodu (szczególnie dla job files dla różnych miast).

## Struktura Helm Chart

Utworzę standardową strukturę Helm chart:

- `Chart.yaml` - definicja charta
- `values.yaml` - wartości domyślne dla wszystkich zasobów
- `templates/` - katalog z templatami:
- `_helpers.tpl` - funkcje pomocnicze
- `namespace.yaml` - namespace template
- `configmap.yaml` - configmap template
- `pvc.yaml` - PVC template
- `job.yaml` - **jeden template** dla wszystkich miast (używając `range` przez listę cities)
- `cronjob.yaml` - cronjob template z dynamicznymi kontenerami dla miast
- `pvc-reader.yaml` - PVC reader pod template

## Założenia

1. **Namespace**: Ujednolicenie do jednego namespace (domyślnie `scraper`, konfigurowalne przez `values.yaml`)
2. **Cities**: Wszystkie miasta (warszawa, wroclaw, lodz) będą zarządzane przez jedną listę w `values.yaml`
3. **CronJob**: Zostanie rozszerzony o wszystkie miasta z listy (obecnie brakuje lodz)
4. **Job**: Jeden template generujący Job dla każdego miasta z listy

## Główne zmiany

### 1. `values.yaml`

- Definicja listy miast jako zmienna globalna
- Konfiguracja dla każdego miasta (liczba stron, itp.)
- Wspólne ustawienia (obraz, zasoby, timeouts, namespace)
- Konfiguracja CronJob (schedule, timezone)

### 2. `templates/job.yaml`

- Jeden template używający `{{- range .Values.cities }}`
- Generuje Job dla każdego miasta z listy
- Unika duplikacji kodu z `job-lodz.yaml`, `job-warszawa.yaml`, `job-wroclaw.yaml`

### 3. `templates/cronjob.yaml`

- Dynamiczne generowanie kontenerów dla wszystkich miast
- Rozszerzenie o brakujące miasto (lodz)

### 4. `templates/configmap.yaml`

- Dynamiczne generowanie kluczy dla miast na podstawie listy

## Pliki do utworzenia

1. `Chart.yaml`
2. `values.yaml`
3. `templates/_helpers.tpl`
4. `templates/namespace.yaml`
5. `templates/configmap.yaml`
6. `templates/pvc.yaml`
7. `templates/job.yaml` (jeden zamiast trzech plików)
8. `templates/cronjob.yaml`
9. `templates/pvc-reader.yaml`

## Zachowanie istniejącej funkcjonalności

- Wszystkie zmienne środowiskowe
- Mount volumes i PVC
- Limity zasobów
- Backoff limits i timeouts
- Labels i selectors
