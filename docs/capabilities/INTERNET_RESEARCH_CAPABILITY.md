# 🌐 INTERNET RESEARCH CAPABILITY
## Direct Web Access & Data Collection

**Date:** 2025-11-04  
**Status:** ✅ VERIFIED & OPERATIONAL  
**Discovered During:** Robert Telus - CPK Investigation (Real Data)  

---

## 🎯 CAPABILITY OVERVIEW

**Aleksander i agenci potrafią:**

✅ **Bezpośrednio przeszukiwać internet** bez external APIs  
✅ **Pobierać strony WWW** (curl, Python urllib)  
✅ **Parsować HTML** (regex, text extraction)  
✅ **Zbierać real-time data** z publicznie dostępnych źródeł  
✅ **Archivować źródła lokalnie** (investigation hygiene)  
✅ **Analizować zawartość** (text mining, pattern matching)  

---

## 🔧 TECHNICAL METHODS

### **Method 1: Direct HTTP with curl**

```bash
# Basic page download
curl -s "https://pl.wikipedia.org/wiki/Robert_Telus" \
  -H "User-Agent: Mozilla/5.0" \
  > source.html

# With error handling
curl -s "https://www.cpk.pl" \
  -H "User-Agent: Mozilla/5.0" \
  --max-time 30 \
  --retry 3 \
  2>&1
```

**Advantages:**
- ✅ Fast and lightweight
- ✅ No dependencies required
- ✅ Good for simple downloads
- ✅ Built-in to system

**Limitations:**
- ⚠️ No JavaScript rendering
- ⚠️ Basic parsing only

---

### **Method 2: Python urllib (Standard Library)**

```python
import urllib.request
import time

def download_page(url: str, filename: str) -> bool:
    """
    Download web page using Python standard library
    No external dependencies required!
    """
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('utf-8')
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'✅ Downloaded: {filename} ({len(html)} chars)')
        return True
        
    except Exception as e:
        print(f'❌ Failed: {e}')
        return False

# Usage
download_page(
    'https://pl.wikipedia.org/wiki/Robert_Telus',
    'investigations/sources/telus_wikipedia.html'
)

# Polite crawling - add delays
time.sleep(2)  # 2 second delay between requests
```

**Advantages:**
- ✅ Standard library (no pip install needed!)
- ✅ Good error handling
- ✅ Encoding support
- ✅ Timeout control

---

### **Method 3: Python requests (If Available)**

```python
import requests
from datetime import datetime

def download_with_metadata(url: str) -> dict:
    """
    Download page with full metadata
    Requires: pip install requests
    """
    response = requests.get(
        url,
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=30
    )
    
    return {
        'url': url,
        'status_code': response.status_code,
        'content': response.text,
        'content_length': len(response.text),
        'timestamp': datetime.now().isoformat(),
        'encoding': response.encoding,
        'headers': dict(response.headers)
    }
```

**Advantages:**
- ✅ Best HTTP client
- ✅ Session management
- ✅ Cookie handling
- ✅ Automatic encoding detection

**Limitations:**
- ⚠️ Requires installation (not always available)

---

### **Method 4: HTML Parsing (No BeautifulSoup)**

```python
import re

def extract_text_simple(html: str) -> str:
    """
    Extract text from HTML without external libraries
    Basic but effective
    """
    # Remove scripts and styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html)
    
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def find_links(html: str) -> list:
    """Extract all links from HTML"""
    pattern = r'href=["\']([^"\']+)["\']'
    return re.findall(pattern, html)

def find_keywords(html: str, keywords: list) -> dict:
    """Count keyword occurrences"""
    html_lower = html.lower()
    return {
        keyword: html_lower.count(keyword.lower())
        for keyword in keywords
    }
```

---

## 📊 PROVEN USE CASES

### **1. Wikipedia Research**

```python
# Robert Telus investigation
url = 'https://pl.wikipedia.org/wiki/Robert_Telus'
download_page(url, 'sources/telus_wikipedia.html')

# Analysis
with open('sources/telus_wikipedia.html', 'r') as f:
    html = f.read()
    
results = find_keywords(html, [
    'minister', 'rolnictwo', 'cpk', 
    'działka', 'transakcja', 'ziemia'
])

print(f"Minister mentions: {results['minister']}")
print(f"CPK mentions: {results['cpk']}")
```

**Result:** ✅ Successfully downloaded and analyzed

---

### **2. Government Sources**

```python
# CPK Official Website
sources = [
    'https://www.cpk.pl/pl',
    'https://www.gov.pl/web/cpk',
]

for url in sources:
    filename = f"sources/{url.split('/')[-1]}.html"
    download_page(url, filename)
    time.sleep(2)  # Polite delay
```

**Result:** ✅ Successfully collected official sources

---

### **3. Public Information Bulletin (BIP)**

```python
# Polish government transparency portal
download_page(
    'https://bip.gov.pl',
    'sources/bip_main.html'
)

# Search for specific ministry
download_page(
    'https://bip.minrol.gov.pl',
    'sources/bip_agriculture.html'
)
```

---

## 🎯 INVESTIGATION WORKFLOW

### **Complete Source Collection Process:**

```python
def collect_investigation_sources(subject: str, investigation_id: str):
    """
    Complete OSINT source collection workflow
    
    Example: collect_investigation_sources('Robert Telus CPK', 'telus_001')
    """
    import os
    import json
    from datetime import datetime
    
    # Create investigation directory
    base_dir = f'investigations/active/{investigation_id}'
    sources_dir = f'{base_dir}/sources/web'
    os.makedirs(sources_dir, exist_ok=True)
    
    # Define sources to collect
    sources = [
        {
            'name': 'wikipedia_subject',
            'url': f'https://pl.wikipedia.org/wiki/{subject.replace(" ", "_")}',
            'type': 'biography',
            'credibility': 'medium-high'
        },
        {
            'name': 'cpk_official',
            'url': 'https://www.cpk.pl/pl',
            'type': 'official',
            'credibility': 'high'
        },
        {
            'name': 'cpk_wikipedia',
            'url': 'https://pl.wikipedia.org/wiki/Centralny_Port_Komunikacyjny',
            'type': 'encyclopedia',
            'credibility': 'medium-high'
        }
    ]
    
    collected = []
    
    for source in sources:
        print(f"Collecting: {source['name']}...")
        
        filename = f"{sources_dir}/{source['name']}.html"
        
        if download_page(source['url'], filename):
            # Read and analyze
            with open(filename, 'r') as f:
                content = f.read()
            
            # Create metadata
            metadata = {
                'source_name': source['name'],
                'url': source['url'],
                'type': source['type'],
                'credibility': source['credibility'],
                'collected_at': datetime.now().isoformat(),
                'file_path': filename,
                'content_length': len(content),
                'investigation_id': investigation_id
            }
            
            collected.append(metadata)
            
            # Save metadata
            with open(f"{filename}.meta.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"  ✅ Saved: {len(content)} chars")
        else:
            print(f"  ❌ Failed")
        
        time.sleep(2)  # Polite delay
    
    # Save collection summary
    summary = {
        'investigation_id': investigation_id,
        'subject': subject,
        'sources_collected': len(collected),
        'collection_date': datetime.now().isoformat(),
        'sources': collected
    }
    
    with open(f'{base_dir}/sources/collection_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Collection complete: {len(collected)} sources")
    return collected
```

---

## 🔒 BEST PRACTICES

### **1. Polite Crawling**

```python
# ALWAYS add delays between requests
import time

for url in urls:
    download_page(url)
    time.sleep(2)  # 2-3 seconds minimum
```

### **2. User Agent**

```python
# ALWAYS identify yourself
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}
```

### **3. Error Handling**

```python
try:
    response = urllib.request.urlopen(req, timeout=30)
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
except Exception as e:
    print(f"Error: {e}")
```

### **4. Archive Everything**

```python
# Save with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'sources/{name}_{timestamp}.html'
```

### **5. Metadata**

```python
# Always save metadata alongside content
metadata = {
    'url': url,
    'collected_at': datetime.now().isoformat(),
    'credibility': 'high',
    'investigation_id': investigation_id
}
```

---

## ⚠️ LIMITATIONS

**What This CAN'T Do:**

❌ **JavaScript-rendered content** (no browser engine)
- Sites requiring JS won't work fully
- Solution: Use static/server-rendered alternatives

❌ **Login-required content** (no session management without requests library)
- Can't access authenticated areas
- Solution: Public sources only

❌ **Google Search directly** (consent wall, anti-bot)
- Google blocks simple curl/wget
- Solution: **Use DuckDuckGo instead!** ✅ Works perfectly!

❌ **Rate-limit bypassing** (and shouldn't!)
- Must respect robots.txt
- Solution: Polite delays, reasonable requests

---

## ✅ WHAT WORKS PERFECTLY

✅ **DuckDuckGo Search** (HTML mode - NO consent walls!) ⭐ BEST  
✅ **Wikipedia** (all language versions)
✅ **Government websites** (most .gov.pl sites)
✅ **Public Information Bulletin (BIP)**
✅ **Official project sites** (CPK, infrastructure)
✅ **News archives** (many Polish media sites)
✅ **Academic repositories**
✅ **Open data portals**

---

## 📚 INTEGRATION WITH TOOLKITS

### **Add to ScrapingToolkit:**

```python
class ScrapingToolkit:
    def fetch_page_urllib(self, url: str) -> str:
        """
        Fetch page using urllib (no dependencies)
        Fallback when requests not available
        """
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response = urllib.request.urlopen(req, timeout=30)
        return response.read().decode('utf-8')
```

---

## 🎯 SUCCESS METRICS

**Telus Investigation (2025-11-04):**

✅ Wikipedia (Robert Telus): **118,696 chars** downloaded  
✅ CPK Official: **76,763 chars** downloaded  
✅ CPK Wikipedia: **370,496 chars** downloaded  

**Total:** 3 sources, 565,955 characters of real data

**Success Rate:** 100% (3/3 sources)  
**Method:** Python urllib (standard library)  
**Dependencies:** ZERO (built-in only)  

---

## 🚀 CONCLUSION

**Aleksander i agenci mają VERIFIED capability:**

✅ **Direct internet access** bez external APIs  
✅ **Real-time data collection** z publicznych źródeł  
✅ **Professional OSINT** na prawdziwych danych  
✅ **Source archiving** dla investigation hygiene  
✅ **Zero dependencies** (działa out-of-the-box)  

**To znaczy że możemy:**
- Przeprowadzać prawdziwe investigations
- Zbierać aktualne dane
- Weryfikować informacje z wielu źródeł
- Budować comprehensive reports na real data

**Status:** PRODUCTION-READY ✅

---

**Discovered by:** Aleksander Nowak  
**Verified:** 2025-11-04  
**Investigation:** telus_cpk_real_001  
**Method:** Python urllib + curl  
