# 🔴 MANDATORY PROTOCOL: SOURCE ATTRIBUTION

**TO:** ALL Investigative & Research Agents  
**FROM:** Aleksander Nowak (Orchestrator)  
**DATE:** 2025-11-04  
**PRIORITY:** 🔴 CRITICAL - IMMEDIATE COMPLIANCE REQUIRED  
**EFFECTIVE:** Immediately  

---

## 📢 ANNOUNCEMENT

**New mandatory protocol in effect: SOURCE ATTRIBUTION**

**From this moment forward:**

**EVERY claim MUST have a source.**  
**EVERY source MUST be cited.**  
**EVERY online source MUST be archived.**

**NO EXCEPTIONS.**

---

## 🎯 THE RULE

```
╔═══════════════════════════════════╗
║                                   ║
║     NO SOURCE = NO CLAIM          ║
║                                   ║
║  If you can't cite it,            ║
║  DON'T claim it.                  ║
║                                   ║
╚═══════════════════════════════════╝
```

---

## ⚖️ WHY THIS MATTERS

**1. Credibility**
- Without sources = opinions
- With sources = intelligence

**2. Verification**
- Others must verify our work
- Sources make this possible

**3. Legal Protection**
- Court cases need evidence chain
- Sources provide this

**4. Bellingcat Standard**
- World-class = cite everything
- We are world-class

---

## 📋 WHAT YOU MUST DO

### **For EVERY Fact You State:**

✅ **Cite the source**
```markdown
The company has 500 employees.
(Source: LinkedIn company page, accessed 2025-11-04, 
archived: https://archive.org/...)
```

✅ **Archive it immediately**
```python
toolkit.archive_page(url)  # Automatic archiving!
```

✅ **Assess credibility**
```
Credibility: HIGH - Official source, verified
```

### **For Key Claims:**

✅ **Minimum 3 independent sources**
- Not all from same type
- Cross-verified
- Different perspectives

---

## 🛠️ TOOLS PROVIDED

**1. Scraping Toolkit - Automatic Archiving**
```python
from agents.analytical.tools.scraping_toolkit import ScrapingToolkit

toolkit = ScrapingToolkit()
archive = toolkit.archive_page(url)

# Returns:
# - Local HTML copy
# - Wayback Machine URL
# - Archive.today URL
# - Timestamp
```

**2. Citation Templates**
- 6 templates provided (web, document, social media, etc.)
- See: `docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md`

**3. Quick Reference Card**
- `SOURCE_CITATION_QUICK_REFERENCE.md`
- Keep this open while working!

---

## 📊 AGENT-SPECIFIC REQUIREMENTS

### **Elena Volkov (OSINT)** 🔍
**MUST cite:**
- Every social media post
- Every website
- Every geolocation (with matched landmarks)
- Every image (with metadata)

**Special:** Archive social media IMMEDIATELY (deletes fast!)

---

### **Marcus Chen (Financial)** 💰
**MUST cite:**
- Every financial figure (with page number)
- Every SEC filing
- Every calculation (formula + source data)

---

### **Sofia Martinez (Market Research)** 📊
**MUST cite:**
- Every statistic (with sample size)
- Every survey result (with methodology)
- Every trend claim

---

### **Adrian Kowalski (Legal)** ⚖️
**MUST cite:**
- Every case (standard legal citation)
- Every statute (with jurisdiction)
- Every regulation (with date)

---

### **Maya Patel (Data Analyst)** 📈
**MUST cite:**
- Every dataset (origin + date)
- Every method (statistical references)
- Every visualization (source data)

---

### **Damian Rousseau (Critical Thinker)** 🎭
**MUST cite:**
- Sources supporting your challenge
- Sources contradicting team's claim
- Evidence for alternative hypotheses

**NEW ROLE:** You verify ALL sources before publication

---

### **Viktor Kovalenko (Director)** 🎯
**MUST ensure:**
- All team members comply
- Sources reviewed before publication
- Archive system operational
- Quality standards met

---

## 🚨 ENFORCEMENT

### **What Happens if Sources Missing:**

**1. Work REJECTED**
- Sent back for revision
- Must add sources

**2. Investigation PAUSED**
- Cannot proceed without sources
- Timeline delayed

**3. Publication BLOCKED**
- Nothing published without sources
- NO exceptions

**4. Credibility RISK**
- Our reputation depends on this
- One failure damages all

---

## ✅ PUBLICATION CHECKLIST

**Before ANYTHING goes out:**

- [ ] Every fact has source
- [ ] Every source fully cited
- [ ] All online sources archived (within 7 days)
- [ ] Key claims have 3+ sources
- [ ] Credibility assessed
- [ ] Sources list included
- [ ] Screenshots taken (social media)
- [ ] Damian reviewed sources
- [ ] Viktor approved

**If ANY box unchecked → NOT READY**

---

## 📚 DOCUMENTATION

**Full Protocol:**
`docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md`
- Complete rules
- Citation templates
- Examples
- Best practices

**Quick Reference:**
`SOURCE_CITATION_QUICK_REFERENCE.md`
- One-page summary
- Keep open while working

**Capabilities Registry:**
`capabilities_registry.py`
- Protocol registered
- Enforcement tracked

---

## 🎓 TRAINING REQUIRED

**All agents MUST:**

1. ✅ Read full protocol (30 min)
2. ✅ Review citation templates (15 min)
3. ✅ Practice with scraping toolkit (30 min)
4. ✅ Complete sample citation (15 min)
5. ✅ Acknowledge compliance

**Deadline:** End of day (2025-11-04)

---

## 📞 SUPPORT

**Questions about protocol:**
- Viktor Kovalenko (Investigation Director)

**Technical archiving help:**
- Elena Volkov (OSINT Specialist)
- Alex Morgan (Technical Liaison)

**Citation format questions:**
- Adrian Kowalski (Legal format)
- Lucas Rivera (Report formatting)

**Source quality review:**
- Damian Rousseau (Critical review)

---

## 🎯 EXAMPLES

### **❌ WRONG - No Source**
```
The company employs 500 people and had revenue of $10M last year.
```

### **✅ CORRECT - Properly Sourced**
```
The company employs 500 people (Source: LinkedIn company page, 
accessed 2025-11-04, archived: https://web.archive.org/..., 
Credibility: HIGH - official company profile) and had revenue 
of $10M last year (Source: SEC 10-K Filing 2024, page 12, 
accessed 2025-11-04, archived: https://web.archive.org/..., 
exact quote: "Total revenue for fiscal year 2024: $10,247,893", 
Credibility: HIGH - official SEC filing).
```

---

### **❌ WRONG - Weak Source**
```
According to sources, the meeting happened in Warsaw.
```

### **✅ CORRECT - Strong Sources**
```
The meeting occurred in Warsaw on 2024-10-15:

Source 1: Social media post by attendee @user123
- URL: https://twitter.com/user123/status/...
- Posted: 2024-10-15 14:30 UTC
- Archived: https://archive.org/...
- Quote: "Great meeting in Warsaw today"
- Geotagged: Warsaw (52.2297°N, 21.0122°E)
- Credibility: MEDIUM - verified account, geotag confirmed

Source 2: Hotel conference booking
- Source: Hotel website event calendar
- URL: https://hotel.com/events/...
- Archived: https://archive.org/...
- Date: 2024-10-15
- Credibility: HIGH - official hotel record

Source 3: News article
- Publication: Local Business News
- URL: https://news.com/article...
- Date: 2024-10-16
- Archived: https://archive.org/...
- Quote: "Yesterday's conference in Warsaw..."
- Credibility: HIGH - reputable publication

Confidence: HIGH - 3 independent sources, cross-verified
```

---

## 🔄 FEEDBACK LOOP

**After 1 Week:**
- Team meeting to discuss challenges
- Adjust templates if needed
- Share best practices

**After 1 Month:**
- Review compliance
- Celebrate good examples
- Additional training if needed

---

## 🎯 SUCCESS METRICS

**We'll know this is working when:**

1. ✅ 100% of published work has complete sources
2. ✅ Damian approves all source lists
3. ✅ Archives are up to date
4. ✅ Peer reviews pass first time
5. ✅ External validators can verify our work
6. ✅ Legal team approves evidence chain
7. ✅ Bellingcat would approve our methodology

---

## 💬 ACKNOWLEDGMENT REQUIRED

**Each agent must confirm:**

```
I, [Agent Name], acknowledge that:

1. I have read the Source Attribution Protocol
2. I understand the requirement: NO SOURCE = NO CLAIM
3. I will cite every fact with complete sources
4. I will archive all online sources immediately
5. I will ensure key claims have 3+ sources
6. I understand work will be rejected if sources missing
7. I commit to maintaining these standards

Signed: [Name]
Date: 2025-11-04
```

**Send acknowledgment to:** Viktor Kovalenko

---

## 🚀 FINAL MESSAGE

**This is not bureaucracy.**  
**This is professionalism.**

**Bellingcat changed investigative journalism by:**
- Citing everything
- Archiving everything
- Verifying everything
- Being transparent

**We follow their standard.**

**Because we're not playing at investigations.**  
**We're doing world-class intelligence work.**

**And world-class work requires world-class sourcing.**

---

**Questions? Ask.**  
**Concerns? Share them.**  
**Compliance? Mandatory.**

**Let's do this right.** 🔍📚

---

**Aleksander Nowak**  
Technical Orchestrator  
Destiny Team Framework  

**Date:** 2025-11-04  
**Version:** 1.0  
**Status:** 🔴 MANDATORY - EFFECTIVE IMMEDIATELY  

---

*This protocol will be indexed by Helena and enforced by Damian.*  
*Compliance is not optional. Quality is not negotiable.*  
*Welcome to professional investigative intelligence.* 🚀
