#!/bin/bash
# Test Elasticsearch Batch Integration

echo "🔍 Testing Elasticsearch Batch Integration"
echo "=========================================="
echo ""

# Check if Elasticsearch is running
echo "1️⃣ Checking Elasticsearch..."
if curl -s -u elastic:changeme123 http://localhost:9200/_cluster/health > /dev/null 2>&1; then
    echo "✅ Elasticsearch is running"
    
    # Get cluster health
    HEALTH=$(curl -s -u elastic:changeme123 http://localhost:9200/_cluster/health | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
    echo "   Cluster status: $HEALTH"
else
    echo "❌ Elasticsearch is not running!"
    echo "   Please start Elasticsearch first"
    exit 1
fi

# Check if PostgreSQL is running
echo ""
echo "2️⃣ Checking PostgreSQL..."
if psql -h localhost -U user -d destiny_team -c "SELECT 1" > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
    
    # Check if table exists
    TABLE_EXISTS=$(psql -h localhost -U user -d destiny_team -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'es_document_references');" | tr -d ' ')
    if [ "$TABLE_EXISTS" = "t" ]; then
        echo "✅ es_document_references table exists"
    else
        echo "⚠️  Creating es_document_references table..."
        psql -h localhost -U user -d destiny_team < sql/es_document_references_schema.sql
    fi
else
    echo "❌ PostgreSQL is not running!"
    exit 1
fi

# Check PDF directory
echo ""
echo "3️⃣ Checking PDF directory..."
PDF_DIR="investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs"
if [ -d "$PDF_DIR" ]; then
    PDF_COUNT=$(find "$PDF_DIR" -name "*.pdf" | wc -l | tr -d ' ')
    echo "✅ Found $PDF_COUNT PDF files"
else
    echo "❌ PDF directory not found: $PDF_DIR"
    exit 1
fi

# Run small batch test
echo ""
echo "4️⃣ Running batch processing test (first 10 PDFs)..."
echo "=================================================="

# Create test script
cat > test_batch_10.py << 'EOF'
import sys
sys.path.insert(0, ".")
from pathlib import Path
from process_pdfs_to_elasticsearch import PDFBatchProcessor

processor = PDFBatchProcessor(batch_size=10)
pdf_dir = Path("investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs")
pdfs = list(pdf_dir.glob("*.pdf"))[:10]

print(f"Processing {len(pdfs)} PDFs...")
for pdf in pdfs:
    processor.process_pdf_directory(pdf.parent, "test_batch")
    break  # Just process first batch

# Test search
processor.search_financial_data("financial statement")
EOF

python3 test_batch_10.py

# Check results
echo ""
echo "5️⃣ Checking results..."
echo "====================="

# Count ES documents
ES_COUNT=$(curl -s -u elastic:changeme123 http://localhost:9200/osint_reports_pdf/_count | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])" 2>/dev/null || echo "0")
echo "📊 Elasticsearch documents: $ES_COUNT"

# Count PG references
PG_COUNT=$(psql -h localhost -U user -d destiny_team -t -c "SELECT COUNT(*) FROM es_document_references;" | tr -d ' ')
echo "📊 PostgreSQL references: $PG_COUNT"

# Sample search
echo ""
echo "6️⃣ Sample search test..."
echo "========================"

curl -s -u elastic:changeme123 \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "match": {
        "content": "przychody"
      }
    },
    "size": 3,
    "_source": ["filename", "report_year"]
  }' \
  http://localhost:9200/osint_reports_pdf/_search | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
hits = data.get('hits', {}).get('hits', [])
if hits:
    print('Found', data['hits']['total']['value'], 'documents matching \"przychody\"')
    for hit in hits:
        src = hit['_source']
        print(f'  - {src.get(\"filename\", \"Unknown\")} ({src.get(\"report_year\", \"N/A\")})')
else:
    print('No results found')
"

# Cleanup
rm -f test_batch_10.py

echo ""
echo "✅ Test complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Process all PDFs: python3 process_pdfs_to_elasticsearch.py"
echo "   2. Search data: python3 process_pdfs_to_elasticsearch.py --search 'your query'"
echo "   3. Monitor: tail -f elasticsearch_batch.log"
echo ""