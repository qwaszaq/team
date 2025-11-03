# 📖 Destiny Chat UI - User Guide

## Wprowadzenie

Destiny Chat UI to graficzny interfejs do komunikacji z 9 wyspecjalizowanymi agentami AI z Destiny Team Framework. Każdy agent ma swoją specjalizację i może pomóc w różnych aspektach projektów.

---

## 🤖 Poznaj zespół

### 1. Aleksander Nowak - Orchestrator
**Specjalizacja:** Koordynacja zespołu, strategiczne decyzje

**Kiedy go używać:**
- Planowanie projektu
- Delegowanie zadań
- Koordynacja między wieloma agentami
- Decyzje strategiczne

**Przykłady:**
```
"Chcę zbudować aplikację e-commerce. Od czego zacząć?"
"Pomóż mi zaplanować projekt OSINT"
"Potrzebuję zespołu do stworzenia MVP"
```

---

### 2. Tomasz Zieliński - Senior Developer
**Specjalizacja:** Full-stack development, Python, system architecture

**Kiedy go używać:**
- Implementacja kodu
- Code review
- Debugging
- Technical solutions

**Przykłady:**
```
"Zaimplementuj system logowania z OAuth2"
"Jak zbudować REST API w FastAPI?"
"Review mojego kodu Python"
```

---

### 3. Anna Nowakowska - QA Engineer
**Specjalizacja:** Testing, quality assurance

**Kiedy jej używać:**
- Testowanie aplikacji
- Tworzenie test cases
- Automatyzacja testów
- Quality checks

**Przykłady:**
```
"Stwórz test plan dla login feature"
"Jakie testy powinienem napisać?"
"Zautomatyzuj testy end-to-end"
```

---

### 4. Joanna Mazur - UX/UI Designer
**Specjalizacja:** User experience, interface design

**Kiedy jej używać:**
- Design interfejsu
- Wireframes i mockups
- User flow
- Design system

**Przykłady:**
```
"Zaprojektuj dashboard dla admina"
"Jak usprawnić UX w checkoucie?"
"Stwórz wireframes dla mobile app"
```

---

### 5. Magdalena Kowalska - Product Manager
**Specjalizacja:** Requirements, roadmap, priorities

**Kiedy jej używać:**
- Definicja requirements
- Planowanie roadmap
- Priorytetyzacja features
- Stakeholder management

**Przykłady:**
```
"Zdefiniuj requirements dla MVP"
"Jakie features są najważniejsze?"
"Stwórz product roadmap na Q1"
```

---

### 6. Katarzyna Wiśniewska - Software Architect
**Specjalizacja:** System architecture, technical decisions

**Kiedy jej używać:**
- Architektura systemu
- Technology stack decisions
- Scalability planning
- System design

**Przykłady:**
```
"Jak zarchitekturować microservices?"
"Którą bazę danych wybrać?"
"Design system architecture dla 1M users"
```

---

### 7. Piotr Szymański - DevOps Engineer
**Specjalizacja:** CI/CD, Docker, deployment

**Kiedy go używać:**
- Setup CI/CD
- Docker containerization
- Deployment automation
- Infrastructure

**Przykłady:**
```
"Setup Docker dla mojego projektu"
"Jak zautomatyzować deployment?"
"Stwórz CI/CD pipeline"
```

---

### 8. Michał Dąbrowski - Security Specialist
**Specjalizacja:** Security, compliance, audits

**Kiedy go używać:**
- Security audits
- Vulnerability assessment
- Security best practices
- Compliance checks

**Przykłady:**
```
"Security audit mojej aplikacji"
"Jak zabezpieczyć API?"
"GDPR compliance checklist"
```

---

### 9. Dr. Joanna Wójcik - Data Scientist
**Specjalizacja:** Data analysis, ML, algorithms

**Kiedy jej używać:**
- Data analysis
- Machine learning
- Algorithms
- Statistical modeling

**Przykłady:**
```
"Analiza danych z bazy użytkowników"
"Jak zaimplementować recommendation system?"
"Predict user churn"
```

---

## 💬 Jak rozmawiać z agentami

### Opcja 1: @All (Zespół)
Wysyła do Aleksandra, który koordynuje zespół:
```
@All: "Potrzebuję zbudować system CRM"
```

Aleksander przeanalizuje i:
- Deleguje zadania do właściwych agentów
- Koordynuje workflow
- Zbiera wyniki

---

### Opcja 2: Konkretny agent
Bezpośrednio do specjalisty:
```
@Tomasz: "Zaimplementuj API endpoint"
@Joanna: "Zaprojektuj UI dla dashboardu"
@Anna: "Przetestuj login flow"
```

---

### Opcja 3: Sekwencja
Możesz rozmawiać z wieloma agentami po kolei:
```
1. @Magdalena: "Zdefiniuj requirements dla MVP"
   (czekasz na odpowiedź)

2. @Katarzyna: "Zaprojektuj architekturę na podstawie requirements"
   (czekasz na odpowiedź)

3. @Tomasz: "Zaimplementuj zgodnie z architekturą"
   (czekasz na odpowiedź)

4. @Anna: "Przetestuj implementację"
```

---

## 🎯 Przykładowe scenariusze

### Scenariusz 1: Nowy projekt od zera

**Krok 1:** Plan
```
@Aleksander: "Chcę zbudować aplikację do zarządzania zadaniami (task manager). 
Pomóż mi zaplanować projekt."
```

**Krok 2:** Requirements
```
@Magdalena: "Zdefiniuj detailed requirements dla task managera"
```

**Krok 3:** Architektura
```
@Katarzyna: "Zaprojektuj architekturę systemu"
```

**Krok 4:** Design
```
@Joanna: "Zaprojektuj UI dla main dashboard"
```

**Krok 5:** Implementation
```
@Tomasz: "Zaimplementuj backend API"
```

**Krok 6:** Testing
```
@Anna: "Stwórz test plan i execute tests"
```

**Krok 7:** Deployment
```
@Piotr: "Setup Docker i deployment"
```

---

### Scenariusz 2: Code review

```
@Tomasz: "Review tego kodu:
[wklej kod]
Co mogę poprawić?"
```

---

### Scenariusz 3: Debugging

```
@Tomasz: "Mam bug: użytkownik nie może się zalogować. 
Error: 'Invalid credentials' nawet z dobrymi danymi.
Pomóż mi znaleźć problem."
```

---

### Scenariusz 4: Security audit

```
@Michał: "Security audit mojego API:
- POST /api/login
- GET /api/users
- POST /api/users/{id}/update

Jakie są vulnerabilities?"
```

---

## ⌨️ Keyboard Shortcuts

- **Enter** - Wyślij wiadomość
- **Shift + Enter** - Nowa linia w wiadomości
- **Esc** - Wyczyść pole input (future)

---

## 🎨 Tips & Tricks

### 1. Bądź konkretny
❌ "Pomóż mi"
✅ "Zaimplementuj login system z JWT authentication"

### 2. Podawaj kontekst
❌ "Napraw bug"
✅ "Bug w login flow: error 500 when clicking submit with empty password"

### 3. Dziel na małe zadania
❌ "Zbuduj całą aplikację"
✅ "Zaimplementuj user registration endpoint"

### 4. Używaj właściwego agenta
- **@Tomasz** - kod
- **@Joanna** - design
- **@Anna** - testy
- **@Aleksander** - gdy nie wiesz kogo wybrać

---

## 🔍 FAQ

**Q: Czy mogę rozmawiać z wieloma agentami jednocześnie?**
A: Tak! Użyj @All, a Aleksander skoordynuje zespół.

**Q: Czy agenci pamiętają poprzednie rozmowy?**
A: Tak, wszystkie konwersacje są zapisywane w bazie danych (PostgreSQL).

**Q: Czy mogę eksportować historię rozmów?**
A: Nie w obecnej wersji (POC), ale będzie w przyszłości.

**Q: Czy agenci mogą tworzyć pliki?**
A: W POC - nie. W pełnej wersji - tak.

**Q: Czy mogę używać Destiny Chat UI dla własnych projektów?**
A: Tak! To jest właśnie cel - używaj agentów do budowania prawdziwych projektów.

---

## 📝 Best Practices

### 1. Rozpocznij od planu
Zacznij od @Aleksander lub @Magdalena, żeby ustalić plan.

### 2. Follow workflow
```
Requirements → Architecture → Design → Implementation → Testing → Deployment
```

### 3. Review przed deployment
Zawsze poproś @Anna o testy i @Michał o security review.

### 4. Dokumentuj
Zapisuj ważne decyzje i rozwiązania (Helena to zrobi automatycznie).

---

## 🆘 Potrzebujesz pomocy?

Napisz do:
- **@Aleksander** - general help
- **@Helena** - documentation
- Lub zobacz [Troubleshooting](../QUICK_START.md#troubleshooting)

---

**Happy chatting with Destiny Team!** 🚀

*Autor: Helena Kowalczyk (Knowledge Manager)*  
*Data: 2025-11-03*
