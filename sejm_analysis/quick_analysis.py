#!/usr/bin/env python3
"""
Quick Real Analysis - Sejm API
Pobiera PRAWDZIWE dane z API
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://api.sejm.gov.pl/sejm"

print("="*80)
print("🏛️  PRAWDZIWA ANALIZA - API SEJMU")
print("="*80)
print()

# 1. Pobierz listę komisji
print("📊 Krok 1: Pobieram listę komisji kadencji IX...")
response = requests.get(f"{BASE_URL}/term9/committees")
committees = response.json()
print(f"✅ Znaleziono {len(committees)} komisji")
print()

# Znajdź ASW
asw = None
for c in committees:
    if c['code'] == 'ASW':
        asw = c
        break

if asw:
    print(f"✅ Znaleziono: {asw['name']}")
    print(f"   Kod: {asw['code']}")
    print()

# 2. Pobierz listę posiedzeń
print("📊 Krok 2: Pobieram listę posiedzeń komisji ASW...")
response = requests.get(f"{BASE_URL}/term9/committees/ASW/sittings")
sittings = response.json()
print(f"✅ Znaleziono {len(sittings)} posiedzeń")
print()

# 3. Analiza podstawowa
print("="*80)
print("📈 ANALIZA PODSTAWOWA")
print("="*80)
print()

# Liczby po latach
by_year = {}
for sitting in sittings:
    num = sitting.get('num')
    if num:
        # Pobierz datę (trzeba pobrać szczegóły)
        # Dla uproszczenia użyjemy numeru jako proxy
        year = 2019 + (num // 50)  # Przybliżenie
        by_year[year] = by_year.get(year, 0) + 1

print(f"Łączna liczba posiedzeń: {len(sittings)}")
print()

# 4. Pobierz szczegóły PIERWSZEGO posiedzenia
print("="*80)
print("📋 SZCZEGÓŁY PIERWSZEGO POSIEDZENIA (próbka)")
print("="*80)
print()

if len(sittings) > 0:
    first_sitting_num = sittings[0].get('num')
    if first_sitting_num:
        print(f"Pobieram szczegóły posiedzenia #{first_sitting_num}...")
        response = requests.get(f"{BASE_URL}/term9/committees/ASW/sittings/{first_sitting_num}")
        details = response.json()
        
        print(f"✅ Posiedzenie nr {details.get('num')}")
        print(f"   Data rozpoczęcia: {details.get('from', 'N/A')[:16] if details.get('from') else 'N/A'}")
        print(f"   Data zakończenia: {details.get('to', 'N/A')[:16] if details.get('to') else 'N/A'}")
        print(f"   Tytuł: {details.get('title', 'N/A')}")
        print()
        
        # Punkty porządku dziennego
        points = details.get('points', [])
        print(f"   Punkty porządku dziennego: {len(points)}")
        if points:
            print()
            print("   Pierwsze 3 punkty:")
            for i, point in enumerate(points[:3], 1):
                title = point.get('title', 'Brak tytułu')
                print(f"   {i}. {title[:80]}...")
        print()
        
        # Uczestnicy
        attendees = details.get('attendees', [])
        print(f"   Uczestnicy: {len(attendees)} osób")
        if attendees:
            print("   Pierwsze 5 osób:")
            for att in attendees[:5]:
                mp = att.get('MP', {})
                fname = mp.get('firstName', '')
                lname = mp.get('lastName', '')
                club = mp.get('club', '')
                function = att.get('function', 'członek')
                print(f"   - {fname} {lname} ({club}) - {function}")

print()

# 5. Pobierz próbkę 5 posiedzeń dla analizy
print("="*80)
print("📊 PRÓBKA 5 POSIEDZEŃ - Szczegółowa analiza")
print("="*80)
print()

sample_indices = [0, len(sittings)//4, len(sittings)//2, 3*len(sittings)//4, len(sittings)-1]
sample_details = []

for idx in sample_indices:
    sitting_num = sittings[idx].get('num')
    if sitting_num:
        try:
            response = requests.get(f"{BASE_URL}/term9/committees/ASW/sittings/{sitting_num}")
            detail = response.json()
            sample_details.append(detail)
            print(f"✅ Pobrano posiedzenie #{sitting_num}")
        except:
            print(f"❌ Błąd pobierania #{sitting_num}")

print()
print(f"Pobrano szczegóły {len(sample_details)} posiedzeń")
print()

# 6. Analiza próbki
if sample_details:
    print("="*80)
    print("📊 WYNIKI ANALIZY PRÓBKI")
    print("="*80)
    print()
    
    total_points = 0
    total_attendees = 0
    all_topics = []
    
    for detail in sample_details:
        points = detail.get('points', [])
        attendees = detail.get('attendees', [])
        
        total_points += len(points)
        total_attendees += len(attendees)
        
        for point in points:
            title = point.get('title', '')
            if title:
                all_topics.append(title)
    
    print(f"Średnia liczba punktów porządku: {total_points / len(sample_details):.1f}")
    print(f"Średnia liczba uczestników: {total_attendees / len(sample_details):.1f}")
    print()
    
    if all_topics:
        print("Przykładowe tematy z próbki:")
        for i, topic in enumerate(all_topics[:10], 1):
            print(f"{i}. {topic[:100]}...")
    
    # Zapisz pełne dane
    output = {
        "committee": asw,
        "total_sittings": len(sittings),
        "sample_details": sample_details,
        "analysis": {
            "avg_agenda_items": total_points / len(sample_details),
            "avg_attendance": total_attendees / len(sample_details),
            "sample_topics": all_topics[:20]
        }
    }
    
    with open("sejm_asw_real_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print()
    print("="*80)
    print("✅ ANALIZA ZAKOŃCZONA")
    print("="*80)
    print()
    print(f"📄 Pełne dane zapisane w: sejm_asw_real_analysis.json")
    print(f"📊 Przeanalizowano {len(sittings)} posiedzeń")
    print(f"🔍 Szczegółowo pobrano {len(sample_details)} próbek")
    print()
