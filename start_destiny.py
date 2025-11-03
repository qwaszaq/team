#!/usr/bin/env python3
"""
🎯 DESTINY TEAM - Simple Interactive Chat
Prosty sposób na rozmowę z zespołem AI w terminalu

Użycie:
    python start_destiny.py
"""

import sys
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path

from master_orchestrator import MasterOrchestrator
from postgres_context_store import PostgresContextStore, StoredMessage


class DestinyChat:
    """Prosty interfejs chat do rozmowy z zespołem"""
    
    def __init__(self):
        self.project_id: Optional[str] = None
        self.project_name: Optional[str] = None
        self.orchestrator: Optional[MasterOrchestrator] = None
        self.postgres: Optional[PostgresContextStore] = None
        
    def initialize_system(self):
        """Inicjalizacja wszystkich warstw"""
        print("\n🚀 Inicjalizacja Destiny Team...")
        print()
        
        try:
            self.orchestrator = MasterOrchestrator(
                postgres_conn="dbname=destiny_team user=user password=password host=localhost port=5432",
                neo4j_uri="bolt://localhost:7687",
                neo4j_user="neo4j",
                neo4j_password="password",
                qdrant_url="http://localhost:6333",
                redis_host="localhost",
                redis_port=6379,
                lmstudio_url="http://localhost:1234/v1"
            )
            
            self.postgres = self.orchestrator.postgres
            
            print("✅ System gotowy!")
            return True
            
        except Exception as e:
            print(f"❌ Błąd inicjalizacji: {e}")
            print("\nSprawdź czy Docker kontenery działają:")
            print("  docker ps | grep -E 'postgres|neo4j|redis|qdrant'")
            return False
    
    def select_or_create_project(self):
        """Wybór lub utworzenie projektu"""
        print("\n" + "="*70)
        print("  📋 PROJEKT")
        print("="*70)
        print()
        
        # Pokaż istniejące projekty
        try:
            with self.postgres.conn.cursor() as cur:
                cur.execute("""
                    SELECT project_id, project_name, created_at 
                    FROM projects 
                    ORDER BY created_at DESC 
                    LIMIT 10
                """)
                projects = cur.fetchall()
                
            if projects:
                print("📁 Istniejące projekty:")
                for i, (pid, pname, created) in enumerate(projects, 1):
                    print(f"  {i}. {pname} (ID: {pid[:20]}...)")
                print()
        except Exception:
            projects = []
        
        print("Opcje:")
        print("  [ENTER] - Nowy projekt")
        if projects:
            print("  [1-9]   - Wybierz istniejący projekt")
        print()
        
        choice = input("Wybór: ").strip()
        
        if choice.isdigit() and projects and 1 <= int(choice) <= len(projects):
            # Wybrano istniejący projekt
            idx = int(choice) - 1
            self.project_id = projects[idx][0]
            self.project_name = projects[idx][1]
            print(f"\n✅ Wybrany projekt: {self.project_name}")
            
        else:
            # Nowy projekt
            print()
            name = input("Nazwa nowego projektu: ").strip()
            if not name:
                name = "Untitled Project"
            
            desc = input("Krótki opis (opcjonalnie): ").strip()
            if not desc:
                desc = f"Projekt utworzony {datetime.now().strftime('%Y-%m-%d')}"
            
            self.project_id = f"project-{uuid.uuid4().hex[:8]}"
            self.project_name = name
            
            print(f"\n🔧 Tworzenie projektu '{name}'...")
            success = self.orchestrator.create_project(
                self.project_id,
                name,
                desc
            )
            
            if success:
                print(f"✅ Projekt utworzony! ID: {self.project_id}")
            else:
                print("❌ Nie udało się utworzyć projektu")
                return False
        
        return True
    
    def show_welcome(self):
        """Powitanie"""
        print("\n" + "🌟 "*35)
        print(f"  DESTINY TEAM - Projekt: {self.project_name}")
        print("🌟 "*35)
        print()
        print("👥 Twój zespół (9 agentów AI):")
        print("   🎯 Aleksander Nowak - Orchestrator")
        print("   📚 Dr. Helena Kowalczyk - Knowledge Manager")
        print("   📋 Magdalena Kowalska - Product Manager")
        print("   🏗️ Katarzyna Wiśniewska - Architect")
        print("   💻 Tomasz Zieliński - Developer")
        print("   🧪 Anna Nowakowska - QA Engineer")
        print("   🚀 Piotr Szymański - DevOps Engineer")
        print("   🔒 Michał Dąbrowski - Security Specialist")
        print("   📊 Dr. Joanna Wójcik - Data Scientist")
        print()
        print("💡 Jak używać:")
        print("   • Pisz normalnie, jakbyś rozmawiał z zespołem")
        print("   • Zadawaj pytania, dawaj polecenia, omawiaj decyzje")
        print("   • Wszystko jest automatycznie zapisywane")
        print("   • Wpisz 'exit' lub 'quit' aby zakończyć")
        print("   • Ctrl+C też działa")
        print()
        print("="*70)
        print()
    
    def get_team_response(self, user_message: str) -> str:
        """
        Symulacja odpowiedzi zespołu.
        
        W pełnej wersji tutaj byłaby integracja z prawdziwymi AI modelami.
        Na razie - inteligentna symulacja bazująca na kontekście.
        """
        
        # Zapisz wiadomość użytkownika
        msg = StoredMessage(
            id=f"user-{uuid.uuid4().hex[:8]}",
            project_id=self.project_id,
            sender="Artur (You)",
            recipient=None,
            message_type="REQUEST",
            content=user_message,
            context={},
            timestamp=datetime.now(),
            importance=0.8
        )
        self.postgres.store_message(msg)
        
        # Proste dopasowanie intencji
        message_lower = user_message.lower()
        
        # Decyzje architektoniczne
        if any(word in message_lower for word in ['baza', 'database', 'postgresql', 'mongodb']):
            response = """
🏗️ Katarzyna Wiśniewska (Architect):

Rozważałam opcje baz danych dla naszego projektu:

📊 Opcje:
1. PostgreSQL - ACID compliance, relacyjna, sprawdzona
2. MongoDB - NoSQL, elastyczna, dobra dla dynamicznych schematów
3. MySQL - stabilna, szeroko używana

💡 Moja rekomendacja: PostgreSQL
Powody:
• Transakcje ACID - ważne dla spójności danych
• Zaawansowane funkcje (JSONB, full-text search)
• Dojrzała i stabilna
• Świetna dokumentacja i community

Co myślisz? Czy PostgreSQL pasuje do Twoich potrzeb?
"""
            agent = "Katarzyna Wiśniewska"
            
        # Security
        elif any(word in message_lower for word in ['bezpieczeństwo', 'security', 'auth', 'login']):
            response = """
🔒 Michał Dąbrowski (Security):

Kwestie bezpieczeństwa są kluczowe. Oto moja analiza:

🔐 Podstawy bezpieczeństwa:
1. Autentykacja: OAuth 2.0 + JWT tokens
2. Szyfrowanie: HTTPS (TLS 1.3) dla wszystkich połączeń
3. Rate limiting: Ochrona przed brute force
4. Input validation: Zapobieganie SQL injection, XSS
5. Password hashing: bcrypt lub Argon2

⚠️ Krytyczne:
• Nigdy nie przechowuj plaintext passwords
• Implementuj 2FA dla wrażliwych operacji
• Regularnie aktualizuj dependencies
• Log wszystkie security events

Chcesz żebym przygotował szczegółowy security checklist?
"""
            agent = "Michał Dąbrowski"
            
        # Requirements / Product
        elif any(word in message_lower for word in ['funkcje', 'features', 'wymagania', 'requirements']):
            response = """
📋 Magdalena Kowalska (Product Manager):

Świetnie! Porozmawiajmy o wymaganiach projektu.

❓ Kluczowe pytania:
1. Kto jest głównym użytkownikiem? (persona)
2. Jaki problem rozwiązujemy?
3. Must-have vs Nice-to-have features?
4. Timeline i budżet?

📝 Zacznijmy od MVP (Minimum Viable Product):
• Jakie 3-5 funkcji są absolutnie niezbędne?
• Co możemy dodać w kolejnej iteracji?

Opowiedz mi więcej o wizji projektu, a pomogę zdefiniować scope!
"""
            agent = "Magdalena Kowalska"
            
        # Development / Implementation
        elif any(word in message_lower for word in ['kod', 'code', 'implement', 'zaimplementuj']):
            response = """
💻 Tomasz Zieliński (Developer):

Jestem gotowy do implementacji!

🛠️ Mój process:
1. Rozumienie wymagań (co dokładnie budujemy?)
2. Design API/struktury
3. Implementacja + unit tests
4. Code review ready code
5. Dokumentacja

📚 Stack którym się zajmuję:
• Backend: Python (Flask/FastAPI), Node.js
• Frontend: React, Vue
• Database: SQL queries, ORMs
• DevOps: Docker, basic CI/CD

Czym mam się zająć? Daj mi konkretne zadanie, a zacznę kodować!
"""
            agent = "Tomasz Zieliński"
            
        # Testing
        elif any(word in message_lower for word in ['test', 'quality', 'qa', 'bug']):
            response = """
🧪 Anna Nowakowska (QA Engineer):

Testing to moja specjalność!

✅ Co testuję:
• Functional testing - czy działa zgodnie z spec
• Edge cases - nietypowe scenariusze
• Performance - czy jest wystarczająco szybkie
• Security - podstawowe testy bezpieczeństwa
• User experience - czy jest intuicyjne

📋 Mój plan testowy obejmuje:
1. Unit tests (developer responsibility)
2. Integration tests (moja strefa)
3. E2E tests (user flows)
4. Manual exploratory testing

Kiedy coś będzie gotowe do testowania, dam Ci feedback!
"""
            agent = "Anna Nowakowska"
            
        # Deployment / DevOps
        elif any(word in message_lower for word in ['deploy', 'produkcja', 'production', 'server']):
            response = """
🚀 Piotr Szymański (DevOps):

Deployment? Moja działka!

🔧 Co setupuję:
• CI/CD pipeline (automatyczne deployment)
• Docker containers (łatwe skalowanie)
• Monitoring i logging (wiemy co się dzieje)
• Backup strategy (bezpieczeństwo danych)

☁️ Hosting opcje:
1. AWS (wszechstronny, droższy)
2. DigitalOcean (prosty, tańszy)
3. Railway/Render (najszybszy start)

🎯 Dla startu polecam:
Docker Compose lokalnie → potem Railway dla MVP → jak rośniemy to AWS

Chcesz żebym przygotował deployment plan?
"""
            agent = "Piotr Szymański"
            
        # Data / Analytics
        elif any(word in message_lower for word in ['data', 'analiza', 'analytics', 'ml', 'ai']):
            response = """
📊 Dr. Joanna Wójcik (Data Scientist):

Dane to moja pasja!

🔬 Co mogę zrobić:
• Analiza danych (insights z istniejących danych)
• Predictive models (przewidywanie trendów)
• Data pipelines (ETL processes)
• Visualizations (dashboard, wykresy)

💡 Kiedy potrzeba ML/AI:
✅ Dużo danych historycznych
✅ Powtarzalne wzorce
✅ Jasny cel (co predykujemy?)
❌ Mało danych = simple rules lepsze niż ML

Jakie dane mamy? Co chcemy z nich wyciągnąć?
"""
            agent = "Dr. Joanna Wójcik"
            
        # Aleksander - Orchestrator (ogólne, koordynacja)
        elif any(word in message_lower for word in ['plan', 'team', 'następny', 'co dalej', 'help']):
            response = """
🎯 Aleksander Nowak (Orchestrator):

Cześć! Koordynuję nasz zespół.

📋 Co mogę dla Ciebie zrobić:
• Pomóc zaplanować projekt (roadmap, milestones)
• Rozdzielić zadania między agentów
• Rozwiązać konflikty w zespole
• Podsumować status projektu

👥 Zespół jest gotowy! Mogę:
1. Zapytać Product Manager o requirements
2. Poprosić Architect o design systemu
3. Zlecić Developerowi implementację
4. Koordynować testing i deployment

Po prostu powiedz mi czego potrzebujesz, a zadbam żeby odpowiedni agent się tym zajął!
"""
            agent = "Aleksander Nowak"
            
        # Helena - Documentation (gdy pytają o historię, decyzje)
        elif any(word in message_lower for word in ['historia', 'history', 'decyzj', 'decision', 'dlaczego']):
            response = """
📚 Dr. Helena Kowalczyk (Knowledge Manager):

Wszystko dokumentuję i pamiętam!

📖 Mogę Ci pokazać:
• Historia projektu (wszystkie wiadomości)
• Decyzje i ich uzasadnienia (dlaczego tak wybraliśmy)
• Kluczowe momenty (milestones)
• Status obecny (gdzie jesteśmy)

🔍 Mogę też:
• Szukać w historii ("co mówiliśmy o bazie danych?")
• Generować raporty (tygodniowe podsumowanie)
• Przypominać o uzgodnieniach

Czego szukasz w historii projektu?
"""
            agent = "Dr. Helena Kowalczyk"
            
        # Default - Aleksander jako coordinator
        else:
            response = f"""
🎯 Aleksander Nowak (Orchestrator):

Rozumiem. Rozważmy to z zespołem.

Twoja wiadomość: "{user_message}"

Mogę:
1. Zapytać konkretnego agenta o opinię
2. Zorganizować krótką dyskusję zespołu
3. Pomóc doprecyzować potrzeby

💡 Wskazówka: Możesz bezpośrednio zwrócić się do agenta, np:
• "Katarzyna, jaka architektura?"
• "Tomasz, zaimplementuj auth"
• "Magdalena, jakie są wymagania?"

Co chcesz żebyśmy zrobili?
"""
            agent = "Aleksander Nowak"
        
        # Zapisz odpowiedź
        response_msg = StoredMessage(
            id=f"agent-{uuid.uuid4().hex[:8]}",
            project_id=self.project_id,
            sender=agent,
            recipient="Artur (You)",
            message_type="RESPONSE",
            content=response,
            context={"responding_to": user_message},
            timestamp=datetime.now(),
            importance=0.7
        )
        self.postgres.store_message(response_msg)
        
        return response
    
    def chat_loop(self):
        """Główna pętla rozmowy"""
        print("💬 Zacznij rozmowę z zespołem!\n")
        
        message_count = 0
        
        try:
            while True:
                # Prompt użytkownika
                user_input = input("\n📝 Ty: ").strip()
                
                if not user_input:
                    continue
                
                # Sprawdź exit
                if user_input.lower() in ['exit', 'quit', 'bye', 'koniec']:
                    print("\n👋 Kończę sesję...")
                    self.save_and_exit()
                    break
                
                # Specjalne komendy
                if user_input.lower() == 'help':
                    print("\n💡 Dostępne komendy:")
                    print("   • Pisz normalnie - zespół odpowie")
                    print("   • 'status' - pokaż status projektu")
                    print("   • 'history' - ostatnie wiadomości")
                    print("   • 'exit' - zakończ")
                    continue
                
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                    
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                # Normalny chat - zespół odpowiada
                print("\n🤔 (Zespół myśli...)")
                response = self.get_team_response(user_input)
                print(response)
                
                message_count += 1
                
                # Co 5 wiadomości - podpowiedź o zapisie
                if message_count % 5 == 0:
                    print("\n💾 Zapisano automatycznie w bazie danych")
                
        except KeyboardInterrupt:
            print("\n\n👋 Przerwano (Ctrl+C)")
            self.save_and_exit()
    
    def show_status(self):
        """Pokaż status projektu"""
        print("\n📊 STATUS PROJEKTU")
        print("="*70)
        
        try:
            with self.postgres.conn.cursor() as cur:
                # Liczba wiadomości
                cur.execute("""
                    SELECT COUNT(*) FROM messages WHERE project_id = %s
                """, (self.project_id,))
                msg_count = cur.fetchone()[0]
                
                # Ostatnia aktywność
                cur.execute("""
                    SELECT sender, content, timestamp 
                    FROM messages 
                    WHERE project_id = %s 
                    ORDER BY timestamp DESC LIMIT 1
                """, (self.project_id,))
                last = cur.fetchone()
                
                print(f"Projekt: {self.project_name}")
                print(f"ID: {self.project_id}")
                print(f"Wiadomości: {msg_count}")
                if last:
                    print(f"Ostatnia aktywność: {last[2].strftime('%Y-%m-%d %H:%M')}")
                    print(f"  {last[0]}: {last[1][:60]}...")
                print("="*70)
        except Exception as e:
            print(f"Błąd: {e}")
    
    def show_history(self, limit=5):
        """Pokaż ostatnie wiadomości"""
        print(f"\n📜 OSTATNIE {limit} WIADOMOŚCI")
        print("="*70)
        
        try:
            with self.postgres.conn.cursor() as cur:
                cur.execute("""
                    SELECT sender, content, timestamp 
                    FROM messages 
                    WHERE project_id = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (self.project_id, limit))
                
                messages = cur.fetchall()
                
                for sender, content, ts in reversed(messages):
                    print(f"\n[{ts.strftime('%H:%M')}] {sender}:")
                    # Pokaż pierwsze 100 znaków
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"  {preview}")
                
                print("="*70)
        except Exception as e:
            print(f"Błąd: {e}")
    
    def save_and_exit(self):
        """Zapisz i zakończ"""
        print("\n📚 Dr. Helena Kowalczyk:")
        print("   Zapisuję podsumowanie sesji...")
        
        try:
            # Podsumowanie sesji
            with self.postgres.conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM messages 
                    WHERE project_id = %s 
                    AND timestamp > NOW() - INTERVAL '1 hour'
                """, (self.project_id,))
                recent = cur.fetchone()[0]
            
            print(f"   ✅ Zapisano {recent} wiadomości z tej sesji")
            print(f"   ✅ Wszystko w bazie danych")
            print(f"   ✅ Możesz wrócić w każdej chwili")
            
        except Exception as e:
            print(f"   ⚠️  Błąd zapisu: {e}")
        
        print("\n✨ Do zobaczenia! Projekt: " + self.project_name)
        print()


def main():
    """Main entry point"""
    print("\n" + "🌟 "*35)
    print("  ✨ DESTINY TEAM - Interactive Chat ✨")
    print("🌟 "*35)
    
    chat = DestinyChat()
    
    # 1. Initialize
    if not chat.initialize_system():
        print("\n❌ Nie można uruchomić systemu")
        sys.exit(1)
    
    # 2. Select/Create project
    if not chat.select_or_create_project():
        print("\n❌ Nie można otworzyć projektu")
        sys.exit(1)
    
    # 3. Welcome
    chat.show_welcome()
    
    # 4. Chat loop
    chat.chat_loop()


if __name__ == "__main__":
    main()
