#!/usr/bin/env python3
"""
CONTEXT CAPACITY TEST - Verify Core Value Proposition

Tests the claim: "Multi-layer multi-agent system enlarges context 
far above 1M tokens through independent agent contexts"

This test answers:
1. Does each agent have independent context?
2. What's the total context capacity?
3. Is it actually >1M tokens?
4. How does it compare to single-agent systems?
"""

import psycopg2
import subprocess
import json
from typing import Dict, List

class ContextCapacityTest:
    """Test and measure total context capacity of the system"""
    
    def __init__(self):
        self.postgres_conn = "dbname=destiny_team user=user password=password host=localhost port=5432"
        self.project_id = "destiny-team-framework-master"
        
    def test_agent_context_isolation(self) -> Dict:
        """
        Test 1: Verify each agent has independent context storage
        
        Expected: agent_contexts table with separate entries per agent
        """
        print("\n" + "="*80)
        print("TEST 1: Agent Context Isolation")
        print("="*80)
        
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            # Check if agent_contexts table exists
            cur.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_name = 'agent_contexts'
            """)
            
            if cur.fetchone()[0] == 0:
                print("❌ FAIL: agent_contexts table doesn't exist")
                return {"passed": False, "score": 0, "reason": "No agent context table"}
            
            # Check for multiple agents with contexts
            cur.execute("""
                SELECT agent_name, COUNT(*) as context_items
                FROM agent_contexts
                WHERE project_id = %s
                GROUP BY agent_name
                ORDER BY agent_name
            """, (self.project_id,))
            
            agents = cur.fetchall()
            
            print(f"\n📊 Agents with independent contexts:")
            for agent, count in agents:
                print(f"  • {agent}: {count} context items")
            
            if len(agents) >= 3:
                print(f"\n✅ PASS: {len(agents)} agents have independent contexts")
                score = min(len(agents) * 10, 30)  # Up to 30 points
                return {
                    "passed": True,
                    "score": score,
                    "agent_count": len(agents),
                    "agents": [a[0] for a in agents]
                }
            else:
                print(f"\n⚠️  PARTIAL: Only {len(agents)} agents have contexts (expected 3+)")
                return {
                    "passed": False,
                    "score": len(agents) * 5,
                    "agent_count": len(agents)
                }
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return {"passed": False, "score": 0, "error": str(e)}
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    
    def measure_postgresql_context(self) -> Dict:
        """
        Measure context capacity in PostgreSQL
        
        Includes:
        - Decisions (with rationale, context)
        - Messages (team communication)
        - Agent-specific contexts
        """
        print("\n" + "="*80)
        print("TEST 2: PostgreSQL Context Capacity")
        print("="*80)
        
        try:
            conn = psycopg2.connect(self.postgres_conn)
            cur = conn.cursor()
            
            # Get all text content from decisions
            cur.execute("""
                SELECT 
                    decision_text,
                    context::text
                FROM decisions
                WHERE project_id = %s
            """, (self.project_id,))
            
            decisions = cur.fetchall()
            decision_chars = sum(
                len(d[0] or '') + len(d[1] or '') 
                for d in decisions
            )
            
            # Get all messages
            cur.execute("""
                SELECT content
                FROM messages
                WHERE project_id = %s
            """, (self.project_id,))
            
            messages = cur.fetchall()
            message_chars = sum(len(m[0] or '') for m in messages)
            
            # Get agent contexts
            cur.execute("""
                SELECT context_value::text
                FROM agent_contexts
                WHERE project_id = %s
            """, (self.project_id,))
            
            contexts = cur.fetchall()
            context_chars = sum(len(c[0] or '') for c in contexts)
            
            total_chars = decision_chars + message_chars + context_chars
            # Rough estimate: 4 chars per token
            estimated_tokens = total_chars / 4
            
            print(f"\n📊 PostgreSQL Context:")
            print(f"  Decisions: {len(decisions)} records ({decision_chars:,} chars)")
            print(f"  Messages: {len(messages)} records ({message_chars:,} chars)")
            print(f"  Agent contexts: {len(contexts)} records ({context_chars:,} chars)")
            print(f"  Total chars: {total_chars:,}")
            print(f"  Estimated tokens: {estimated_tokens:,.0f}")
            
            cur.close()
            conn.close()
            
            return {
                "source": "PostgreSQL",
                "chars": total_chars,
                "tokens": estimated_tokens,
                "records": len(decisions) + len(messages) + len(contexts)
            }
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return {"source": "PostgreSQL", "chars": 0, "tokens": 0, "error": str(e)}
    
    def measure_neo4j_context(self) -> Dict:
        """
        Measure context in Neo4j (decision chains, reasoning)
        """
        print("\n" + "="*80)
        print("TEST 3: Neo4j Context Capacity (Decision Chains)")
        print("="*80)
        
        try:
            # Count nodes and get sample of text
            cypher = """
            MATCH (n)
            WHERE n.text IS NOT NULL OR n.name IS NOT NULL
            RETURN 
                labels(n)[0] as type,
                COALESCE(n.text, n.name, '') as content
            LIMIT 100
            """
            
            result = subprocess.run([
                'docker', 'exec', 'sms-neo4j',
                'cypher-shell', '-u', 'neo4j', '-p', 'password',
                '--format', 'plain',
                cypher
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Estimate based on sample
                lines = result.stdout.strip().split('\n')
                total_chars = sum(len(line) for line in lines)
                
                # Rough estimate (assuming 100 is representative sample)
                # Get actual node count
                count_result = subprocess.run([
                    'docker', 'exec', 'sms-neo4j',
                    'cypher-shell', '-u', 'neo4j', '-p', 'password',
                    '--format', 'plain',
                    'MATCH (n) RETURN count(n) as total'
                ], capture_output=True, text=True, timeout=10)
                
                node_count = 0
                if count_result.returncode == 0:
                    try:
                        node_count = int(count_result.stdout.strip().split('\n')[-1])
                    except:
                        node_count = 0
                
                # Extrapolate from sample
                avg_chars_per_node = total_chars / max(len(lines) - 1, 1)
                estimated_total_chars = int(avg_chars_per_node * node_count)
                estimated_tokens = estimated_total_chars / 4
                
                print(f"\n📊 Neo4j Context:")
                print(f"  Total nodes: {node_count}")
                print(f"  Sample chars: {total_chars:,}")
                print(f"  Estimated total chars: {estimated_total_chars:,}")
                print(f"  Estimated tokens: {estimated_tokens:,.0f}")
                
                return {
                    "source": "Neo4j",
                    "chars": estimated_total_chars,
                    "tokens": estimated_tokens,
                    "nodes": node_count
                }
            else:
                print("⚠️  Could not query Neo4j")
                return {"source": "Neo4j", "chars": 0, "tokens": 0}
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return {"source": "Neo4j", "chars": 0, "tokens": 0, "error": str(e)}
    
    def measure_qdrant_context(self) -> Dict:
        """
        Measure context in Qdrant (semantic embeddings + payloads)
        """
        print("\n" + "="*80)
        print("TEST 4: Qdrant Context Capacity (Embeddings + Payloads)")
        print("="*80)
        
        try:
            # Get collection info
            result = subprocess.run([
                'curl', '-s', f'http://localhost:6333/collections/{self.project_id}'
            ], capture_output=True, text=True, timeout=10)
            
            data = json.loads(result.stdout)
            points_count = data['result']['points_count']
            vector_size = data['result']['config']['params']['vectors']['size']
            
            # Get sample points to estimate payload size
            result = subprocess.run([
                'curl', '-s', '-X', 'POST',
                f'http://localhost:6333/collections/{self.project_id}/points/scroll',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({"limit": 10, "with_payload": True, "with_vector": False})
            ], capture_output=True, text=True, timeout=10)
            
            sample_data = json.loads(result.stdout)
            sample_points = sample_data['result']['points']
            
            # Estimate payload size
            total_payload_chars = 0
            for point in sample_points:
                payload_str = json.dumps(point.get('payload', {}))
                total_payload_chars += len(payload_str)
            
            avg_payload_chars = total_payload_chars / max(len(sample_points), 1)
            estimated_total_payload_chars = int(avg_payload_chars * points_count)
            
            # Vector storage (each vector is vector_size floats)
            # Not counted as "context" but important for capacity
            
            estimated_tokens = estimated_total_payload_chars / 4
            
            print(f"\n📊 Qdrant Context:")
            print(f"  Total points: {points_count}")
            print(f"  Vector size: {vector_size} dimensions")
            print(f"  Avg payload chars: {avg_payload_chars:.0f}")
            print(f"  Estimated total payload chars: {estimated_total_payload_chars:,}")
            print(f"  Estimated tokens: {estimated_tokens:,.0f}")
            
            return {
                "source": "Qdrant",
                "chars": estimated_total_payload_chars,
                "tokens": estimated_tokens,
                "points": points_count,
                "vector_size": vector_size
            }
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return {"source": "Qdrant", "chars": 0, "tokens": 0, "error": str(e)}
    
    def calculate_total_capacity(self, measurements: List[Dict]) -> Dict:
        """
        Calculate total system context capacity
        """
        print("\n" + "="*80)
        print("TEST 5: Total System Context Capacity")
        print("="*80)
        
        total_tokens = sum(m.get('tokens', 0) for m in measurements)
        total_chars = sum(m.get('chars', 0) for m in measurements)
        
        print(f"\n📊 Total Context Across All Layers:")
        print(f"  {'─'*60}")
        
        for m in measurements:
            source = m.get('source', 'Unknown')
            tokens = m.get('tokens', 0)
            print(f"  {source:20s}: {tokens:>12,.0f} tokens")
        
        print(f"  {'─'*60}")
        print(f"  {'TOTAL':20s}: {total_tokens:>12,.0f} tokens")
        print(f"  {'TOTAL CHARS':20s}: {total_chars:>12,} chars")
        
        # Compare to 1M token threshold
        print(f"\n📊 Comparison to Claim:")
        if total_tokens > 1_000_000:
            ratio = total_tokens / 1_000_000
            print(f"  ✅ EXCEEDS 1M tokens: {ratio:.1f}x over threshold")
            print(f"  ✅ Claim VERIFIED: System provides >1M token context")
            passed = True
            score = 100
        elif total_tokens > 500_000:
            ratio = total_tokens / 1_000_000
            print(f"  ⚠️  APPROACHING 1M tokens: {ratio:.1%} of threshold")
            print(f"  ⚠️  Claim PARTIALLY verified (likely to exceed with more use)")
            passed = False
            score = 50
        else:
            ratio = total_tokens / 1_000_000
            print(f"  ❌ BELOW 1M tokens: Only {ratio:.1%} of threshold")
            print(f"  ❌ Claim NOT verified with current data")
            passed = False
            score = 0
        
        return {
            "total_tokens": total_tokens,
            "total_chars": total_chars,
            "exceeds_1m": passed,
            "ratio_to_1m": total_tokens / 1_000_000,
            "score": score
        }
    
    def compare_to_single_agent(self, total_tokens: float) -> Dict:
        """
        Compare to typical single-agent system context window
        """
        print("\n" + "="*80)
        print("TEST 6: Context Enlargement vs Single-Agent Systems")
        print("="*80)
        
        # Typical context windows
        systems = {
            "GPT-4": 128_000,
            "GPT-4 Turbo": 128_000,
            "Claude 3": 200_000,
            "Claude 3.5 Sonnet": 200_000,
            "Gemini 1.5 Pro": 1_000_000,
        }
        
        print(f"\n📊 Context Window Comparison:")
        print(f"  {'─'*60}")
        print(f"  {'System':30s} {'Context Window':>15s} {'vs Destiny':>15s}")
        print(f"  {'─'*60}")
        
        for name, window in systems.items():
            ratio = total_tokens / window if window > 0 else 0
            print(f"  {name:30s} {window:>12,} {ratio:>13.1f}x")
        
        print(f"  {'─'*60}")
        print(f"  {'Destiny Team Framework':30s} {total_tokens:>12,.0f}")
        print(f"  {'─'*60}")
        
        # Calculate average improvement
        avg_single_agent = sum(systems.values()) / len(systems)
        improvement = (total_tokens / avg_single_agent) if avg_single_agent > 0 else 0
        
        print(f"\n📊 Analysis:")
        print(f"  Average single-agent window: {avg_single_agent:,.0f} tokens")
        print(f"  Destiny Team total: {total_tokens:,.0f} tokens")
        print(f"  Improvement factor: {improvement:.1f}x")
        
        if improvement >= 5:
            print(f"  ✅ SIGNIFICANT enlargement (≥5x)")
            score = 30
        elif improvement >= 2:
            print(f"  ✅ GOOD enlargement (2-5x)")
            score = 20
        elif improvement >= 1:
            print(f"  ⚠️  MARGINAL enlargement (1-2x)")
            score = 10
        else:
            print(f"  ❌ NO enlargement (<1x)")
            score = 0
        
        return {
            "avg_single_agent": avg_single_agent,
            "destiny_total": total_tokens,
            "improvement_factor": improvement,
            "score": score
        }
    
    def run_all_tests(self) -> Dict:
        """Run complete context capacity test suite"""
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "CONTEXT CAPACITY TEST SUITE".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        results = {}
        
        # Test 1: Agent context isolation
        results['isolation'] = self.test_agent_context_isolation()
        
        # Test 2-4: Measure each layer
        measurements = []
        measurements.append(self.measure_postgresql_context())
        measurements.append(self.measure_neo4j_context())
        measurements.append(self.measure_qdrant_context())
        
        # Test 5: Total capacity
        results['total'] = self.calculate_total_capacity(measurements)
        
        # Test 6: Comparison
        results['comparison'] = self.compare_to_single_agent(
            results['total']['total_tokens']
        )
        
        # Calculate final score
        total_score = (
            results['isolation']['score'] +
            results['total']['score'] +
            results['comparison']['score']
        )
        max_score = 30 + 100 + 30  # 160 total
        percentage = (total_score / max_score) * 100
        
        # Final report
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "FINAL RESULTS".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        
        print(f"\n📊 Score Breakdown:")
        print(f"  Agent Isolation:   {results['isolation']['score']}/30")
        print(f"  Total Capacity:    {results['total']['score']}/100")
        print(f"  Context Enlargement: {results['comparison']['score']}/30")
        print(f"  {'─'*40}")
        print(f"  TOTAL:             {total_score}/{max_score} ({percentage:.0f}%)")
        
        print(f"\n📊 Key Findings:")
        print(f"  • Agents with contexts: {results['isolation'].get('agent_count', 0)}")
        print(f"  • Total context capacity: {results['total']['total_tokens']:,.0f} tokens")
        print(f"  • Exceeds 1M threshold: {'YES ✅' if results['total']['exceeds_1m'] else 'NO ❌'}")
        print(f"  • Enlargement vs single-agent: {results['comparison']['improvement_factor']:.1f}x")
        
        print(f"\n🎯 ANSWER TO CORE QUESTION:")
        print(f"  'Is it a multi-layer multi-agent task force system with")
        print(f"   independent context for each agent, enlarging context")
        print(f"   far above 1M tokens?'")
        print()
        
        all_verified = (
            results['isolation']['passed'] and
            results['total']['exceeds_1m'] and
            results['comparison']['improvement_factor'] >= 2
        )
        
        if all_verified:
            print(f"  ✅ YES - All claims VERIFIED")
        elif results['total']['exceeds_1m']:
            print(f"  ⚠️  PARTIALLY - Exceeds 1M but some aspects incomplete")
        else:
            print(f"  ❌ NO - Claims not fully substantiated")
        
        return {
            "score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "verified": all_verified,
            "details": results
        }


if __name__ == "__main__":
    tester = ContextCapacityTest()
    results = tester.run_all_tests()
    
    print("\n" + "="*80)
    print(f"Test completed with score: {results['percentage']:.0f}%")
    print("="*80)
