#!/usr/bin/env python3
"""
Demo wyszukiwania semantycznego w Qdrant
"""
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# Wyszukaj dokumenty o "użyciu systemu"
print("🔍 Wyszukuję: 'jak używać systemu destiny'")
print("=" * 60)

results = client.search(
    collection_name="destiny-team-framework-master",
    query_text="jak używać systemu destiny",
    limit=5
)

for i, result in enumerate(results, 1):
    print(f"\n{i}. {result.payload.get('title', 'Bez tytułu')}")
    print(f"   📊 Trafność: {result.score:.3f}")
    print(f"   📁 Plik: {result.payload.get('file_path', 'Unknown')}")
    print(f"   📝 Preview: {result.payload.get('content_preview', '')[:150]}...")

print("\n" + "=" * 60)
print(f"✅ Znaleziono {len(results)} dokumentów!")
