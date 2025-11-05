#!/usr/bin/env python3
"""
Professional CBA Analysis
Pełna profesjonalna analiza raportów CBA zgodnie z metodologią 7 faz
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Optional

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

# Load extracted data
try:
    with open('/Users/artur/coursor-agents-destiny-folder/CBA_FULL_CONTENT_ANALYSIS_data.json', 'r', encoding='utf-8') as f:
        cba_data = json.load(f)
except:
    cba_data = {'documents': [], 'analysis': {}}


class ProfessionalCBAnalyzer:
    """Professional analysis following 7-phase methodology"""
    
    def __init__(self, extracted_data: Dict):
        self.data = extracted_data
        self.documents = extracted_data.get('documents', [])
        self.analysis = extracted_data.get('analysis', {})
        
    def phase1_structure_analysis(self) -> Dict:
        """Phase 1: Document Structure Analysis"""
        print("\n" + "="*80)
        print("FAZA 1: ANALIZA STRUKTURY DOKUMENTÓW")
        print("="*80)
        
        structures = {}
        
        for doc in self.documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            
            if not text or len(text) < 100:
                continue
            
            # Extract section headers (common patterns)
            sections = self._extract_sections(text[:5000])  # First 5000 chars
            
            if year:
                structures[year] = {
                    'filename': filename,
                    'sections': sections,
                    'text_length': len(text),
                }
        
        print(f"✅ Przeanalizowano struktury: {len(structures)} dokumentów")
        
        return {
            'total_documents': len(structures),
            'structures': structures,
            'common_sections': self._identify_common_sections(structures),
        }
    
    def _extract_sections(self, text: str) -> List[str]:
        """Extract section headers from text"""
        sections = []
        
        # Common patterns for CBA reports
        patterns = [
            r'(?:Rozdział|ROZDZIAŁ|Dział|DZIAŁ)\s+[IVX\d]+[\.\)]?\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
            r'^\s*([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{5,50})\s*$',
            r'[0-9]+\.\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            sections.extend(matches)
        
        return sections[:15]  # Top 15 sections
    
    def _identify_common_sections(self, structures: Dict) -> List[str]:
        """Identify sections common across documents"""
        all_sections = []
        for struct in structures.values():
            all_sections.extend(struct.get('sections', []))
        
        # Count frequency
        section_counts = defaultdict(int)
        for section in all_sections:
            section_counts[section.lower().strip()] += 1
        
        # Return most common
        common = sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in common[:20]]
    
    def phase2_quantitative_extraction(self) -> Dict:
        """Phase 2: Quantitative Data Extraction"""
        print("\n" + "="*80)
        print("FAZA 2: EKSTRAKCJA DANYCH ILOŚCIOWYCH")
        print("="*80)
        
        metrics = {}
        
        # Patterns for key metrics
        patterns = {
            'sprawy_operacyjne': [
                r'spraw[^.]*operacyjn[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+spraw[^.]*operacyjn',
                r'wszczęto\s+(\d{1,4})\s+spraw',
            ],
            'sprawy_zakończone': [
                r'zakończon[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zakończon',
            ],
            'zatrzymania': [
                r'zatrzyman[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zatrzymań',
            ],
            'skazania': [
                r'skazan[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+skazań',
            ],
            'budzet': [
                r'budżet[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)[^.]*budżet',
            ],
            'funkcjonariusze': [
                r'funkcjonariusz[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+funkcjonariusz',
            ],
        }
        
        for doc in self.documents:
            year = doc.get('year')
            text = doc.get('text', '')
            
            if not year or not text:
                continue
            
            year_metrics = {}
            
            for metric_name, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        try:
                            # Take first match, clean it
                            value = matches[0]
                            if isinstance(value, tuple):
                                value = value[0]
                            
                            # Clean number (remove spaces)
                            value = value.replace(' ', '').replace(',', '')
                            numeric_value = int(value)
                            
                            if metric_name == 'budzet' and numeric_value < 1000:
                                # Probably in millions, multiply
                                numeric_value = numeric_value * 1000000
                            
                            year_metrics[metric_name] = numeric_value
                            break
                        except:
                            continue
            
            if year_metrics:
                metrics[year] = year_metrics
        
        print(f"✅ Wyekstrahowano metryki dla {len(metrics)} lat")
        
        return metrics
    
    def phase3_qualitative_analysis(self) -> Dict:
        """Phase 3: Qualitative Analysis"""
        print("\n" + "="*80)
        print("FAZA 3: ANALIZA JAKOŚCIOWA")
        print("="*80)
        
        narrative_analysis = {}
        
        for doc in self.documents:
            year = doc.get('year')
            text = doc.get('text', '')
            
            if not year or not text:
                continue
            
            # Analyze tone and language
            tone_indicators = {
                'positive': len(re.findall(r'sukces|osiągnięci|efektywn|poprawa', text, re.IGNORECASE)),
                'challenge': len(re.findall(r'wyzwani|trudności|problem|ograniczen', text, re.IGNORECASE)),
                'cooperation': len(re.findall(r'współprac|kooperacj|partnerstw', text, re.IGNORECASE)),
                'innovation': len(re.findall(r'nowoczesn|innowacj|rozwój|modernizacj', text, re.IGNORECASE)),
            }
            
            # Key themes
            themes = {
                'korupcja': len(re.findall(r'korupcj|łapówk|przekup', text, re.IGNORECASE)),
                'współpraca_międzynarodowa': len(re.findall(r'międzynarodow|europejsk|unij', text, re.IGNORECASE)),
                'szkolenia': len(re.findall(r'szkoleni|kurs|edukacj|trening', text, re.IGNORECASE)),
                'technologia': len(re.findall(r'technolog|cyfrow|system informatyczn|IT', text, re.IGNORECASE)),
            }
            
            narrative_analysis[year] = {
                'tone': tone_indicators,
                'themes': themes,
                'dominant_tone': max(tone_indicators.items(), key=lambda x: x[1])[0] if tone_indicators else None,
                'dominant_theme': max(themes.items(), key=lambda x: x[1])[0] if themes else None,
            }
        
        print(f"✅ Przeanalizowano narrację dla {len(narrative_analysis)} lat")
        
        return narrative_analysis
    
    def phase4_temporal_trends(self, metrics: Dict) -> Dict:
        """Phase 4: Temporal Trend Analysis"""
        print("\n" + "="*80)
        print("FAZA 4: ANALIZA TRENDÓW TEMPORALNYCH")
        print("="*80)
        
        if not metrics:
            return {}
        
        trends = {}
        
        # For each metric, calculate trends
        for metric_name in ['sprawy_operacyjne', 'zatrzymania', 'skazania', 'budzet']:
            values = []
            years = []
            
            for year in sorted(metrics.keys()):
                if metric_name in metrics[year]:
                    values.append(metrics[year][metric_name])
                    years.append(year)
            
            if len(values) >= 2:
                # Calculate trend
                first_value = values[0]
                last_value = values[-1]
                growth = ((last_value - first_value) / first_value * 100) if first_value > 0 else 0
                
                # Calculate CAGR
                if len(years) > 1:
                    years_diff = years[-1] - years[0]
                    if years_diff > 0:
                        cagr = (((last_value / first_value) ** (1 / years_diff)) - 1) * 100
                    else:
                        cagr = 0
                else:
                    cagr = 0
                
                trends[metric_name] = {
                    'years': years,
                    'values': values,
                    'first_value': first_value,
                    'last_value': last_value,
                    'total_growth': growth,
                    'cagr': cagr,
                    'trend': 'increasing' if growth > 0 else 'decreasing' if growth < 0 else 'stable',
                }
        
        print(f"✅ Przeanalizowano trendy dla {len(trends)} metryk")
        
        return trends
    
    def phase5_comparative_analysis(self, metrics: Dict) -> Dict:
        """Phase 5: Comparative & Contextual Analysis"""
        print("\n" + "="*80)
        print("FAZA 5: ANALIZA PORÓWNAWCZA")
        print("="*80)
        
        comparative = {
            'efficiency_metrics': {},
            'periods': {},
        }
        
        # Calculate efficiency metrics
        for year in sorted(metrics.keys()):
            year_data = metrics[year]
            
            # Success rate
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne']
                skazania = year_data['skazania']
                if sprawy > 0:
                    success_rate = (skazania / sprawy) * 100
                    comparative['efficiency_metrics'][year] = {
                        'success_rate': success_rate,
                        'cases': sprawy,
                        'convictions': skazania,
                    }
            
            # Budget efficiency
            if 'budzet' in year_data and 'sprawy_operacyjne' in year_data:
                budzet = year_data['budzet']
                sprawy = year_data['sprawy_operacyjne']
                if sprawy > 0:
                    cost_per_case = budzet / sprawy
                    comparative['efficiency_metrics'][year] = comparative['efficiency_metrics'].get(year, {})
                    comparative['efficiency_metrics'][year]['cost_per_case'] = cost_per_case
        
        # Periodization
        years = sorted(metrics.keys())
        if len(years) >= 6:
            mid_point = len(years) // 2
            comparative['periods'] = {
                'early': years[:mid_point],
                'recent': years[mid_point:],
            }
        
        print(f"✅ Przeanalizowano efektywność dla {len(comparative['efficiency_metrics'])} lat")
        
        return comparative
    
    def phase6_critical_assessment(self, metrics: Dict) -> Dict:
        """Phase 6: Critical Assessment"""
        print("\n" + "="*80)
        print("FAZA 6: OCENA KRYTYCZNA")
        print("="*80)
        
        assessment = {
            'data_completeness': {},
            'consistency_issues': [],
            'methodology_changes': [],
            'missing_years': [],
            'confidence_scores': {},
        }
        
        # Check data completeness
        all_years = set(range(2008, 2025))
        found_years = set(metrics.keys())
        missing_years = sorted(all_years - found_years)
        assessment['missing_years'] = missing_years
        
        # Check consistency
        for year in sorted(metrics.keys()):
            year_data = metrics[year]
            completeness = len([k for k in year_data.keys() if year_data[k] is not None]) / len(year_data)
            assessment['data_completeness'][year] = completeness
            
            # Check for anomalies
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne']
                skazania = year_data['skazania']
                if skazania > sprawy:
                    assessment['consistency_issues'].append({
                        'year': year,
                        'issue': f'Skazania ({skazania}) > Sprawy ({sprawy})',
                        'type': 'logical_inconsistency',
                    })
        
        print(f"✅ Ocena krytyczna: {len(assessment['consistency_issues'])} problemów znalezionych")
        
        return assessment
    
    def phase7_synthesis(self, all_results: Dict) -> Dict:
        """Phase 7: Insight Synthesis"""
        print("\n" + "="*80)
        print("FAZA 7: SYNTEZA WNIOSKÓW")
        print("="*80)
        
        synthesis = {
            'key_findings': [],
            'trends': [],
            'efficiency_insights': [],
            'recommendations': [],
        }
        
        metrics = all_results.get('phase2', {})
        trends = all_results.get('phase4', {})
        comparative = all_results.get('phase5', {})
        
        # Key findings
        if trends:
            for metric_name, trend_data in trends.items():
                if trend_data.get('trend') != 'stable':
                    synthesis['key_findings'].append({
                        'metric': metric_name,
                        'trend': trend_data['trend'],
                        'growth': trend_data.get('total_growth', 0),
                        'cagr': trend_data.get('cagr', 0),
                    })
        
        # Efficiency insights
        efficiency = comparative.get('efficiency_metrics', {})
        if efficiency:
            avg_success_rate = sum(e.get('success_rate', 0) for e in efficiency.values()) / len(efficiency)
            synthesis['efficiency_insights'].append({
                'average_success_rate': avg_success_rate,
                'trend': 'improving' if len(efficiency) > 1 else 'unknown',
            })
        
        # Recommendations
        assessment = all_results.get('phase6', {})
        if assessment.get('missing_years'):
            synthesis['recommendations'].append({
                'type': 'data_completeness',
                'text': f"Pozyskać brakujące raporty dla lat: {', '.join(map(str, assessment['missing_years']))}",
            })
        
        print(f"✅ Synteza: {len(synthesis['key_findings'])} kluczowych odkryć")
        
        return synthesis
    
    def generate_professional_report(self, output_path: str):
        """Generate comprehensive professional report"""
        print("\n" + "="*80)
        print("GENEROWANIE PROFESJONALNEGO RAPORTU")
        print("="*80)
        
        # Run all phases
        phase1 = self.phase1_structure_analysis()
        phase2 = self.phase2_quantitative_extraction()
        phase3 = self.phase3_qualitative_analysis()
        phase4 = self.phase4_temporal_trends(phase2)
        phase5 = self.phase5_comparative_analysis(phase2)
        phase6 = self.phase6_critical_assessment(phase2)
        
        all_results = {
            'phase1': phase1,
            'phase2': phase2,
            'phase3': phase3,
            'phase4': phase4,
            'phase5': phase5,
            'phase6': phase6,
        }
        
        phase7 = self.phase7_synthesis(all_results)
        all_results['phase7'] = phase7
        
        # Generate report
        report = self._build_report(all_results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Raport zapisany: {output_path}")
        
        # Save structured data
        json_path = output_path.replace('.md', '_full_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Dane zapisane: {json_path}")
        
        return output_path
    
    def _build_report(self, results: Dict) -> str:
        """Build comprehensive report"""
        
        phase1 = results['phase1']
        phase2 = results['phase2']
        phase3 = results['phase3']
        phase4 = results['phase4']
        phase5 = results['phase5']
        phase6 = results['phase6']
        phase7 = results['phase7']
        
        report = f"""# 🔍 PROFESJONALNA ANALIZA RAPORTÓW CBA
## Comprehensive Multi-Dimensional Analysis (2008-2024)

**Data Analizy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Metodologia:** 7-Phase Professional Analysis  
**Dokumenty:** {len(self.documents)} raportów CBA  
**Zakres:** 2008-2024

---

## 📊 EXECUTIVE SUMMARY

### Kluczowe Ustalenia

"""
        
        # Key findings
        for finding in phase7.get('key_findings', [])[:5]:
            metric = finding['metric'].replace('_', ' ').title()
            trend = finding['trend']
            growth = finding.get('growth', 0)
            report += f"- **{metric}**: Trend {trend} ({growth:.1f}% zmiana)\n"
        
        report += f"""

### Metryki Efektywności

"""
        
        efficiency = phase5.get('efficiency_metrics', {})
        if efficiency:
            avg_success = sum(e.get('success_rate', 0) for e in efficiency.values()) / len(efficiency)
            report += f"- **Średnia skuteczność:** {avg_success:.1f}% (skazania / sprawy)\n"
        
        report += f"""

---

## 1. ANALIZA STRUKTURY DOKUMENTÓW

### Struktura Raportów

**Wspólne sekcje (identyfikowane w dokumentach):**
"""
        
        common_sections = phase1.get('common_sections', [])
        for section in common_sections[:10]:
            report += f"- {section.title()}\n"
        
        report += f"""

### Ewolucja Struktury

**Dokumenty przeanalizowane:** {phase1['total_documents']}  
**Pokrycie czasowe:** {min(phase1['structures'].keys()) if phase1['structures'] else 'N/A'} - {max(phase1['structures'].keys()) if phase1['structures'] else 'N/A'}

---

## 2. EKSTRAKCJA DANYCH ILOŚCIOWYCH

### Kluczowe Metryki według Lat

| Rok | Sprawy Operacyjne | Zatrzymania | Skazania | Budżet (mln zł) | Funkcjonariusze |
|-----|-------------------|-------------|----------|-----------------|-----------------|
"""
        
        for year in sorted(phase2.keys()):
            data = phase2[year]
            sprawy = data.get('sprawy_operacyjne', 'N/A')
            zatrzymania = data.get('zatrzymania', 'N/A')
            skazania = data.get('skazania', 'N/A')
            budzet = data.get('budzet', 'N/A')
            if isinstance(budzet, int):
                budzet = f"{budzet/1000000:.1f}"
            funkcjonariusze = data.get('funkcjonariusze', 'N/A')
            
            report += f"| {year} | {sprawy} | {zatrzymania} | {skazania} | {budzet} | {funkcjonariusze} |\n"
        
        report += f"""

**Uwaga:** Niektóre wartości mogą być niepełne lub wymagać weryfikacji w pełnych dokumentach.

---

## 3. ANALIZA JAKOŚCIOWA

### Analiza Narracji i Tonu

**Dominujące tematy według lat:**
"""
        
        for year in sorted(phase3.keys())[-5:]:  # Last 5 years
            data = phase3[year]
            dominant_theme = data.get('dominant_theme', 'N/A')
            dominant_tone = data.get('dominant_tone', 'N/A')
            report += f"- **{year}**: {dominant_theme} (ton: {dominant_tone})\n"
        
        report += f"""

---

## 4. ANALIZA TRENDÓW TEMPORALNYCH

### Trendy Kluczowych Metryk

"""
        
        for metric_name, trend_data in phase4.items():
            metric_display = metric_name.replace('_', ' ').title()
            trend = trend_data.get('trend', 'unknown')
            growth = trend_data.get('total_growth', 0)
            cagr = trend_data.get('cagr', 0)
            
            report += f"""
#### {metric_display}

- **Trend:** {trend}
- **Całkowity wzrost:** {growth:.1f}%
- **CAGR:** {cagr:.2f}%
- **Wartość początkowa:** {trend_data.get('first_value', 'N/A')}
- **Wartość końcowa:** {trend_data.get('last_value', 'N/A')}
"""
        
        report += f"""

---

## 5. ANALIZA PORÓWNAWCZA I EFEKTYWNOŚCI

### Metryki Efektywności

| Rok | Success Rate (%) | Cost per Case (zł) |
|-----|-----------------|-------------------|
"""
        
        for year in sorted(efficiency.keys()):
            eff_data = efficiency[year]
            success_rate = eff_data.get('success_rate', 'N/A')
            cost_per_case = eff_data.get('cost_per_case', 'N/A')
            if isinstance(cost_per_case, (int, float)):
                cost_per_case = f"{cost_per_case:,.0f}"
            
            report += f"| {year} | {success_rate:.1f} | {cost_per_case} |\n" if isinstance(success_rate, (int, float)) else f"| {year} | {success_rate} | {cost_per_case} |\n"
        
        report += f"""

---

## 6. OCENA KRYTYCZNA

### Kompletność Danych

**Brakujące lata:** {', '.join(map(str, phase6.get('missing_years', [])))}

**Problemy spójności:** {len(phase6.get('consistency_issues', []))}

"""
        
        if phase6.get('consistency_issues'):
            report += "**Zidentyfikowane problemy:**\n"
            for issue in phase6['consistency_issues']:
                report += f"- {issue['year']}: {issue['issue']}\n"
        
        report += f"""

---

## 7. WNIOSKI I REKOMENDACJE

### Główne Wnioski

"""
        
        for finding in phase7.get('key_findings', []):
            metric = finding['metric'].replace('_', ' ').title()
            trend = finding['trend']
            report += f"- **{metric}** wykazuje trend **{trend}**\n"
        
        report += f"""

### Rekomendacje

"""
        
        for rec in phase7.get('recommendations', []):
            report += f"- {rec['text']}\n"
        
        report += f"""

---

## 📋 METODOLOGIA

Analiza przeprowadzona zgodnie z 7-fazową metodologią profesjonalną:

1. ✅ Analiza struktury dokumentów
2. ✅ Ekstrakcja danych ilościowych
3. ✅ Analiza jakościowa (narracja, ton)
4. ✅ Analiza trendów temporalnych
5. ✅ Analiza porównawcza i efektywności
6. ✅ Ocena krytyczna
7. ✅ Synteza wniosków

---

**Przygotowane przez:** Professional CBA Analyst  
**Metodologia:** 7-Phase Comprehensive Analysis  
**Timestamp:** {datetime.now().isoformat()}

**Uwaga:** Niniejszy raport został wygenerowany na podstawie automatycznej ekstrakcji tekstu z dokumentów PDF. Wszystkie wartości liczbowe powinny być zweryfikowane w źródłowych dokumentach.
"""
        
        return report


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("PROFESJONALNA ANALIZA CBA - 7 FAZ")
    print("="*80)
    
    analyzer = ProfessionalCBAnalyzer(cba_data)
    
    output_path = "/Users/artur/coursor-agents-destiny-folder/CBA_PROFESSIONAL_ANALYSIS_REPORT.md"
    
    analyzer.generate_professional_report(output_path)
    
    print("\n" + "="*80)
    print("✅ ANALIZA ZAKOŃCZONA!")
    print("="*80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
