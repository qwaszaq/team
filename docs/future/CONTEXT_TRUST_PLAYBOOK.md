# Context Trust Playbook

**Cel:** Zminimalizować ryzyko pominięć, mylących streszczeń i błędnych decyzji przy pracy agentów na dużej (>1M tokenów) bazie wiedzy.

---

## 1. Monitorowanie zapisów (Helena)

- **Automatyczne alerty:** jeśli zapis do którejkolwiek warstwy (PostgreSQL/Neo4j/Qdrant/Redis) się nie powiedzie, Helena loguje ostrzeżenie. Dodaj powiadomienie (np. e‑mail, Slack) na bazie wpisu w logu `❌`.
- **Dzienny raport:** raz dziennie Helena generuje listę decyzji z ostatnich 24h oraz status zapisu. Raport trzymamy w `/logs/daily_persistence.md`.
- **Testy sanity:** raz w tygodniu uruchamiamy `python3 scripts/persistence_sanity.py`, który losowo wybiera 5 ostatnich wydarzeń i sprawdza obecność w każdej warstwie.

---

## 2. Walidacja wyszukiwania (semantyka)

- **Podgląd wyników:** agent, który pobiera kontekst, zapisuje w logu top‑3 wyniki (fragment + ocena trafności). Człowiek może szybko zweryfikować, czy pasują.
- **Reguła „zawsze cytuj”:** przy tworzeniu streszczenia agent dołącza identyfikator rekordu (`decision_id`, `document_path`). Pozwala to natychmiast wrócić do źródła.
- **Feedback loop:** jeśli agent uzna wynik za nietrafny, zapisuje `feedback_quality: low`. Comiesięczny skrypt liczy ile takich oznaczeń się pojawiło i aktualizuje parametry wyszukiwania.

---

## 3. Kontrola streszczeń

- **Dwupoziomowe streszczenia:**
  1. *Short* (≤120 tokenów) – do szybkiego kontekstu.
  2. *Full digest* – link do pełnego tekstu + struktura nagłówków.
- **Random audit:** raz na 10 streszczeń Helena prosi innego agenta (np. Tomasza) o porównanie skrótu z pełnym dokumentem i oznaczenie `accurate`/`needs_fix`.
- **Checklist dla streszczeń:**
  - zawiera źródło / ID
  - uwzględnia datę
  - wspomina najważniejsze decyzje/ustalenia
  - wyraźnie zaznacza niepewność (`⚠️`)

---

## 4. Procedury dla krytycznych decyzji

- **Podwójne potwierdzenie:** kluczowe decyzje (`importance ≥ 0.9`) muszą zostać zatwierdzone przez drugiego agenta; logujemy `approved_by`.
- **Lista kontrolna:** przed wdrożeniem (np. deployment) Helena odpala checklistę bezpieczeństwa i jakości. Każdy punkt musi mieć `✅`, inaczej proces zatrzymany.
- **Retrospektywy T+24h:** dzień po ważnej decyzji agent sprawdza, czy nowe dane jej nie unieważniają; wpisuje wynik do `post_decision_review`.

---

## 5. Audyty kontekstu

- **Tygodniowe „context diff”:** skrypt `python3 scripts/context_diff.py --range 7d` porównuje, co przybyło w PostgreSQL/Qdrant. Pozwala wykryć nieoczekiwane luki.
- **Próg alarmowy:** jeśli agent ma <2 wpisów w `agent_contexts` przez 14 dni, system wysyła przypomnienie („uzupełnij pamięć osobistą”).
- **Backup & wersjonowanie:** raz dziennie snapshot bazy + eksport `navigation_pointers.json`. Trzymamy min. 7 dni.

---

## 6. Dobre praktyki dla ludzi

- **„Trust but verify”:** zanim użyjesz streszczenia w decyzji, otwórz źródło (link/ID) i zrób szybki przegląd kluczowych sekcji.
- **Notuj wątpliwości:** jeśli coś wygląda podejrzanie, dopisz komentarz – łatwiej będzie poprawić algorytm wyszukiwania.
- **Iteracyjne ulepszanie:** raz w miesiącu przeglądamy zgłoszone problemy i decydujemy, które usprawnienia wprowadzić (np. nowe filtry w Qdrant, lepsze progi ważności).

---

## Quick Start Checklist

1. [ ] Rejestrowanie alertów Helene w Slacku/e‑mailu.  
2. [ ] Wdrożenie dziennego raportu zapisów.  
3. [ ] Włączenie logowania top‑3 wyników wyszukiwania.  
4. [ ] Reguła „zawsze cytuj” dla streszczeń.  
5. [ ] Uruchomienie skryptu `context_diff.py` (cron 1×tydzień).  
6. [ ] Ustalenie budzika dla agentów z pustym `agent_contexts`.  
7. [ ] Comiesięczna sesja „context QA” (przegląd feedbacku).

---

**Efekt:** Agenci pracują na gigantycznym repo kontekstu, ale każdy krok ma zabezpieczenia: brakujące zapisy widać natychmiast, wyniki wyszukiwania można zweryfikować, streszczenia są audytowane, a krytyczne decyzje mają dodatkowe potwierdzenie. Dzięki temu ryzyko pomyłek i „zapominania” spada do minimum.

