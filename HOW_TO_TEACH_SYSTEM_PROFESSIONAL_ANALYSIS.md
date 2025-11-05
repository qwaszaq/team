# 🎓 JAK NAUCZYĆ SYSTEM AUTOMATYCZNEJ ANALIZY RAPORTÓW CBA
## Implementation Guide: Teaching AI System Professional Analysis

**Data:** 2024-11-05  
**Cel:** Przekonwertować profesjonalną metodologię analizy na automatyczny system  
**Approach:** Step-by-step implementation guide

---

## 📊 EXECUTIVE SUMMARY

### Problem

**Obecny system:**
- ✅ Wykrywa dokumenty investigative
- ✅ Ekstrahuje tekst z PDF
- ✅ Liczy keywords
- ❌ **Nie przeprowadza profesjonalnej analizy** (7 faz)
- ❌ **Nie wyciąga strukturalnych danych** (tabele, metryki)
- ❌ **Nie formułuje wniosków strategicznych**

### Rozwiązanie

**System z pełną analizą:**
- ✅ 7-fazowa analiza automatyczna
- ✅ Ekstrakcja strukturalnych danych
- ✅ Analiza temporalna z trendami
- ✅ Analiza jakościowa
- ✅ Synteza wniosków i rekomendacji

---

## 🎯 ARCHITEKTURA SYSTEMU

### Obecna Architektura

```
┌─────────────────────────────────────────┐
│  AutonomousOrchestrator                 │
│  ├─ Document Scanner                    │
│  ├─ Intelligent Classifier             │
│  ├─ Task Generator                     │
│  └─ Basic Agent Execution              │
└─────────────────────────────────────────┘
```

### Docelowa Architektura (z pełną analizą)

```
┌─────────────────────────────────────────────────────────┐
│  AutonomousOrchestrator (Enhanced)                     │
│  ├─ Document Scanner                                    │
│  ├─ Intelligent Classifier                             │
│  ├─ Professional Analyzer (NEW!)                       │
│  │   ├─ Phase 1: Structure Analysis                   │
│  │   ├─ Phase 2: Quantitative Extraction              │
│  │   ├─ Phase 3: Qualitative Analysis                 │
│  │   ├─ Phase 4: Temporal Trends                       │
│  │   ├─ Phase 5: Comparative Analysis                  │
│  │   ├─ Phase 6: Critical Assessment                   │
│  │   └─ Phase 7: Insight Synthesis                     │
│  ├─ Data Extraction Pipeline (NEW!)                   │
│  │   ├─ PDF Table Parser                               │
│  │   ├─ OCR Engine                                      │
│  │   ├─ Structured Data Extractor                       │
│  │   └─ Data Validator                                  │
│  ├─ LLM Analysis Layer (Enhanced)                      │
│  │   ├─ Context-Aware Prompts                           │
│  │   ├─ Evidence-Based Analysis                         │
│  │   └─ Synthesis Engine                                │
│  └─ Report Generator (Enhanced)                         │
│      ├─ Professional Report Templates                   │
│      ├─ Visualization Generator                         │
│      └─ Executive Summary                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 IMPLEMENTACJA: KOMPONENT PO KOMPONENCIE

### 1. Professional Analyzer Module

**Plik:** `src/analysis/professional_analyzer.py`

```python
"""
Professional Analyzer - 7-Phase Analysis Engine
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re
from collections import defaultdict


@dataclass
class AnalysisConfig:
    """Configuration for professional analysis"""
    enable_structure_analysis: bool = True
    enable_quantitative_extraction: bool = True
    enable_qualitative_analysis: bool = True
    enable_temporal_trends: bool = True
    enable_comparative_analysis: bool = True
    enable_critical_assessment: bool = True
    enable_synthesis: bool = True


class ProfessionalAnalyzer:
    """
    Professional 7-Phase Analysis Engine
    
    Performs comprehensive analysis following professional methodology:
    1. Structure Analysis
    2. Quantitative Extraction
    3. Qualitative Analysis
    4. Temporal Trends
    5. Comparative Analysis
    6. Critical Assessment
    7. Insight Synthesis
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None):
        self.config = config or AnalysisConfig()
        
        # Initialize extractors
        self.structure_extractor = StructureExtractor()
        self.quantitative_extractor = QuantitativeExtractor()
        self.qualitative_analyzer = QualitativeAnalyzer()
        self.trend_analyzer = TemporalTrendAnalyzer()
        self.comparative_analyzer = ComparativeAnalyzer()
        self.critical_assessor = CriticalAssessor()
        self.synthesis_engine = SynthesisEngine()
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform complete 7-phase analysis
        
        Args:
            documents: List of document dicts with 'text', 'year', 'filename'
        
        Returns:
            Complete analysis results for all phases
        """
        results = {}
        
        # Phase 1: Structure Analysis
        if self.config.enable_structure_analysis:
            print("📋 Phase 1: Structure Analysis...")
            results['phase1'] = self.structure_extractor.analyze(documents)
        
        # Phase 2: Quantitative Extraction
        if self.config.enable_quantitative_extraction:
            print("📊 Phase 2: Quantitative Extraction...")
            results['phase2'] = self.quantitative_extractor.extract(documents)
        
        # Phase 3: Qualitative Analysis
        if self.config.enable_qualitative_analysis:
            print("📝 Phase 3: Qualitative Analysis...")
            results['phase3'] = self.qualitative_analyzer.analyze(documents)
        
        # Phase 4: Temporal Trends
        if self.config.enable_temporal_trends and 'phase2' in results:
            print("📈 Phase 4: Temporal Trends...")
            results['phase4'] = self.trend_analyzer.analyze(results['phase2'])
        
        # Phase 5: Comparative Analysis
        if self.config.enable_comparative_analysis and 'phase2' in results:
            print("🔍 Phase 5: Comparative Analysis...")
            results['phase5'] = self.comparative_analyzer.analyze(results['phase2'])
        
        # Phase 6: Critical Assessment
        if self.config.enable_critical_assessment:
            print("⚠️  Phase 6: Critical Assessment...")
            results['phase6'] = self.critical_assessor.assess(documents, results)
        
        # Phase 7: Synthesis
        if self.config.enable_synthesis:
            print("💡 Phase 7: Insight Synthesis...")
            results['phase7'] = self.synthesis_engine.synthesize(results)
        
        return results
```

---

### 2. Structure Extractor

**Plik:** `src/analysis/structure_extractor.py`

```python
"""
Phase 1: Document Structure Analysis
"""

import re
from typing import Dict, List, Any
from collections import defaultdict


class StructureExtractor:
    """Extract and analyze document structure"""
    
    def __init__(self):
        # Common section patterns for CBA reports
        self.section_patterns = [
            r'(?:Rozdział|ROZDZIAŁ|Dział|DZIAŁ)\s+[IVX\d]+[\.\)]?\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
            r'^\s*([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{5,50})\s*$',
            r'[0-9]+\.\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
            r'###\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\n]{5,80})',  # Markdown headers
        ]
        
        # Common CBA sections (domain knowledge)
        self.known_sections = [
            'Wprowadzenie',
            'Działalność operacyjna',
            'Sprawy operacyjne',
            'Sprawy kontrolne',
            'Wyniki finansowe',
            'Budżet',
            'Kadra',
            'Funkcjonariusze',
            'Szkolenia',
            'Współpraca międzynarodowa',
            'Podsumowanie',
        ]
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze structure of all documents"""
        
        structures = {}
        all_sections = []
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            
            if not text or len(text) < 100:
                continue
            
            # Extract sections
            sections = self._extract_sections(text)
            
            if year:
                structures[year] = {
                    'filename': filename,
                    'sections': sections,
                    'text_length': len(text),
                    'section_count': len(sections),
                }
                
                all_sections.extend(sections)
        
        # Identify common sections
        common_sections = self._identify_common_sections(all_sections)
        
        # Analyze structure evolution
        evolution = self._analyze_evolution(structures)
        
        return {
            'total_documents': len(structures),
            'structures': structures,
            'common_sections': common_sections,
            'evolution': evolution,
        }
    
    def _extract_sections(self, text: str, max_chars: int = 10000) -> List[str]:
        """Extract section headers from text"""
        sections = []
        text_sample = text[:max_chars]  # First 10k chars usually contain structure
        
        for pattern in self.section_patterns:
            matches = re.findall(pattern, text_sample, re.MULTILINE)
            sections.extend(matches)
        
        # Clean and deduplicate
        sections = [s.strip() for s in sections if len(s.strip()) > 5]
        sections = list(dict.fromkeys(sections))  # Remove duplicates, preserve order
        
        return sections[:20]  # Top 20 sections
    
    def _identify_common_sections(self, all_sections: List[str]) -> List[str]:
        """Identify sections common across documents"""
        section_counts = defaultdict(int)
        
        for section in all_sections:
            normalized = section.lower().strip()
            section_counts[normalized] += 1
        
        # Return most common (appearing in at least 2 documents)
        common = [
            section for section, count in sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
            if count >= 2
        ]
        
        return common[:20]
    
    def _analyze_evolution(self, structures: Dict[int, Dict]) -> Dict[str, Any]:
        """Analyze how structure evolved over time"""
        if len(structures) < 2:
            return {}
        
        years = sorted(structures.keys())
        
        # Calculate average sections per period
        early_years = years[:len(years)//2]
        recent_years = years[len(years)//2:]
        
        early_avg_sections = sum(structures[y]['section_count'] for y in early_years) / len(early_years)
        recent_avg_sections = sum(structures[y]['section_count'] for y in recent_years) / len(recent_years)
        
        return {
            'early_period': {
                'years': early_years,
                'avg_sections': early_avg_sections,
            },
            'recent_period': {
                'years': recent_years,
                'avg_sections': recent_avg_sections,
            },
            'evolution': 'increasing' if recent_avg_sections > early_avg_sections else 'decreasing',
        }
```

---

### 3. Quantitative Extractor

**Plik:** `src/analysis/quantitative_extractor.py`

```python
"""
Phase 2: Quantitative Data Extraction
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class DataConfidence(Enum):
    """Confidence levels for extracted data"""
    VERIFIED = "verified"  # ✅ Verified from source
    EXTRACTED = "extracted"  # ✅ Extracted from document
    ESTIMATED = "estimated"  # ⚠️ Estimated by LLM
    MISSING = "missing"  # ❌ Missing data


@dataclass
class ExtractedMetric:
    """Represents a single extracted metric"""
    name: str
    value: Any
    year: Optional[int]
    confidence: DataConfidence
    source: str  # filename, page, table reference
    context: Optional[str] = None  # surrounding text


class QuantitativeExtractor:
    """Extract quantitative data from documents"""
    
    def __init__(self):
        # Domain-specific patterns for CBA reports
        self.patterns = {
            'sprawy_operacyjne': [
                r'spraw[^.]*operacyjn[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+spraw[^.]*operacyjn',
                r'wszczęto\s+(\d{1,4})\s+spraw',
                r'liczba\s+spraw\s+operacyjnych[^.]*(\d{1,4})',
            ],
            'sprawy_zakończone': [
                r'zakończon[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zakończon',
                r'zakończono\s+(\d{1,4})\s+spraw',
            ],
            'sprawy_w_toku': [
                r'w\s+toku[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+spraw[^.]*w\s+toku',
            ],
            'zatrzymania': [
                r'zatrzyman[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zatrzymań',
                r'zatrzymano\s+(\d{1,4})\s+osób',
            ],
            'zarzuty': [
                r'zarzut[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zarzut',
                r'postawiono\s+(\d{1,4})\s+zarzut',
            ],
            'skazania': [
                r'skazan[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+skazań',
                r'skazano\s+(\d{1,4})\s+osób',
            ],
            'budzet': [
                r'budżet[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)[^.]*budżet',
                r'budżet.*?(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)',
            ],
            'funkcjonariusze': [
                r'funkcjonariusz[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+funkcjonariusz',
                r'liczba\s+funkcjonariuszy[^.]*(\d{1,4})',
            ],
            'szkolenia': [
                r'szkoleni[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+szkoleń',
                r'przeprowadzono\s+(\d{1,4})\s+szkoleń',
            ],
            'odzyskane_srodki': [
                r'odzyskan[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)[^.]*odzyskan',
            ],
        }
    
    def extract(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract quantitative metrics from documents
        
        Returns:
            Dict with metrics per year
        """
        metrics_by_year = {}
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            
            if not year or not text:
                continue
            
            year_metrics = {}
            
            for metric_name, pattern_list in self.patterns.items():
                extracted_metrics = []
                
                for pattern in pattern_list:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    
                    for match in matches[:5]:  # Take up to 5 matches
                        try:
                            value = self._parse_value(match, metric_name)
                            
                            if value is not None:
                                metric = ExtractedMetric(
                                    name=metric_name,
                                    value=value,
                                    year=year,
                                    confidence=DataConfidence.EXTRACTED,
                                    source=f"{filename}",
                                )
                                extracted_metrics.append(metric)
                        except:
                            continue
                
                # Choose best value (highest confidence, most frequent, etc.)
                if extracted_metrics:
                    # Use most common value
                    values = [m.value for m in extracted_metrics]
                    best_value = max(set(values), key=values.count)
                    year_metrics[metric_name] = {
                        'value': best_value,
                        'confidence': DataConfidence.EXTRACTED.value,
                        'source': filename,
                        'matches_found': len(extracted_metrics),
                    }
            
            if year_metrics:
                metrics_by_year[year] = year_metrics
        
        return {
            'metrics': metrics_by_year,
            'total_years': len(metrics_by_year),
            'extraction_summary': self._create_summary(metrics_by_year),
        }
    
    def _parse_value(self, match: Any, metric_name: str) -> Optional[int]:
        """Parse extracted value to integer"""
        if isinstance(match, tuple):
            match = match[0]
        
        # Clean value
        value_str = str(match).replace(' ', '').replace(',', '').replace('.', '')
        
        try:
            value = int(value_str)
            
            # Handle budget (might be in millions)
            if metric_name == 'budzet' and value < 1000:
                value = value * 1000000
            
            return value
        except:
            return None
    
    def _create_summary(self, metrics_by_year: Dict) -> Dict[str, Any]:
        """Create summary of extracted metrics"""
        summary = {
            'total_metrics_extracted': sum(len(m) for m in metrics_by_year.values()),
            'metrics_per_year': {year: len(metrics) for year, metrics in metrics_by_year.items()},
            'coverage': {
                'years_with_data': len(metrics_by_year),
                'years_total': len(set(range(2008, 2025))),
                'coverage_percentage': len(metrics_by_year) / 17 * 100,
            },
        }
        
        return summary
```

---

### 4. Qualitative Analyzer

**Plik:** `src/analysis/qualitative_analyzer.py`

```python
"""
Phase 3: Qualitative Analysis
"""

import re
from typing import Dict, List, Any
from collections import defaultdict


class QualitativeAnalyzer:
    """Analyze qualitative aspects of documents"""
    
    def __init__(self):
        # Tone indicators
        self.tone_patterns = {
            'positive': [
                'sukces', 'osiągnięci', 'efektywn', 'poprawa', 
                'wzrost', 'rozwój', 'udan', 'pozytywn'
            ],
            'challenge': [
                'wyzwani', 'trudności', 'problem', 'ograniczen',
                'bariery', 'utrudnien', 'spadek'
            ],
            'cooperation': [
                'współprac', 'kooperacj', 'partnerstw', 'współdziałan',
                'koordynacj', 'wsparcie'
            ],
            'innovation': [
                'nowoczesn', 'innowacj', 'rozwój', 'modernizacj',
                'technolog', 'cyfrow', 'digitalizacj'
            ],
        }
        
        # Theme patterns
        self.theme_patterns = {
            'korupcja': ['korupcj', 'łapówk', 'przekup', 'antykorupcyjn'],
            'współpraca_międzynarodowa': ['międzynarodow', 'europejsk', 'unij', 'eu'],
            'szkolenia': ['szkoleni', 'kurs', 'edukacj', 'trening'],
            'technologia': ['technolog', 'cyfrow', 'system informatyczn', 'it'],
            'finansowanie': ['budżet', 'finansow', 'nakład', 'środki'],
        }
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform qualitative analysis"""
        
        narrative_analysis = {}
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            
            if not year or not text:
                continue
            
            text_lower = text.lower()
            
            # Analyze tone
            tone_scores = {}
            for tone, keywords in self.tone_patterns.items():
                score = sum(len(re.findall(kw, text_lower)) for kw in keywords)
                tone_scores[tone] = score
            
            # Analyze themes
            theme_scores = {}
            for theme, keywords in self.theme_patterns.items():
                score = sum(len(re.findall(kw, text_lower)) for kw in keywords)
                theme_scores[theme] = score
            
            # Determine dominant tone and theme
            dominant_tone = max(tone_scores.items(), key=lambda x: x[1])[0] if tone_scores else None
            dominant_theme = max(theme_scores.items(), key=lambda x: x[1])[0] if theme_scores else None
            
            narrative_analysis[year] = {
                'tone': tone_scores,
                'themes': theme_scores,
                'dominant_tone': dominant_tone,
                'dominant_theme': dominant_theme,
                'text_length': len(text),
            }
        
        # Cross-temporal analysis
        evolution = self._analyze_evolution(narrative_analysis)
        
        return {
            'narrative_analysis': narrative_analysis,
            'evolution': evolution,
        }
    
    def _analyze_evolution(self, narrative_analysis: Dict[int, Dict]) -> Dict[str, Any]:
        """Analyze how tone and themes evolved"""
        if len(narrative_analysis) < 2:
            return {}
        
        years = sorted(narrative_analysis.keys())
        mid_point = len(years) // 2
        
        early_years = years[:mid_point]
        recent_years = years[mid_point:]
        
        # Average tone scores
        early_avg_tones = defaultdict(float)
        recent_avg_tones = defaultdict(float)
        
        for year in early_years:
            if year in narrative_analysis:
                for tone, score in narrative_analysis[year]['tone'].items():
                    early_avg_tones[tone] += score
        
        for year in recent_years:
            if year in narrative_analysis:
                for tone, score in narrative_analysis[year]['tone'].items():
                    recent_avg_tones[tone] += score
        
        # Normalize
        if early_years:
            early_avg_tones = {k: v / len(early_years) for k, v in early_avg_tones.items()}
        if recent_years:
            recent_avg_tones = {k: v / len(recent_years) for k, v in recent_avg_tones.items()}
        
        return {
            'early_period': dict(early_avg_tones),
            'recent_period': dict(recent_avg_tones),
            'changes': self._calculate_changes(early_avg_tones, recent_avg_tones),
        }
    
    def _calculate_changes(self, early: Dict, recent: Dict) -> Dict[str, float]:
        """Calculate changes between periods"""
        changes = {}
        all_keys = set(early.keys()) | set(recent.keys())
        
        for key in all_keys:
            early_val = early.get(key, 0)
            recent_val = recent.get(key, 0)
            if early_val > 0:
                change = ((recent_val - early_val) / early_val) * 100
            else:
                change = 100 if recent_val > 0 else 0
            changes[key] = change
        
        return changes
```

---

### 5. Temporal Trend Analyzer

**Plik:** `src/analysis/temporal_trend_analyzer.py`

```python
"""
Phase 4: Temporal Trend Analysis
"""

from typing import Dict, List, Any, Optional
import numpy as np
from scipy import stats


class TemporalTrendAnalyzer:
    """Analyze temporal trends in metrics"""
    
    def analyze(self, quantitative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in quantitative metrics"""
        
        metrics = quantitative_data.get('metrics', {})
        if not metrics:
            return {}
        
        trends = {}
        
        # For each metric, calculate trends
        metric_names = set()
        for year_data in metrics.values():
            metric_names.update(year_data.keys())
        
        for metric_name in metric_names:
            values = []
            years = []
            
            for year in sorted(metrics.keys()):
                if metric_name in metrics[year]:
                    value = metrics[year][metric_name].get('value')
                    if value is not None:
                        values.append(value)
                        years.append(year)
            
            if len(values) >= 2:
                trend_data = self._calculate_trend(years, values, metric_name)
                trends[metric_name] = trend_data
        
        return {
            'trends': trends,
            'summary': self._create_trend_summary(trends),
        }
    
    def _calculate_trend(self, years: List[int], values: List[float], metric_name: str) -> Dict[str, Any]:
        """Calculate trend for a metric"""
        
        # Basic statistics
        first_value = values[0]
        last_value = values[-1]
        total_growth = ((last_value - first_value) / first_value * 100) if first_value > 0 else 0
        
        # CAGR (Compound Annual Growth Rate)
        years_diff = years[-1] - years[0]
        if years_diff > 0 and first_value > 0:
            cagr = (((last_value / first_value) ** (1 / years_diff)) - 1) * 100
        else:
            cagr = 0
        
        # Linear regression for trend direction
        if len(years) >= 3:
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
                trend_direction = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
                trend_strength = abs(r_value)  # Correlation coefficient
            except:
                slope = 0
                trend_direction = 'stable'
                trend_strength = 0
        else:
            slope = (last_value - first_value) / years_diff if years_diff > 0 else 0
            trend_direction = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
            trend_strength = 0
        
        # Identify inflection points (if significant)
        inflection_points = self._find_inflection_points(years, values)
        
        return {
            'years': years,
            'values': values,
            'first_value': first_value,
            'last_value': last_value,
            'total_growth': total_growth,
            'cagr': cagr,
            'trend': trend_direction,
            'trend_strength': trend_strength,
            'slope': slope,
            'inflection_points': inflection_points,
        }
    
    def _find_inflection_points(self, years: List[int], values: List[float]) -> List[Dict[str, Any]]:
        """Find inflection points in time series"""
        if len(values) < 3:
            return []
        
        inflection_points = []
        
        for i in range(1, len(values) - 1):
            prev_change = values[i] - values[i-1]
            next_change = values[i+1] - values[i]
            
            # Sign change indicates inflection
            if (prev_change > 0 and next_change < 0) or (prev_change < 0 and next_change > 0):
                inflection_points.append({
                    'year': years[i],
                    'value': values[i],
                    'type': 'peak' if prev_change > 0 else 'trough',
                })
        
        return inflection_points
    
    def _create_trend_summary(self, trends: Dict[str, Dict]) -> Dict[str, Any]:
        """Create summary of all trends"""
        increasing = [name for name, data in trends.items() if data['trend'] == 'increasing']
        decreasing = [name for name, data in trends.items() if data['trend'] == 'decreasing']
        stable = [name for name, data in trends.items() if data['trend'] == 'stable']
        
        return {
            'total_metrics': len(trends),
            'increasing': len(increasing),
            'decreasing': len(decreasing),
            'stable': len(stable),
            'metrics_increasing': increasing,
            'metrics_decreasing': decreasing,
        }
```

---

### 6. Comparative Analyzer

**Plik:** `src/analysis/comparative_analyzer.py`

```python
"""
Phase 5: Comparative & Contextual Analysis
"""

from typing import Dict, List, Any
from collections import defaultdict


class ComparativeAnalyzer:
    """Perform comparative analysis"""
    
    def analyze(self, quantitative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comparative analysis"""
        
        metrics = quantitative_data.get('metrics', {})
        if not metrics:
            return {}
        
        comparative = {
            'efficiency_metrics': {},
            'periods': {},
            'correlations': {},
        }
        
        # Calculate efficiency metrics
        for year in sorted(metrics.keys()):
            year_data = metrics[year]
            
            efficiency = {}
            
            # Success rate
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne']['value']
                skazania = year_data['skazania']['value']
                if sprawy > 0:
                    efficiency['success_rate'] = (skazania / sprawy) * 100
            
            # Budget efficiency
            if 'budzet' in year_data and 'sprawy_operacyjne' in year_data:
                budzet = year_data['budzet']['value']
                sprawy = year_data['sprawy_operacyjne']['value']
                if sprawy > 0:
                    efficiency['cost_per_case'] = budzet / sprawy
            
            # Employee productivity
            if 'funkcjonariusze' in year_data and 'sprawy_operacyjne' in year_data:
                funkcjonariusze = year_data['funkcjonariusze']['value']
                sprawy = year_data['sprawy_operacyjne']['value']
                if funkcjonariusze > 0:
                    efficiency['cases_per_employee'] = sprawy / funkcjonariusze
            
            if efficiency:
                comparative['efficiency_metrics'][year] = efficiency
        
        # Periodization
        years = sorted(metrics.keys())
        if len(years) >= 4:
            mid_point = len(years) // 2
            comparative['periods'] = {
                'early': years[:mid_point],
                'recent': years[mid_point:],
                'comparison': self._compare_periods(years[:mid_point], years[mid_point:], metrics),
            }
        
        # Calculate correlations
        comparative['correlations'] = self._calculate_correlations(metrics)
        
        return comparative
    
    def _compare_periods(self, early_years: List[int], recent_years: List[int], 
                        metrics: Dict[int, Dict]) -> Dict[str, Any]:
        """Compare early vs recent periods"""
        
        comparison = {}
        
        # Aggregate metrics for each period
        early_metrics = defaultdict(list)
        recent_metrics = defaultdict(list)
        
        for year in early_years:
            if year in metrics:
                for metric_name, metric_data in metrics[year].items():
                    early_metrics[metric_name].append(metric_data['value'])
        
        for year in recent_years:
            if year in metrics:
                for metric_name, metric_data in metrics[year].items():
                    recent_metrics[metric_name].append(metric_data['value'])
        
        # Calculate averages and changes
        for metric_name in set(early_metrics.keys()) | set(recent_metrics.keys()):
            early_avg = sum(early_metrics[metric_name]) / len(early_metrics[metric_name]) if early_metrics[metric_name] else 0
            recent_avg = sum(recent_metrics[metric_name]) / len(recent_metrics[metric_name]) if recent_metrics[metric_name] else 0
            
            if early_avg > 0:
                change = ((recent_avg - early_avg) / early_avg) * 100
            else:
                change = 100 if recent_avg > 0 else 0
            
            comparison[metric_name] = {
                'early_avg': early_avg,
                'recent_avg': recent_avg,
                'change': change,
            }
        
        return comparison
    
    def _calculate_correlations(self, metrics: Dict[int, Dict]) -> Dict[str, float]:
        """Calculate correlations between metrics"""
        # This would require more sophisticated analysis
        # For now, return placeholder
        return {}
```

---

### 7. Critical Assessor

**Plik:** `src/analysis/critical_assessor.py`

```python
"""
Phase 6: Critical Assessment
"""

from typing import Dict, List, Any
from collections import defaultdict


class CriticalAssessor:
    """Perform critical assessment of data and analysis"""
    
    def assess(self, documents: List[Dict[str, Any]], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform critical assessment"""
        
        assessment = {
            'data_completeness': {},
            'consistency_issues': [],
            'methodology_changes': [],
            'missing_years': [],
            'confidence_scores': {},
            'limitations': [],
        }
        
        # Check data completeness
        quantitative_data = analysis_results.get('phase2', {})
        metrics = quantitative_data.get('metrics', {})
        
        all_years = set(range(2008, 2025))
        found_years = set(metrics.keys())
        missing_years = sorted(all_years - found_years)
        assessment['missing_years'] = missing_years
        
        # Check completeness per year
        for year in sorted(metrics.keys()):
            year_data = metrics[year]
            completeness = len([k for k in year_data.keys() if year_data[k].get('value') is not None]) / len(year_data) if year_data else 0
            assessment['data_completeness'][year] = completeness
        
        # Check consistency
        for year in sorted(metrics.keys()):
            year_data = metrics[year]
            
            # Logical consistency checks
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne'].get('value')
                skazania = year_data['skazania'].get('value')
                
                if sprawy and skazania and skazania > sprawy:
                    assessment['consistency_issues'].append({
                        'year': year,
                        'issue': f'Skazania ({skazania}) > Sprawy ({sprawy})',
                        'type': 'logical_inconsistency',
                        'severity': 'high',
                    })
            
            if 'budzet' in year_data and 'sprawy_operacyjne' in year_data:
                budzet = year_data['budzet'].get('value')
                sprawy = year_data['sprawy_operacyjne'].get('value')
                
                if budzet and sprawy:
                    cost_per_case = budzet / sprawy
                    if cost_per_case > 10000000:  # > 10M per case seems unreasonable
                        assessment['consistency_issues'].append({
                            'year': year,
                            'issue': f'Cost per case ({cost_per_case:,.0f} zł) seems very high',
                            'type': 'anomaly',
                            'severity': 'medium',
                        })
        
        # Identify limitations
        assessment['limitations'] = [
            'Analysis based on text extraction only (tables may contain additional data)',
            'Regex-based extraction may miss context',
            'No OCR for scanned documents',
            'No manual verification of extracted values',
            'Limited cross-validation between sources',
        ]
        
        # Calculate overall confidence
        if metrics:
            avg_completeness = sum(assessment['data_completeness'].values()) / len(assessment['data_completeness'])
            consistency_score = 1.0 - (len(assessment['consistency_issues']) / len(metrics) * 0.5)
            overall_confidence = (avg_completeness * 0.7 + consistency_score * 0.3)
            
            assessment['overall_confidence'] = overall_confidence
        
        return assessment
```

---

### 8. Synthesis Engine

**Plik:** `src/analysis/synthesis_engine.py`

```python
"""
Phase 7: Insight Synthesis
"""

from typing import Dict, List, Any
from collections import defaultdict


class SynthesisEngine:
    """Synthesize insights from all analysis phases"""
    
    def synthesize(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize insights from all phases"""
        
        synthesis = {
            'key_findings': [],
            'trends': [],
            'efficiency_insights': [],
            'recommendations': [],
            'executive_summary': '',
        }
        
        # Extract key findings from trends
        trends = analysis_results.get('phase4', {}).get('trends', {})
        for metric_name, trend_data in trends.items():
            if trend_data.get('trend') != 'stable':
                synthesis['key_findings'].append({
                    'metric': metric_name.replace('_', ' ').title(),
                    'trend': trend_data['trend'],
                    'growth': trend_data.get('total_growth', 0),
                    'cagr': trend_data.get('cagr', 0),
                    'significance': 'high' if abs(trend_data.get('total_growth', 0)) > 20 else 'medium',
                })
        
        # Efficiency insights
        comparative = analysis_results.get('phase5', {})
        efficiency = comparative.get('efficiency_metrics', {})
        if efficiency:
            avg_success_rate = sum(e.get('success_rate', 0) for e in efficiency.values()) / len(efficiency)
            synthesis['efficiency_insights'].append({
                'metric': 'Average Success Rate',
                'value': avg_success_rate,
                'interpretation': self._interpret_success_rate(avg_success_rate),
            })
        
        # Recommendations
        assessment = analysis_results.get('phase6', {})
        if assessment.get('missing_years'):
            synthesis['recommendations'].append({
                'type': 'data_completeness',
                'priority': 'high',
                'text': f"Pozyskać brakujące raporty dla lat: {', '.join(map(str, assessment['missing_years']))}",
            })
        
        if assessment.get('consistency_issues'):
            synthesis['recommendations'].append({
                'type': 'data_quality',
                'priority': 'medium',
                'text': f"Zweryfikować {len(assessment['consistency_issues'])} znalezionych niespójności w danych",
            })
        
        # Generate executive summary
        synthesis['executive_summary'] = self._generate_executive_summary(synthesis)
        
        return synthesis
    
    def _interpret_success_rate(self, rate: float) -> str:
        """Interpret success rate"""
        if rate >= 50:
            return "Bardzo wysoka skuteczność"
        elif rate >= 30:
            return "Wysoka skuteczność"
        elif rate >= 15:
            return "Średnia skuteczność"
        else:
            return "Niska skuteczność"
    
    def _generate_executive_summary(self, synthesis: Dict[str, Any]) -> str:
        """Generate executive summary"""
        summary_parts = []
        
        # Key findings
        if synthesis['key_findings']:
            summary_parts.append(f"Zidentyfikowano {len(synthesis['key_findings'])} kluczowych trendów.")
        
        # Efficiency
        if synthesis['efficiency_insights']:
            summary_parts.append("Analiza efektywności ujawniła kluczowe metryki wydajności.")
        
        # Recommendations
        if synthesis['recommendations']:
            summary_parts.append(f"Sformułowano {len(synthesis['recommendations'])} rekomendacji.")
        
        return " ".join(summary_parts) if summary_parts else "Analiza przeprowadzona zgodnie z metodologią 7 faz."
```

---

## 🔗 INTEGRACJA Z AUTONOMOUS ORCHESTRATOR

### Modyfikacja AutonomousOrchestrator

**Plik:** `src/autonomous/autonomous_orchestrator.py`

```python
# Add import
from src.analysis.professional_analyzer import ProfessionalAnalyzer, AnalysisConfig

class AutonomousOrchestrator:
    def __init__(self, enable_investigative: bool = True):
        # ... existing code ...
        
        # NEW: Professional Analyzer
        self.professional_analyzer = ProfessionalAnalyzer(
            config=AnalysisConfig(
                enable_structure_analysis=True,
                enable_quantitative_extraction=True,
                enable_qualitative_analysis=True,
                enable_temporal_trends=True,
                enable_comparative_analysis=True,
                enable_critical_assessment=True,
                enable_synthesis=True,
            )
        )
    
    def _execute_investigative_task(self, case_id: str, task: Dict[str, Any], 
                                    investigation_type: str) -> Dict[str, Any]:
        """Execute task using investigative team"""
        
        # STEP 1: Extract documents
        file_paths = task['files'][:5]
        documents = []
        
        for file_path in file_paths:
            # Parse document
            parse_result = self._extract_content_from_file(file_path)
            if parse_result.success:
                year = self._extract_year(file_path)
                documents.append({
                    'filename': Path(file_path).name,
                    'text': parse_result.text,
                    'year': year,
                    'path': file_path,
                })
        
        # STEP 2: Professional Analysis (7 phases)
        print(f"   🔍 Running Professional Analysis (7 phases)...")
        professional_results = self.professional_analyzer.analyze(documents)
        
        # STEP 3: Use LLM for synthesis (with extracted data)
        llm_prompt = self._build_llm_prompt_with_data(professional_results, documents)
        
        # STEP 4: Investigative Team Analysis
        investigation_results = self.investigative_team.investigate(
            subject=f"Case {case_id}",
            investigation_type=investigation_type,
            priority="high"
        )
        
        # STEP 5: Combine professional analysis + investigative insights
        combined_results = self._combine_results(professional_results, investigation_results)
        
        return {
            'task': task,
            'professional_analysis': professional_results,
            'investigative_analysis': investigation_results,
            'combined': combined_results,
        }
    
    def _build_llm_prompt_with_data(self, professional_results: Dict, documents: List[Dict]) -> str:
        """Build LLM prompt with extracted data"""
        
        prompt = """Przeanalizuj następujące ZWERYFIKOWANE dane z raportów CBA:

"""
        
        # Add extracted quantitative data
        metrics = professional_results.get('phase2', {}).get('metrics', {})
        if metrics:
            prompt += "=== WYEKSTRAHOWANE DANE LICZBOWE ===\n\n"
            for year in sorted(metrics.keys()):
                prompt += f"Rok {year}:\n"
                for metric_name, metric_data in metrics[year].items():
                    value = metric_data.get('value')
                    if value is not None:
                        prompt += f"  - {metric_name}: {value} ✅\n"
                prompt += "\n"
        
        # Add trends
        trends = professional_results.get('phase4', {}).get('trends', {})
        if trends:
            prompt += "\n=== TRENDY TEMPORALNE ===\n\n"
            for metric_name, trend_data in trends.items():
                prompt += f"{metric_name}: {trend_data['trend']} ({trend_data.get('total_growth', 0):.1f}%)\n"
        
        prompt += """
WAŻNE:
- Nie generuj nowych liczb ani danych
- Analizuj TYLKO podane wyekstrahowane dane
- Jeśli brakuje danych, oznacz jako "[BRAK DANYCH]"
- Wszystkie wnioski powinny bazować na podanych danych

Zadania:
1. Przeanalizuj trendy w podanych danych
2. Zidentyfikuj kluczowe zmiany w czasie
3. Sformułuj wnioski strategiczne
4. Wskaż obszary wymagające uwagi
"""
        
        return prompt
```

---

## 🎯 LLM PROMPT ENGINEERING

### Template dla LLM Analysis

**Plik:** `src/analysis/llm_prompts.py`

```python
"""
LLM Prompt Templates for Professional Analysis
"""

PROFESSIONAL_ANALYSIS_PROMPT = """
Jesteś profesjonalnym analitykiem raportów instytucjonalnych.

Dostarczono Ci następujące ZWERYFIKOWANE dane z raportów CBA:

{extracted_data}

TRENDY TEMPORALNE:
{trends}

ANALIZA STRUKTURY:
{structure_analysis}

ANALIZA JAKOŚCIOWA:
{qualitative_analysis}

ZADANIA:

1. ANALIZA TRENDÓW:
   - Przeanalizuj zmiany w czasie dla każdej metryki
   - Zidentyfikuj punkty zwrotne i anomalie
   - Wyjaśnij możliwe przyczyny zmian

2. ANALIZA EFEKTYWNOŚCI:
   - Oblicz i przeanalizuj metryki efektywności (success rate, cost per case)
   - Porównaj efektywność między okresami
   - Zidentyfikuj obszary do poprawy

3. WNIOSKI STRATEGICZNE:
   - Sformułuj główne wnioski z analizy
   - Zidentyfikuj trendy strategiczne
   - Wskaż kluczowe osiągnięcia i wyzwania

4. REKOMENDACJE:
   - Rekomendacje operacyjne (krótkoterminowe)
   - Rekomendacje strategiczne (długoterminowe)
   - Priorytety działania

WAŻNE ZASADY:
- Nie generuj nowych liczb - użyj TYLKO podanych danych
- Jeśli brakuje danych, oznacz jako "[BRAK DANYCH]"
- Wszystkie liczby powinny mieć źródło (rok, dokument)
- Bądź krytyczny - kwestionuj dane jeśli są niespójne
- Formułuj wnioski oparte na dowodach

Format odpowiedzi:
- Executive Summary (2-3 akapity)
- Analiza Trendów (szczegółowa)
- Analiza Efektywności
- Wnioski Strategiczne
- Rekomendacje
"""

SYNTHESIS_PROMPT = """
Syntezuj następujące wyniki analizy profesjonalnej:

STRUKTURA: {structure}
DANE ILOŚCIOWE: {quantitative}
ANALIZA JAKOŚCIOWA: {qualitative}
TRENDY: {trends}
PORÓWNAWCZA: {comparative}
OCENA KRYTYCZNA: {critical}

Stwórz spójny raport analityczny zawierający:
1. Executive Summary
2. Kluczowe Ustalenia
3. Trendy Strategiczne
4. Analiza Efektywności
5. Wnioski i Rekomendacje
"""
```

---

## 📊 DATA EXTRACTION PIPELINE

### Enhanced PDF Parsing

**Plik:** `src/parsing/enhanced_pdf_parser.py`

```python
"""
Enhanced PDF Parser with Table Extraction
"""

import camelot
import pdfplumber
from typing import List, Dict, Any


class EnhancedPDFParser:
    """Enhanced PDF parser with table extraction"""
    
    def parse_with_tables(self, pdf_path: str) -> Dict[str, Any]:
        """Parse PDF with table extraction"""
        
        result = {
            'text': '',
            'tables': [],
            'metadata': {},
        }
        
        # Method 1: Extract text
        text = self._extract_text(pdf_path)
        result['text'] = text
        
        # Method 2: Extract tables (camelot - best for text-based tables)
        try:
            camelot_tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
            for table in camelot_tables:
                result['tables'].append({
                    'method': 'camelot',
                    'page': table.page,
                    'data': table.df.to_dict('records'),
                    'accuracy': table.accuracy,
                })
        except Exception as e:
            print(f"Camelot extraction failed: {e}")
        
        # Method 3: Extract tables (pdfplumber - fallback)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        result['tables'].append({
                            'method': 'pdfplumber',
                            'page': page_num + 1,
                            'data': table,
                        })
        except Exception as e:
            print(f"PDFPlumber extraction failed: {e}")
        
        return result
    
    def extract_structured_metrics(self, pdf_path: str) -> Dict[str, Any]:
        """Extract structured metrics from PDF tables"""
        
        result = self.parse_with_tables(pdf_path)
        metrics = {}
        
        # Search tables for key metrics
        for table in result['tables']:
            table_data = table.get('data', [])
            
            # Look for CBA-specific metrics in tables
            for row in table_data:
                if isinstance(row, dict):
                    # Check row keys/values for metric names
                    for key, value in row.items():
                        if 'spraw' in str(key).lower() and isinstance(value, (int, float)):
                            metrics['sprawy_operacyjne'] = int(value)
                        elif 'budżet' in str(key).lower() and isinstance(value, (int, float)):
                            metrics['budzet'] = int(value)
                        # ... more patterns
        
        return metrics
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### Phase 1: Core Components (Week 1)

- [ ] **ProfessionalAnalyzer class**
  - [ ] Structure Extractor
  - [ ] Quantitative Extractor
  - [ ] Qualitative Analyzer
  - [ ] Temporal Trend Analyzer
  - [ ] Comparative Analyzer
  - [ ] Critical Assessor
  - [ ] Synthesis Engine

- [ ] **Integration with AutonomousOrchestrator**
  - [ ] Add ProfessionalAnalyzer to __init__
  - [ ] Modify _execute_investigative_task
  - [ ] Build LLM prompts with extracted data

- [ ] **Testing**
  - [ ] Unit tests for each extractor
  - [ ] Integration test with CBA documents
  - [ ] Validation of extracted metrics

### Phase 2: Enhanced Extraction (Week 2)

- [ ] **PDF Table Parsing**
  - [ ] Install camelot-py, pdfplumber
  - [ ] Implement EnhancedPDFParser
  - [ ] Extract structured data from tables

- [ ] **Data Validation**
  - [ ] Cross-validation between sources
  - [ ] Consistency checks
  - [ ] Confidence scoring

- [ ] **Source Citation**
  - [ ] Track sources for each metric
  - [ ] Generate citations
  - [ ] Integrate with reports

### Phase 3: LLM Integration (Week 2-3)

- [ ] **Prompt Engineering**
  - [ ] Professional analysis prompts
  - [ ] Evidence-based prompts
  - [ ] Synthesis prompts

- [ ] **LLM Analysis Layer**
  - [ ] Context-aware analysis
  - [ ] Multi-step reasoning
  - [ ] Synthesis generation

### Phase 4: Report Generation (Week 3)

- [ ] **Professional Report Templates**
  - [ ] Executive Summary template
  - [ ] Detailed analysis template
  - [ ] Recommendations template

- [ ] **Visualization**
  - [ ] Trend charts
  - [ ] Comparison charts
  - [ ] Efficiency metrics

---

## 📋 DEPENDENCIES

### Python Packages

```bash
# Enhanced PDF parsing
pip install camelot-py[cv] tabula-py pdfplumber

# Statistical analysis
pip install numpy scipy pandas

# Optional: Visualization
pip install matplotlib plotly
```

### System Dependencies

```bash
# macOS
brew install tesseract poppler ghostscript

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils ghostscript
```

---

## 🎓 LEARNING FROM EXAMPLES

### Training Data Structure

**Plik:** `training_data/cba_analysis_examples.json`

```json
{
  "examples": [
    {
      "input": {
        "documents": [...],
        "extracted_data": {...}
      },
      "output": {
        "professional_analysis": {...},
        "key_findings": [...],
        "recommendations": [...]
      },
      "metadata": {
        "analysis_type": "cba_reports",
        "year_range": "2008-2024"
      }
    }
  ]
}
```

### Fine-tuning Approach

1. **Collect Examples:**
   - 10-20 profesjonalnych analiz CBA
   - Przykłady innych typów dokumentów
   - Manual annotations

2. **Train Model:**
   - Fine-tune LLM na przykładach
   - Specialized model dla analizy dokumentów
   - Evaluation na test set

3. **Deploy:**
   - Integrate fine-tuned model
   - A/B testing vs. base model
   - Continuous improvement

---

## 📊 METRYKI SUKCESU

### Quality Metrics

| Metryka | Cel | Pomiar |
|---------|-----|--------|
| **Precyzja ekstrakcji** | >90% | Porównanie z manual extraction |
| **Pokrycie metryk** | >80% | % lat z wyekstrahowanymi danymi |
| **Weryfikowalność** | 100% | Wszystkie liczby mają źródło |
| **Redukcja halucynacji** | 100% | Zero wymyślonych liczb |
| **Jakość wniosków** | High | Expert review |

### Performance Metrics

| Metryka | Cel | Pomiar |
|---------|-----|--------|
| **Czas analizy** | <5 min | Per document set |
| **Przetwarzanie** | >10 docs/min | Throughput |
| **Zużycie LLM** | Minimal | Token usage |

---

## 🎯 QUICK START GUIDE

### Step 1: Install Dependencies

```bash
# Python packages
pip install camelot-py[cv] pdfplumber numpy scipy

# System dependencies (macOS)
brew install tesseract poppler ghostscript
```

### Step 2: Implement Core Components

```bash
# Create directory structure
mkdir -p src/analysis

# Create files:
# - src/analysis/professional_analyzer.py
# - src/analysis/structure_extractor.py
# - src/analysis/quantitative_extractor.py
# - src/analysis/qualitative_analyzer.py
# - src/analysis/temporal_trend_analyzer.py
# - src/analysis/comparative_analyzer.py
# - src/analysis/critical_assessor.py
# - src/analysis/synthesis_engine.py
```

### Step 3: Integrate with Orchestrator

```python
# Modify src/autonomous/autonomous_orchestrator.py
from src.analysis.professional_analyzer import ProfessionalAnalyzer

class AutonomousOrchestrator:
    def __init__(self):
        # ... existing code ...
        self.professional_analyzer = ProfessionalAnalyzer()
```

### Step 4: Test

```bash
# Test on CBA documents
python destiny_auto.py testdocsLLM/ --case-id cba_professional_test
```

---

## 💡 BEST PRACTICES

### 1. Data Extraction First

**Zasada:** Ekstrahuj dane PRZED analizą LLM

```python
# ✅ GOOD: Extract first, then analyze
extracted_data = extractor.extract(pdf_path)
analysis = llm.analyze(extracted_data)

# ❌ BAD: Let LLM extract from raw text
analysis = llm.analyze(raw_text)  # Will hallucinate!
```

### 2. Source Attribution

**Zasada:** Każda liczba musi mieć źródło

```python
metric = {
    'value': 1234,
    'source': 'PDF 2021, str. 15, tabela 2',
    'confidence': 'verified',
    'extraction_method': 'table_parser'
}
```

### 3. Confidence Marking

**Zasada:** Oznacz niepewność

```python
# ✅ GOOD
value = {
    'value': 1234,
    'confidence': 'extracted',  # ✅ Verified
    'marker': '✅'
}

# ⚠️ WARNING
value = {
    'value': 1234,
    'confidence': 'estimated',  # ⚠️ LLM estimate
    'marker': '⚠️'
}

# ❌ MISSING
value = {
    'value': None,
    'confidence': 'missing',  # ❌ No data
    'marker': '❌'
}
```

### 4. Validation Layer

**Zasada:** Waliduj przed użyciem

```python
# Validate extracted data
validation = validator.validate(extracted_data)

if validation['confidence'] < 0.7:
    # Flag for manual review
    flag_for_review(extracted_data)
```

---

## 🎓 CONTINUOUS LEARNING

### Feedback Loop

```
1. System extracts data
2. Human reviews results
3. Identify errors/improvements
4. Update patterns/extractors
5. Retrain if needed
6. Deploy improved version
```

### Pattern Refinement

**Process:**
1. Start with basic regex patterns
2. Test on real documents
3. Identify false positives/negatives
4. Refine patterns
5. Add domain-specific patterns
6. Iterate

### Model Fine-tuning

**Approach:**
1. Collect professional analyses
2. Create training dataset
3. Fine-tune LLM
4. Evaluate on test set
5. Deploy and monitor

---

## 📋 SUMMARY: IMPLEMENTATION ROADMAP

### Week 1: Core Analysis Engine
- ✅ ProfessionalAnalyzer class
- ✅ All 7 phase extractors
- ✅ Integration with Orchestrator
- ✅ Basic testing

### Week 2: Enhanced Extraction
- ✅ PDF table parsing
- ✅ Data validation
- ✅ Source citation
- ✅ Confidence marking

### Week 3: LLM Integration & Reports
- ✅ Professional prompts
- ✅ LLM analysis layer
- ✅ Report generation
- ✅ Visualization

### Week 4: Testing & Refinement
- ✅ Comprehensive testing
- ✅ Pattern refinement
- ✅ Performance optimization
- ✅ Documentation

---

**Przygotowane przez:** System Architecture Team  
**Data:** 2024-11-05  
**Status:** Ready for Implementation

**Następne kroki:**
1. Review architecture
2. Implement core components
3. Test on CBA documents
4. Iterate and improve
