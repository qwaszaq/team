# 📚 SOURCE ATTRIBUTION PROTOCOL - Mandatory for All Investigations

**Status:** 🔴 MANDATORY - NO EXCEPTIONS  
**Applies to:** ALL Investigative & Research Agents  
**Standard:** Bellingcat-level source documentation  
**Date:** 2025-11-04  
**Version:** 1.0  

---

## 🎯 Core Principle

**EVERY CLAIM MUST HAVE A SOURCE.**

No exceptions. No "I think" or "probably" or "it seems".

**If you can't cite a source, DON'T make the claim.**

---

## ⚖️ Why This Matters

### **1. Credibility**
Without sources, we're just opinions.  
With sources, we're evidence-based intelligence.

### **2. Verification**
Others must be able to verify our findings.  
Sources make this possible.

### **3. Reproducibility**
Science requires reproducibility.  
Investigations do too.

### **4. Legal Protection**
Court cases require evidence chain.  
Sources provide this.

### **5. Bellingcat Standard**
World-class investigations cite everything.  
We meet world-class standards.

---

## 📋 MANDATORY RULES

### **Rule 1: Every Fact Needs a Source**

**❌ WRONG:**
```
The company has 500 employees.
```

**✅ CORRECT:**
```
The company has 500 employees (Source: LinkedIn company page, 
accessed 2025-11-04, archived: https://archive.org/...)
```

---

### **Rule 2: Every Source Needs Full Citation**

**Minimum Required Information:**
- [ ] Source name/title
- [ ] URL (if online)
- [ ] Access date
- [ ] Archive link (CRITICAL!)
- [ ] Relevant quote/excerpt
- [ ] Page number (if document)

**❌ WRONG:**
```
According to the report, sales increased.
```

**✅ CORRECT:**
```
According to the Q3 2025 Financial Report (Source: 
company.com/reports/q3-2025.pdf, accessed 2025-11-04, 
archived: https://archive.org/..., page 12, "Sales increased 
by 15% year-over-year")
```

---

### **Rule 3: Archive Everything Immediately**

**Content disappears. Always archive.**

**Required:**
- [ ] Wayback Machine (archive.org)
- [ ] Archive.today
- [ ] Local copy (screenshot + HTML)
- [ ] Document timestamp

**Tools:**
```python
# Use ScrapingToolkit
from agents.analytical.tools.scraping_toolkit import ScrapingToolkit

toolkit = ScrapingToolkit()
archive_info = toolkit.archive_page(url)
# Returns: local path, Wayback URL, timestamp
```

---

### **Rule 4: Multiple Sources for Key Claims**

**Single source = weak**  
**2+ sources = stronger**  
**3+ sources = HIGH confidence**

**For critical findings:**
- Minimum 3 independent sources
- Different source types (not all news, not all social media)
- Cross-referenced and verified

---

### **Rule 5: Rate Source Credibility**

**Every source needs credibility assessment:**

```
Source: [Name]
URL: [Link]
Archive: [Archive link]
Credibility: [High/Medium/Low]
Reasoning: [Why this rating]
Bias: [Known biases]
Verification: [How verified]
```

**Credibility Levels:**

**HIGH:**
- Official government records
- Academic peer-reviewed studies
- Direct primary sources
- Verified firsthand accounts

**MEDIUM:**
- Reputable news organizations
- Industry reports
- Expert testimonies
- Public databases

**LOW:**
- Anonymous sources
- Social media (unverified)
- Biased sources
- Third-hand information

---

## 📝 Source Citation Templates

### **Template 1: Website/Article**

```markdown
**Source:** [Article/Page Title]
**URL:** [Full URL]
**Author:** [Author name if available]
**Publication:** [Website/Publication name]
**Date Published:** [Publication date]
**Date Accessed:** [When you accessed it]
**Archive:** [Wayback Machine URL]
**Relevant Quote:** "[Exact quote]"
**Credibility:** [High/Medium/Low]
**Notes:** [Any additional context]
```

**Example:**
```markdown
**Source:** "MH17: New Evidence Shows Russian Military Involvement"
**URL:** https://www.bellingcat.com/news/2018/05/25/mh17-russian-gru-commander-orion-identified-oleg-ivannikov/
**Author:** Bellingcat Investigation Team
**Publication:** Bellingcat
**Date Published:** 2018-05-25
**Date Accessed:** 2025-11-04
**Archive:** https://web.archive.org/web/20250101000000/...
**Relevant Quote:** "The commander, known as 'Orion', has been identified as Colonel Oleg Ivannikov of the Russian GRU"
**Credibility:** HIGH - Bellingcat verified investigation with multiple sources
**Notes:** Part of larger MH17 investigation series
```

---

### **Template 2: Document (PDF, Report)**

```markdown
**Source:** [Document Title]
**Type:** [Report/Study/Filing/etc.]
**Author/Organization:** [Who created it]
**Date:** [Publication date]
**URL:** [Link to document]
**Archive:** [Archive link]
**Page Reference:** [Specific pages]
**Relevant Excerpt:** "[Quote from document]"
**Credibility:** [High/Medium/Low]
**Verification:** [How authenticity verified]
```

---

### **Template 3: Social Media Post**

```markdown
**Source:** Social Media Post
**Platform:** [Twitter/Facebook/Telegram/etc.]
**Username:** [@username]
**Profile URL:** [Link to profile]
**Post URL:** [Direct link to post]
**Date Posted:** [When posted]
**Date Accessed:** [When you accessed]
**Archive:** [Archive link - CRITICAL!]
**Screenshot:** [Path to screenshot]
**Content:** "[Full text of post]"
**Verification:** [Account verified? Cross-checked?]
**Credibility:** [Assessment]
**Context:** [Why this source matters]
```

**⚠️ CRITICAL for social media:**
- Archive IMMEDIATELY (content deletes fast!)
- Screenshot with timestamp visible
- Check account verification
- Look for coordinated campaigns
- Verify with other sources

---

### **Template 4: Database/API**

```markdown
**Source:** [Database Name]
**Type:** Database/API Query
**URL:** [API endpoint or database URL]
**Query:** [Exact query used]
**Date Accessed:** [When accessed]
**Results Count:** [Number of results]
**Sample Data:** [Representative sample]
**Verification:** [How data quality verified]
**Credibility:** [Official/Unofficial]
**Notes:** [Any limitations or caveats]
```

---

### **Template 5: Interview/Personal Communication**

```markdown
**Source:** Personal Communication
**Type:** [Interview/Email/Phone/etc.]
**Person:** [Name and title]
**Organization:** [Affiliation]
**Date:** [When communication occurred]
**Method:** [How communicated]
**Recording:** [Audio/Video/Notes available?]
**Key Points:** [Summary of relevant information]
**Consent:** [Permission to cite? On/off record?]
**Credibility:** [Expert credentials verified?]
**Verification:** [How identity verified]
```

---

### **Template 6: Geolocation Evidence**

```markdown
**Source:** Geolocation Analysis
**Type:** Visual geolocation
**Image/Video URL:** [Source material]
**Location Identified:** [GPS coordinates]
**Confidence:** [High/Medium/Low]
**Matching Points:** [List of landmarks matched]
**Tools Used:** [Google Earth, Yandex Maps, etc.]
**Date of Image:** [When image was taken]
**Date of Analysis:** [When you did geolocation]
**Verification:** [How verified - shadow analysis, multiple angles, etc.]
**Archive:** [All source materials archived]
**Screenshots:** [Path to comparison screenshots]
```

---

## 🔍 Source Verification Checklist

**Before citing any source, verify:**

- [ ] **Authenticity:** Is this source real/genuine?
- [ ] **Date:** When was it created/published?
- [ ] **Author:** Who created it? Credible?
- [ ] **Context:** What's the full context?
- [ ] **Bias:** Any known biases or conflicts of interest?
- [ ] **Corroboration:** Do other sources confirm this?
- [ ] **Archive:** Is it archived? (If online)
- [ ] **Quality:** Is information reliable?
- [ ] **Relevance:** Does it actually support the claim?

---

## 📊 Source Management

### **Use ScrapingToolkit for Automatic Archiving:**

```python
from agents.analytical.tools.scraping_toolkit import ScrapingToolkit

toolkit = ScrapingToolkit()

# Archive a source
archive_info = toolkit.archive_page(url)

# Returns:
{
    'url': 'https://example.com/article',
    'archived_at': '2025-11-04T10:30:00',
    'html_file': './archives/20251104_103000_abc123.html',
    'wayback': 'https://web.archive.org/...',
    'archive_today': 'https://archive.ph/...'
}

# Use in citation:
citation = f"""
Source: {title}
URL: {archive_info['url']}
Accessed: {archive_info['archived_at']}
Archive: {archive_info['wayback']}
"""
```

---

## 📁 Source Organization

### **Create Sources Directory:**

```
investigation_name/
├── sources/
│   ├── web_archives/
│   │   ├── source_001_example_com.html
│   │   ├── source_001_screenshot.png
│   │   └── source_001_metadata.json
│   ├── documents/
│   │   ├── report_q3_2025.pdf
│   │   └── financial_statement.xlsx
│   ├── images/
│   │   ├── evidence_photo_01.jpg
│   │   └── evidence_photo_01_metadata.json
│   ├── social_media/
│   │   ├── tweet_123456_archive.html
│   │   └── tweet_123456_screenshot.png
│   └── sources_index.md  # Master list of all sources
├── analysis/
└── report/
```

---

## 📝 Source Documentation Format

**In every report, include Sources section:**

```markdown
## Sources

### Primary Sources (Direct Evidence)
1. [Source 1 - Full citation]
2. [Source 2 - Full citation]

### Secondary Sources (Supporting Evidence)
1. [Source A - Full citation]
2. [Source B - Full citation]

### Databases/APIs Accessed
1. [Database 1 - Query details]
2. [API 2 - Endpoint details]

### Interviews/Communications
1. [Interview 1 - Details]
2. [Communication 2 - Details]

### Archive Links
- All sources archived: [Master archive link]
- Archive date: [Date]
- Total sources: [Count]
```

---

## 🎯 Agent-Specific Requirements

### **Elena Volkov (OSINT Specialist)** 🔍
**MUST cite for:**
- ✅ Every social media post referenced
- ✅ Every website scraped
- ✅ Every domain lookup
- ✅ Every geolocation claim
- ✅ Every image analyzed

**Special requirements:**
- Archive social media IMMEDIATELY (deletes fast!)
- Screenshot with timestamp visible
- Metadata extraction documented
- Geolocation confidence with matched landmarks

---

### **Marcus Chen (Financial Analyst)** 💰
**MUST cite for:**
- ✅ Every financial figure
- ✅ Every SEC filing referenced
- ✅ Every company data point
- ✅ Every market analysis
- ✅ Every calculation (show formula + source data)

**Special requirements:**
- Document exact source of numbers
- Page numbers for reports
- Date of data (financial data changes)
- Calculation methodology transparent

---

### **Sofia Martinez (Market Research)** 📊
**MUST cite for:**
- ✅ Every market statistic
- ✅ Every competitor analysis
- ✅ Every trend claim
- ✅ Every survey result
- ✅ Every industry report

**Special requirements:**
- Sample size for surveys
- Methodology documentation
- Date of data collection
- Industry report credentials

---

### **Adrian Kowalski (Legal Analyst)** ⚖️
**MUST cite for:**
- ✅ Every legal case referenced
- ✅ Every statute cited
- ✅ Every regulation mentioned
- ✅ Every legal opinion
- ✅ Every precedent

**Special requirements:**
- Case citation format (standard legal)
- Jurisdiction specified
- Date of ruling/law
- Current status (still valid?)

---

### **Maya Patel (Data Analyst)** 📈
**MUST cite for:**
- ✅ Every dataset used
- ✅ Every statistical method
- ✅ Every calculation
- ✅ Every visualization (source data)
- ✅ Every analysis conclusion

**Special requirements:**
- Dataset origin and date
- Statistical method reference
- Code/formula transparency
- Raw data availability

---

### **Damian Rousseau (Critical Thinker)** 🎭
**MUST cite when challenging:**
- ✅ Alternative hypotheses (what suggests them?)
- ✅ Bias claims (what indicates bias?)
- ✅ Red flags (specific evidence)
- ✅ Contradictions (cite both sources)
- ✅ Weaknesses (specific examples)

**Special requirements:**
- Citation of both supporting and contradicting evidence
- Transparent reasoning
- Alternative explanations sourced

---

### **Viktor Kovalenko (Director)** 🎯
**MUST ensure:**
- ✅ All team members cite sources
- ✅ Source quality reviewed
- ✅ Critical claims have 3+ sources
- ✅ Archive system working
- ✅ Source list complete before publication

---

## 🚨 Consequences of Non-Compliance

### **What Happens if Sources Missing:**

**1. Work REJECTED:**
- Report sent back for revision
- Must add sources before acceptance

**2. Confidence LOWERED:**
- Unsourced claims = LOW confidence
- Cannot publish without sources

**3. Investigation DELAYED:**
- Missing sources delay completion
- Must backtrack to find sources

**4. Credibility DAMAGED:**
- Team reputation depends on sourcing
- One unsourced report damages all future work

**5. Legal RISK:**
- Court cases require evidence chain
- Unsourced claims inadmissible

---

## ✅ Quality Check Before Publication

**Before ANY report goes out, verify:**

- [ ] Every fact has a source
- [ ] Every source fully cited (all fields completed)
- [ ] All online sources archived (Wayback + local)
- [ ] Key claims have 3+ sources
- [ ] Source credibility assessed
- [ ] Sources list included in report
- [ ] Archive dates within last 7 days (for online sources)
- [ ] Screenshots taken (for social media)
- [ ] Metadata extracted and documented
- [ ] Peer reviewed (Damian checks sources)

**If ANY checkbox is unchecked → NOT READY FOR PUBLICATION**

---

## 🎓 Training & Examples

### **Good Example (Bellingcat MH17):**

```markdown
**Claim:** Buk missile launcher photographed in Donetsk on July 17, 2014

**Source 1:** Twitter post by @user123
- URL: https://twitter.com/user123/status/...
- Archived: https://web.archive.org/...
- Screenshot: evidence/twitter_buk_01.png
- Posted: 2014-07-17 14:23 UTC
- Content: Photo of Buk launcher with location metadata
- Verification: GPS coordinates in EXIF match Donetsk (48.0159°N, 37.8029°E)

**Source 2:** YouTube video
- URL: https://youtube.com/watch?v=...
- Archived: Local copy + Wayback
- Posted: 2014-07-17
- Content: Video showing same Buk from different angle
- Geolocation: Matched to Donetsk using building facades

**Source 3:** VKontakte social media post
- URL: https://vk.com/...
- Archived: Screenshot + Wayback
- Posted: 2014-07-17
- Content: User posted photo of "interesting military equipment"
- Verification: Matched same vehicle from distinctive damage pattern

**Confidence:** HIGH - 3 independent sources, geolocated, cross-verified
```

---

## 🔧 Tools for Source Management

### **1. ScrapingToolkit - Archiving**
```python
toolkit.archive_page(url)
```

### **2. MathematicalToolkit - Statistics**
```python
# When citing statistics
stats = toolkit.basic_stats(data)
citation = f"Mean: {stats['mean']} (Source: [data source], calculated using standard statistical methods)"
```

### **3. Metadata Extraction**
```python
# When citing images
from PIL import Image
from PIL.ExifTags import TAGS

exif = extract_exif(image_path)
citation = f"Image metadata: GPS {exif['GPS']}, Timestamp: {exif['DateTime']} (Source: EXIF data from original file)"
```

---

## 📚 References

**Standards We Follow:**
1. **Bellingcat Digital Forensics**
   - https://www.bellingcat.com/resources/
   - World-class source attribution

2. **Academic Citation Standards**
   - APA, MLA, Chicago for different contexts
   - Peer-reviewed publication standards

3. **Legal Evidence Standards**
   - Chain of custody
   - Authentication requirements
   - Admissibility criteria

4. **Journalistic Ethics**
   - SPJ Code of Ethics
   - Verification requirements
   - Source protection

---

## 🎯 Summary

**THE RULE:**
```
NO SOURCE = NO CLAIM
```

**THE STANDARD:**
- Every fact cited
- Every source archived
- Every claim verifiable
- Every investigation reproducible

**THE RESULT:**
- Credible intelligence
- Court-admissible evidence
- Reproducible findings
- World-class quality

---

## 📞 Questions?

**Source attribution issues:**
- Contact: Viktor Kovalenko (Investigation Director)
- Contact: Elena Volkov (OSINT - archiving expert)

**Technical help:**
- Contact: Alex Morgan (Technical Liaison)
- Tools: ScrapingToolkit documentation

**Quality review:**
- Contact: Damian Rousseau (Critical review of sources)

---

**This is NOT optional. This is MANDATORY.**

**Every agent. Every investigation. Every time.**

**Welcome to professional investigative intelligence.** 🔍📚

---

**Version:** 1.0  
**Date:** 2025-11-04  
**Status:** 🔴 MANDATORY - ACTIVE IMMEDIATELY  
**Review:** Monthly  

*This protocol will be indexed by Helena and available in all 4 databases.*
