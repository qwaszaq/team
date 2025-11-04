# Test Automatycznego Wykonywania

**Data:** 2025-11-04 10:10
**Cel:** Weryfikacja że Helena FAKTYCZNIE wykonuje do wszystkich 4 baz

## Expected Behavior:

Po zapisaniu tego dokumentu, Helena powinna:

1. ✅ **ZAINDEXOWAĆ do Qdrant** (pojawi się w dashboard)
2. ✅ **WYKONAĆ SQL do PostgreSQL** (rekord w tabeli documents)
3. ✅ **WYKONAĆ Cypher do Neo4j** (node Document)
4. ✅ **WYKONAĆ commands do Redis** (keys doc:*)

## Weryfikacja:

### Qdrant:
```
curl -X POST http://localhost:6333/collections/destiny-team-framework-master/points/scroll \
  -d '{"filter": {"must": [{"key": "title", "match": {"text": "Test Automatycznego"}}]}}'
```

### PostgreSQL:
```
SELECT * FROM documents WHERE title LIKE '%Test Automatycznego%';
```

### Neo4j:
```
MATCH (d:Document) WHERE d.title CONTAINS 'Test Automatycznego' RETURN d;
```

### Redis:
```
KEYS doc:*Test*
```

**Jeśli wszystkie 4 zapytania zwracają dane - system działa w 100%!**
