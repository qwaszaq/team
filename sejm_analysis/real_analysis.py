#!/usr/bin/env python3
"""
REAL Analysis - Sejm API
Prawdziwe dane, prawdziwa analiza!
"""

import requests
import json
import re
from collections import Counter
from datetime import datetime

BASE_URL = "https://api.sejm.gov.pl/sejm"

print("="*80)
print("🏛️  PRAWDZIWA ANALIZA KOMISJI SEJMU - ASW (2019-2023)")
print("="*80)
print()

# 1. Pobierz komisję
print("📊 Pobieranie danych komisji ASW...")
response = requests.get(f"{BASE_URL}/term9/committees/ASW")
committee = response.json()

print(f"✅ Komisja: {committee['name']}")
print(f"   Data powołania: {committee.get('appointmentDate', 'N/A')}")
print()

# 2. Pobierz WSZYSTKIE posiedzenia
print("📊 Pobieranie listy posiedzeń...")
response = requests.get(f"{BASE_URL}/term9/committees/ASW/sittings")
sittings = response.json()

print(f"✅ Pobrano {len(sittings)} posiedzeń")
print()

# 3. PRAWDZIWA ANALIZA
print("="*80)
print("📊 ANALIZA PODSTAWOWA")
print("="*80)
print()

# Analiza dat
dates = []
by_year = {}
by_month = {}

for sitting in sittings:
    date = sitting.get('date')
    if date:
        dates.append(date)
        year = date[:4]
        month = date[:7]
        by_year[year] = by_year.get(year, 0) + 1
        by_month[month] = by_month.get(month, 0) + 1

if dates:
    print(f"📅 Zakres dat: {min(dates)} do {max(dates)}")
    print()

print("📊 Posiedzenia po latach:")
for year in sorted(by_year.keys()):
    bar = "█" * (by_year[year] // 2)
    print(f"   {year}: {by_year[year]:3d} posiedzeń {bar}")

print()
print(f"Średnio: {len(sittings) / len(by_year):.1f} posiedzeń/rok")
print()

# Najaktywniejsze miesiące
top_months = sorted(by_month.items(), key=lambda x: x[1], reverse=True)[:5]
print("Najaktywniejsze miesiące:")
for month, count in top_months:
    print(f"   {month}: {count} posiedzeń")
print()

# 4. Analiza agendy (parsowanie HTML)
print("="*80)
print("📋 ANALIZA TEMATÓW")
print("="*80)
print()

all_agenda_text = []
for sitting in sittings:
    agenda = sitting.get('agenda', '')
    if agenda:
        # Usuń HTML tags
        clean_text = re.sub(r'<[^>]+>', ' ', agenda)
        clean_text = clean_text.strip()
        all_agenda_text.append(clean_text)

print(f"Posiedzenia z agendą: {len(all_agenda_text)}")
print()

# Ekstraktuj słowa kluczowe
all_words = []
for text in all_agenda_text:
    # Znajdź istotne słowa (> 4 znaki)
    words = re.findall(r'\b[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]{5,}\b', text)
    all_words.extend([w.lower() for w in words if w not in ['komisji', 'posiedzenie', 'przedstawia']])

word_freq = Counter(all_words)
top_words = word_freq.most_common(30)

print("30 najczęstszych słów kluczowych:")
for i, (word, count) in enumerate(top_words, 1):
    print(f"   {i:2d}. {word:20s} ({count:3d} wystąpień)")

print()

# 5. Przykładowe tematy
print("="*80)
print("📝 PRZYKŁADOWE TEMATY POSIEDZEŃ (pierwsze 10)")
print("="*80)
print()

for i, text in enumerate(all_agenda_text[:10], 1):
    # Skróć do 100 znaków
    short = text[:120] + "..." if len(text) > 120 else text
    print(f"{i:2d}. {short}")

print()

# 6. Analiza statusu i trybu
print("="*80)
print("📊 TRYB I STATUS POSIEDZEŃ")
print("="*80)
print()

status_count = Counter([s.get('status') for s in sittings if s.get('status')])
remote_count = sum(1 for s in sittings if s.get('remote'))
video_count = sum(1 for s in sittings if s.get('video'))

print(f"Status posiedzeń:")
for status, count in status_count.items():
    print(f"   {status}: {count}")
print()

print(f"Posiedzenia zdalne (COVID): {remote_count} ({remote_count/len(sittings)*100:.1f}%)")
print(f"Posiedzenia z nagraniem video: {video_count} ({video_count/len(sittings)*100:.1f}%)")
print()

# 7. Analiza czasu trwania
durations = []
for sitting in sittings:
    start = sitting.get('startDateTime')
    end = sitting.get('endDateTime')
    
    if start and end:
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            duration = (end_dt - start_dt).total_seconds() / 3600
            durations.append(duration)
        except:
            pass

if durations:
    print("="*80)
    print("⏱️  CZAS TRWANIA POSIEDZEŃ")
    print("="*80)
    print()
    print(f"Posiedzeń z danymi o czasie: {len(durations)}")
    print(f"Średni czas: {sum(durations)/len(durations):.1f} godziny")
    print(f"Najkrótsze: {min(durations):.1f}h")
    print(f"Najdłuższe: {max(durations):.1f}h")
    print()

# 8. Zapisz wyniki
output = {
    "committee": committee,
    "term": 9,
    "analysis_date": datetime.now().isoformat(),
    "statistics": {
        "total_sittings": len(sittings),
        "date_range": {"start": min(dates), "end": max(dates)} if dates else {},
        "by_year": by_year,
        "avg_per_year": len(sittings) / len(by_year) if by_year else 0,
        "remote_meetings": remote_count,
        "with_video": video_count,
        "avg_duration_hours": sum(durations)/len(durations) if durations else 0
    },
    "top_keywords": [{"word": w, "count": c} for w, c in top_words[:30]],
    "sample_agendas": all_agenda_text[:20],
    "all_sittings": sittings[:10]  # Pierwsze 10 dla próbki
}

with open("sejm_asw_complete_analysis.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("="*80)
print("✅ ANALIZA ZAKOŃCZONA")
print("="*80)
print()
print(f"📄 Kompletne dane zapisane: sejm_asw_complete_analysis.json")
print(f"📊 Przeanalizowano wszystkie {len(sittings)} posiedzeń")
print(f"🔍 Wyekstraktowano {len(all_words)} słów kluczowych")
print()
