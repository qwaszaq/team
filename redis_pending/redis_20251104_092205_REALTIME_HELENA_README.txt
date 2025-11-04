SET doc:REALTIME_HELENA_README:title "🚀 Real-Time Helena Document Processor"
SET doc:REALTIME_HELENA_README:type "team_documentation"
SET doc:REALTIME_HELENA_README:path "docs/team/REALTIME_HELENA_README.md"
SET doc:REALTIME_HELENA_README:content "# 🚀 Real-Time Helena Document Processor

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

Teraz po prostu pracuj normalnie. Każdy plik `.md` który za"
EXPIRE doc:REALTIME_HELENA_README:content 86400
SADD docs:all "REALTIME_HELENA_README"
SADD docs:type:team_documentation "REALTIME_HELENA_README"