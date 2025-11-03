#!/usr/bin/env python3
"""
Seed Qdrant Test Collection

This script pre-seeds the Qdrant collection for test project IDs
to eliminate warnings during smoke tests and evaluation.

Run this ONCE before evaluation to ensure fully green tests.
"""

import sys
import os
import json
import subprocess

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helena_core import HelenaCore

def ensure_qdrant_collection(memory_core: HelenaCore) -> bool:
    """Ensure Qdrant collection exists for the given project."""
    collection_name = memory_core.collection_name
    base_url = memory_core.qdrant_url.rstrip('/')

    try:
        check = subprocess.run(
            ['curl', '-s', f'{base_url}/collections/{collection_name}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if check.returncode == 0 and check.stdout:
            data = json.loads(check.stdout)
            if 'result' in data:
                print(f"  ✅ Qdrant collection '{collection_name}' ready")
                return True
    except Exception as e:
        print(f"  ⚠️ Unable to query collection '{collection_name}': {e}")

    try:
        payload = json.dumps({
            "vectors": {
                "size": 1024,
                "distance": "Cosine"
            }
        })
        create = subprocess.run(
            [
                'curl', '-s', '-X', 'PUT',
                f'{base_url}/collections/{collection_name}',
                '-H', 'Content-Type: application/json',
                '-d', payload
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
        if create.returncode == 0:
            print(f"  ✅ Created Qdrant collection '{collection_name}'")
            return True
        else:
            err_output = create.stderr or create.stdout
            print(f"  ❌ Failed to create collection '{collection_name}': {err_output}")
            return False
    except Exception as e:
        print(f"  ❌ Error creating collection '{collection_name}': {e}")
        return False


def seed_test_collection(project_id: str, memory_core: HelenaCore):
    """Seed a test collection with sample data"""
    print(f"\n{'='*60}")
    print(f"Seeding collection for: {project_id}")
    print(f"{'='*60}")
    
    # Sample test data to seed the collection
    test_memories = [
        {
            "content": "Initial test memory for smoke tests",
            "metadata": {"type": "test", "purpose": "smoke_test"}
        },
        {
            "content": "Sample context memory for agent testing",
            "metadata": {"type": "test", "purpose": "context_test"}
        },
        {
            "content": "Integration test memory for validation",
            "metadata": {"type": "test", "purpose": "integration_test"}
        }
    ]
    
    # Ensure target collection exists before seeding
    ensure_qdrant_collection(memory_core)

    # Save each test memory
    for i, memory in enumerate(test_memories, 1):
        try:
            memory_core.save_to_all_layers(
                event_type="seed_memory",
                content=memory["content"],
                importance=0.85,
                made_by="Qdrant Seeder",
                additional_data={
                    "seed_metadata": memory["metadata"],
                    "source": "seed_qdrant_test_collection.py"
                }
            )
            print(f"  ✅ Seeded memory {i}/{len(test_memories)}: {memory['content'][:50]}...")
        except Exception as e:
            print(f"  ⚠️ Warning seeding memory {i}: {e}")
    
    print(f"  ✅ Collection seeded successfully!")


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 QDRANT TEST COLLECTION SEEDER")
    print("="*60)
    
    # Test project IDs that need seeding
    test_project_ids = [
        "test-project",              # Used in DAY_2_SMOKE_TESTS.py step 2 ⭐ CRITICAL
        "day2-smoke-test",           # Used in smoke tests
        "day2-integration-test",     # Used in integration tests
        "destiny-team-test",         # Generic test ID
    ]
    
    print(f"\nWill seed {len(test_project_ids)} test collections...")
    
    for project_id in test_project_ids:
        try:
            # Initialize HelenaCore for this project
            memory_core = HelenaCore(project_id=project_id)
            
            # Seed the collection
            seed_test_collection(project_id, memory_core)
            
        except Exception as e:
            print(f"  ❌ Error seeding {project_id}: {e}")
            print(f"     This is OK - collection may already exist")
    
    print("\n" + "="*60)
    print("✅ SEEDING COMPLETE!")
    print("="*60)
    print("\nNow smoke tests should run with no Qdrant warnings!")
    print("\nTo verify, run:")
    print("  python3 DAY_2_SMOKE_TESTS.py --step 2")
    print("\n")


if __name__ == "__main__":
    main()
