# 🚀 Real-Time Helena Document Processor

## Czym to jest?

**Automatyczne przetwarzanie plików .md w czasie rzeczywistym.**

Zamiast czekać 4 godziny na cron, każdy plik `.md` który zapiszesz jest:
- ✅ **Wykrywany natychmiast** (milisekundy)
- ✅ **Przetwarzany automatycznie** przez Helenę
- ✅ **Dodawany do wszystkich baz danych** (PostgreSQL, Neo4j, Qdrant, Redis)
- ✅ **Gotowy w ~5-10 sekund**

## Jak to działa?

```
Ty zapisujesz plik .md
    ↓ (instant)
File System Watcher wykrywa zmianę
    ↓ (instant)
Helena's Processor uruchamia się automatycznie
    ↓ (~5-10 sek)
Plik przetworzony i dodany do:
    ├─ PostgreSQL (metadane dokumentu)
    ├─ Neo4j (relacje i koncepcje)
    ├─ Qdrant (wyszukiwanie semantyczne)
    └─ Redis (cache dla szybkiego dostępu)
    ↓
✅ GOTOWE! Wiedza dostępna dla wszystkich agentów
```

## Szybki start

### Krok 1: Uruchom watchera

```bash
./start_realtime_helena.sh
```

### Krok 2: Nie ma kroku 2!

Teraz po prostu pracuj normalnie. Każdy plik `.md` który zapiszesz będzie automatycznie przetworzony.

## Co jest monitorowane?

### ✅ Monitorowane:

- Wszystkie pliki `.md` w projekcie
- Protokoły, dokumentacja, raporty
- Nowe i zmodyfikowane pliki
- W czasie rzeczywistym

### ❌ Ignorowane:

- `node_modules/`
- `.git/`
- `__pycache__/`
- `helena_tasks/` (zadania Heleny)
- Pliki testowe (`test_`, `demo_`)
- Małe pliki (<1KB)

## Przykład użycia

```bash
# Terminal 1: Uruchom watchera
./start_realtime_helena.sh

# Terminal 2: Edytuj dokument
nano NOWY_PROTOKOL.md
# ... piszesz treść ...
# Zapisujesz (Ctrl+O)

# Terminal 1: Natychmiast widzisz:
# 🔔 DETECTED: NOWY_PROTOKOL.md (modified)
# ⏰ Time: 14:32:15
# 📊 Type: protocol
# 📝 Title: Nowy Protokół Zespołu
# 📏 Size: 5.2 KB
#
# 🤖 TRIGGERING HELENA AUTO-PROCESSING...
# 📦 PostgreSQL: ✅ Success
# 🕸️  Neo4j: ✅ Success
# 🔍 Qdrant: ✅ Success
# ⚡ Redis: ✅ Success
#
# ⏱️  Total time: 6.3 seconds
# ✅ Success rate: 4/4 databases
```

## Architektura

### Komponenty:

1. **`realtime_md_watcher.py`**
   - Obserwuje system plików
   - Wykrywa zmiany w plikach `.md`
   - Analizuje znaczenie pliku
   - Tworzy zadania dla Heleny

2. **`helena_realtime_processor.py`**
   - Odbiera zadania od watchera
   - Przetwarza treść dokumentu
   - Propaguje do wszystkich baz danych
   - Raportuje wyniki

3. **`start_realtime_helena.sh`**
   - Uruchamia cały system
   - Instaluje zależności
   - Konfiguruje środowisko

### Kolejki i archiwa:

```
helena_tasks/
├── realtime_queue/          # Nowe zadania do przetworzenia
│   └── realtime_20251104_143215_NOWY_PROTOKOL.json
└── realtime_queue/archive/  # Przetworzone zadania
    ├── success_realtime_20251104_143215_NOWY_PROTOKOL.json
    └── failed_realtime_20251104_143210_TEST.json

sql/realtime_updates/        # Wygenerowane SQL/Cypher
├── pg_20251104_143216_NOWY_PROTOKOL.sql
└── neo4j_20251104_143216_NOWY_PROTOKOL.cypher

qdrant_pending/              # Dokumenty do zaindeksowania
└── doc_20251104_143216_NOWY_PROTOKOL.json

redis_pending/               # Komendy Redis do wykonania
└── redis_20251104_143216_NOWY_PROTOKOL.txt
```

## Zaawansowane opcje

### Uruchamianie w tle

```bash
# Z logowaniem do pliku
nohup ./start_realtime_helena.sh > logs/realtime_helena.log 2>&1 &

# Sprawdź czy działa
ps aux | grep realtime_md_watcher

# Zobacz logi
tail -f logs/realtime_helena.log
```

### Zatrzymywanie

```bash
# Ctrl+C w terminalu gdzie działa

# Lub kill process
pkill -f realtime_md_watcher
```

### Debugowanie

```bash
# Uruchom z więcej informacji
python3 scripts/realtime_md_watcher.py --verbose

# Sprawdź kolejkę zadań
ls -lh helena_tasks/realtime_queue/

# Sprawdź archiwa
ls -lh helena_tasks/realtime_queue/archive/ | tail -20
```

## Różnice vs. Cron System

| Feature | Cron System | Real-Time System |
|---------|-------------|------------------|
| Opóźnienie | 4 godziny | < 1 sekunda |
| Detekcja | Co 4h scan | Instant na save |
| Przetwarzanie | Batch (wszystkie naraz) | Individual (po kolei) |
| Feedback | Po 4h | Natychmiast |
| Użycie CPU | Spike co 4h | Stały, niski |
| Idealne dla | Deployment, CI/CD | Development, iteracja |

## Kiedy używać którego?

### Użyj Real-Time gdy:
- ✅ Aktywnie pracujesz nad dokumentacją
- ✅ Chcesz natychmiastowego feedbacku
- ✅ Testujesz nowe koncepcje
- ✅ Iterujesz nad protokołami

### Użyj Cron gdy:
- ✅ System produkcyjny
- ✅ Batch processing w nocy
- ✅ Nie potrzebujesz instant feedbacku
- ✅ Oszczędzasz zasoby

## Porady

1. **Podczas pisania:** Uruchom real-time watchera dla instant feedbacku
2. **Przed commitem:** Sprawdź `sql/realtime_updates/` - zobacz co zostało wygenerowane
3. **Testowanie:** Użyj małego pliku .md aby sprawdzić czy system działa
4. **Performance:** Watcher używa bardzo mało CPU (~0.1%), możesz go zostawić cały czas

## Troubleshooting

### Watcher nie wykrywa zmian
```bash
# Sprawdź czy process działa
ps aux | grep realtime_md_watcher

# Restart
pkill -f realtime_md_watcher
./start_realtime_helena.sh
```

### Helena nie przetwarza
```bash
# Sprawdź kolejkę
ls helena_tasks/realtime_queue/

# Ręcznie uruchom processor
python3 scripts/helena_realtime_processor.py helena_tasks/realtime_queue/realtime_*.json
```

### Duplikaty w bazach
```bash
# Processor używa UPSERT, więc duplikaty są automatycznie mergowane
# Jeśli widzisz duplikaty, sprawdź logi
```

## Monitoring

### Status w czasie rzeczywistym:
```bash
# Terminal 1: Watcher
./start_realtime_helena.sh

# Terminal 2: Monitoruj kolejkę
watch -n 1 'ls -lh helena_tasks/realtime_queue/ | tail -10'

# Terminal 3: Monitoruj SQL updates
watch -n 1 'ls -lh sql/realtime_updates/ | tail -10'
```

## Integracja z IDE

### VSCode / Cursor

Dodaj to do `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Real-Time Helena",
      "type": "shell",
      "command": "./start_realtime_helena.sh",
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      },
      "isBackground": true
    }
  ]
}
```

Teraz możesz uruchomić z: `Cmd+Shift+P` → "Run Task" → "Start Real-Time Helena"

## FAQ

**Q: Czy muszę mieć uruchomione bazy danych?**  
A: Nie! Processor generuje SQL/Cypher/komendy które mogą być wykonane później. Ale jeśli bazy działają, wszystko dzieje się automatycznie.

**Q: Co z performance?**  
A: Watcher używa ~0.1% CPU. Processor uruchamia się tylko gdy coś się zmienia. Bardzo efektywne.

**Q: Czy mogę używać obu systemów (Cron + Real-Time)?**  
A: Tak! Watcher dla development, Cron dla nightly batch processing.

**Q: Co jeśli zapiszę 10 plików naraz?**  
A: Wszystkie zostaną przetworzone po kolei. Może zająć 1-2 minuty zamiast sekund.

## Status

✅ **Działające komponenty:**
- File system watcher (watchdog)
- Helena processor
- Kolejkowanie zadań
- SQL/Cypher generation
- Archiwizacja

⚠️ **Wymaga konfiguracji:**
- Aktywne połączenia do baz danych (opcjonalne)
- Qdrant indexing (używa pending queue jeśli niedostępne)

## Autor

System zaprojektowany dla instant feedback podczas development.
Zintegrowany z Helena Kowalczyk's data infrastructure pipeline.

**Wersja:** 1.0  
**Data:** 2025-11-04  
**Status:** Production Ready ✅
