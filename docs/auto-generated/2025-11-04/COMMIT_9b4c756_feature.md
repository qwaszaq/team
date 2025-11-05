# Implement batch processing system to resolve PostgreSQL performance crisis

**Auto-Generated Documentation**

**Date:** 2025-11-04 22:14:36
**Commit:** `9b4c756`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Message

**feat: Implement batch processing system to resolve PostgreSQL performance crisis**

CRITICAL FIX: Database was experiencing 431+ second hangs due to real-time processing overload

Changes:
- Added intelligent batch processing system with 5-second and hourly options
- Implemented connection pooling (max 3 connections vs unlimited before)
- Created emergency fix scripts for immediate database recovery
- Set up hourly batch processor as macOS service (com.destiny.hourly-batch)
- Added comprehensive migration plan from real-time to batch processing

Performance improvements:
- 95% reduction in database writes
- 25x throughput increase (from 20 to 500+ ops/sec)
- Eliminated lock contention issues
- Reduced GIN index maintenance overhead

New tools:
- batch_processing_system.py: Core batching engine
- hourly_batch_processor.py: Scheduled hourly processing
- helena_batch_processor.py: Helena's batch-aware processor
- emergency_fix.sh: Immediate database recovery script
- queue_for_batch.sh: Helper to queue files
- check_batch_status.sh: Monitor batch system

Documentation:
- POSTGRES_STUCK_ANALYSIS.md: Root cause analysis
- BATCH_MIGRATION_PLAN.md: Step-by-step migration guide
- TECHNICAL_TEAM_RESPONSE.json: Emergency response details

The hourly batch service is now running and will process queued documents
every hour at :00, dramatically reducing database load while maintaining
data integrity.


## 📁 Files Changed

**Total:** 698 file(s)

### Python Files (26)

- `agents/analytical/damian_agent.py`
- `agents/analytical/tools/__init__.py`
- `agents/analytical/tools/mathematical_toolkit.py`
- `agents/analytical/tools/scraping_toolkit.py`
- `aleksander_emergency_response.py`
- `batch_processing_system.py`
- `capabilities_registry.py`
- `examples/search_orchestrator_usage.py`
- `helena_batch_processor.py`
- `helena_core.py`
- `hourly_batch_processor.py`
- `local_orchestrator.py`
- `orchestration/elasticsearch_integration_concept.py`
- `orchestration/elasticsearch_integration_evaluation.py`
- `scripts/extract_pdf_text_to_es.py`
- `scripts/hybrid_osint_processor_test.py`
- `scripts/ingest_investigation_osint.py`
- `scripts/scrape_grupaazoty_pdfs.py`
- `scripts/sync_documents_to_neo4j.py`
- `scripts/sync_es_references_to_pg.py`
- `search_orchestrator.py`
- `supervisor_interface.py`
- `technical_emergency_response.py`
- `test_hybrid_system.py`
- `tests/test_search_orchestrator_real_data.py`
- `tests/test_smart_references_integration.py`


### Shell Files (4)

- `check_batch_status.sh`
- `emergency_fix.sh`
- `queue_for_batch.sh`
- `setup_hourly_batch.sh`


### Documentation Files (53)

- `BATCH_MIGRATION_PLAN.md`
- `POSTGRES_STUCK_ANALYSIS.md`
- `README.md`
- `SOURCE_CITATION_QUICK_REFERENCE.md`
- `docs/DATA_ARCHITECTURE_ANALYSIS.md`
- `docs/SEARCH_ORCHESTRATOR.md`
- `docs/architecture/DATA_SEPARATION_ARCHITECTURE.md`
- `docs/architecture/HYBRID_ONPREM_INTELLIGENCE_SYSTEM.md`
- `docs/auto-generated/2025-11-04/COMMIT_038e967_feature.md`
- `docs/auto-generated/2025-11-04/COMMIT_300ea7b_feature.md`
- `docs/auto-generated/2025-11-04/COMMIT_388327f_feature.md`
- `docs/auto-generated/2025-11-04/COMMIT_594e664_feature.md`
- `docs/auto-generated/2025-11-04/COMMIT_6a77410_documentation.md`
- `docs/auto-generated/2025-11-04/COMMIT_7c01260_change.md`
- `docs/capabilities/DUCKDUCKGO_SEARCH_METHOD.md`
- `docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md`
- `docs/capabilities/INTERNET_RESEARCH_CAPABILITY.md`
- `docs/concepts/BELLINGCAT_LEVEL_OSINT.md`
- `docs/concepts/COMPREHENSIVE_OSINT_SYSTEM.md`
- `docs/concepts/DESTINY_CHAT_UI_HYBRID_INTEGRATION.md`
- `docs/guides/HYBRID_SYSTEM_COMPLETE_OVERVIEW.md`
- `docs/guides/HYBRID_SYSTEM_QUICK_START.md`
- `docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md`
- `docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md`
- `docs/status/MORNING_BRIEF_20251104.md`
- `docs/status/SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.md`
- `docs/team/ADAPTIVE_LEARNING_SYSTEM.md`
- `docs/team/MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.md`
- `docs/team/SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.md`
- `docs/team/SYSTEM_CAPABILITIES_UPDATE_2025_11_04.md`
- `docs/technical/AGENT_TOOLKITS_COMPLETE.md`
- `helena_tasks/helena_task_20251104_140000_database_schema.md`
- `helena_tasks/helena_task_20251104_140000_documentation.md`
- `helena_tasks/helena_task_20251104_140000_general_change.md`
- `helena_tasks/helena_task_20251104_140000_knowledge_graph.md`
- `helena_tasks/helena_task_20251104_150000_agent_code.md`
- `helena_tasks/helena_task_20251104_150000_documentation.md`
- `helena_tasks/helena_task_20251104_150000_general_change.md`
- `helena_tasks/helena_task_20251104_190000_agent_code.md`
- `helena_tasks/helena_task_20251104_190000_documentation.md`
- `helena_tasks/helena_task_20251104_190000_general_change.md`
- `helena_tasks/helena_task_20251104_200000_documentation.md`
- `helena_tasks/helena_task_20251104_210000_documentation.md`
- `helena_tasks/helena_task_20251104_210000_general_change.md`
- `investigations/active/telus_cpk_real_001/FINAL_OSINT_REPORT.md`
- `investigations/active/telus_cpk_real_001/INVESTIGATION_STATUS.md`
- `investigations/telus_cpk_land_investigation/FINAL_INVESTIGATION_REPORT.md`
- `investigations/telus_cpk_land_investigation/INVESTIGATION_PLAN.md`
- `investigations/telus_cpk_land_investigation/analysis/ADRIAN_LEGAL_ANALYSIS.md`
- `investigations/telus_cpk_land_investigation/analysis/DAMIAN_CRITICAL_REVIEW.md`
- `investigations/telus_cpk_land_investigation/analysis/ELENA_OSINT_REPORT.md`
- `investigations/telus_cpk_land_investigation/analysis/MARCUS_FINANCIAL_ANALYSIS.md`
- `investigations/telus_cpk_land_investigation/analysis/MAYA_DATA_TIMELINE_ANALYSIS.md`


### Configuration Files (112)

- `.change_tracking_state.json`
- `TECHNICAL_TEAM_RESPONSE.json`
- `bus/urgent_technical_review.json`
- `helena_tasks/processed/success_realtime_20251104_132625_COMMIT_300ea7b_feature.json`
- `helena_tasks/processed/success_realtime_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_142244_RESEARCH_DELIVERY_SUMMARY.json`
- `helena_tasks/processed/success_realtime_20251104_142308_COMMIT_7c01260_change.json`
- `helena_tasks/processed/success_realtime_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json`
- `helena_tasks/processed/success_realtime_20251104_143526_FACE_RECOGNITION_TECHNICAL_VALIDATION.json`
- `helena_tasks/processed/success_realtime_20251104_143610_COMMIT_594e664_feature.json`
- `helena_tasks/processed/success_realtime_20251104_144914_COMMIT_6a77410_documentation.json`
- `helena_tasks/processed/success_realtime_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json`
- `helena_tasks/processed/success_realtime_20251104_145753_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json`
- `helena_tasks/processed/success_realtime_20251104_145842_COMMIT_038e967_feature.json`
- `helena_tasks/processed/success_realtime_20251104_150726_SEJM_API_ANALYSIS_CONCEPT.json`
- `helena_tasks/processed/success_realtime_20251104_151038_SEJM_ASW_ANALYSIS_2019_2023.json`
- `helena_tasks/processed/success_realtime_20251104_151116_COMMIT_388327f_feature.json`
- `helena_tasks/processed/success_realtime_20251104_183127_INSTITUTIONAL_API_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_183139_README.json`
- `helena_tasks/processed/success_realtime_20251104_183144_README.json`
- `helena_tasks/processed/success_realtime_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json`
- `helena_tasks/processed/success_realtime_20251104_184219_BELLINGCAT_LEVEL_OSINT.json`
- `helena_tasks/processed/success_realtime_20251104_184617_BELLINGCAT_METHODOLOGY_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_184916_AGENT_TOOLKITS_COMPLETE.json`
- `helena_tasks/processed/success_realtime_20251104_185327_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json`
- `helena_tasks/processed/success_realtime_20251104_185810_ADAPTIVE_LEARNING_SYSTEM.json`
- `helena_tasks/processed/success_realtime_20251104_185958_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json`
- `helena_tasks/processed/success_realtime_20251104_190458_SOURCE_ATTRIBUTION_PROTOCOL.json`
- `helena_tasks/processed/success_realtime_20251104_190530_SOURCE_CITATION_QUICK_REFERENCE.json`
- `helena_tasks/processed/success_realtime_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json`
- `helena_tasks/processed/success_realtime_20251104_190812_INVESTIGATION_PLAN.json`
- `helena_tasks/processed/success_realtime_20251104_190943_ELENA_OSINT_REPORT.json`
- `helena_tasks/processed/success_realtime_20251104_191154_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json`
- `helena_tasks/processed/success_realtime_20251104_191612_MARCUS_FINANCIAL_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_192245_DAMIAN_CRITICAL_REVIEW.json`
- `helena_tasks/processed/success_realtime_20251104_192454_FINAL_INVESTIGATION_REPORT.json`
- `helena_tasks/processed/success_realtime_20251104_193139_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json`
- `helena_tasks/processed/success_realtime_20251104_193555_HYBRID_SYSTEM_QUICK_START.json`
- `helena_tasks/processed/success_realtime_20251104_193622_README.json`
- `helena_tasks/processed/success_realtime_20251104_194001_DATA_SEPARATION_ARCHITECTURE.json`
- `helena_tasks/processed/success_realtime_20251104_194329_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json`
- `helena_tasks/processed/success_realtime_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json`
- `helena_tasks/processed/success_realtime_20251104_195309_INTERNET_RESEARCH_CAPABILITY.json`
- `helena_tasks/processed/success_realtime_20251104_195344_INTERNET_RESEARCH_CAPABILITY.json`
- `helena_tasks/processed/success_realtime_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json`
- `helena_tasks/processed/success_realtime_20251104_195846_INVESTIGATION_STATUS.json`
- `helena_tasks/processed/success_realtime_20251104_203406_FINAL_OSINT_REPORT.json`
- `helena_tasks/processed/success_realtime_20251104_203700_FINAL_OSINT_REPORT.json`
- `helena_tasks/processed/success_realtime_20251104_204516_FINAL_OSINT_REPORT.json`
- `helena_tasks/processed/success_realtime_20251104_211442_SEARCH_ORCHESTRATOR.json`
- `helena_tasks/processed/success_realtime_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_220219_POSTGRES_STUCK_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251104_220923_BATCH_MIGRATION_PLAN.json`
- `investigations/concepts/elasticsearch_integration_20251104_210917.json`
- `investigations/concepts/search_orchestrator_test_report.json`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/summary.json`
- `orchestration/eval_20251104_213005_report.json`
- `qdrant_pending/indexed/doc_20251104_132626_COMMIT_300ea7b_feature.json`
- `qdrant_pending/indexed/doc_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_142244_RESEARCH_DELIVERY_SUMMARY.json`
- `qdrant_pending/indexed/doc_20251104_142308_COMMIT_7c01260_change.json`
- `qdrant_pending/indexed/doc_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json`
- `qdrant_pending/indexed/doc_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.json`
- `qdrant_pending/indexed/doc_20251104_143611_COMMIT_594e664_feature.json`
- `qdrant_pending/indexed/doc_20251104_144915_COMMIT_6a77410_documentation.json`
- `qdrant_pending/indexed/doc_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json`
- `qdrant_pending/indexed/doc_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json`
- `qdrant_pending/indexed/doc_20251104_145842_COMMIT_038e967_feature.json`
- `qdrant_pending/indexed/doc_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.json`
- `qdrant_pending/indexed/doc_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.json`
- `qdrant_pending/indexed/doc_20251104_151117_COMMIT_388327f_feature.json`
- `qdrant_pending/indexed/doc_20251104_183128_INSTITUTIONAL_API_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_183139_README.json`
- `qdrant_pending/indexed/doc_20251104_183144_README.json`
- `qdrant_pending/indexed/doc_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json`
- `qdrant_pending/indexed/doc_20251104_184219_BELLINGCAT_LEVEL_OSINT.json`
- `qdrant_pending/indexed/doc_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_184917_AGENT_TOOLKITS_COMPLETE.json`
- `qdrant_pending/indexed/doc_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json`
- `qdrant_pending/indexed/doc_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.json`
- `qdrant_pending/indexed/doc_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json`
- `qdrant_pending/indexed/doc_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.json`
- `qdrant_pending/indexed/doc_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.json`
- `qdrant_pending/indexed/doc_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json`
- `qdrant_pending/indexed/doc_20251104_190812_INVESTIGATION_PLAN.json`
- `qdrant_pending/indexed/doc_20251104_190943_ELENA_OSINT_REPORT.json`
- `qdrant_pending/indexed/doc_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json`
- `qdrant_pending/indexed/doc_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_192245_DAMIAN_CRITICAL_REVIEW.json`
- `qdrant_pending/indexed/doc_20251104_192454_FINAL_INVESTIGATION_REPORT.json`
- `qdrant_pending/indexed/doc_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json`
- `qdrant_pending/indexed/doc_20251104_193555_HYBRID_SYSTEM_QUICK_START.json`
- `qdrant_pending/indexed/doc_20251104_193622_README.json`
- `qdrant_pending/indexed/doc_20251104_194002_DATA_SEPARATION_ARCHITECTURE.json`
- `qdrant_pending/indexed/doc_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json`
- `qdrant_pending/indexed/doc_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json`
- `qdrant_pending/indexed/doc_20251104_195310_INTERNET_RESEARCH_CAPABILITY.json`
- `qdrant_pending/indexed/doc_20251104_195345_INTERNET_RESEARCH_CAPABILITY.json`
- `qdrant_pending/indexed/doc_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json`
- `qdrant_pending/indexed/doc_20251104_195847_INVESTIGATION_STATUS.json`
- `qdrant_pending/indexed/doc_20251104_203406_FINAL_OSINT_REPORT.json`
- `qdrant_pending/indexed/doc_20251104_203700_FINAL_OSINT_REPORT.json`
- `qdrant_pending/indexed/doc_20251104_204516_FINAL_OSINT_REPORT.json`
- `qdrant_pending/indexed/doc_20251104_211443_SEARCH_ORCHESTRATOR.json`
- `qdrant_pending/indexed/doc_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_220219_POSTGRES_STUCK_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251104_220923_BATCH_MIGRATION_PLAN.json`
- `shared_workspace/tasks/task_cpk_research_demo.json`


### Other Files (503)

- `com.destiny.hourly-batch.plist`
- `investigations/active/telus_cpk_real_001/sources/web/businessinsider_telus.html`
- `investigations/active/telus_cpk_real_001/sources/web/cpk_official.html`
- `investigations/active/telus_cpk_real_001/sources/web/cpk_wikipedia.html`
- `investigations/active/telus_cpk_real_001/sources/web/onet_telus_cpk.html`
- `investigations/active/telus_cpk_real_001/sources/web/tvn24_telus_cpk.html`
- `investigations/active/telus_cpk_real_001/sources/web/wikipedia_telus.html`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/elasticsearch_bulk.ndjson`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/elasticsearch_text_updates.ndjson`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119530rdroczneskonsolidowanesprawozdaniefinansowezaiiikwarta2010.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119707azotytarnowqsriiikwarta2009.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119739rdroczneskonsolidowanesprawozdaniefinansowezaiiikwarta2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119889azotytarnowqsrikwarta2009.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120049skonsolidowanesprawozdaniezaikwarta2011opublikowany.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120309skonsolidowanesprawozdaniezaikwarta2010.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120313raportivq2009bezpodpisow.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329483078azotytarnowqsriiikwartal2008.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329483098azotytarnowqsrivkwarta2008.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329485603sprawozdaniefinansoweiikwartal2008.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1Ocena_20Rady_20Nadzorczej_202019.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1__C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20skonsolidowane_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202021_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2019.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2__C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20jednostkowe_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202021_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/3_Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20p_C3_B3_C5_82rocze_202021_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/4_O_C5_9Bwiadczenie_20Zarz_C4_85du_20Grupy_20Azoty_20S.A._20o_20zgodno_C5_9Bci_20i_20prawdziwo_C5_9Bci_20_C5_9Br_C3_B3drocznego_20sprawozdania_20finansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/C59ArC3B3droczne20skrC3B3cone20jednostkowe20sprawozdanie20finansowe20za20okres20620miesiC499cy20zakoC584czony203020czerwca20201920roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/C59ArC3B3droczne20skrC3B3cone20skonsolidowane20sprawozdanie20finansowe20za20okres20620miesiC499cy20zakoC584czony203020czerwca20201920roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_OswiadczenieZarzadu-2021-12-31-pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_SprawozdanieFinansowe-2021-12-31-pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_SprawozdanieZarzadu-2021-12-31-pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_List_Prezesa_Zarzadu_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2025.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_20_I_kwarta_C5_82_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2024_roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2025.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2025.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2023_.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2025.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20Sprawozdanie20Finansowe201H2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20Sprawozdanie20Finansowe201H2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe20SpC3B3C582ki20Grupa20Azoty20za20rok202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe20za20rok202016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List20Prezesa20ZarzC485du.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/ListPrez_GrupaAzoty-2024-12-31-0-pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List_20Prezesa_20Zarz_C4_85du.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List_Prezesa_Zarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20Rady20Nadzorczej20-20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20Rady20Nadzorczej20-20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20-20podmiot20uprawniony20do20badania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20-20sprawozdania20finansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20Grupy20Azoty20S.A.20o20zgodnoC59Bci20i20prawdziwoC59Bci20C59BrC3B3drocznego20sprawozdania20finansowego30.06.2019.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20Grupy20Azoty20do20sprawozdaC58420za20201820rok.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20podmiocie20uprawnionym20-20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20podmiocie20uprawnionym20-20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20sprawozdaniu20jednostkowym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20sprawozdaniu20skonsolidowanym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20Grupy_20Azoty_20S.A._20o_20zgodno_C5_9Bci_20i_20prawdziwo_C5_9Bci_20_C5_9Br_C3_B3drocznego_20sprawozdania_20finansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20o_20podmiocie_20uprawnionym_20-_20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20o_20sprawozdaniu_20skonsolidowanym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena20Rady20Nadzorczej.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_20Rady_20Nadzorczej_20-_20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_skonsolidowane_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_Zarzadu_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_Zarzadu_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_finansowe_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_skonsolidowane_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_skonsolidowane_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Opinia20i20raport20biegC582ego20rewidenta20-20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Opinia20i20raport20biegC582ego20rewidenta20-20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady-Nadzorczej_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_skonsolidowane_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_skonsolidowane_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Zarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport20biegC582ego20rewidenta20-20sprawozdanie20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport20biegC582ego20rewidenta20-20sprawozdanie20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20z_20przegl_C4_85du_20JSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20z_20przegl_C4_85du_20SSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Bieglego_Rewidenta-sig-sig.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Bieglego_Rewidenta_skonsolidowane-sig-sig.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GASA_JSF.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GASA_SSF.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GAT_JSF_H1_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GK_GAT_SSF_H1_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport__przegl_C4_85du_GAT_.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_z_przegladu_GK_GAT.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20Sprawozdanie20Finansowe201H2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20Grupy20KapitaC582owej20Grupa20Azoty20z20pC582atnoC59Bci20na20rzecz20administracji20publicznej20za20201820rok.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe201H2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe20Grupy20KapitaC582owej20Grupa20Azoty20za20rok202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe20za20rok202016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20wybrane20dane20finansowe202016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20wybrane20dane20finansowe202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_20sprawozdanie_20finansowe_202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_20wybrane_20dane_20finansowe_202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_wybrane_dane_finansowe_2021.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20kwartalny203Q2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20Grupy20KapitaC582owej20Grupa20Azoty20za20I20kwartaC58220201920roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20120kwartaC582202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20320kwartaC582202018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20I20kwartaC582202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20GKGA_20za_20III_20kwarta_C5_82_202021.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20III_20kwarta_C5_82_202019_20roku_1_.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20kwarta_C5_82_202020_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_raport_okresowy_Grupy_Kapitalowej_Grupa_Azoty_za_III_kwartal_2020_.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Spraw_zrown_rozw_2024.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie-SPS-2016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie-z-platnosci-na-rzecz-administracji-publicznej-2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du201H2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci202016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20GK202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20Grupy20Azoty20S.A.20oraz20Grupy20KapitaC582owej20Grupa20Azoty20za20okres201220miesiC499cy20zakoC584czony203120grudnia20201820roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20Grupy20KapitaC582owej20Grupa20Azoty20za20I20pC3B3C582rocze20201920roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20Zarzadu201H2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20biegC582ego20rewidenta20-20sprawozdanie20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20na20temat20informacji20niefinansowych20Grupy20KapitaC582owej20Grupa20Azoty20za20okres201220miesiC499cy20zakoC584czony203120grudnia20201820roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20z20badania20-20jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20z20badania20-20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20GK_202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20p_C3_B3_C5_82rocze_202020_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20nt_20informacji_20niefinansowych_202017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_2023.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_za_2021_rok.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_za_2021_rok_pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzB_GAT_2022.xhtml.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzB_GK_GAT_2022.xhtml.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzD_GrupaAzoty-2024-12-31-0-pl.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2019.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201Q202019.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe203Q2017.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe203Q2018.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_201H_202020.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_201Q_202020.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_20III_20kwarta_C5_82_202021.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_20I_20p_C3_B3_C5_82rocze_202021.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_1Q_2022.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_2021.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_3Q2020.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/_C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20jednostkowe_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202020_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/_C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20skonsolidowane_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_202020_20roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowe2013.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowe2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowezarok2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/listprezesa-1h2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/listprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdaniejednostkowe2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdanieskonsolidowaners2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegoreiwdenta-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozd.jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozd.skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniaosprawozdaniuskonsolidowanymiopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdaniejednostkowe2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdanieskonsolidowaners2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieoskonsolidowanymsprawozdaniurs2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowym2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowymiopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowymipodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniuskonsolidowanym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniuskonsolidowanymipodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu-podmiotuprawnionydobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu-sprawozdaniafinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduopodmiocieuprawnionym-jednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduopodmiocieuprawnionym-skonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduosprawozdaniuskonsolidowanym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduwsprawiepodmiotuuprawnionegodobadaniasprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduwsprawierzetelnoscisporzadzeniesprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/pismoprezesazarzadu2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/pismoprezesazarzadurs2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/polroczneskonsolidowanesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/polroczneskroconejednostkowesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007opiniairaportbieglegorewidenta.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007oswiadczenieopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007oswiadczenieosprawozdaniurocznym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007sprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007sprawozdaniezdzialalnoscispolki.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008opiniapodmiotuuprawnionegodobadaniajednostkowegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008opiniapodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieojednostkowymsprawozdaniurocznym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieopodmiocieuprawnionymdobadaniajednostkowegosprawozdaniafinsnowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieopodmiocieuprawnionymdobadaniaskonsolidowanegosprawozdaniafinsnowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieoskonsolidowanymsprawozdaniurocznym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008pismoprezesazarzadusprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008pismoprezesazarzadusprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008raportpodmiotuuprawnionegodobadaniajednostkowegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008raportpodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008rocznejednostkowesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008roczneskonsolidowanesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008sprawozdaniejednostkowezdzialalnoscispolki.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009opiniabieglegorewidenta.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009oswiadczenieopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009oswiadczenieosprawozdaniujednostkowym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009raportpodmiotuuprawnionegodobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009rocznejednostkowesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009sprawozdaniejednostkowezdzialalnoscispolki.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009wybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010jednostkowesprawozdaniefinansowezarok2010.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010opiniabieglegorewidenta.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010oswiadczenieopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010oswiadczenieosprawozdaniujednostkowym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010raportpodmiotuuprawnionegodobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010sprawozdaniezarzaduzdzialalnoscispolki.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010wybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportadytora-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdaniejednostkowe1.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdanieskonsolidowane1.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegorewidenta-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegorewidenta-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegosprjednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegosprskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportniezaleznegobieglegorewidenta3q2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportpodmiotuuprawnionegodobadania-sprawozdaniejednostkowe2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportpodmiotuuprawnionegodobadania-sprawozdanieskonsolidowaners2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportuzupelniajacybieglegorewidenta-sprawozdaniejednostkowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportuzupelniajacybieglegorewidenta-sprawozdanieskonsolidowane.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007opiniapodmiotuuprawnionegodobadaniasprawozdanfinansowychobadanymrocznymskonsolidowanymsprawozdaniufinansowym.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007oswiadczeniezarzaduwsprawiepodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007oswiadczeniezarzaduwsprawierzetelnoscisporzadzeniaskonsolidowanegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007raportpodmiotuuprawnionegodobadaniasprawozdanfinansowychzbadaniarocznegoskonsolidowanegosprawozdaniafinansowego.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007roczneskonsolidowanesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009opiniabieglegorewidenta.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009oswiadczenieopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009oswiadczenieoskonsolidowanymsprawozdaniu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009raportpodmiotuuprawnionegodobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009roczneskonsolidowanesprawozdaniefinansowezarok2009.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzarok2009.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009wybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010opiniabieglegorewidenta.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010oswiadczenieopodmiocieuprawnionymdobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010oswiadczenieoskonsolidowanymsprawozdaniu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010pismoprezesazarzadu.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010raportpodmiotuuprawnionegodobadania.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010skonsolidowanesprawozdaniefinansowegkazotytarnow.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010sprawozdaniezarzaduzdzialalnoscigkazotytarnow.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010wybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe2013.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansoweipolrocze2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezaipolrocze2010.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezaipolrocze2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2011rs2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowers2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny1q2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny1q2013.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny3q2016rokuskorygowany.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12016.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq32014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyzaiiikwartal2012roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowy3q2015skorygowany.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyza1polrocze2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2013.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2016roku.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportq32013.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigk.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigk2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigkzaipolrocze2012.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejrs2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzaipolrocze2010.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzaipolrocze2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzakladyazotowewtarnowie-moscicachsawipolroczu2008.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2011.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2014.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2015.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/wybranedanefinansowe.pdf`
- `investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/wybranedanefinansowe2008rr.pdf`
- `redis_pending/redis_20251104_132626_COMMIT_300ea7b_feature.txt`
- `redis_pending/redis_20251104_142120_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.txt`
- `redis_pending/redis_20251104_142244_RESEARCH_DELIVERY_SUMMARY.txt`
- `redis_pending/redis_20251104_142308_COMMIT_7c01260_change.txt`
- `redis_pending/redis_20251104_143218_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.txt`
- `redis_pending/redis_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.txt`
- `redis_pending/redis_20251104_143611_COMMIT_594e664_feature.txt`
- `redis_pending/redis_20251104_144915_COMMIT_6a77410_documentation.txt`
- `redis_pending/redis_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.txt`
- `redis_pending/redis_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.txt`
- `redis_pending/redis_20251104_145842_COMMIT_038e967_feature.txt`
- `redis_pending/redis_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.txt`
- `redis_pending/redis_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.txt`
- `redis_pending/redis_20251104_151117_COMMIT_388327f_feature.txt`
- `redis_pending/redis_20251104_183128_INSTITUTIONAL_API_ANALYSIS.txt`
- `redis_pending/redis_20251104_183139_README.txt`
- `redis_pending/redis_20251104_183144_README.txt`
- `redis_pending/redis_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.txt`
- `redis_pending/redis_20251104_184219_BELLINGCAT_LEVEL_OSINT.txt`
- `redis_pending/redis_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.txt`
- `redis_pending/redis_20251104_184917_AGENT_TOOLKITS_COMPLETE.txt`
- `redis_pending/redis_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.txt`
- `redis_pending/redis_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.txt`
- `redis_pending/redis_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.txt`
- `redis_pending/redis_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.txt`
- `redis_pending/redis_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.txt`
- `redis_pending/redis_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.txt`
- `redis_pending/redis_20251104_190812_INVESTIGATION_PLAN.txt`
- `redis_pending/redis_20251104_190944_ELENA_OSINT_REPORT.txt`
- `redis_pending/redis_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.txt`
- `redis_pending/redis_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.txt`
- `redis_pending/redis_20251104_191829_ADRIAN_LEGAL_ANALYSIS.txt`
- `redis_pending/redis_20251104_192040_MAYA_DATA_TIMELINE_ANALYSIS.txt`
- `redis_pending/redis_20251104_192245_DAMIAN_CRITICAL_REVIEW.txt`
- `redis_pending/redis_20251104_192454_FINAL_INVESTIGATION_REPORT.txt`
- `redis_pending/redis_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.txt`
- `redis_pending/redis_20251104_193555_HYBRID_SYSTEM_QUICK_START.txt`
- `redis_pending/redis_20251104_193622_README.txt`
- `redis_pending/redis_20251104_194002_DATA_SEPARATION_ARCHITECTURE.txt`
- `redis_pending/redis_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.txt`
- `redis_pending/redis_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.txt`
- `redis_pending/redis_20251104_195310_INTERNET_RESEARCH_CAPABILITY.txt`
- `redis_pending/redis_20251104_195345_INTERNET_RESEARCH_CAPABILITY.txt`
- `redis_pending/redis_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.txt`
- `redis_pending/redis_20251104_195847_INVESTIGATION_STATUS.txt`
- `redis_pending/redis_20251104_203406_FINAL_OSINT_REPORT.txt`
- `redis_pending/redis_20251104_203700_FINAL_OSINT_REPORT.txt`
- `redis_pending/redis_20251104_204516_FINAL_OSINT_REPORT.txt`
- `redis_pending/redis_20251104_211443_SEARCH_ORCHESTRATOR.txt`
- `redis_pending/redis_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.txt`
- `redis_pending/redis_20251104_220219_POSTGRES_STUCK_ANALYSIS.txt`
- `redis_pending/redis_20251104_220924_BATCH_MIGRATION_PLAN.txt`
- `requirements.txt`
- `sql/es_document_references_schema.sql`
- `sql/realtime_updates/neo4j_20251104_132626_COMMIT_300ea7b_feature.cypher`
- `sql/realtime_updates/neo4j_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_142244_RESEARCH_DELIVERY_SUMMARY.cypher`
- `sql/realtime_updates/neo4j_20251104_142308_COMMIT_7c01260_change.cypher`
- `sql/realtime_updates/neo4j_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.cypher`
- `sql/realtime_updates/neo4j_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.cypher`
- `sql/realtime_updates/neo4j_20251104_143611_COMMIT_594e664_feature.cypher`
- `sql/realtime_updates/neo4j_20251104_144915_COMMIT_6a77410_documentation.cypher`
- `sql/realtime_updates/neo4j_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.cypher`
- `sql/realtime_updates/neo4j_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.cypher`
- `sql/realtime_updates/neo4j_20251104_145842_COMMIT_038e967_feature.cypher`
- `sql/realtime_updates/neo4j_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.cypher`
- `sql/realtime_updates/neo4j_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.cypher`
- `sql/realtime_updates/neo4j_20251104_151117_COMMIT_388327f_feature.cypher`
- `sql/realtime_updates/neo4j_20251104_183128_INSTITUTIONAL_API_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_183139_README.cypher`
- `sql/realtime_updates/neo4j_20251104_183144_README.cypher`
- `sql/realtime_updates/neo4j_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.cypher`
- `sql/realtime_updates/neo4j_20251104_184219_BELLINGCAT_LEVEL_OSINT.cypher`
- `sql/realtime_updates/neo4j_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_184917_AGENT_TOOLKITS_COMPLETE.cypher`
- `sql/realtime_updates/neo4j_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.cypher`
- `sql/realtime_updates/neo4j_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.cypher`
- `sql/realtime_updates/neo4j_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.cypher`
- `sql/realtime_updates/neo4j_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.cypher`
- `sql/realtime_updates/neo4j_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.cypher`
- `sql/realtime_updates/neo4j_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.cypher`
- `sql/realtime_updates/neo4j_20251104_190812_INVESTIGATION_PLAN.cypher`
- `sql/realtime_updates/neo4j_20251104_190943_ELENA_OSINT_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.cypher`
- `sql/realtime_updates/neo4j_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_191829_ADRIAN_LEGAL_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_192245_DAMIAN_CRITICAL_REVIEW.cypher`
- `sql/realtime_updates/neo4j_20251104_192454_FINAL_INVESTIGATION_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.cypher`
- `sql/realtime_updates/neo4j_20251104_193555_HYBRID_SYSTEM_QUICK_START.cypher`
- `sql/realtime_updates/neo4j_20251104_193622_README.cypher`
- `sql/realtime_updates/neo4j_20251104_194002_DATA_SEPARATION_ARCHITECTURE.cypher`
- `sql/realtime_updates/neo4j_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.cypher`
- `sql/realtime_updates/neo4j_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.cypher`
- `sql/realtime_updates/neo4j_20251104_195310_INTERNET_RESEARCH_CAPABILITY.cypher`
- `sql/realtime_updates/neo4j_20251104_195345_INTERNET_RESEARCH_CAPABILITY.cypher`
- `sql/realtime_updates/neo4j_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.cypher`
- `sql/realtime_updates/neo4j_20251104_195847_INVESTIGATION_STATUS.cypher`
- `sql/realtime_updates/neo4j_20251104_203406_FINAL_OSINT_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251104_203700_FINAL_OSINT_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251104_204516_FINAL_OSINT_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251104_211443_SEARCH_ORCHESTRATOR.cypher`
- `sql/realtime_updates/neo4j_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_220219_POSTGRES_STUCK_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251104_220923_BATCH_MIGRATION_PLAN.cypher`
- `sql/realtime_updates/pg_20251104_132626_COMMIT_300ea7b_feature.sql`
- `sql/realtime_updates/pg_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_142244_RESEARCH_DELIVERY_SUMMARY.sql`
- `sql/realtime_updates/pg_20251104_142308_COMMIT_7c01260_change.sql`
- `sql/realtime_updates/pg_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.sql`
- `sql/realtime_updates/pg_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.sql`
- `sql/realtime_updates/pg_20251104_143611_COMMIT_594e664_feature.sql`
- `sql/realtime_updates/pg_20251104_144915_COMMIT_6a77410_documentation.sql`
- `sql/realtime_updates/pg_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.sql`
- `sql/realtime_updates/pg_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.sql`
- `sql/realtime_updates/pg_20251104_145842_COMMIT_038e967_feature.sql`
- `sql/realtime_updates/pg_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.sql`
- `sql/realtime_updates/pg_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.sql`
- `sql/realtime_updates/pg_20251104_151117_COMMIT_388327f_feature.sql`
- `sql/realtime_updates/pg_20251104_183128_INSTITUTIONAL_API_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_183139_README.sql`
- `sql/realtime_updates/pg_20251104_183144_README.sql`
- `sql/realtime_updates/pg_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.sql`
- `sql/realtime_updates/pg_20251104_184219_BELLINGCAT_LEVEL_OSINT.sql`
- `sql/realtime_updates/pg_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_184917_AGENT_TOOLKITS_COMPLETE.sql`
- `sql/realtime_updates/pg_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.sql`
- `sql/realtime_updates/pg_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.sql`
- `sql/realtime_updates/pg_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.sql`
- `sql/realtime_updates/pg_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.sql`
- `sql/realtime_updates/pg_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.sql`
- `sql/realtime_updates/pg_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.sql`
- `sql/realtime_updates/pg_20251104_190812_INVESTIGATION_PLAN.sql`
- `sql/realtime_updates/pg_20251104_190943_ELENA_OSINT_REPORT.sql`
- `sql/realtime_updates/pg_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.sql`
- `sql/realtime_updates/pg_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_191829_ADRIAN_LEGAL_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_192245_DAMIAN_CRITICAL_REVIEW.sql`
- `sql/realtime_updates/pg_20251104_192454_FINAL_INVESTIGATION_REPORT.sql`
- `sql/realtime_updates/pg_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.sql`
- `sql/realtime_updates/pg_20251104_193555_HYBRID_SYSTEM_QUICK_START.sql`
- `sql/realtime_updates/pg_20251104_193622_README.sql`
- `sql/realtime_updates/pg_20251104_194002_DATA_SEPARATION_ARCHITECTURE.sql`
- `sql/realtime_updates/pg_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.sql`
- `sql/realtime_updates/pg_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.sql`
- `sql/realtime_updates/pg_20251104_195310_INTERNET_RESEARCH_CAPABILITY.sql`
- `sql/realtime_updates/pg_20251104_195345_INTERNET_RESEARCH_CAPABILITY.sql`
- `sql/realtime_updates/pg_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.sql`
- `sql/realtime_updates/pg_20251104_195847_INVESTIGATION_STATUS.sql`
- `sql/realtime_updates/pg_20251104_203406_FINAL_OSINT_REPORT.sql`
- `sql/realtime_updates/pg_20251104_203700_FINAL_OSINT_REPORT.sql`
- `sql/realtime_updates/pg_20251104_204516_FINAL_OSINT_REPORT.sql`
- `sql/realtime_updates/pg_20251104_211443_SEARCH_ORCHESTRATOR.sql`
- `sql/realtime_updates/pg_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_220219_POSTGRES_STUCK_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql`


## 📊 Statistics

```
9b4c756 feat: Implement batch processing system to resolve PostgreSQL performance crisis
 .change_tracking_state.json                        |      4 +-
 BATCH_MIGRATION_PLAN.md                            |    157 +
 POSTGRES_STUCK_ANALYSIS.md                         |     82 +
 README.md                                          |     25 +-
 SOURCE_CITATION_QUICK_REFERENCE.md                 |     99 +
 TECHNICAL_TEAM_RESPONSE.json                       |     90 +
 agents/analytical/damian_agent.py                  |    686 +-
 agents/analytical/tools/__init__.py                |      4 +
 agents/analytical/tools/mathematical_toolkit.py    |    505 +
 agents/analytical/tools/scraping_toolkit.py        |    485 +
 aleksander_emergency_response.py                   |    274 +
 batch_processing_system.py                         |    399 +
 bus/urgent_technical_review.json                   |     27 +
 capabilities_registry.py                           |    681 +
 check_batch_status.sh                              |     28 +
 com.destiny.hourly-batch.plist                     |     29 +
 docs/DATA_ARCHITECTURE_ANALYSIS.md                 |    298 +
 docs/SEARCH_ORCHESTRATOR.md                        |    420 +
 docs/architecture/DATA_SEPARATION_ARCHITECTURE.md  |    731 +
 .../HYBRID_ONPREM_INTELLIGENCE_SYSTEM.md           |   1053 +
 .../2025-11-04/COMMIT_038e967_feature.md           |    263 +
 .../2025-11-04/COMMIT_300ea7b_feature.md           |    361 +
 .../2025-11-04/COMMIT_388327f_feature.md           |    224 +
 .../2025-11-04/COMMIT_594e664_feature.md           |    222 +
 .../2025-11-04/COMMIT_6a77410_documentation.md     |     71 +
 .../2025-11-04/COMMIT_7c01260_change.md            |    185 +
 docs/capabilities/DUCKDUCKGO_SEARCH_METHOD.md      |    397 +
 docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md    |    286 +
 docs/capabilities/INTERNET_RESEARCH_CAPABILITY.md  |    492 +
 docs/concepts/BELLINGCAT_LEVEL_OSINT.md            |   1242 +
 docs/concepts/COMPREHENSIVE_OSINT_SYSTEM.md        |    850 +
 .../concepts/DESTINY_CHAT_UI_HYBRID_INTEGRATION.md |    536 +
 docs/guides/HYBRID_SYSTEM_COMPLETE_OVERVIEW.md     |   1187 +
 docs/guides/HYBRID_SYSTEM_QUICK_START.md           |    587 +
 docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md      |    679 +
 docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md   |   1538 +
 docs/status/MORNING_BRIEF_20251104.md              |    105 +-
 .../SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.md     |    430 +
 docs/team/ADAPTIVE_LEARNING_SYSTEM.md              |    427 +
 .../MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.md   |    421 +
 .../team/SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.md |    576 +
 docs/team/SYSTEM_CAPABILITIES_UPDATE_2025_11_04.md |    555 +
 docs/technical/AGENT_TOOLKITS_COMPLETE.md          |   1327 +
 emergency_fix.sh                                   |     61 +
 examples/search_orchestrator_usage.py              |    280 +
 helena_batch_processor.py                          |    245 +
 helena_core.py                                     |     49 +-
 .../helena_task_20251104_140000_database_schema.md |    203 +
 .../helena_task_20251104_140000_documentation.md   |    206 +
 .../helena_task_20251104_140000_general_change.md  |    188 +
 .../helena_task_20251104_140000_knowledge_graph.md |    193 +
 .../helena_task_20251104_150000_agent_code.md      |    205 +
 .../helena_task_20251104_150000_documentation.md   |    205 +
 .../helena_task_20251104_150000_general_change.md  |    207 +
 .../helena_task_20251104_190000_agent_code.md      |    194 +
 .../helena_task_20251104_190000_documentation.md   |    200 +
 .../helena_task_20251104_190000_general_change.md  |    204 +
 .../helena_task_20251104_200000_documentation.md   |    197 +
 .../helena_task_20251104_210000_documentation.md   |    206 +
 .../helena_task_20251104_210000_general_change.md  |    199 +
 ...ime_20251104_132625_COMMIT_300ea7b_feature.json |      9 +
 ...42119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json |      9 +
 ..._20251104_142244_RESEARCH_DELIVERY_SUMMARY.json |      9 +
 ...time_20251104_142308_COMMIT_7c01260_change.json |      9 +
 ..._143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json |      9 +
 ...3526_FACE_RECOGNITION_TECHNICAL_VALIDATION.json |      9 +
 ...ime_20251104_143610_COMMIT_594e664_feature.json |      9 +
 ...251104_144914_COMMIT_6a77410_documentation.json |      9 +
 ...251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json |      9 +
 ...45753_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json |      9 +
 ...ime_20251104_145842_COMMIT_038e967_feature.json |      9 +
 ..._20251104_150726_SEJM_API_ANALYSIS_CONCEPT.json |      9 +
 ...0251104_151038_SEJM_ASW_ANALYSIS_2019_2023.json |      9 +
 ...ime_20251104_151116_COMMIT_388327f_feature.json |      9 +
 ...20251104_183127_INSTITUTIONAL_API_ANALYSIS.json |      9 +
 .../success_realtime_20251104_183139_README.json   |      9 +
 .../success_realtime_20251104_183144_README.json   |      9 +
 ...20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json |      9 +
 ...ime_20251104_184219_BELLINGCAT_LEVEL_OSINT.json |      9 +
 ...104_184617_BELLINGCAT_METHODOLOGY_ANALYSIS.json |      9 +
 ...me_20251104_184916_AGENT_TOOLKITS_COMPLETE.json |      9 +
 ...5327_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json |      9 +
 ...e_20251104_185810_ADAPTIVE_LEARNING_SYSTEM.json |      9 +
 ...58_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json |      9 +
 ...0251104_190458_SOURCE_ATTRIBUTION_PROTOCOL.json |      9 +
 ...104_190530_SOURCE_CITATION_QUICK_REFERENCE.json |      9 +
 ..._MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json |      9 +
 ...ealtime_20251104_190812_INVESTIGATION_PLAN.json |      9 +
 ...ealtime_20251104_190943_ELENA_OSINT_REPORT.json |      9 +
 ...154_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json |      9 +
 ..._20251104_191612_MARCUS_FINANCIAL_ANALYSIS.json |      9 +
 ...time_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json |      9 +
 ...0251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json |      9 +
 ...ime_20251104_192245_DAMIAN_CRITICAL_REVIEW.json |      9 +
 ...20251104_192454_FINAL_INVESTIGATION_REPORT.json |      9 +
 ...4_193139_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json |      9 +
 ..._20251104_193555_HYBRID_SYSTEM_QUICK_START.json |      9 +
 .../success_realtime_20251104_193622_README.json   |      9 +
 ...251104_194001_DATA_SEPARATION_ARCHITECTURE.json |      9 +
 ...104_194329_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json |      9 +
 ..._194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json |      9 +
 ...251104_195309_INTERNET_RESEARCH_CAPABILITY.json |      9 +
 ...251104_195344_INTERNET_RESEARCH_CAPABILITY.json |      9 +
 ...e_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json |      9 +
 ...ltime_20251104_195846_INVESTIGATION_STATUS.json |      9 +
 ...ealtime_20251104_203406_FINAL_OSINT_REPORT.json |      9 +
 ...ealtime_20251104_203700_FINAL_OSINT_REPORT.json |      9 +
 ...ealtime_20251104_204516_FINAL_OSINT_REPORT.json |      9 +
 ...altime_20251104_211442_SEARCH_ORCHESTRATOR.json |      9 +
 ...20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json |      9 +
 ...me_20251104_220219_POSTGRES_STUCK_ANALYSIS.json |      9 +
 ...ltime_20251104_220923_BATCH_MIGRATION_PLAN.json |      9 +
 hourly_batch_processor.py                          |    389 +
 .../telus_cpk_real_001/FINAL_OSINT_REPORT.md       |     95 +
 .../telus_cpk_real_001/INVESTIGATION_STATUS.md     |     78 +
 .../sources/web/businessinsider_telus.html         |   5316 +
 .../sources/web/cpk_official.html                  |    936 +
 .../sources/web/cpk_wikipedia.html                 |   1814 +
 .../sources/web/onet_telus_cpk.html                |    383 +
 .../sources/web/tvn24_telus_cpk.html               |   1033 +
 .../sources/web/wikipedia_telus.html               |   1118 +
 .../elasticsearch_integration_20251104_210917.json |    236 +
 .../concepts/search_orchestrator_test_report.json  |    151 +
 .../run_20251104_205052/elasticsearch_bulk.ndjson  |    750 +
 .../elasticsearch_text_updates.ndjson              |    450 +
 ...idowanesprawozdaniefinansowezaiiikwarta2010.pdf |    Bin 0 -> 1902851 bytes
 .../pdfs/1329119707azotytarnowqsriiikwarta2009.pdf |    Bin 0 -> 799869 bytes
 ...idowanesprawozdaniefinansowezaiiikwarta2011.pdf |    Bin 0 -> 2281268 bytes
 .../pdfs/1329119889azotytarnowqsrikwarta2009.pdf   |    Bin 0 -> 14394452 bytes
 ...dowanesprawozdaniezaikwarta2011opublikowany.pdf |    Bin 0 -> 1735915 bytes
 ...0309skonsolidowanesprawozdaniezaikwarta2010.pdf |    Bin 0 -> 684221 bytes
 .../pdfs/1329120313raportivq2009bezpodpisow.pdf    |    Bin 0 -> 691735 bytes
 .../1329483078azotytarnowqsriiikwartal2008.pdf     |    Bin 0 -> 607078 bytes
 .../pdfs/1329483098azotytarnowqsrivkwarta2008.pdf  |    Bin 0 -> 792306 bytes
 ...329485603sprawozdaniefinansoweiikwartal2008.pdf |    Bin 0 -> 493644 bytes
 .../pdfs/1Ocena_20Rady_20Nadzorczej_202019.pdf     |    Bin 0 -> 148657 bytes
 ...ako_C5_84czony_2030_20czerwca_202021_20roku.pdf |    Bin 0 -> 1805227 bytes
 .../run_20251104_205052/pdfs/2017.pdf              |    Bin 0 -> 1251228 bytes
 .../run_20251104_205052/pdfs/2018.pdf              |  24282 ++++
 .../run_20251104_205052/pdfs/2019.pdf              |  21835 ++++
 ...ako_C5_84czony_2030_20czerwca_202021_20roku.pdf |    Bin 0 -> 1437880 bytes
 ...20za_20I_20p_C3_B3_C5_82rocze_202021_20roku.pdf |    Bin 0 -> 2374237 bytes
 ...C3_B3drocznego_20sprawozdania_20finansowego.pdf |    Bin 0 -> 694115 bytes
 ...9cy20zakoC584czony203020czerwca20201920roku.pdf |  48580 +++++++
 ...9cy20zakoC584czony203020czerwca20201920roku.pdf |  70995 ++++++++++
 ...rupaAzoty_OswiadczenieZarzadu-2021-12-31-pl.pdf |    Bin 0 -> 345252 bytes
 ...paAzoty_SprawozdanieFinansowe-2021-12-31-pl.pdf |    Bin 0 -> 2331855 bytes
 ...rupaAzoty_SprawozdanieZarzadu-2021-12-31-pl.pdf |    Bin 0 -> 4088161 bytes
 .../pdfs/Grupa_Azoty_List_Prezesa_Zarzadu_2022.pdf |    Bin 0 -> 96970 bytes
 .../pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu.pdf      |    Bin 0 -> 599624 bytes
 .../pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2022.pdf |    Bin 0 -> 635990 bytes
 .../pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2023.pdf |    Bin 0 -> 658391 bytes
 .../pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2024.pdf |    Bin 0 -> 189356 bytes
 ..._Skonsolidowane_Sprawozdanie_Finansowe_2022.pdf |    Bin 0 -> 2812457 bytes
 ..._Skonsolidowane_Sprawozdanie_Finansowe_2023.pdf |    Bin 0 -> 5653226 bytes
 ..._Skonsolidowane_Sprawozdanie_Finansowe_2024.pdf |    Bin 0 -> 2801610 bytes
 ...olidowane_Sprawozdanie_Finansowe_I_polrocze.pdf |    Bin 0 -> 2367986 bytes
 ...wane_Sprawozdanie_Finansowe_I_polrocze_2023.pdf |    Bin 0 -> 2326903 bytes
 ...wane_Sprawozdanie_Finansowe_I_polrocze_2024.pdf |    Bin 0 -> 2059464 bytes
 ...wane_Sprawozdanie_Finansowe_I_polrocze_2025.pdf |  56906 ++++++++
 ...solidowany_Raport_za_20_I_kwarta_C5_82_2022.pdf |    Bin 0 -> 2421152 bytes
 ...y_Skonsolidowany_Raport_za_III_kwartal_2022.pdf |    Bin 0 -> 2707126 bytes
 ...y_Skonsolidowany_Raport_za_III_kwartal_2023.pdf |    Bin 0 -> 2818070 bytes
 ...y_Skonsolidowany_Raport_za_III_kwartal_2024.pdf |    Bin 0 -> 2713302 bytes
 ...oty_Skonsolidowany_Raport_za_I_kwartal_2023.pdf |    Bin 0 -> 2653741 bytes
 ...konsolidowany_Raport_za_I_kwartal_2024_roku.pdf |    Bin 0 -> 6486143 bytes
 ...oty_Skonsolidowany_Raport_za_I_kwartal_2025.pdf |    Bin 0 -> 2301368 bytes
 .../Grupa_Azoty_Sprawozdanie_Finansowe_2022.pdf    |    Bin 0 -> 2436592 bytes
 .../Grupa_Azoty_Sprawozdanie_Finansowe_2023.pdf    |    Bin 0 -> 5179337 bytes
 .../Grupa_Azoty_Sprawozdanie_Finansowe_2024.pdf    |    Bin 0 -> 2079981 bytes
 ...upa_Azoty_Sprawozdanie_Finansowe_I_polrocze.pdf |    Bin 0 -> 1963466 bytes
 ...zoty_Sprawozdanie_Finansowe_I_polrocze_2023.pdf |    Bin 0 -> 1997184 bytes
 ...zoty_Sprawozdanie_Finansowe_I_polrocze_2024.pdf |    Bin 0 -> 1872494 bytes
 ...zoty_Sprawozdanie_Finansowe_I_polrocze_2025.pdf |  41856 ++++++
 .../pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2022.pdf |    Bin 0 -> 3736601 bytes
 .../pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2023.pdf |    Bin 0 -> 4413382 bytes
 ..._Azoty_Sprawozdanie_Zarzadu_I_polrocze_2022.pdf |    Bin 0 -> 2237984 bytes
 ...Azoty_Sprawozdanie_Zarzadu_I_polrocze_2023_.pdf |    Bin 0 -> 2237892 bytes
 ..._Azoty_Sprawozdanie_Zarzadu_I_polrocze_2024.pdf |    Bin 0 -> 2494136 bytes
 ..._Azoty_Sprawozdanie_Zarzadu_I_polrocze_2025.pdf |    Bin 0 -> 1804537 bytes
 ...zoty_Sprawozdanie_z_platnosci_adm_publ_2022.pdf |    Bin 0 -> 525612 bytes
 ...zoty_Sprawozdanie_z_platnosci_adm_publ_2023.pdf |    Bin 0 -> 1642941 bytes
 ...zoty_Sprawozdanie_z_platnosci_adm_publ_2024.pdf |    Bin 0 -> 726590 bytes
 ...ednostkowe20Sprawozdanie20Finansowe201H2017.pdf |    Bin 0 -> 894751 bytes
 ...ednostkowe20Sprawozdanie20Finansowe201H2018.pdf |    Bin 0 -> 1102116 bytes
 .../Jednostkowe20sprawozdanie20finansowe202017.pdf |    Bin 0 -> 2402380 bytes
 ...20SpC3B3C582ki20Grupa20Azoty20za20rok202018.pdf | 100698 ++++++++++++++
 ...owe20sprawozdanie20finansowe20za20rok202016.pdf |    Bin 0 -> 2046605 bytes
 ...Jednostkowe20wybrane20dane20finansowe202016.pdf |    Bin 0 -> 115844 bytes
 ...Jednostkowe20wybrane20dane20finansowe202017.pdf |    Bin 0 -> 161876 bytes
 ...Jednostkowe20wybrane20dane20finansowe202018.pdf |    Bin 0 -> 163879 bytes
 .../pdfs/List20Prezesa20ZarzC485du.pdf             |    Bin 0 -> 2033459 bytes
 .../pdfs/ListPrez_GrupaAzoty-2024-12-31-0-pl.pdf   |    Bin 0 -> 1641773 bytes
 .../pdfs/List_20Prezesa_20Zarz_C4_85du.pdf         |    Bin 0 -> 1053313 bytes
 .../pdfs/List_Prezesa_Zarzadu.pdf                  |    Bin 0 -> 630846 bytes
 ...iadczenie20Rady20Nadzorczej20-20jednostkowe.pdf |    Bin 0 -> 352704 bytes
 ...czenie20Rady20Nadzorczej20-20skonsolidowane.pdf |    Bin 0 -> 355893 bytes
 ...C485du20-20podmiot20uprawniony20do20badania.pdf |    Bin 0 -> 305323 bytes
 ...nie20ZarzC485du20-20sprawozdania20finansowe.pdf |    Bin 0 -> 134156 bytes
 ...cznego20sprawozdania20finansowego30.06.2019.pdf |   2275 +
 ...py20Azoty20do20sprawozdaC58420za20201820rok.pdf |   2128 +
 ...20o20podmiocie20uprawnionym20-20jednostkowe.pdf |    Bin 0 -> 337804 bytes
 ...20podmiocie20uprawnionym20-20skonsolidowane.pdf |    Bin 0 -> 319789 bytes
 ...20ZarzC485du20o20sprawozdaniu20jednostkowym.pdf |    Bin 0 -> 354883 bytes
 ...arzC485du20o20sprawozdaniu20skonsolidowanym.pdf |    Bin 0 -> 333535 bytes
 ...C3_B3drocznego_20sprawozdania_20finansowego.pdf |   2669 +
 ...odmiocie_20uprawnionym_20-_20skonsolidowane.pdf |    Bin 0 -> 338172 bytes
 ...4_85du_20o_20sprawozdaniu_20skonsolidowanym.pdf |    Bin 0 -> 358285 bytes
 .../pdfs/Ocena20Rady20Nadzorczej.pdf               |    Bin 0 -> 1258527 bytes
 ...Ocena_20Rady_20Nadzorczej_20-_20jednostkowe.pdf |    Bin 0 -> 149910 bytes
 .../pdfs/Ocena_Rady_Nadzorczej_2024.pdf            |    Bin 0 -> 346803 bytes
 .../Ocena_Rady_Nadzorczej_skonsolidowane_2024.pdf  |    Bin 0 -> 346818 bytes
 .../Ocena_Rady_Nadzorczej_sprawozdanie_2023.pdf    |    Bin 0 -> 173487 bytes
 ...a_Rady_Nadzorczej_sprawozdanie_Zarzadu_2022.pdf |    Bin 0 -> 808103 bytes
 ...a_Rady_Nadzorczej_sprawozdanie_Zarzadu_2023.pdf |    Bin 0 -> 173477 bytes
 ...Rady_Nadzorczej_sprawozdanie_finansowe_2022.pdf |    Bin 0 -> 810278 bytes
 ...Nadzorczej_sprawozdanie_skonsolidowane_2022.pdf |    Bin 0 -> 810188 bytes
 ...Nadzorczej_sprawozdanie_skonsolidowane_2023.pdf |    Bin 0 -> 173487 bytes
 ...ort20biegC582ego20rewidenta20-20jednostkowe.pdf |    Bin 0 -> 1048644 bytes
 ...20biegC582ego20rewidenta20-20skonsolidowane.pdf |    Bin 0 -> 1294289 bytes
 .../pdfs/Oswiadczenie_Rady-Nadzorczej_2023.pdf     |    Bin 0 -> 145371 bytes
 .../pdfs/Oswiadczenie_Rady_Nadzorczej.pdf          |    Bin 0 -> 197637 bytes
 .../pdfs/Oswiadczenie_Rady_Nadzorczej_2022.pdf     |    Bin 0 -> 447821 bytes
 .../pdfs/Oswiadczenie_Rady_Nadzorczej_2024.pdf     |    Bin 0 -> 321013 bytes
 ...dczenie_Rady_Nadzorczej_skonsolidowane_2023.pdf |    Bin 0 -> 145501 bytes
 ...dczenie_Rady_Nadzorczej_skonsolidowane_2024.pdf |    Bin 0 -> 321158 bytes
 .../pdfs/Oswiadczenie_Zarzadu.pdf                  |    Bin 0 -> 756792 bytes
 ...go20rewidenta20-20sprawozdanie20jednostkowe.pdf |    Bin 0 -> 267304 bytes
 ...0rewidenta20-20sprawozdanie20skonsolidowane.pdf |    Bin 0 -> 268401 bytes
 ...0rewidenta_20-_20sprawozdanie_20jednostkowe.pdf |    Bin 0 -> 506832 bytes
 ...widenta_20-_20sprawozdanie_20skonsolidowane.pdf |    Bin 0 -> 507591 bytes
 ...u_20JSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf |    Bin 0 -> 321021 bytes
 ...u_20SSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf |    Bin 0 -> 320917 bytes
 .../pdfs/Raport_Bieglego_Rewidenta-sig-sig.pdf     |    Bin 0 -> 536754 bytes
 ...t_Bieglego_Rewidenta_skonsolidowane-sig-sig.pdf |    Bin 0 -> 536210 bytes
 .../pdfs/Raport_Przeglad_GASA_JSF.pdf              |    Bin 0 -> 475187 bytes
 .../pdfs/Raport_Przeglad_GASA_SSF.pdf              |    Bin 0 -> 475608 bytes
 .../pdfs/Raport_Przeglad_GAT_JSF_H1_2024.pdf       |    Bin 0 -> 330062 bytes
 .../pdfs/Raport_Przeglad_GK_GAT_SSF_H1_2024.pdf    |    Bin 0 -> 331145 bytes
 .../pdfs/Raport__przegl_C4_85du_GAT_.pdf           |    Bin 0 -> 323131 bytes
 .../pdfs/Raport_z_przegladu_GK_GAT.pdf             |    Bin 0 -> 318932 bytes
 ...solidowane20Sprawozdanie20Finansowe201H2018.pdf |    Bin 0 -> 1641142 bytes
 ...z20administracji20publicznej20za20201820rok.pdf |   6637 +
 ...solidowane20sprawozdanie20finansowe201H2017.pdf |    Bin 0 -> 1199890 bytes
 ...KapitaC582owej20Grupa20Azoty20za20rok202018.pdf | 122321 ++++++++++++++++++
 ...ane20sprawozdanie20finansowe20za20rok202016.pdf |    Bin 0 -> 2310298 bytes
 ...nsolidowane20wybrane20dane20finansowe202016.pdf |    Bin 0 -> 116977 bytes
 ...nsolidowane20wybrane20dane20finansowe202018.pdf |    Bin 0 -> 164632 bytes
 ...olidowane_20sprawozdanie_20finansowe_202017.pdf |    Bin 0 -> 2729884 bytes
 ...idowane_20wybrane_20dane_20finansowe_202017.pdf |    Bin 0 -> 163084 bytes
 .../Skonsolidowane_wybrane_dane_finansowe_2021.pdf |    Bin 0 -> 303598 bytes
 .../Skonsolidowany20raport20kwartalny203Q2017.pdf  |    Bin 0 -> 1617612 bytes
 ...Grupa20Azoty20za20I20kwartaC58220201920roku.pdf |  52684 ++++++++
 ...20raport20okresowy20za20120kwartaC582202018.pdf |    Bin 0 -> 1894924 bytes
 ...20raport20okresowy20za20320kwartaC582202018.pdf |    Bin 0 -> 2321303 bytes
 ...20raport20okresowy20za20I20kwartaC582202017.pdf |    Bin 0 -> 1513391 bytes
 ...owy_20GKGA_20za_20III_20kwarta_C5_82_202021.pdf |    Bin 0 -> 2355733 bytes
 ..._20za_20III_20kwarta_C5_82_202019_20roku_1_.pdf |  85539 ++++++++++++
 ...Azoty_20za_20I_20kwarta_C5_82_202020_20roku.pdf |  53154 ++++++++
 ...apitalowej_Grupa_Azoty_za_III_kwartal_2020_.pdf |    Bin 0 -> 2596901 bytes
 .../pdfs/Spraw_zrown_rozw_2024.pdf                 |    Bin 0 -> 1857112 bytes
 .../pdfs/Sprawozdanie-SPS-2016.pdf                 |    Bin 0 -> 317940 bytes
 ...osci-na-rzecz-administracji-publicznej-2017.pdf |    Bin 0 -> 550690 bytes
 .../pdfs/Sprawozdanie20ZarzC485du201H2017.pdf      |    Bin 0 -> 1165730 bytes
 ...ie20ZarzC485du20z20dziaC582alnoC59Bci202016.pdf |    Bin 0 -> 2496740 bytes
 ...ZarzC485du20z20dziaC582alnoC59Bci20GK202017.pdf |    Bin 0 -> 3206851 bytes
 ...9cy20zakoC584czony203120grudnia20201820roku.pdf |  74799 +++++++++++
 ...a20Azoty20za20I20pC3B3C582rocze20201920roku.pdf |  29152 +++++
 .../pdfs/Sprawozdanie20Zarzadu201H2018.pdf         |    Bin 0 -> 1444120 bytes
 ...go20rewidenta20-20sprawozdanie20jednostkowe.pdf |    Bin 0 -> 397180 bytes
 ...9cy20zakoC584czony203120grudnia20201820roku.pdf |  24282 ++++
 .../Sprawozdanie20z20badania20-20jednostkowe.pdf   |    Bin 0 -> 348656 bytes
 ...Sprawozdanie20z20badania20-20skonsolidowane.pdf |    Bin 0 -> 385686 bytes
 ...du_20z_20dzia_C5_82alno_C5_9Bci_20GK_202017.pdf |    Bin 0 -> 3206851 bytes
 ...20za_20I_20p_C3_B3_C5_82rocze_202020_20roku.pdf |  29340 +++++
 ...widenta_20-_20sprawozdanie_20skonsolidowane.pdf |    Bin 0 -> 512296 bytes
 ...e_20nt_20informacji_20niefinansowych_202017.pdf |    Bin 0 -> 1251228 bytes
 ..._informacji_niefinansowych_Grupy_Azoty_2022.pdf |    Bin 0 -> 3702219 bytes
 ..._informacji_niefinansowych_Grupy_Azoty_2023.pdf |    Bin 0 -> 6157316 bytes
 ...acji_niefinansowych_Grupy_Azoty_za_2021_rok.pdf |    Bin 0 -> 4095810 bytes
 ...i_niefinansowych_Grupy_Azoty_za_2021_rok_pl.pdf |    Bin 0 -> 4087279 bytes
 .../pdfs/SzB_GAT_2022.xhtml.pdf                    |    Bin 0 -> 1320611 bytes
 .../pdfs/SzB_GK_GAT_2022.xhtml.pdf                 |    Bin 0 -> 1637274 bytes
 .../pdfs/SzD_GrupaAzoty-2024-12-31-0-pl.pdf        |    Bin 0 -> 5524388 bytes
 .../pdfs/Wybrane20dane20finansowe201H2017.pdf      |    Bin 0 -> 197123 bytes
 .../pdfs/Wybrane20dane20finansowe201H2018.pdf      |    Bin 0 -> 233646 bytes
 .../pdfs/Wybrane20dane20finansowe201H2019.pdf      |    Bin 0 -> 232972 bytes
 .../pdfs/Wybrane20dane20finansowe201Q202019.pdf    |    Bin 0 -> 232561 bytes
 .../pdfs/Wybrane20dane20finansowe203Q2017.pdf      |    Bin 0 -> 232267 bytes
 .../pdfs/Wybrane20dane20finansowe203Q2018.pdf      |    Bin 0 -> 233137 bytes
 .../Wybrane_20dane_20finansowe_201H_202020.pdf     |    Bin 0 -> 233722 bytes
 .../Wybrane_20dane_20finansowe_201Q_202020.pdf     |    Bin 0 -> 232162 bytes
 ...ane_20finansowe_20III_20kwarta_C5_82_202021.pdf |    Bin 0 -> 150798 bytes
 ...20finansowe_20I_20p_C3_B3_C5_82rocze_202021.pdf |    Bin 0 -> 233949 bytes
 .../pdfs/Wybrane_dane_finansowe_1Q_2022.pdf        |    Bin 0 -> 369186 bytes
 .../pdfs/Wybrane_dane_finansowe_2021.pdf           |    Bin 0 -> 302828 bytes
 .../pdfs/Wybrane_dane_finansowe_3Q2020.pdf         |    Bin 0 -> 232316 bytes
 ...ako_C5_84czony_2030_20czerwca_202020_20roku.pdf |  47074 +++++++
 ...a_20okres_206_20miesi_C4_99cy_202020_20roku.pdf |  67089 ++++++++++
 .../pdfs/jednostkowesprawozdaniefinansowe2013.pdf  |    Bin 0 -> 1833173 bytes
 .../pdfs/jednostkowesprawozdaniefinansowe2014.pdf  |    Bin 0 -> 1663676 bytes
 .../jednostkowesprawozdaniefinansowezarok2011.pdf  |    Bin 0 -> 2484474 bytes
 .../jednostkowesprawozdaniefinansowezarok2012.pdf  |    Bin 0 -> 1730088 bytes
 .../jednostkowesprawozdaniefinansowezarok2015.pdf  |    Bin 0 -> 1903016 bytes
 .../pdfs/jednostkowewybranedanefinansowe.pdf       |    Bin 0 -> 115325 bytes
 .../pdfs/jednostkowewybranedanefinansowe2011.pdf   |    Bin 0 -> 491145 bytes
 .../pdfs/jednostkowewybranedanefinansowe2015.pdf   |    Bin 0 -> 115768 bytes
 .../jednostkowewybranedanefinansowezarok2012.pdf   |    Bin 0 -> 116005 bytes
 .../pdfs/listprezesa-1h2014.pdf                    |    Bin 0 -> 232661 bytes
 .../pdfs/listprezesazarzadu.pdf                    |    Bin 0 -> 2351919 bytes
 ...iabieglegorewidenta-sprawozdaniejednostkowe.pdf |    Bin 0 -> 265293 bytes
 ...eglegorewidenta-sprawozdaniejednostkowe2011.pdf |    Bin 0 -> 957582 bytes
 ...ieglegorewidenta-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 203375 bytes
 ...orewidenta-sprawozdanieskonsolidowaners2011.pdf |    Bin 0 -> 928092 bytes
 ...ieglegoreiwdenta-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 587590 bytes
 ...aportbieglegorewidenta-sprawozd.jednostkowe.pdf |    Bin 0 -> 580231 bytes
 ...rtbieglegorewidenta-sprawozd.skonsolidowane.pdf |    Bin 0 -> 7103069 bytes
 ...rtbieglegorewidenta-sprawozdaniejednostkowe.pdf |    Bin 0 -> 1467026 bytes
 ...ieglegorewidenta-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 1532485 bytes
 ...nsolidowanymiopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 375387 bytes
 .../pdfs/oswiadczeniazarzadu.pdf                   |    Bin 0 -> 360518 bytes
 .../pdfs/oswiadczeniazarzadu1h2012.pdf             |    Bin 0 -> 376694 bytes
 .../pdfs/oswiadczeniazarzadu1h2014.pdf             |    Bin 0 -> 691830 bytes
 .../pdfs/oswiadczeniazarzadu1h2015.pdf             |    Bin 0 -> 674744 bytes
 ...prawnionymdobadania-sprawozdaniejednostkowe.pdf |    Bin 0 -> 168699 bytes
 ...nionymdobadania-sprawozdaniejednostkowe2011.pdf |    Bin 0 -> 301368 bytes
 ...wnionymdobadania-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 169279 bytes
 ...mdobadania-sprawozdanieskonsolidowaners2011.pdf |    Bin 0 -> 303219 bytes
 ...iadczenieoskonsolidowanymsprawozdaniurs2011.pdf |    Bin 0 -> 325878 bytes
 .../pdfs/oswiadczenieosprawozdaniujednostkowym.pdf |    Bin 0 -> 176422 bytes
 .../oswiadczenieosprawozdaniujednostkowym2011.pdf  |    Bin 0 -> 308445 bytes
 ...jednostkowymiopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 363786 bytes
 ...ujednostkowymipodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 499628 bytes
 .../oswiadczenieosprawozdaniuskonsolidowanym.pdf   |    Bin 0 -> 177491 bytes
 ...onsolidowanymipodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 505537 bytes
 ...iadczeniezarzadu-podmiotuprawnionydobadania.pdf |    Bin 0 -> 319690 bytes
 .../oswiadczeniezarzadu-sprawozdaniafinansowe.pdf  |    Bin 0 -> 312865 bytes
 .../pdfs/oswiadczeniezarzadu.pdf                   |    Bin 0 -> 139346 bytes
 ...niezarzaduopodmiocieuprawnionym-jednostkowe.pdf |    Bin 0 -> 279805 bytes
 ...zarzaduopodmiocieuprawnionym-skonsolidowane.pdf |    Bin 0 -> 275761 bytes
 ...adczeniezarzaduosprawozdaniuskonsolidowanym.pdf |    Bin 0 -> 286526 bytes
 ...prawnionegodobadaniasprawozdaniafinansowego.pdf |    Bin 0 -> 65269 bytes
 ...telnoscisporzadzeniesprawozdaniafinansowego.pdf |    Bin 0 -> 74527 bytes
 .../pdfs/pismoprezesazarzadu2011.pdf               |    Bin 0 -> 704228 bytes
 .../pdfs/pismoprezesazarzadurs2011.pdf             |    Bin 0 -> 704228 bytes
 ...olroczneskonsolidowanesprawozdaniefinansowe.pdf |    Bin 0 -> 9802171 bytes
 ...zneskroconejednostkowesprawozdaniefinansowe.pdf |    Bin 0 -> 1459828 bytes
 .../pdfs/r2007opiniairaportbieglegorewidenta.pdf   |    Bin 0 -> 4171355 bytes
 ...7oswiadczenieopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 662003 bytes
 .../pdfs/r2007oswiadczenieosprawozdaniurocznym.pdf |    Bin 0 -> 724439 bytes
 .../pdfs/r2007pismoprezesazarzadu.pdf              |    Bin 0 -> 1654320 bytes
 .../pdfs/r2007sprawozdaniefinansowe.pdf            |    Bin 0 -> 11298152 bytes
 .../pdfs/r2007sprawozdaniezdzialalnoscispolki.pdf  |    Bin 0 -> 7712087 bytes
 ...badaniajednostkowegosprawozdaniafinansowego.pdf |    Bin 0 -> 552558 bytes
 ...aniaskonsolidowanegosprawozdaniafinansowego.pdf |    Bin 0 -> 164373 bytes
 ...swiadczenieojednostkowymsprawozdaniurocznym.pdf |    Bin 0 -> 148585 bytes
 ...obadaniajednostkowegosprawozdaniafinsnowego.pdf |    Bin 0 -> 136638 bytes
 ...daniaskonsolidowanegosprawozdaniafinsnowego.pdf |    Bin 0 -> 147821 bytes
 ...adczenieoskonsolidowanymsprawozdaniurocznym.pdf |    Bin 0 -> 167212 bytes
 ...8pismoprezesazarzadusprawozdaniejednostkowe.pdf |    Bin 0 -> 551812 bytes
 ...smoprezesazarzadusprawozdanieskonsolidowane.pdf |    Bin 0 -> 451879 bytes
 ...badaniajednostkowegosprawozdaniafinansowego.pdf |    Bin 0 -> 858805 bytes
 ...aniaskonsolidowanegosprawozdaniafinansowego.pdf |    Bin 0 -> 730025 bytes
 ...r2008rocznejednostkowesprawozdaniefinansowe.pdf |    Bin 0 -> 13640973 bytes
 ...08roczneskonsolidowanesprawozdaniefinansowe.pdf |    Bin 0 -> 14926000 bytes
 ...8sprawozdaniejednostkowezdzialalnoscispolki.pdf |    Bin 0 -> 11236691 bytes
 ...ozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf |    Bin 0 -> 8506688 bytes
 .../pdfs/r2009opiniabieglegorewidenta.pdf          |    Bin 0 -> 314389 bytes
 ...9oswiadczenieopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 77514 bytes
 .../r2009oswiadczenieosprawozdaniujednostkowym.pdf |    Bin 0 -> 84947 bytes
 .../pdfs/r2009pismoprezesazarzadu.pdf              |    Bin 0 -> 487684 bytes
 .../r2009raportpodmiotuuprawnionegodobadania.pdf   |    Bin 0 -> 1371793 bytes
 ...r2009rocznejednostkowesprawozdaniefinansowe.pdf |    Bin 0 -> 931539 bytes
 ...9sprawozdaniejednostkowezdzialalnoscispolki.pdf |    Bin 0 -> 926313 bytes
 .../pdfs/r2009wybranedanefinansowe.pdf             |    Bin 0 -> 94109 bytes
 ...10jednostkowesprawozdaniefinansowezarok2010.pdf |    Bin 0 -> 2522237 bytes
 .../pdfs/r2010opiniabieglegorewidenta.pdf          |    Bin 0 -> 978116 bytes
 ...0oswiadczenieopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 275975 bytes
 .../r2010oswiadczenieosprawozdaniujednostkowym.pdf |    Bin 0 -> 298091 bytes
 .../pdfs/r2010pismoprezesazarzadu.pdf              |    Bin 0 -> 2141179 bytes
 .../r2010raportpodmiotuuprawnionegodobadania.pdf   |    Bin 0 -> 1247808 bytes
 ...r2010sprawozdaniezarzaduzdzialalnoscispolki.pdf |    Bin 0 -> 1037016 bytes
 .../pdfs/r2010wybranedanefinansowe.pdf             |    Bin 0 -> 512353 bytes
 .../raportadytora-sprawozdanieskonsolidowane.pdf   |    Bin 0 -> 754613 bytes
 .../raportaudytora-sprawozdaniejednostkowe.pdf     |    Bin 0 -> 74954 bytes
 .../raportaudytora-sprawozdaniejednostkowe1.pdf    |    Bin 0 -> 736141 bytes
 .../raportaudytora-sprawozdanieskonsolidowane.pdf  |    Bin 0 -> 75946 bytes
 .../raportaudytora-sprawozdanieskonsolidowane1.pdf |    Bin 0 -> 750777 bytes
 ...rtbieglegorewidenta-sprawozdaniejednostkowe.pdf |    Bin 0 -> 557472 bytes
 ...ieglegorewidenta-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 931866 bytes
 .../pdfs/raportbieglegosprjednostkowe.pdf          |    Bin 0 -> 618961 bytes
 .../pdfs/raportbieglegosprskonsolidowane.pdf       |    Bin 0 -> 641744 bytes
 .../raportniezaleznegobieglegorewidenta3q2012.pdf  |    Bin 0 -> 682363 bytes
 ...ionegodobadania-sprawozdaniejednostkowe2011.pdf |    Bin 0 -> 1220004 bytes
 ...odobadania-sprawozdanieskonsolidowaners2011.pdf |    Bin 0 -> 1425335 bytes
 ...cybieglegorewidenta-sprawozdaniejednostkowe.pdf |    Bin 0 -> 1527251 bytes
 ...ieglegorewidenta-sprawozdanieskonsolidowane.pdf |    Bin 0 -> 2528745 bytes
 ...ocznymskonsolidowanymsprawozdaniufinansowym.pdf |    Bin 0 -> 1096642 bytes
 ...aniaskonsolidowanegosprawozdaniafinansowego.pdf |    Bin 0 -> 155436 bytes
 ...eniaskonsolidowanegosprawozdaniafinansowego.pdf |    Bin 0 -> 172296 bytes
 .../pdfs/rs2007pismoprezesazarzadu.pdf             |    Bin 0 -> 370120 bytes
 ...negoskonsolidowanegosprawozdaniafinansowego.pdf |    Bin 0 -> 4006255 bytes
 ...07roczneskonsolidowanesprawozdaniefinansowe.pdf |    Bin 0 -> 5631642 bytes
 ...ozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf |    Bin 0 -> 5692146 bytes
 .../pdfs/rs2009opiniabieglegorewidenta.pdf         |    Bin 0 -> 376769 bytes
 ...9oswiadczenieopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 87831 bytes
 ...009oswiadczenieoskonsolidowanymsprawozdaniu.pdf |    Bin 0 -> 100324 bytes
 .../pdfs/rs2009pismoprezesazarzadu.pdf             |    Bin 0 -> 562741 bytes
 .../rs2009raportpodmiotuuprawnionegodobadania.pdf  |    Bin 0 -> 1535571 bytes
 ...konsolidowanesprawozdaniefinansowezarok2009.pdf |    Bin 0 -> 1112082 bytes
 ...rzaduzdzialalnoscigrupykapitalowejzarok2009.pdf |    Bin 0 -> 1121882 bytes
 .../pdfs/rs2009wybranedanefinansowe.pdf            |    Bin 0 -> 110335 bytes
 .../pdfs/rs2010opiniabieglegorewidenta.pdf         |    Bin 0 -> 940114 bytes
 ...0oswiadczenieopodmiocieuprawnionymdobadania.pdf |    Bin 0 -> 289764 bytes
 ...010oswiadczenieoskonsolidowanymsprawozdaniu.pdf |    Bin 0 -> 316715 bytes
 .../pdfs/rs2010pismoprezesazarzadu.pdf             |    Bin 0 -> 2138398 bytes
 .../rs2010raportpodmiotuuprawnionegodobadania.pdf  |    Bin 0 -> 1459646 bytes
 ...olidowanesprawozdaniefinansowegkazotytarnow.pdf |    Bin 0 -> 2776907 bytes
 ...rawozdaniezarzaduzdzialalnoscigkazotytarnow.pdf |    Bin 0 -> 2121090 bytes
 .../pdfs/rs2010wybranedanefinansowe.pdf            |    Bin 0 -> 513701 bytes
 .../pdfs/skonsolidowanesprawozdaniefinansowe.pdf   |    Bin 0 -> 7967827 bytes
 .../skonsolidowanesprawozdaniefinansowe2013.pdf    |    Bin 0 -> 2303424 bytes
 .../skonsolidowanesprawozdaniefinansowe2014.pdf    |    Bin 0 -> 2166651 bytes
 ...olidowanesprawozdaniefinansoweipolrocze2012.pdf |    Bin 0 -> 1814019 bytes
 ...idowanesprawozdaniefinansowezaipolrocze2010.pdf |    Bin 0 -> 699659 bytes
 ...idowanesprawozdaniefinansowezaipolrocze2011.pdf |    Bin 0 -> 1728281 bytes
 ...idowanesprawozdaniefinansowezarok2011rs2011.pdf |    Bin 0 -> 2843835 bytes
 ...konsolidowanesprawozdaniefinansowezarok2012.pdf |    Bin 0 -> 1915374 bytes
 ...konsolidowanesprawozdaniefinansowezarok2015.pdf |    Bin 0 -> 2138067 bytes
 .../pdfs/skonsolidowanewybranedanefinansowe.pdf    |    Bin 0 -> 116825 bytes
 .../skonsolidowanewybranedanefinansowe2014.pdf     |    Bin 0 -> 115944 bytes
 .../skonsolidowanewybranedanefinansowe2015.pdf     |    Bin 0 -> 116305 bytes
 .../skonsolidowanewybranedanefinansowers2011.pdf   |    Bin 0 -> 502557 bytes
 .../pdfs/skonsolidowanyraportkwartalny1q2012.pdf   |    Bin 0 -> 2076659 bytes
 .../pdfs/skonsolidowanyraportkwartalny1q2013.pdf   |    Bin 0 -> 1966864 bytes
 ...idowanyraportkwartalny3q2016rokuskorygowany.pdf |    Bin 0 -> 1641326 bytes
 .../pdfs/skonsolidowanyraportkwartalnyq12014.pdf   |    Bin 0 -> 1496268 bytes
 .../pdfs/skonsolidowanyraportkwartalnyq12015.pdf   |    Bin 0 -> 1448700 bytes
 .../pdfs/skonsolidowanyraportkwartalnyq12016.pdf   |    Bin 0 -> 1597319 bytes
 .../pdfs/skonsolidowanyraportkwartalnyq32014.pdf   |    Bin 0 -> 1555229 bytes
 ...lidowanyraportkwartalnyzaiiikwartal2012roku.pdf |    Bin 0 -> 2243171 bytes
 ...onsolidowanyraportokresowy3q2015skorygowany.pdf |    Bin 0 -> 1558564 bytes
 ...skonsolidowanyraportokresowyza1polrocze2014.pdf |    Bin 0 -> 1978296 bytes
 ...skonsolidowanyraportokresowyzaipolrocze2013.pdf |    Bin 0 -> 2115261 bytes
 ...skonsolidowanyraportokresowyzaipolrocze2015.pdf |    Bin 0 -> 2044432 bytes
 ...solidowanyraportokresowyzaipolrocze2016roku.pdf |    Bin 0 -> 2199310 bytes
 .../pdfs/skonsolidowanyraportq32013.pdf            |    Bin 0 -> 1786578 bytes
 .../pdfs/sprawozdaniezarzaduzdzialalnoscigk.pdf    |    Bin 0 -> 2118748 bytes
 .../sprawozdaniezarzaduzdzialalnoscigk2014.pdf     |    Bin 0 -> 1890461 bytes
 ...zdaniezarzaduzdzialalnoscigkzaipolrocze2012.pdf |    Bin 0 -> 1915831 bytes
 ...ozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf |    Bin 0 -> 4857015 bytes
 ...ezarzaduzdzialalnoscigrupykapitalowejrs2011.pdf |    Bin 0 -> 2896006 bytes
 ...dzialalnoscigrupykapitalowejzaipolrocze2010.pdf |    Bin 0 -> 561992 bytes
 ...dzialalnoscigrupykapitalowejzaipolrocze2011.pdf |    Bin 0 -> 1389531 bytes
 ...yazotowewtarnowie-moscicachsawipolroczu2008.pdf |    Bin 0 -> 27356246 bytes
 .../sprawozdaniezarzaduzdzialalnoscispolki.pdf     |    Bin 0 -> 1640353 bytes
 .../sprawozdaniezarzaduzdzialalnoscispolki2011.pdf |    Bin 0 -> 2322735 bytes
 .../sprawozdaniezarzaduzdzialalnoscispolki2014.pdf |    Bin 0 -> 1457565 bytes
 .../sprawozdaniezarzaduzdzialalnoscispolki2015.pdf |    Bin 0 -> 1630507 bytes
 .../pdfs/wybranedanefinansowe.pdf                  |    Bin 0 -> 232931 bytes
 .../pdfs/wybranedanefinansowe2008rr.pdf            |    Bin 0 -> 292760 bytes
 .../run_20251104_205052/summary.json               |      8 +
 .../FINAL_INVESTIGATION_REPORT.md                  |    852 +
 .../INVESTIGATION_PLAN.md                          |    237 +
 .../analysis/ADRIAN_LEGAL_ANALYSIS.md              |    693 +
 .../analysis/DAMIAN_CRITICAL_REVIEW.md             |    799 +
 .../analysis/ELENA_OSINT_REPORT.md                 |    430 +
 .../analysis/MARCUS_FINANCIAL_ANALYSIS.md          |    495 +
 .../analysis/MAYA_DATA_TIMELINE_ANALYSIS.md        |    663 +
 local_orchestrator.py                              |    663 +
 orchestration/elasticsearch_integration_concept.py |    333 +
 .../elasticsearch_integration_evaluation.py        |    532 +
 orchestration/eval_20251104_213005_report.json     |    376 +
 ...doc_20251104_132626_COMMIT_300ea7b_feature.json |      8 +
 ...42119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json |      8 +
 ..._20251104_142244_RESEARCH_DELIVERY_SUMMARY.json |      8 +
 .../doc_20251104_142308_COMMIT_7c01260_change.json |      8 +
 ..._143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json |      8 +
 ...3527_FACE_RECOGNITION_TECHNICAL_VALIDATION.json |      8 +
 ...doc_20251104_143611_COMMIT_594e664_feature.json |      8 +
 ...251104_144915_COMMIT_6a77410_documentation.json |      8 +
 ...251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json |      8 +
 ...45754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json |      8 +
 ...doc_20251104_145842_COMMIT_038e967_feature.json |      8 +
 ..._20251104_150727_SEJM_API_ANALYSIS_CONCEPT.json |      8 +
 ...0251104_151039_SEJM_ASW_ANALYSIS_2019_2023.json |      8 +
 ...doc_20251104_151117_COMMIT_388327f_feature.json |      8 +
 ...20251104_183128_INSTITUTIONAL_API_ANALYSIS.json |      8 +
 .../indexed/doc_20251104_183139_README.json        |      8 +
 .../indexed/doc_20251104_183144_README.json        |      8 +
 ...20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json |      8 +
 ...doc_20251104_184219_BELLINGCAT_LEVEL_OSINT.json |      8 +
 ...104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.json |      8 +
 ...oc_20251104_184917_AGENT_TOOLKITS_COMPLETE.json |      8 +
 ...5328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json |      8 +
 ...c_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.json |      8 +
 ...59_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json |      8 +
 ...0251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.json |      8 +
 ...104_190531_SOURCE_CITATION_QUICK_REFERENCE.json |      8 +
 ..._MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json |      8 +
 .../doc_20251104_190812_INVESTIGATION_PLAN.json    |      8 +
 .../doc_20251104_190943_ELENA_OSINT_REPORT.json    |      8 +
 ...155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json |      8 +
 ..._20251104_191613_MARCUS_FINANCIAL_ANALYSIS.json |      8 +
 .../doc_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json |      8 +
 ...0251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json |      8 +
 ...doc_20251104_192245_DAMIAN_CRITICAL_REVIEW.json |      8 +
 ...20251104_192454_FINAL_INVESTIGATION_REPORT.json |      8 +
 ...4_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json |      8 +
 ..._20251104_193555_HYBRID_SYSTEM_QUICK_START.json |      8 +
 .../indexed/doc_20251104_193622_README.json        |      8 +
 ...251104_194002_DATA_SEPARATION_ARCHITECTURE.json |      8 +
 ...104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json |      8 +
 ..._194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json |      8 +
 ...251104_195310_INTERNET_RESEARCH_CAPABILITY.json |      8 +
 ...251104_195345_INTERNET_RESEARCH_CAPABILITY.json |      8 +
 ...c_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json |      8 +
 .../doc_20251104_195847_INVESTIGATION_STATUS.json  |      8 +
 .../doc_20251104_203406_FINAL_OSINT_REPORT.json    |      8 +
 .../doc_20251104_203700_FINAL_OSINT_REPORT.json    |      8 +
 .../doc_20251104_204516_FINAL_OSINT_REPORT.json    |      8 +
 .../doc_20251104_211443_SEARCH_ORCHESTRATOR.json   |      8 +
 ...20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json |      8 +
 ...oc_20251104_220219_POSTGRES_STUCK_ANALYSIS.json |      8 +
 .../doc_20251104_220923_BATCH_MIGRATION_PLAN.json  |      8 +
 queue_for_batch.sh                                 |      9 +
 ...edis_20251104_132626_COMMIT_300ea7b_feature.txt |     42 +
 ...142120_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.txt |     33 +
 ...s_20251104_142244_RESEARCH_DELIVERY_SUMMARY.txt |     45 +
 ...redis_20251104_142308_COMMIT_7c01260_change.txt |     43 +
 ...4_143218_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.txt |     39 +
 ...43527_FACE_RECOGNITION_TECHNICAL_VALIDATION.txt |     33 +
 ...edis_20251104_143611_COMMIT_594e664_feature.txt |     46 +
 ...0251104_144915_COMMIT_6a77410_documentation.txt |     56 +
 ...0251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.txt |     38 +
 ...145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.txt |     45 +
 ...edis_20251104_145842_COMMIT_038e967_feature.txt |     47 +
 ...s_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.txt |     47 +
 ...20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.txt |     41 +
 ...edis_20251104_151117_COMMIT_388327f_feature.txt |     43 +
 ..._20251104_183128_INSTITUTIONAL_API_ANALYSIS.txt |     43 +
 redis_pending/redis_20251104_183139_README.txt     |     49 +
 redis_pending/redis_20251104_183144_README.txt     |     49 +
 ..._20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.txt |     32 +
 ...edis_20251104_184219_BELLINGCAT_LEVEL_OSINT.txt |     30 +
 ...1104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.txt |     36 +
 ...dis_20251104_184917_AGENT_TOOLKITS_COMPLETE.txt |     39 +
 ...85328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.txt |     39 +
 ...is_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.txt |     53 +
 ...959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.txt |     39 +
 ...20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.txt |     53 +
 ...1104_190531_SOURCE_CITATION_QUICK_REFERENCE.txt |     66 +
 ...8_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.txt |     54 +
 .../redis_20251104_190812_INVESTIGATION_PLAN.txt   |     35 +
 .../redis_20251104_190944_ELENA_OSINT_REPORT.txt   |     38 +
 ...1155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.txt |     44 +
 ...s_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.txt |     41 +
 ...redis_20251104_191829_ADRIAN_LEGAL_ANALYSIS.txt |     35 +
 ...20251104_192040_MAYA_DATA_TIMELINE_ANALYSIS.txt |     41 +
 ...edis_20251104_192245_DAMIAN_CRITICAL_REVIEW.txt |     41 +
 ..._20251104_192454_FINAL_INVESTIGATION_REPORT.txt |     31 +
 ...04_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.txt |     37 +
 ...s_20251104_193555_HYBRID_SYSTEM_QUICK_START.txt |     38 +
 redis_pending/redis_20251104_193622_README.txt     |     49 +
 ...0251104_194002_DATA_SEPARATION_ARCHITECTURE.txt |     39 +
 ...1104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.txt |     41 +
 ...4_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.txt |     41 +
 ...0251104_195310_INTERNET_RESEARCH_CAPABILITY.txt |     49 +
 ...0251104_195345_INTERNET_RESEARCH_CAPABILITY.txt |     49 +
 ...is_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.txt |     48 +
 .../redis_20251104_195847_INVESTIGATION_STATUS.txt |     43 +
 .../redis_20251104_203406_FINAL_OSINT_REPORT.txt   |     20 +
 .../redis_20251104_203700_FINAL_OSINT_REPORT.txt   |     20 +
 .../redis_20251104_204516_FINAL_OSINT_REPORT.txt   |     20 +
 .../redis_20251104_211443_SEARCH_ORCHESTRATOR.txt  |     29 +
 ..._20251104_212055_DATA_ARCHITECTURE_ANALYSIS.txt |     37 +
 ...dis_20251104_220219_POSTGRES_STUCK_ANALYSIS.txt |     31 +
 .../redis_20251104_220924_BATCH_MIGRATION_PLAN.txt |     31 +
 requirements.txt                                   |      1 +
 scripts/extract_pdf_text_to_es.py                  |    168 +
 scripts/hybrid_osint_processor_test.py             |    588 +
 scripts/ingest_investigation_osint.py              |    108 +
 scripts/scrape_grupaazoty_pdfs.py                  |    186 +
 scripts/sync_documents_to_neo4j.py                 |    139 +
 scripts/sync_es_references_to_pg.py                |    252 +
 search_orchestrator.py                             |    704 +
 setup_hourly_batch.sh                              |    152 +
 shared_workspace/tasks/task_cpk_research_demo.json |    127 +
 sql/es_document_references_schema.sql              |    162 +
 ...j_20251104_132626_COMMIT_300ea7b_feature.cypher |     10 +
 ...119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.cypher |     10 +
 ...0251104_142244_RESEARCH_DELIVERY_SUMMARY.cypher |     10 +
 ...4j_20251104_142308_COMMIT_7c01260_change.cypher |     10 +
 ...43217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.cypher |     10 +
 ...27_FACE_RECOGNITION_TECHNICAL_VALIDATION.cypher |     10 +
 ...j_20251104_143611_COMMIT_594e664_feature.cypher |     10 +
 ...1104_144915_COMMIT_6a77410_documentation.cypher |     10 +
 ...1104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.cypher |     10 +
 ...754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.cypher |     10 +
 ...j_20251104_145842_COMMIT_038e967_feature.cypher |     10 +
 ...0251104_150727_SEJM_API_ANALYSIS_CONCEPT.cypher |     10 +
 ...51104_151039_SEJM_ASW_ANALYSIS_2019_2023.cypher |     10 +
 ...j_20251104_151117_COMMIT_388327f_feature.cypher |     10 +
 ...251104_183128_INSTITUTIONAL_API_ANALYSIS.cypher |     10 +
 .../neo4j_20251104_183139_README.cypher            |     10 +
 .../neo4j_20251104_183144_README.cypher            |     10 +
 ...251104_183843_COMPREHENSIVE_OSINT_SYSTEM.cypher |     10 +
 ...j_20251104_184219_BELLINGCAT_LEVEL_OSINT.cypher |     10 +
 ...4_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.cypher |     10 +
 ..._20251104_184917_AGENT_TOOLKITS_COMPLETE.cypher |     10 +
 ...28_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.cypher |     10 +
 ...20251104_185811_ADAPTIVE_LEARNING_SYSTEM.cypher |     10 +
 ..._SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.cypher |     10 +
 ...51104_190459_SOURCE_ATTRIBUTION_PROTOCOL.cypher |     10 +
 ...4_190531_SOURCE_CITATION_QUICK_REFERENCE.cypher |     10 +
 ...ANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.cypher |     10 +
 ...neo4j_20251104_190812_INVESTIGATION_PLAN.cypher |     10 +
 ...neo4j_20251104_190943_ELENA_OSINT_REPORT.cypher |     10 +
 ...5_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.cypher |     10 +
 ...0251104_191613_MARCUS_FINANCIAL_ANALYSIS.cypher |     10 +
 ...4j_20251104_191829_ADRIAN_LEGAL_ANALYSIS.cypher |     10 +
 ...51104_192039_MAYA_DATA_TIMELINE_ANALYSIS.cypher |     10 +
 ...j_20251104_192245_DAMIAN_CRITICAL_REVIEW.cypher |     10 +
 ...251104_192454_FINAL_INVESTIGATION_REPORT.cypher |     10 +
 ...193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.cypher |     10 +
 ...0251104_193555_HYBRID_SYSTEM_QUICK_START.cypher |     10 +
 .../neo4j_20251104_193622_README.cypher            |     10 +
 ...1104_194002_DATA_SEPARATION_ARCHITECTURE.cypher |     10 +
 ...4_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.cypher |     10 +
 ...94521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.cypher |     10 +
 ...1104_195310_INTERNET_RESEARCH_CAPABILITY.cypher |     10 +
 ...1104_195345_INTERNET_RESEARCH_CAPABILITY.cypher |     10 +
 ...20251104_195433_DUCKDUCKGO_SEARCH_METHOD.cypher |     10 +
 ...o4j_20251104_195847_INVESTIGATION_STATUS.cypher |     10 +
 ...neo4j_20251104_203406_FINAL_OSINT_REPORT.cypher |     10 +
 ...neo4j_20251104_203700_FINAL_OSINT_REPORT.cypher |     10 +
 ...neo4j_20251104_204516_FINAL_OSINT_REPORT.cypher |     10 +
 ...eo4j_20251104_211443_SEARCH_ORCHESTRATOR.cypher |     10 +
 ...251104_212055_DATA_ARCHITECTURE_ANALYSIS.cypher |     10 +
 ..._20251104_220219_POSTGRES_STUCK_ANALYSIS.cypher |     10 +
 ...o4j_20251104_220923_BATCH_MIGRATION_PLAN.cypher |     10 +
 .../pg_20251104_132626_COMMIT_300ea7b_feature.sql  |     26 +
 ...142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.sql |     21 +
 ...g_20251104_142244_RESEARCH_DELIVERY_SUMMARY.sql |     24 +
 .../pg_20251104_142308_COMMIT_7c01260_change.sql   |     26 +
 ...4_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.sql |     21 +
 ...43527_FACE_RECOGNITION_TECHNICAL_VALIDATION.sql |     20 +
 .../pg_20251104_143611_COMMIT_594e664_feature.sql  |     26 +
 ...0251104_144915_COMMIT_6a77410_documentation.sql |     26 +
 ...0251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.sql |     24 +
 ...145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.sql |     20 +
 .../pg_20251104_145842_COMMIT_038e967_feature.sql  |     28 +
 ...g_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.sql |     20 +
 ...20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.sql |     20 +
 .../pg_20251104_151117_COMMIT_388327f_feature.sql  |     26 +
 ..._20251104_183128_INSTITUTIONAL_API_ANALYSIS.sql |     25 +
 sql/realtime_updates/pg_20251104_183139_README.sql |     19 +
 sql/realtime_updates/pg_20251104_183144_README.sql |     19 +
 ..._20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.sql |     20 +
 .../pg_20251104_184219_BELLINGCAT_LEVEL_OSINT.sql  |     18 +
 ...1104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.sql |     19 +
 .../pg_20251104_184917_AGENT_TOOLKITS_COMPLETE.sql |     20 +
 ...85328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.sql |     19 +
 ...pg_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.sql |     27 +
 ...959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.sql |     24 +
 ...20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.sql |     19 +
 ...1104_190531_SOURCE_CITATION_QUICK_REFERENCE.sql |     31 +
 ...8_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.sql |     20 +
 .../pg_20251104_190812_INVESTIGATION_PLAN.sql      |     20 +
 .../pg_20251104_190943_ELENA_OSINT_REPORT.sql      |     20 +
 ...1155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.sql |     20 +
 ...g_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.sql |     20 +
 .../pg_20251104_191829_ADRIAN_LEGAL_ANALYSIS.sql   |     20 +
 ...20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.sql |     20 +
 .../pg_20251104_192245_DAMIAN_CRITICAL_REVIEW.sql  |     19 +
 ..._20251104_192454_FINAL_INVESTIGATION_REPORT.sql |     19 +
 ...04_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.sql |     20 +
 ...g_20251104_193555_HYBRID_SYSTEM_QUICK_START.sql |     23 +
 sql/realtime_updates/pg_20251104_193622_README.sql |     19 +
 ...0251104_194002_DATA_SEPARATION_ARCHITECTURE.sql |     19 +
 ...1104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.sql |     20 +
 ...4_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.sql |     20 +
 ...0251104_195310_INTERNET_RESEARCH_CAPABILITY.sql |     20 +
 ...0251104_195345_INTERNET_RESEARCH_CAPABILITY.sql |     20 +
 ...pg_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.sql |     24 +
 .../pg_20251104_195847_INVESTIGATION_STATUS.sql    |     20 +
 .../pg_20251104_203406_FINAL_OSINT_REPORT.sql      |     17 +
 .../pg_20251104_203700_FINAL_OSINT_REPORT.sql      |     17 +
 .../pg_20251104_204516_FINAL_OSINT_REPORT.sql      |     17 +
 .../pg_20251104_211443_SEARCH_ORCHESTRATOR.sql     |     20 +
 ..._20251104_212055_DATA_ARCHITECTURE_ANALYSIS.sql |     21 +
 .../pg_20251104_220219_POSTGRES_STUCK_ANALYSIS.sql |     18 +
 .../pg_20251104_220923_BATCH_MIGRATION_PLAN.sql    |     21 +
 supervisor_interface.py                            |    643 +
 technical_emergency_response.py                    |    257 +
 test_hybrid_system.py                              |    326 +
 tests/test_search_orchestrator_real_data.py        |    654 +
 tests/test_smart_references_integration.py         |    267 +
 698 files changed, 1014510 insertions(+), 252 deletions(-)
```

## 🤖 Metadata

```json
{
  "commit_hash": "9b4c75686879959be54c74a7fa3069f3c556e4e1",
  "commit_type": "feature",
  "timestamp": 1762290876,
  "files_changed": [
    ".change_tracking_state.json",
    "BATCH_MIGRATION_PLAN.md",
    "POSTGRES_STUCK_ANALYSIS.md",
    "README.md",
    "SOURCE_CITATION_QUICK_REFERENCE.md",
    "TECHNICAL_TEAM_RESPONSE.json",
    "agents/analytical/damian_agent.py",
    "agents/analytical/tools/__init__.py",
    "agents/analytical/tools/mathematical_toolkit.py",
    "agents/analytical/tools/scraping_toolkit.py",
    "aleksander_emergency_response.py",
    "batch_processing_system.py",
    "bus/urgent_technical_review.json",
    "capabilities_registry.py",
    "check_batch_status.sh",
    "com.destiny.hourly-batch.plist",
    "docs/DATA_ARCHITECTURE_ANALYSIS.md",
    "docs/SEARCH_ORCHESTRATOR.md",
    "docs/architecture/DATA_SEPARATION_ARCHITECTURE.md",
    "docs/architecture/HYBRID_ONPREM_INTELLIGENCE_SYSTEM.md",
    "docs/auto-generated/2025-11-04/COMMIT_038e967_feature.md",
    "docs/auto-generated/2025-11-04/COMMIT_300ea7b_feature.md",
    "docs/auto-generated/2025-11-04/COMMIT_388327f_feature.md",
    "docs/auto-generated/2025-11-04/COMMIT_594e664_feature.md",
    "docs/auto-generated/2025-11-04/COMMIT_6a77410_documentation.md",
    "docs/auto-generated/2025-11-04/COMMIT_7c01260_change.md",
    "docs/capabilities/DUCKDUCKGO_SEARCH_METHOD.md",
    "docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md",
    "docs/capabilities/INTERNET_RESEARCH_CAPABILITY.md",
    "docs/concepts/BELLINGCAT_LEVEL_OSINT.md",
    "docs/concepts/COMPREHENSIVE_OSINT_SYSTEM.md",
    "docs/concepts/DESTINY_CHAT_UI_HYBRID_INTEGRATION.md",
    "docs/guides/HYBRID_SYSTEM_COMPLETE_OVERVIEW.md",
    "docs/guides/HYBRID_SYSTEM_QUICK_START.md",
    "docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md",
    "docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md",
    "docs/status/MORNING_BRIEF_20251104.md",
    "docs/status/SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.md",
    "docs/team/ADAPTIVE_LEARNING_SYSTEM.md",
    "docs/team/MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.md",
    "docs/team/SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.md",
    "docs/team/SYSTEM_CAPABILITIES_UPDATE_2025_11_04.md",
    "docs/technical/AGENT_TOOLKITS_COMPLETE.md",
    "emergency_fix.sh",
    "examples/search_orchestrator_usage.py",
    "helena_batch_processor.py",
    "helena_core.py",
    "helena_tasks/helena_task_20251104_140000_database_schema.md",
    "helena_tasks/helena_task_20251104_140000_documentation.md",
    "helena_tasks/helena_task_20251104_140000_general_change.md",
    "helena_tasks/helena_task_20251104_140000_knowledge_graph.md",
    "helena_tasks/helena_task_20251104_150000_agent_code.md",
    "helena_tasks/helena_task_20251104_150000_documentation.md",
    "helena_tasks/helena_task_20251104_150000_general_change.md",
    "helena_tasks/helena_task_20251104_190000_agent_code.md",
    "helena_tasks/helena_task_20251104_190000_documentation.md",
    "helena_tasks/helena_task_20251104_190000_general_change.md",
    "helena_tasks/helena_task_20251104_200000_documentation.md",
    "helena_tasks/helena_task_20251104_210000_documentation.md",
    "helena_tasks/helena_task_20251104_210000_general_change.md",
    "helena_tasks/processed/success_realtime_20251104_132625_COMMIT_300ea7b_feature.json",
    "helena_tasks/processed/success_realtime_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_142244_RESEARCH_DELIVERY_SUMMARY.json",
    "helena_tasks/processed/success_realtime_20251104_142308_COMMIT_7c01260_change.json",
    "helena_tasks/processed/success_realtime_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json",
    "helena_tasks/processed/success_realtime_20251104_143526_FACE_RECOGNITION_TECHNICAL_VALIDATION.json",
    "helena_tasks/processed/success_realtime_20251104_143610_COMMIT_594e664_feature.json",
    "helena_tasks/processed/success_realtime_20251104_144914_COMMIT_6a77410_documentation.json",
    "helena_tasks/processed/success_realtime_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json",
    "helena_tasks/processed/success_realtime_20251104_145753_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json",
    "helena_tasks/processed/success_realtime_20251104_145842_COMMIT_038e967_feature.json",
    "helena_tasks/processed/success_realtime_20251104_150726_SEJM_API_ANALYSIS_CONCEPT.json",
    "helena_tasks/processed/success_realtime_20251104_151038_SEJM_ASW_ANALYSIS_2019_2023.json",
    "helena_tasks/processed/success_realtime_20251104_151116_COMMIT_388327f_feature.json",
    "helena_tasks/processed/success_realtime_20251104_183127_INSTITUTIONAL_API_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_183139_README.json",
    "helena_tasks/processed/success_realtime_20251104_183144_README.json",
    "helena_tasks/processed/success_realtime_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json",
    "helena_tasks/processed/success_realtime_20251104_184219_BELLINGCAT_LEVEL_OSINT.json",
    "helena_tasks/processed/success_realtime_20251104_184617_BELLINGCAT_METHODOLOGY_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_184916_AGENT_TOOLKITS_COMPLETE.json",
    "helena_tasks/processed/success_realtime_20251104_185327_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json",
    "helena_tasks/processed/success_realtime_20251104_185810_ADAPTIVE_LEARNING_SYSTEM.json",
    "helena_tasks/processed/success_realtime_20251104_185958_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json",
    "helena_tasks/processed/success_realtime_20251104_190458_SOURCE_ATTRIBUTION_PROTOCOL.json",
    "helena_tasks/processed/success_realtime_20251104_190530_SOURCE_CITATION_QUICK_REFERENCE.json",
    "helena_tasks/processed/success_realtime_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json",
    "helena_tasks/processed/success_realtime_20251104_190812_INVESTIGATION_PLAN.json",
    "helena_tasks/processed/success_realtime_20251104_190943_ELENA_OSINT_REPORT.json",
    "helena_tasks/processed/success_realtime_20251104_191154_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json",
    "helena_tasks/processed/success_realtime_20251104_191612_MARCUS_FINANCIAL_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_192245_DAMIAN_CRITICAL_REVIEW.json",
    "helena_tasks/processed/success_realtime_20251104_192454_FINAL_INVESTIGATION_REPORT.json",
    "helena_tasks/processed/success_realtime_20251104_193139_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json",
    "helena_tasks/processed/success_realtime_20251104_193555_HYBRID_SYSTEM_QUICK_START.json",
    "helena_tasks/processed/success_realtime_20251104_193622_README.json",
    "helena_tasks/processed/success_realtime_20251104_194001_DATA_SEPARATION_ARCHITECTURE.json",
    "helena_tasks/processed/success_realtime_20251104_194329_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json",
    "helena_tasks/processed/success_realtime_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json",
    "helena_tasks/processed/success_realtime_20251104_195309_INTERNET_RESEARCH_CAPABILITY.json",
    "helena_tasks/processed/success_realtime_20251104_195344_INTERNET_RESEARCH_CAPABILITY.json",
    "helena_tasks/processed/success_realtime_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json",
    "helena_tasks/processed/success_realtime_20251104_195846_INVESTIGATION_STATUS.json",
    "helena_tasks/processed/success_realtime_20251104_203406_FINAL_OSINT_REPORT.json",
    "helena_tasks/processed/success_realtime_20251104_203700_FINAL_OSINT_REPORT.json",
    "helena_tasks/processed/success_realtime_20251104_204516_FINAL_OSINT_REPORT.json",
    "helena_tasks/processed/success_realtime_20251104_211442_SEARCH_ORCHESTRATOR.json",
    "helena_tasks/processed/success_realtime_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_220219_POSTGRES_STUCK_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251104_220923_BATCH_MIGRATION_PLAN.json",
    "hourly_batch_processor.py",
    "investigations/active/telus_cpk_real_001/FINAL_OSINT_REPORT.md",
    "investigations/active/telus_cpk_real_001/INVESTIGATION_STATUS.md",
    "investigations/active/telus_cpk_real_001/sources/web/businessinsider_telus.html",
    "investigations/active/telus_cpk_real_001/sources/web/cpk_official.html",
    "investigations/active/telus_cpk_real_001/sources/web/cpk_wikipedia.html",
    "investigations/active/telus_cpk_real_001/sources/web/onet_telus_cpk.html",
    "investigations/active/telus_cpk_real_001/sources/web/tvn24_telus_cpk.html",
    "investigations/active/telus_cpk_real_001/sources/web/wikipedia_telus.html",
    "investigations/concepts/elasticsearch_integration_20251104_210917.json",
    "investigations/concepts/search_orchestrator_test_report.json",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/elasticsearch_bulk.ndjson",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/elasticsearch_text_updates.ndjson",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119530rdroczneskonsolidowanesprawozdaniefinansowezaiiikwarta2010.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119707azotytarnowqsriiikwarta2009.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119739rdroczneskonsolidowanesprawozdaniefinansowezaiiikwarta2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329119889azotytarnowqsrikwarta2009.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120049skonsolidowanesprawozdaniezaikwarta2011opublikowany.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120309skonsolidowanesprawozdaniezaikwarta2010.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329120313raportivq2009bezpodpisow.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329483078azotytarnowqsriiikwartal2008.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329483098azotytarnowqsrivkwarta2008.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1329485603sprawozdaniefinansoweiikwartal2008.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1Ocena_20Rady_20Nadzorczej_202019.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/1__C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20skonsolidowane_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202021_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2019.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/2__C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20jednostkowe_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202021_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/3_Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20p_C3_B3_C5_82rocze_202021_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/4_O_C5_9Bwiadczenie_20Zarz_C4_85du_20Grupy_20Azoty_20S.A._20o_20zgodno_C5_9Bci_20i_20prawdziwo_C5_9Bci_20_C5_9Br_C3_B3drocznego_20sprawozdania_20finansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/C59ArC3B3droczne20skrC3B3cone20jednostkowe20sprawozdanie20finansowe20za20okres20620miesiC499cy20zakoC584czony203020czerwca20201920roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/C59ArC3B3droczne20skrC3B3cone20skonsolidowane20sprawozdanie20finansowe20za20okres20620miesiC499cy20zakoC584czony203020czerwca20201920roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_OswiadczenieZarzadu-2021-12-31-pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_SprawozdanieFinansowe-2021-12-31-pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/GrupaAzoty_SprawozdanieZarzadu-2021-12-31-pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_List_Prezesa_Zarzadu_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Oswiadczenie_Zarzadu_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_I_polrocze_2025.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_20_I_kwarta_C5_82_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_III_kwartal_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2024_roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowany_Raport_za_I_kwartal_2025.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Finansowe_I_polrocze_2025.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2023_.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_Zarzadu_I_polrocze_2025.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Sprawozdanie_z_platnosci_adm_publ_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20Sprawozdanie20Finansowe201H2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20Sprawozdanie20Finansowe201H2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe20SpC3B3C582ki20Grupa20Azoty20za20rok202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20sprawozdanie20finansowe20za20rok202016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Jednostkowe20wybrane20dane20finansowe202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List20Prezesa20ZarzC485du.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/ListPrez_GrupaAzoty-2024-12-31-0-pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List_20Prezesa_20Zarz_C4_85du.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/List_Prezesa_Zarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20Rady20Nadzorczej20-20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20Rady20Nadzorczej20-20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20-20podmiot20uprawniony20do20badania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20-20sprawozdania20finansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20Grupy20Azoty20S.A.20o20zgodnoC59Bci20i20prawdziwoC59Bci20C59BrC3B3drocznego20sprawozdania20finansowego30.06.2019.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20Grupy20Azoty20do20sprawozdaC58420za20201820rok.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20podmiocie20uprawnionym20-20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20podmiocie20uprawnionym20-20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20sprawozdaniu20jednostkowym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/OC59Bwiadczenie20ZarzC485du20o20sprawozdaniu20skonsolidowanym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20Grupy_20Azoty_20S.A._20o_20zgodno_C5_9Bci_20i_20prawdziwo_C5_9Bci_20_C5_9Br_C3_B3drocznego_20sprawozdania_20finansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20o_20podmiocie_20uprawnionym_20-_20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/O_C5_9Bwiadczenie_20Zarz_C4_85du_20o_20sprawozdaniu_20skonsolidowanym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena20Rady20Nadzorczej.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_20Rady_20Nadzorczej_20-_20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_skonsolidowane_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_Zarzadu_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_Zarzadu_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_finansowe_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_skonsolidowane_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Ocena_Rady_Nadzorczej_sprawozdanie_skonsolidowane_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Opinia20i20raport20biegC582ego20rewidenta20-20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Opinia20i20raport20biegC582ego20rewidenta20-20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady-Nadzorczej_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_skonsolidowane_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Rady_Nadzorczej_skonsolidowane_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Oswiadczenie_Zarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport20biegC582ego20rewidenta20-20sprawozdanie20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport20biegC582ego20rewidenta20-20sprawozdanie20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20z_20przegl_C4_85du_20JSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_20z_20przegl_C4_85du_20SSF_20Grupa_20Azoty_20S.A._30062021-sig.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Bieglego_Rewidenta-sig-sig.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Bieglego_Rewidenta_skonsolidowane-sig-sig.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GASA_JSF.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GASA_SSF.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GAT_JSF_H1_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_Przeglad_GK_GAT_SSF_H1_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport__przegl_C4_85du_GAT_.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Raport_z_przegladu_GK_GAT.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20Sprawozdanie20Finansowe201H2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20Grupy20KapitaC582owej20Grupa20Azoty20z20pC582atnoC59Bci20na20rzecz20administracji20publicznej20za20201820rok.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe201H2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe20Grupy20KapitaC582owej20Grupa20Azoty20za20rok202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20sprawozdanie20finansowe20za20rok202016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20wybrane20dane20finansowe202016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane20wybrane20dane20finansowe202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_20sprawozdanie_20finansowe_202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_20wybrane_20dane_20finansowe_202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowane_wybrane_dane_finansowe_2021.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20kwartalny203Q2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20Grupy20KapitaC582owej20Grupa20Azoty20za20I20kwartaC58220201920roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20120kwartaC582202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20320kwartaC582202018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany20raport20okresowy20za20I20kwartaC582202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20GKGA_20za_20III_20kwarta_C5_82_202021.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20III_20kwarta_C5_82_202019_20roku_1_.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_20raport_20okresowy_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20kwarta_C5_82_202020_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Skonsolidowany_raport_okresowy_Grupy_Kapitalowej_Grupa_Azoty_za_III_kwartal_2020_.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Spraw_zrown_rozw_2024.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie-SPS-2016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie-z-platnosci-na-rzecz-administracji-publicznej-2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du201H2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci202016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20GK202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20Grupy20Azoty20S.A.20oraz20Grupy20KapitaC582owej20Grupa20Azoty20za20okres201220miesiC499cy20zakoC584czony203120grudnia20201820roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20ZarzC485du20z20dziaC582alnoC59Bci20Grupy20KapitaC582owej20Grupa20Azoty20za20I20pC3B3C582rocze20201920roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20Zarzadu201H2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20biegC582ego20rewidenta20-20sprawozdanie20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20na20temat20informacji20niefinansowych20Grupy20KapitaC582owej20Grupa20Azoty20za20okres201220miesiC499cy20zakoC584czony203120grudnia20201820roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20z20badania20-20jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie20z20badania20-20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20GK_202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20Zarz_C4_85du_20z_20dzia_C5_82alno_C5_9Bci_20Grupy_20Kapita_C5_82owej_20Grupa_20Azoty_20za_20I_20p_C3_B3_C5_82rocze_202020_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20bieg_C5_82ego_20rewidenta_20-_20sprawozdanie_20skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_20nt_20informacji_20niefinansowych_202017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_2023.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_za_2021_rok.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Sprawozdanie_na_temat_informacji_niefinansowych_Grupy_Azoty_za_2021_rok_pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzB_GAT_2022.xhtml.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzB_GK_GAT_2022.xhtml.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/SzD_GrupaAzoty-2024-12-31-0-pl.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201H2019.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe201Q202019.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe203Q2017.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane20dane20finansowe203Q2018.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_201H_202020.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_201Q_202020.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_20III_20kwarta_C5_82_202021.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_20dane_20finansowe_20I_20p_C3_B3_C5_82rocze_202021.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_1Q_2022.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_2021.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Wybrane_dane_finansowe_3Q2020.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/_C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20jednostkowe_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_20zako_C5_84czony_2030_20czerwca_202020_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/_C5_9Ar_C3_B3droczne_20skr_C3_B3cone_20skonsolidowane_20sprawozdanie_20finansowe_20za_20okres_206_20miesi_C4_99cy_202020_20roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowe2013.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowe2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowesprawozdaniefinansowezarok2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowe2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/jednostkowewybranedanefinansowezarok2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/listprezesa-1h2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/listprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdaniejednostkowe2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniabieglegorewidenta-sprawozdanieskonsolidowaners2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegoreiwdenta-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozd.jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozd.skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/opiniairaportbieglegorewidenta-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniaosprawozdaniuskonsolidowanymiopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniazarzadu1h2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdaniejednostkowe2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieopodmiocieuprawnionymdobadania-sprawozdanieskonsolidowaners2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieoskonsolidowanymsprawozdaniurs2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowym2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowymiopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniujednostkowymipodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniuskonsolidowanym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczenieosprawozdaniuskonsolidowanymipodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu-podmiotuprawnionydobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu-sprawozdaniafinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduopodmiocieuprawnionym-jednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduopodmiocieuprawnionym-skonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduosprawozdaniuskonsolidowanym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduwsprawiepodmiotuuprawnionegodobadaniasprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/oswiadczeniezarzaduwsprawierzetelnoscisporzadzeniesprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/pismoprezesazarzadu2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/pismoprezesazarzadurs2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/polroczneskonsolidowanesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/polroczneskroconejednostkowesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007opiniairaportbieglegorewidenta.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007oswiadczenieopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007oswiadczenieosprawozdaniurocznym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007sprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2007sprawozdaniezdzialalnoscispolki.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008opiniapodmiotuuprawnionegodobadaniajednostkowegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008opiniapodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieojednostkowymsprawozdaniurocznym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieopodmiocieuprawnionymdobadaniajednostkowegosprawozdaniafinsnowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieopodmiocieuprawnionymdobadaniaskonsolidowanegosprawozdaniafinsnowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008oswiadczenieoskonsolidowanymsprawozdaniurocznym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008pismoprezesazarzadusprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008pismoprezesazarzadusprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008raportpodmiotuuprawnionegodobadaniajednostkowegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008raportpodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008rocznejednostkowesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008roczneskonsolidowanesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008sprawozdaniejednostkowezdzialalnoscispolki.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2008sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009opiniabieglegorewidenta.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009oswiadczenieopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009oswiadczenieosprawozdaniujednostkowym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009raportpodmiotuuprawnionegodobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009rocznejednostkowesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009sprawozdaniejednostkowezdzialalnoscispolki.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2009wybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010jednostkowesprawozdaniefinansowezarok2010.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010opiniabieglegorewidenta.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010oswiadczenieopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010oswiadczenieosprawozdaniujednostkowym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010raportpodmiotuuprawnionegodobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010sprawozdaniezarzaduzdzialalnoscispolki.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/r2010wybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportadytora-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdaniejednostkowe1.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportaudytora-sprawozdanieskonsolidowane1.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegorewidenta-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegorewidenta-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegosprjednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportbieglegosprskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportniezaleznegobieglegorewidenta3q2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportpodmiotuuprawnionegodobadania-sprawozdaniejednostkowe2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportpodmiotuuprawnionegodobadania-sprawozdanieskonsolidowaners2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportuzupelniajacybieglegorewidenta-sprawozdaniejednostkowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/raportuzupelniajacybieglegorewidenta-sprawozdanieskonsolidowane.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007opiniapodmiotuuprawnionegodobadaniasprawozdanfinansowychobadanymrocznymskonsolidowanymsprawozdaniufinansowym.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007oswiadczeniezarzaduwsprawiepodmiotuuprawnionegodobadaniaskonsolidowanegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007oswiadczeniezarzaduwsprawierzetelnoscisporzadzeniaskonsolidowanegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007raportpodmiotuuprawnionegodobadaniasprawozdanfinansowychzbadaniarocznegoskonsolidowanegosprawozdaniafinansowego.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007roczneskonsolidowanesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2007sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009opiniabieglegorewidenta.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009oswiadczenieopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009oswiadczenieoskonsolidowanymsprawozdaniu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009raportpodmiotuuprawnionegodobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009roczneskonsolidowanesprawozdaniefinansowezarok2009.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzarok2009.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2009wybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010opiniabieglegorewidenta.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010oswiadczenieopodmiocieuprawnionymdobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010oswiadczenieoskonsolidowanymsprawozdaniu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010pismoprezesazarzadu.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010raportpodmiotuuprawnionegodobadania.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010skonsolidowanesprawozdaniefinansowegkazotytarnow.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010sprawozdaniezarzaduzdzialalnoscigkazotytarnow.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/rs2010wybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe2013.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowe2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansoweipolrocze2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezaipolrocze2010.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezaipolrocze2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2011rs2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanesprawozdaniefinansowezarok2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowe2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanewybranedanefinansowers2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny1q2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny1q2013.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalny3q2016rokuskorygowany.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq12016.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyq32014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportkwartalnyzaiiikwartal2012roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowy3q2015skorygowany.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyza1polrocze2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2013.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportokresowyzaipolrocze2016roku.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/skonsolidowanyraportq32013.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigk.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigk2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigkzaipolrocze2012.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowej.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejrs2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzaipolrocze2010.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzaipolrocze2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscigrupykapitalowejzakladyazotowewtarnowie-moscicachsawipolroczu2008.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2011.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2014.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/sprawozdaniezarzaduzdzialalnoscispolki2015.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/wybranedanefinansowe.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/wybranedanefinansowe2008rr.pdf",
    "investigations/external/grupa_azoty_reports/run_20251104_205052/summary.json",
    "investigations/telus_cpk_land_investigation/FINAL_INVESTIGATION_REPORT.md",
    "investigations/telus_cpk_land_investigation/INVESTIGATION_PLAN.md",
    "investigations/telus_cpk_land_investigation/analysis/ADRIAN_LEGAL_ANALYSIS.md",
    "investigations/telus_cpk_land_investigation/analysis/DAMIAN_CRITICAL_REVIEW.md",
    "investigations/telus_cpk_land_investigation/analysis/ELENA_OSINT_REPORT.md",
    "investigations/telus_cpk_land_investigation/analysis/MARCUS_FINANCIAL_ANALYSIS.md",
    "investigations/telus_cpk_land_investigation/analysis/MAYA_DATA_TIMELINE_ANALYSIS.md",
    "local_orchestrator.py",
    "orchestration/elasticsearch_integration_concept.py",
    "orchestration/elasticsearch_integration_evaluation.py",
    "orchestration/eval_20251104_213005_report.json",
    "qdrant_pending/indexed/doc_20251104_132626_COMMIT_300ea7b_feature.json",
    "qdrant_pending/indexed/doc_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_142244_RESEARCH_DELIVERY_SUMMARY.json",
    "qdrant_pending/indexed/doc_20251104_142308_COMMIT_7c01260_change.json",
    "qdrant_pending/indexed/doc_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.json",
    "qdrant_pending/indexed/doc_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.json",
    "qdrant_pending/indexed/doc_20251104_143611_COMMIT_594e664_feature.json",
    "qdrant_pending/indexed/doc_20251104_144915_COMMIT_6a77410_documentation.json",
    "qdrant_pending/indexed/doc_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.json",
    "qdrant_pending/indexed/doc_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.json",
    "qdrant_pending/indexed/doc_20251104_145842_COMMIT_038e967_feature.json",
    "qdrant_pending/indexed/doc_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.json",
    "qdrant_pending/indexed/doc_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.json",
    "qdrant_pending/indexed/doc_20251104_151117_COMMIT_388327f_feature.json",
    "qdrant_pending/indexed/doc_20251104_183128_INSTITUTIONAL_API_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_183139_README.json",
    "qdrant_pending/indexed/doc_20251104_183144_README.json",
    "qdrant_pending/indexed/doc_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.json",
    "qdrant_pending/indexed/doc_20251104_184219_BELLINGCAT_LEVEL_OSINT.json",
    "qdrant_pending/indexed/doc_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_184917_AGENT_TOOLKITS_COMPLETE.json",
    "qdrant_pending/indexed/doc_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.json",
    "qdrant_pending/indexed/doc_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.json",
    "qdrant_pending/indexed/doc_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.json",
    "qdrant_pending/indexed/doc_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.json",
    "qdrant_pending/indexed/doc_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.json",
    "qdrant_pending/indexed/doc_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.json",
    "qdrant_pending/indexed/doc_20251104_190812_INVESTIGATION_PLAN.json",
    "qdrant_pending/indexed/doc_20251104_190943_ELENA_OSINT_REPORT.json",
    "qdrant_pending/indexed/doc_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.json",
    "qdrant_pending/indexed/doc_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_191829_ADRIAN_LEGAL_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_192245_DAMIAN_CRITICAL_REVIEW.json",
    "qdrant_pending/indexed/doc_20251104_192454_FINAL_INVESTIGATION_REPORT.json",
    "qdrant_pending/indexed/doc_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.json",
    "qdrant_pending/indexed/doc_20251104_193555_HYBRID_SYSTEM_QUICK_START.json",
    "qdrant_pending/indexed/doc_20251104_193622_README.json",
    "qdrant_pending/indexed/doc_20251104_194002_DATA_SEPARATION_ARCHITECTURE.json",
    "qdrant_pending/indexed/doc_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.json",
    "qdrant_pending/indexed/doc_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.json",
    "qdrant_pending/indexed/doc_20251104_195310_INTERNET_RESEARCH_CAPABILITY.json",
    "qdrant_pending/indexed/doc_20251104_195345_INTERNET_RESEARCH_CAPABILITY.json",
    "qdrant_pending/indexed/doc_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.json",
    "qdrant_pending/indexed/doc_20251104_195847_INVESTIGATION_STATUS.json",
    "qdrant_pending/indexed/doc_20251104_203406_FINAL_OSINT_REPORT.json",
    "qdrant_pending/indexed/doc_20251104_203700_FINAL_OSINT_REPORT.json",
    "qdrant_pending/indexed/doc_20251104_204516_FINAL_OSINT_REPORT.json",
    "qdrant_pending/indexed/doc_20251104_211443_SEARCH_ORCHESTRATOR.json",
    "qdrant_pending/indexed/doc_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_220219_POSTGRES_STUCK_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251104_220923_BATCH_MIGRATION_PLAN.json",
    "queue_for_batch.sh",
    "redis_pending/redis_20251104_132626_COMMIT_300ea7b_feature.txt",
    "redis_pending/redis_20251104_142120_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.txt",
    "redis_pending/redis_20251104_142244_RESEARCH_DELIVERY_SUMMARY.txt",
    "redis_pending/redis_20251104_142308_COMMIT_7c01260_change.txt",
    "redis_pending/redis_20251104_143218_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.txt",
    "redis_pending/redis_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.txt",
    "redis_pending/redis_20251104_143611_COMMIT_594e664_feature.txt",
    "redis_pending/redis_20251104_144915_COMMIT_6a77410_documentation.txt",
    "redis_pending/redis_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.txt",
    "redis_pending/redis_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.txt",
    "redis_pending/redis_20251104_145842_COMMIT_038e967_feature.txt",
    "redis_pending/redis_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.txt",
    "redis_pending/redis_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.txt",
    "redis_pending/redis_20251104_151117_COMMIT_388327f_feature.txt",
    "redis_pending/redis_20251104_183128_INSTITUTIONAL_API_ANALYSIS.txt",
    "redis_pending/redis_20251104_183139_README.txt",
    "redis_pending/redis_20251104_183144_README.txt",
    "redis_pending/redis_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.txt",
    "redis_pending/redis_20251104_184219_BELLINGCAT_LEVEL_OSINT.txt",
    "redis_pending/redis_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.txt",
    "redis_pending/redis_20251104_184917_AGENT_TOOLKITS_COMPLETE.txt",
    "redis_pending/redis_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.txt",
    "redis_pending/redis_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.txt",
    "redis_pending/redis_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.txt",
    "redis_pending/redis_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.txt",
    "redis_pending/redis_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.txt",
    "redis_pending/redis_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.txt",
    "redis_pending/redis_20251104_190812_INVESTIGATION_PLAN.txt",
    "redis_pending/redis_20251104_190944_ELENA_OSINT_REPORT.txt",
    "redis_pending/redis_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.txt",
    "redis_pending/redis_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.txt",
    "redis_pending/redis_20251104_191829_ADRIAN_LEGAL_ANALYSIS.txt",
    "redis_pending/redis_20251104_192040_MAYA_DATA_TIMELINE_ANALYSIS.txt",
    "redis_pending/redis_20251104_192245_DAMIAN_CRITICAL_REVIEW.txt",
    "redis_pending/redis_20251104_192454_FINAL_INVESTIGATION_REPORT.txt",
    "redis_pending/redis_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.txt",
    "redis_pending/redis_20251104_193555_HYBRID_SYSTEM_QUICK_START.txt",
    "redis_pending/redis_20251104_193622_README.txt",
    "redis_pending/redis_20251104_194002_DATA_SEPARATION_ARCHITECTURE.txt",
    "redis_pending/redis_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.txt",
    "redis_pending/redis_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.txt",
    "redis_pending/redis_20251104_195310_INTERNET_RESEARCH_CAPABILITY.txt",
    "redis_pending/redis_20251104_195345_INTERNET_RESEARCH_CAPABILITY.txt",
    "redis_pending/redis_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.txt",
    "redis_pending/redis_20251104_195847_INVESTIGATION_STATUS.txt",
    "redis_pending/redis_20251104_203406_FINAL_OSINT_REPORT.txt",
    "redis_pending/redis_20251104_203700_FINAL_OSINT_REPORT.txt",
    "redis_pending/redis_20251104_204516_FINAL_OSINT_REPORT.txt",
    "redis_pending/redis_20251104_211443_SEARCH_ORCHESTRATOR.txt",
    "redis_pending/redis_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.txt",
    "redis_pending/redis_20251104_220219_POSTGRES_STUCK_ANALYSIS.txt",
    "redis_pending/redis_20251104_220924_BATCH_MIGRATION_PLAN.txt",
    "requirements.txt",
    "scripts/extract_pdf_text_to_es.py",
    "scripts/hybrid_osint_processor_test.py",
    "scripts/ingest_investigation_osint.py",
    "scripts/scrape_grupaazoty_pdfs.py",
    "scripts/sync_documents_to_neo4j.py",
    "scripts/sync_es_references_to_pg.py",
    "search_orchestrator.py",
    "setup_hourly_batch.sh",
    "shared_workspace/tasks/task_cpk_research_demo.json",
    "sql/es_document_references_schema.sql",
    "sql/realtime_updates/neo4j_20251104_132626_COMMIT_300ea7b_feature.cypher",
    "sql/realtime_updates/neo4j_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_142244_RESEARCH_DELIVERY_SUMMARY.cypher",
    "sql/realtime_updates/neo4j_20251104_142308_COMMIT_7c01260_change.cypher",
    "sql/realtime_updates/neo4j_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.cypher",
    "sql/realtime_updates/neo4j_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.cypher",
    "sql/realtime_updates/neo4j_20251104_143611_COMMIT_594e664_feature.cypher",
    "sql/realtime_updates/neo4j_20251104_144915_COMMIT_6a77410_documentation.cypher",
    "sql/realtime_updates/neo4j_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.cypher",
    "sql/realtime_updates/neo4j_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.cypher",
    "sql/realtime_updates/neo4j_20251104_145842_COMMIT_038e967_feature.cypher",
    "sql/realtime_updates/neo4j_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.cypher",
    "sql/realtime_updates/neo4j_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.cypher",
    "sql/realtime_updates/neo4j_20251104_151117_COMMIT_388327f_feature.cypher",
    "sql/realtime_updates/neo4j_20251104_183128_INSTITUTIONAL_API_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_183139_README.cypher",
    "sql/realtime_updates/neo4j_20251104_183144_README.cypher",
    "sql/realtime_updates/neo4j_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.cypher",
    "sql/realtime_updates/neo4j_20251104_184219_BELLINGCAT_LEVEL_OSINT.cypher",
    "sql/realtime_updates/neo4j_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_184917_AGENT_TOOLKITS_COMPLETE.cypher",
    "sql/realtime_updates/neo4j_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.cypher",
    "sql/realtime_updates/neo4j_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.cypher",
    "sql/realtime_updates/neo4j_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.cypher",
    "sql/realtime_updates/neo4j_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.cypher",
    "sql/realtime_updates/neo4j_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.cypher",
    "sql/realtime_updates/neo4j_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.cypher",
    "sql/realtime_updates/neo4j_20251104_190812_INVESTIGATION_PLAN.cypher",
    "sql/realtime_updates/neo4j_20251104_190943_ELENA_OSINT_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.cypher",
    "sql/realtime_updates/neo4j_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_191829_ADRIAN_LEGAL_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_192245_DAMIAN_CRITICAL_REVIEW.cypher",
    "sql/realtime_updates/neo4j_20251104_192454_FINAL_INVESTIGATION_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.cypher",
    "sql/realtime_updates/neo4j_20251104_193555_HYBRID_SYSTEM_QUICK_START.cypher",
    "sql/realtime_updates/neo4j_20251104_193622_README.cypher",
    "sql/realtime_updates/neo4j_20251104_194002_DATA_SEPARATION_ARCHITECTURE.cypher",
    "sql/realtime_updates/neo4j_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.cypher",
    "sql/realtime_updates/neo4j_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.cypher",
    "sql/realtime_updates/neo4j_20251104_195310_INTERNET_RESEARCH_CAPABILITY.cypher",
    "sql/realtime_updates/neo4j_20251104_195345_INTERNET_RESEARCH_CAPABILITY.cypher",
    "sql/realtime_updates/neo4j_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.cypher",
    "sql/realtime_updates/neo4j_20251104_195847_INVESTIGATION_STATUS.cypher",
    "sql/realtime_updates/neo4j_20251104_203406_FINAL_OSINT_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251104_203700_FINAL_OSINT_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251104_204516_FINAL_OSINT_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251104_211443_SEARCH_ORCHESTRATOR.cypher",
    "sql/realtime_updates/neo4j_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_220219_POSTGRES_STUCK_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251104_220923_BATCH_MIGRATION_PLAN.cypher",
    "sql/realtime_updates/pg_20251104_132626_COMMIT_300ea7b_feature.sql",
    "sql/realtime_updates/pg_20251104_142119_FACE_RECOGNITION_OPENSOURCE_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_142244_RESEARCH_DELIVERY_SUMMARY.sql",
    "sql/realtime_updates/pg_20251104_142308_COMMIT_7c01260_change.sql",
    "sql/realtime_updates/pg_20251104_143217_FACE_RECOGNITION_LIBRARY_DEEP_DIVE.sql",
    "sql/realtime_updates/pg_20251104_143527_FACE_RECOGNITION_TECHNICAL_VALIDATION.sql",
    "sql/realtime_updates/pg_20251104_143611_COMMIT_594e664_feature.sql",
    "sql/realtime_updates/pg_20251104_144915_COMMIT_6a77410_documentation.sql",
    "sql/realtime_updates/pg_20251104_145607_DEEP_RESEARCH_AGENTS_CONCEPT.sql",
    "sql/realtime_updates/pg_20251104_145754_DEEP_RESEARCH_TECHNICAL_ARCHITECTURE.sql",
    "sql/realtime_updates/pg_20251104_145842_COMMIT_038e967_feature.sql",
    "sql/realtime_updates/pg_20251104_150727_SEJM_API_ANALYSIS_CONCEPT.sql",
    "sql/realtime_updates/pg_20251104_151039_SEJM_ASW_ANALYSIS_2019_2023.sql",
    "sql/realtime_updates/pg_20251104_151117_COMMIT_388327f_feature.sql",
    "sql/realtime_updates/pg_20251104_183128_INSTITUTIONAL_API_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_183139_README.sql",
    "sql/realtime_updates/pg_20251104_183144_README.sql",
    "sql/realtime_updates/pg_20251104_183843_COMPREHENSIVE_OSINT_SYSTEM.sql",
    "sql/realtime_updates/pg_20251104_184219_BELLINGCAT_LEVEL_OSINT.sql",
    "sql/realtime_updates/pg_20251104_184618_BELLINGCAT_METHODOLOGY_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_184917_AGENT_TOOLKITS_COMPLETE.sql",
    "sql/realtime_updates/pg_20251104_185328_SYSTEM_CAPABILITIES_UPDATE_2025_11_04.sql",
    "sql/realtime_updates/pg_20251104_185811_ADAPTIVE_LEARNING_SYSTEM.sql",
    "sql/realtime_updates/pg_20251104_185959_SESSION_SUMMARY_2025_11_04_OSINT_SYSTEM.sql",
    "sql/realtime_updates/pg_20251104_190459_SOURCE_ATTRIBUTION_PROTOCOL.sql",
    "sql/realtime_updates/pg_20251104_190531_SOURCE_CITATION_QUICK_REFERENCE.sql",
    "sql/realtime_updates/pg_20251104_190638_MANDATORY_SOURCE_ATTRIBUTION_ANNOUNCEMENT.sql",
    "sql/realtime_updates/pg_20251104_190812_INVESTIGATION_PLAN.sql",
    "sql/realtime_updates/pg_20251104_190943_ELENA_OSINT_REPORT.sql",
    "sql/realtime_updates/pg_20251104_191155_SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.sql",
    "sql/realtime_updates/pg_20251104_191613_MARCUS_FINANCIAL_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_191829_ADRIAN_LEGAL_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_192039_MAYA_DATA_TIMELINE_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_192245_DAMIAN_CRITICAL_REVIEW.sql",
    "sql/realtime_updates/pg_20251104_192454_FINAL_INVESTIGATION_REPORT.sql",
    "sql/realtime_updates/pg_20251104_193140_HYBRID_ONPREM_INTELLIGENCE_SYSTEM.sql",
    "sql/realtime_updates/pg_20251104_193555_HYBRID_SYSTEM_QUICK_START.sql",
    "sql/realtime_updates/pg_20251104_193622_README.sql",
    "sql/realtime_updates/pg_20251104_194002_DATA_SEPARATION_ARCHITECTURE.sql",
    "sql/realtime_updates/pg_20251104_194330_HYBRID_SYSTEM_COMPLETE_OVERVIEW.sql",
    "sql/realtime_updates/pg_20251104_194521_DESTINY_CHAT_UI_HYBRID_INTEGRATION.sql",
    "sql/realtime_updates/pg_20251104_195310_INTERNET_RESEARCH_CAPABILITY.sql",
    "sql/realtime_updates/pg_20251104_195345_INTERNET_RESEARCH_CAPABILITY.sql",
    "sql/realtime_updates/pg_20251104_195433_DUCKDUCKGO_SEARCH_METHOD.sql",
    "sql/realtime_updates/pg_20251104_195847_INVESTIGATION_STATUS.sql",
    "sql/realtime_updates/pg_20251104_203406_FINAL_OSINT_REPORT.sql",
    "sql/realtime_updates/pg_20251104_203700_FINAL_OSINT_REPORT.sql",
    "sql/realtime_updates/pg_20251104_204516_FINAL_OSINT_REPORT.sql",
    "sql/realtime_updates/pg_20251104_211443_SEARCH_ORCHESTRATOR.sql",
    "sql/realtime_updates/pg_20251104_212055_DATA_ARCHITECTURE_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_220219_POSTGRES_STUCK_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251104_220923_BATCH_MIGRATION_PLAN.sql",
    "supervisor_interface.py",
    "technical_emergency_response.py",
    "test_hybrid_system.py",
    "tests/test_search_orchestrator_real_data.py",
    "tests/test_smart_references_integration.py"
  ],
  "auto_generated": true
}
```

---
*This document was automatically generated from a git commit.*
*Helena will process this and add to all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis).*