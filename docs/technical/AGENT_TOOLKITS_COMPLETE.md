# 🛠️ Agent Toolkits - Complete Technical Specification

**Prepared by:** Alex Morgan (Technical Liaison) + Elena Volkov (OSINT)  
**Date:** 2025-11-04  
**Status:** 🔨 IMPLEMENTATION READY  
**Focus:** Practical tools agenci mogą używać natychmiast  

---

## 🎯 Overview

Każdy agent potrzebuje **zestawu narzędzi** do swojej pracy. Ten dokument definiuje:
1. **Scraping Toolkit** - zbieranie danych z internetu
2. **Mathematical Toolkit** - obliczenia, analiza, statystyka
3. **Image Intelligence Toolkit** - analiza obrazów
4. **Text Intelligence Toolkit** - analiza tekstu
5. **Geolocation Toolkit** - lokalizacja geograficzna

---

## 📦 1. SCRAPING TOOLKIT

### **Purpose:** Zbieranie danych z websites, APIs, social media

### **Tech Stack:**

```python
# requirements.txt
requests==2.31.0          # HTTP requests (podstawa)
beautifulsoup4==4.12.2    # HTML parsing (proste)
lxml==4.9.3               # XML/HTML parser (szybki)
scrapy==2.11.0            # Full scraping framework (zaawansowane)
selenium==4.15.0          # Browser automation (JavaScript)
playwright==1.40.0        # Modern browser automation (lepszy niż Selenium)
httpx==0.25.0             # Async HTTP client
aiohttp==3.9.0            # Async HTTP dla Scrapy
fake-useragent==1.4.0     # Losowe User-Agents (unikanie blokady)
```

### **A. Basic Web Scraping (BeautifulSoup)**

```python
"""
Use case: Proste website'y, HTML parsing
Best for: Statyczne strony, pojedyncze requesty
"""

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class BasicScraper:
    """Elena's basic scraping tool"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        
    def fetch_page(self, url, timeout=10):
        """Pobierz stronę HTML"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html):
        """Parse HTML do BeautifulSoup object"""
        return BeautifulSoup(html, 'lxml')
    
    def extract_links(self, soup, base_url=None):
        """Wyciągnij wszystkie linki"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url and not href.startswith('http'):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)
            links.append({
                'url': href,
                'text': a.get_text(strip=True)
            })
        return links
    
    def extract_text(self, soup):
        """Wyciągnij cały tekst ze strony"""
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        return text
    
    def extract_metadata(self, soup):
        """Wyciągnij meta tags"""
        metadata = {}
        
        # Title
        if soup.title:
            metadata['title'] = soup.title.string
        
        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        return metadata
    
    def extract_tables(self, soup):
        """Wyciągnij tabele jako lista dictów"""
        tables = []
        
        for table in soup.find_all('table'):
            rows = []
            headers = []
            
            # Extract headers
            header_row = table.find('thead') or table.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # Extract data rows
            for tr in table.find_all('tr')[1:]:  # Skip header row
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    if headers and len(cells) == len(headers):
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append(cells)
            
            tables.append({
                'headers': headers,
                'rows': rows
            })
        
        return tables

# Example usage:
scraper = BasicScraper()
html = scraper.fetch_page('https://example.com')
soup = scraper.parse_html(html)
links = scraper.extract_links(soup)
text = scraper.extract_text(soup)
tables = scraper.extract_tables(soup)
```

### **B. Dynamic Content Scraping (Playwright)**

```python
"""
Use case: Websites z JavaScript, dynamic loading, SPAs
Best for: Modern websites, social media, interactive pages
"""

from playwright.sync_api import sync_playwright
import time

class DynamicScraper:
    """Scraping websites z JavaScript"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
    
    def start(self):
        """Start browser"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
    
    def stop(self):
        """Close browser"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def scrape_page(self, url, wait_for=None, scroll=False):
        """
        Scrape dynamic page
        
        Args:
            url: URL to scrape
            wait_for: CSS selector to wait for (optional)
            scroll: Scroll to bottom to load lazy content
        """
        page = self.context.new_page()
        
        try:
            # Navigate
            page.goto(url, wait_until='networkidle')
            
            # Wait for specific element
            if wait_for:
                page.wait_for_selector(wait_for, timeout=10000)
            
            # Scroll if needed (lazy loading)
            if scroll:
                self._scroll_to_bottom(page)
            
            # Get content
            content = page.content()
            
            return content
            
        finally:
            page.close()
    
    def _scroll_to_bottom(self, page):
        """Scroll to bottom to trigger lazy loading"""
        previous_height = page.evaluate('document.body.scrollHeight')
        
        while True:
            # Scroll down
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            
            # Check if new content loaded
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
    
    def screenshot(self, url, output_path):
        """Take screenshot"""
        page = self.context.new_page()
        try:
            page.goto(url, wait_until='networkidle')
            page.screenshot(path=output_path, full_page=True)
        finally:
            page.close()
    
    def extract_with_js(self, url, js_code):
        """Execute JavaScript to extract data"""
        page = self.context.new_page()
        try:
            page.goto(url, wait_until='networkidle')
            result = page.evaluate(js_code)
            return result
        finally:
            page.close()

# Example usage:
scraper = DynamicScraper()
scraper.start()

# Scrape dynamic content
html = scraper.scrape_page('https://twitter.com/search?q=osint', 
                           wait_for='article',
                           scroll=True)

# Take screenshot
scraper.screenshot('https://example.com', 'screenshot.png')

# Extract with custom JS
tweets = scraper.extract_with_js('https://twitter.com/...',
    '''
    Array.from(document.querySelectorAll('article')).map(article => ({
        text: article.innerText,
        time: article.querySelector('time')?.dateTime
    }))
    ''')

scraper.stop()
```

### **C. Large-Scale Scraping (Scrapy)**

```python
"""
Use case: Scraping całych websites, tysiące stron
Best for: Systematic scraping, following links, sitemap crawling
"""

import scrapy
from scrapy.crawler import CrawlerProcess

class UniversalSpider(scrapy.Spider):
    """Universal spider for any website"""
    
    name = 'universal'
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,  # Be nice: 1 second between requests
        'AUTOTHROTTLE_ENABLED': True,
    }
    
    def __init__(self, start_url, allowed_domains=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        if allowed_domains:
            self.allowed_domains = allowed_domains
    
    def parse(self, response):
        """Parse page and extract data"""
        
        # Extract data
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'text': ' '.join(response.css('p::text').getall()),
            'links': response.css('a::attr(href)').getall(),
            'images': response.css('img::attr(src)').getall(),
        }
        
        # Follow links
        for link in response.css('a::attr(href)').getall():
            if link:
                yield response.follow(link, callback=self.parse)

# Example: Scrape entire website
def scrape_website(start_url, output_file='output.json'):
    """Scrape website and save to JSON"""
    
    process = CrawlerProcess(settings={
        'FEEDS': {
            output_file: {'format': 'json'},
        },
    })
    
    process.crawl(UniversalSpider, start_url=start_url)
    process.start()

# Usage:
# scrape_website('https://example.com', 'example_data.json')
```

### **D. API Client (Structured)**

```python
"""
Use case: APIs (Twitter, Reddit, etc.)
Best for: Structured data, rate-limited access
"""

import requests
from typing import Dict, List
import time
from datetime import datetime

class APIClient:
    """Generic API client with rate limiting"""
    
    def __init__(self, base_url, api_key=None, rate_limit=10):
        """
        Args:
            base_url: Base URL for API
            api_key: API key (if needed)
            rate_limit: Max requests per second
        """
        self.base_url = base_url
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.last_request_time = 0
        
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def _rate_limit_wait(self):
        """Wait if needed to respect rate limit"""
        if self.rate_limit:
            time_since_last = time.time() - self.last_request_time
            wait_time = (1.0 / self.rate_limit) - time_since_last
            if wait_time > 0:
                time.sleep(wait_time)
        self.last_request_time = time.time()
    
    def get(self, endpoint, params=None):
        """GET request"""
        self._rate_limit_wait()
        
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None, json=None):
        """POST request"""
        self._rate_limit_wait()
        
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, data=data, json=json)
        response.raise_for_status()
        return response.json()
    
    def paginated_get(self, endpoint, params=None, limit=100):
        """Get all results from paginated endpoint"""
        results = []
        page = 1
        
        while True:
            page_params = params.copy() if params else {}
            page_params['page'] = page
            page_params['per_page'] = 100
            
            data = self.get(endpoint, params=page_params)
            
            if not data or len(data) == 0:
                break
            
            results.extend(data)
            
            if len(results) >= limit:
                break
            
            page += 1
        
        return results[:limit]

# Example: Sejm API client (from our previous work!)
class SejmAPIClient(APIClient):
    """Client for Sejm API"""
    
    def __init__(self):
        super().__init__(base_url='https://api.sejm.gov.pl')
    
    def get_committees(self, term=9):
        """Get all committees"""
        return self.get(f'sejm/term{term}/committees')
    
    def get_committee_sittings(self, term, code):
        """Get committee sittings"""
        return self.get(f'sejm/term{term}/committees/{code}/sittings')
```

---

## 🧮 2. MATHEMATICAL TOOLKIT

### **Purpose:** Obliczenia, statystyka, analiza danych

### **Tech Stack:**

```python
# requirements.txt
numpy==1.24.3             # Arrays, linear algebra
scipy==1.11.3             # Scientific computing
pandas==2.1.1             # DataFrames, data analysis
scikit-learn==1.3.1       # Machine learning
statsmodels==0.14.0       # Statistical models
matplotlib==3.8.0         # Plotting
seaborn==0.12.2           # Statistical visualization
plotly==5.17.0            # Interactive plots
```

### **A. NumPy - Array Operations**

```python
"""
Use case: Numerical calculations, arrays, linear algebra
Best for: Fast mathematical operations
"""

import numpy as np

class MathToolkit:
    """Mathematical operations for Maya (Data Analyst)"""
    
    @staticmethod
    def basic_stats(data):
        """Calculate basic statistics"""
        arr = np.array(data)
        
        return {
            'mean': np.mean(arr),
            'median': np.median(arr),
            'std': np.std(arr),
            'min': np.min(arr),
            'max': np.max(arr),
            'quartiles': np.percentile(arr, [25, 50, 75]),
            'count': len(arr)
        }
    
    @staticmethod
    def correlation(x, y):
        """Calculate correlation between two variables"""
        return np.corrcoef(x, y)[0, 1]
    
    @staticmethod
    def moving_average(data, window=3):
        """Calculate moving average"""
        return np.convolve(data, np.ones(window)/window, mode='valid')
    
    @staticmethod
    def normalize(data):
        """Normalize data to 0-1 range"""
        arr = np.array(data)
        min_val = np.min(arr)
        max_val = np.max(arr)
        return (arr - min_val) / (max_val - min_val)
    
    @staticmethod
    def detect_outliers(data, threshold=3):
        """Detect outliers using z-score"""
        arr = np.array(data)
        z_scores = np.abs((arr - np.mean(arr)) / np.std(arr))
        return np.where(z_scores > threshold)[0]
    
    @staticmethod
    def distance_matrix(points):
        """
        Calculate distance matrix between points
        Use case: Geographic distance, similarity
        
        Args:
            points: List of (x, y) tuples or (lat, lon)
        """
        points = np.array(points)
        n = len(points)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                distances[i, j] = np.linalg.norm(points[i] - points[j])
        
        return distances
    
    @staticmethod
    def angle_between_vectors(v1, v2):
        """
        Calculate angle between two vectors
        Use case: Shadow direction analysis, geolocation
        """
        v1 = np.array(v1)
        v2 = np.array(v2)
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle_rad = np.arccos(np.clip(cos_angle, -1, 1))
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg

# Example usage:
toolkit = MathToolkit()

# Basic stats
data = [1, 2, 3, 4, 5, 100]  # Note outlier
stats = toolkit.basic_stats(data)
outliers = toolkit.detect_outliers(data)

# Geographic calculations
locations = [(52.2297, 21.0122), (51.5074, -0.1278)]  # Warsaw, London
distances = toolkit.distance_matrix(locations)
```

### **B. Pandas - Data Analysis**

```python
"""
Use case: Tabular data, time series, aggregations
Best for: Data manipulation, analysis
"""

import pandas as pd
from datetime import datetime

class DataAnalyzer:
    """Data analysis for Maya"""
    
    @staticmethod
    def load_data(source, format='csv'):
        """Load data from various sources"""
        if format == 'csv':
            return pd.read_csv(source)
        elif format == 'json':
            return pd.read_json(source)
        elif format == 'excel':
            return pd.read_excel(source)
        elif format == 'sql':
            # Requires SQLAlchemy
            from sqlalchemy import create_engine
            engine = create_engine(source)
            return pd.read_sql_table('table_name', engine)
    
    @staticmethod
    def describe_data(df):
        """Get comprehensive description"""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing': df.isnull().sum().to_dict(),
            'stats': df.describe().to_dict(),
            'memory': df.memory_usage(deep=True).sum()
        }
    
    @staticmethod
    def clean_data(df):
        """Basic data cleaning"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Fill missing numeric with median
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Fill missing categorical with mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', 
                          inplace=True)
        
        return df
    
    @staticmethod
    def time_series_analysis(df, date_column, value_column):
        """Analyze time series data"""
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
        df.set_index(date_column, inplace=True)
        
        analysis = {
            'daily_avg': df[value_column].resample('D').mean(),
            'weekly_avg': df[value_column].resample('W').mean(),
            'monthly_avg': df[value_column].resample('M').mean(),
            'trend': df[value_column].rolling(window=7).mean(),
            'total': df[value_column].sum(),
            'date_range': (df.index.min(), df.index.max())
        }
        
        return analysis
    
    @staticmethod
    def group_analysis(df, group_by, agg_column):
        """Group and aggregate data"""
        grouped = df.groupby(group_by)[agg_column].agg([
            'count', 'sum', 'mean', 'median', 'std', 'min', 'max'
        ])
        return grouped
    
    @staticmethod
    def pivot_analysis(df, index, columns, values):
        """Create pivot table"""
        return pd.pivot_table(df, 
                             index=index,
                             columns=columns,
                             values=values,
                             aggfunc='count',
                             fill_value=0)
    
    @staticmethod
    def correlation_matrix(df):
        """Calculate correlation matrix"""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr()
    
    @staticmethod
    def export_data(df, output_path, format='csv'):
        """Export data to various formats"""
        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format == 'excel':
            df.to_excel(output_path, index=False)
        elif format == 'html':
            df.to_html(output_path, index=False)

# Example: Analyze Sejm data (from our previous project!)
analyzer = DataAnalyzer()

# Load data
df = pd.read_json('sejm_analysis/sejm_asw_complete_analysis.json')

# Describe
description = analyzer.describe_data(df)

# Time series analysis
if 'date' in df.columns:
    ts_analysis = analyzer.time_series_analysis(df, 'date', 'count')

# Group by year
if 'year' in df.columns:
    yearly = analyzer.group_analysis(df, 'year', 'meeting_count')
```

### **C. SciPy - Scientific Computing**

```python
"""
Use case: Statistical tests, optimization, signal processing
Best for: Scientific analysis
"""

from scipy import stats
from scipy.spatial import distance
from scipy.optimize import minimize

class ScientificToolkit:
    """Advanced scientific computing"""
    
    @staticmethod
    def statistical_test(group1, group2, test='ttest'):
        """
        Compare two groups statistically
        
        Tests:
        - ttest: T-test (parametric)
        - mannwhitney: Mann-Whitney U (non-parametric)
        - kstest: Kolmogorov-Smirnov
        """
        if test == 'ttest':
            statistic, pvalue = stats.ttest_ind(group1, group2)
        elif test == 'mannwhitney':
            statistic, pvalue = stats.mannwhitney(group1, group2)
        elif test == 'kstest':
            statistic, pvalue = stats.ks_2samp(group1, group2)
        
        return {
            'statistic': statistic,
            'pvalue': pvalue,
            'significant': pvalue < 0.05,
            'interpretation': 'Groups differ significantly' if pvalue < 0.05 else 'No significant difference'
        }
    
    @staticmethod
    def correlation_test(x, y, method='pearson'):
        """
        Test correlation between variables
        
        Methods:
        - pearson: Linear correlation
        - spearman: Rank correlation
        - kendalltau: Ordinal correlation
        """
        if method == 'pearson':
            corr, pvalue = stats.pearsonr(x, y)
        elif method == 'spearman':
            corr, pvalue = stats.spearmanr(x, y)
        elif method == 'kendalltau':
            corr, pvalue = stats.kendalltau(x, y)
        
        return {
            'correlation': corr,
            'pvalue': pvalue,
            'significant': pvalue < 0.05,
            'strength': 'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.4 else 'weak'
        }
    
    @staticmethod
    def calculate_distances(point, points, metric='euclidean'):
        """
        Calculate distances from point to multiple points
        
        Use case: Find nearest locations, similarity
        
        Metrics: euclidean, manhattan, cosine, etc.
        """
        distances = [distance.cdist([point], [p], metric=metric)[0][0] for p in points]
        return distances
    
    @staticmethod
    def optimize_function(func, initial_guess, bounds=None):
        """
        Optimize (minimize) a function
        
        Use case: Find best parameters, locations
        """
        result = minimize(func, initial_guess, bounds=bounds)
        return {
            'success': result.success,
            'optimal_values': result.x,
            'optimal_result': result.fun,
            'iterations': result.nit
        }

# Example: Geographic optimization
def distance_to_multiple_points(location, target_locations):
    """Find location that minimizes sum of distances to targets"""
    total_distance = sum([
        distance.euclidean(location, target) 
        for target in target_locations
    ])
    return total_distance

# Find optimal meeting point
targets = [(52.2297, 21.0122), (51.5074, -0.1278), (48.8566, 2.3522)]  # Warsaw, London, Paris
initial = (50.0, 10.0)  # Central Europe

toolkit = ScientificToolkit()
result = toolkit.optimize_function(
    lambda loc: distance_to_multiple_points(loc, targets),
    initial
)
# Result: Optimal meeting location
```

### **D. Scikit-learn - Machine Learning**

```python
"""
Use case: Clustering, classification, anomaly detection
Best for: Pattern recognition, predictions
"""

from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class MLToolkit:
    """Machine learning for pattern detection"""
    
    @staticmethod
    def cluster_data(data, method='kmeans', n_clusters=3):
        """
        Cluster data points
        
        Use case: Group similar entities, detect communities
        """
        # Normalize data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        if method == 'kmeans':
            model = KMeans(n_clusters=n_clusters, random_state=42)
        elif method == 'dbscan':
            model = DBSCAN(eps=0.5, min_samples=5)
        
        labels = model.fit_predict(data_scaled)
        
        return {
            'labels': labels,
            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
            'model': model
        }
    
    @staticmethod
    def detect_anomalies(data, contamination=0.1):
        """
        Detect anomalies in data
        
        Use case: Find suspicious data points, outliers
        """
        from sklearn.ensemble import IsolationForest
        
        model = IsolationForest(contamination=contamination, random_state=42)
        predictions = model.fit_predict(data)
        
        # -1 = anomaly, 1 = normal
        anomaly_indices = np.where(predictions == -1)[0]
        
        return {
            'anomaly_indices': anomaly_indices,
            'n_anomalies': len(anomaly_indices),
            'anomaly_ratio': len(anomaly_indices) / len(data)
        }
    
    @staticmethod
    def reduce_dimensions(data, n_components=2):
        """
        Reduce dimensionality for visualization
        
        Use case: Visualize high-dimensional data
        """
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(data)
        
        return {
            'reduced_data': reduced,
            'explained_variance': pca.explained_variance_ratio_,
            'total_variance_explained': sum(pca.explained_variance_ratio_)
        }

# Example: Cluster social media posts by similarity
# (after converting to embeddings)
```

---

## 📸 3. IMAGE INTELLIGENCE TOOLKIT

### **Tech Stack:**

```python
# requirements.txt
pillow==10.1.0            # Image processing
opencv-python==4.8.1      # Computer vision
pytesseract==0.3.10       # OCR
exiftool==0.12.0          # Metadata extraction
imagehash==4.3.1          # Perceptual hashing
```

### **Implementation:**

```python
"""
Image analysis for Elena
"""

from PIL import Image
import cv2
import pytesseract
import numpy as np
import imagehash

class ImageToolkit:
    """Image intelligence operations"""
    
    @staticmethod
    def extract_exif(image_path):
        """Extract EXIF metadata"""
        from PIL.ExifTags import TAGS
        
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if not exif_data:
            return {}
        
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = value
        
        return metadata
    
    @staticmethod
    def ocr_extract_text(image_path):
        """Extract text from image using OCR"""
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    
    @staticmethod
    def detect_faces(image_path):
        """Detect faces in image"""
        # Load OpenCV face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Read image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return [{
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        } for (x, y, w, h) in faces]
    
    @staticmethod
    def calculate_image_hash(image_path):
        """
        Calculate perceptual hash
        Use case: Find similar/duplicate images
        """
        image = Image.open(image_path)
        return {
            'average_hash': str(imagehash.average_hash(image)),
            'perceptual_hash': str(imagehash.phash(image)),
            'difference_hash': str(imagehash.dhash(image))
        }
    
    @staticmethod
    def compare_images(image1_path, image2_path):
        """Compare two images for similarity"""
        hash1 = imagehash.average_hash(Image.open(image1_path))
        hash2 = imagehash.average_hash(Image.open(image2_path))
        
        difference = hash1 - hash2  # Hamming distance
        
        return {
            'similarity_score': 1 - (difference / 64.0),  # 0-1 scale
            'hamming_distance': difference,
            'identical': difference == 0,
            'similar': difference < 10  # Threshold
        }
    
    @staticmethod
    def analyze_colors(image_path):
        """Extract dominant colors"""
        image = Image.open(image_path)
        image = image.resize((150, 150))  # Reduce size for speed
        
        # Convert to numpy array
        pixels = np.array(image)
        pixels = pixels.reshape(-1, 3)
        
        # Use KMeans to find dominant colors
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        percentages = np.bincount(kmeans.labels_) / len(kmeans.labels_)
        
        return [
            {
                'rgb': tuple(color),
                'hex': '#{:02x}{:02x}{:02x}'.format(*color),
                'percentage': float(pct)
            }
            for color, pct in zip(colors, percentages)
        ]
```

---

## 🗺️ 4. GEOLOCATION TOOLKIT

### **Tech Stack:**

```python
# requirements.txt
geopy==2.4.0              # Geocoding
folium==0.15.0            # Map visualization
pysolar==0.10             # Sun position calculation
timezonefinder==6.2.0     # Timezone from coordinates
```

### **Implementation:**

```python
"""
Geolocation tools for Elena
"""

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from datetime import datetime
from pysolar import solar
from timezonefinder import TimezoneFinder

class GeolocationToolkit:
    """Geographic intelligence operations"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="destiny-osint")
        self.tf = TimezoneFinder()
    
    def geocode(self, address):
        """Convert address to coordinates"""
        location = self.geolocator.geocode(address)
        if location:
            return {
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'raw': location.raw
            }
        return None
    
    def reverse_geocode(self, latitude, longitude):
        """Convert coordinates to address"""
        location = self.geolocator.reverse(f"{latitude}, {longitude}")
        if location:
            return {
                'address': location.address,
                'raw': location.raw
            }
        return None
    
    def calculate_distance(self, coord1, coord2, unit='km'):
        """
        Calculate distance between two coordinates
        
        Args:
            coord1, coord2: (latitude, longitude) tuples
            unit: 'km', 'miles', 'meters'
        """
        distance_km = geodesic(coord1, coord2).kilometers
        
        if unit == 'km':
            return distance_km
        elif unit == 'miles':
            return distance_km * 0.621371
        elif unit == 'meters':
            return distance_km * 1000
    
    def get_timezone(self, latitude, longitude):
        """Get timezone for coordinates"""
        timezone = self.tf.timezone_at(lat=latitude, lng=longitude)
        return timezone
    
    def calculate_sun_position(self, latitude, longitude, date_time):
        """
        Calculate sun position for shadow analysis
        
        CRITICAL FOR CHRONOLOCATION!
        
        Returns:
            azimuth: Direction of sun (0-360°, 0=North)
            altitude: Height of sun above horizon (degrees)
        """
        azimuth = solar.get_azimuth(latitude, longitude, date_time)
        altitude = solar.get_altitude(latitude, longitude, date_time)
        
        return {
            'azimuth': azimuth,
            'altitude': altitude,
            'datetime': date_time,
            'coordinates': (latitude, longitude)
        }
    
    def estimate_time_from_shadow(self, latitude, longitude, date, shadow_azimuth, tolerance=15):
        """
        Estimate time of day from shadow direction
        
        BELLINGCAT TECHNIQUE!
        
        Args:
            latitude, longitude: Location
            date: Date (without time)
            shadow_azimuth: Direction of shadow (degrees from North)
            tolerance: Acceptable error in degrees
        
        Returns:
            List of possible times
        """
        possible_times = []
        
        # Try every 15 minutes throughout the day
        for hour in range(24):
            for minute in [0, 15, 30, 45]:
                test_datetime = datetime(date.year, date.month, date.day, hour, minute)
                
                sun_pos = self.calculate_sun_position(latitude, longitude, test_datetime)
                
                # Shadow is opposite to sun
                shadow_direction_from_sun = (sun_pos['azimuth'] + 180) % 360
                
                # Check if within tolerance
                diff = abs(shadow_direction_from_sun - shadow_azimuth)
                if diff > 180:
                    diff = 360 - diff
                
                if diff <= tolerance:
                    possible_times.append({
                        'time': test_datetime.strftime('%H:%M'),
                        'sun_azimuth': sun_pos['azimuth'],
                        'sun_altitude': sun_pos['altitude'],
                        'match_quality': (tolerance - diff) / tolerance
                    })
        
        # Sort by match quality
        possible_times.sort(key=lambda x: x['match_quality'], reverse=True)
        
        return possible_times
    
    def create_map(self, center, markers=None, output_file='map.html'):
        """
        Create interactive map
        
        Args:
            center: (latitude, longitude)
            markers: List of {'coords': (lat, lon), 'popup': 'text', 'color': 'red'}
        """
        map_obj = folium.Map(location=center, zoom_start=13)
        
        if markers:
            for marker in markers:
                folium.Marker(
                    location=marker['coords'],
                    popup=marker.get('popup', ''),
                    icon=folium.Icon(color=marker.get('color', 'blue'))
                ).add_to(map_obj)
        
        map_obj.save(output_file)
        return output_file

# Example: Shadow analysis (Bellingcat technique!)
toolkit = GeolocationToolkit()

# Known: Location (Warsaw), Date (2024-11-04), Shadow direction (135° from North)
location = (52.2297, 21.0122)  # Warsaw
date = datetime(2024, 11, 4)
shadow_azimuth = 135  # Shadow points Southeast

possible_times = toolkit.estimate_time_from_shadow(
    latitude=location[0],
    longitude=location[1],
    date=date,
    shadow_azimuth=shadow_azimuth,
    tolerance=15
)

print(f"Possible times: {possible_times[:3]}")
# Output: Most likely times when photo was taken!
```

---

## 📊 5. COMPLETE AGENT TOOLKIT CLASS

```python
"""
Complete toolkit dla każdego agenta
All tools in one place
"""

class AgentToolkit:
    """Complete toolkit for OSINT agents"""
    
    def __init__(self, agent_name):
        self.agent_name = agent_name
        
        # Initialize all toolkits
        self.scraper = BasicScraper()
        self.dynamic_scraper = DynamicScraper()
        self.math = MathToolkit()
        self.data_analyzer = DataAnalyzer()
        self.scientific = ScientificToolkit()
        self.ml = MLToolkit()
        self.image = ImageToolkit()
        self.geo = GeolocationToolkit()
    
    def log(self, message):
        """Log message with agent name"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{self.agent_name}] {message}")
    
    # All methods accessible through self.scraper., self.math., etc.

# Usage by Elena:
elena_toolkit = AgentToolkit("Elena Volkov")

# Web scraping
html = elena_toolkit.scraper.fetch_page('https://example.com')

# Image analysis
faces = elena_toolkit.image.detect_faces('photo.jpg')

# Geolocation
location = elena_toolkit.geo.geocode("Warsaw, Poland")

# Math calculations
stats = elena_toolkit.math.basic_stats([1, 2, 3, 4, 5])

# Data analysis
df = elena_toolkit.data_analyzer.load_data('data.csv')
description = elena_toolkit.data_analyzer.describe_data(df)
```

---

## 📦 Installation Script

```bash
#!/bin/bash
# install_toolkits.sh

echo "Installing Agent Toolkits..."

# Core dependencies
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install lxml==4.9.3
pip install playwright==1.40.0
pip install fake-useragent==1.4.0

# Math & Data Science
pip install numpy==1.24.3
pip install scipy==1.11.3
pip install pandas==2.1.1
pip install scikit-learn==1.3.1
pip install statsmodels==0.14.0

# Visualization
pip install matplotlib==3.8.0
pip install seaborn==0.12.2
pip install plotly==5.17.0

# Image Processing
pip install pillow==10.1.0
pip install opencv-python==4.8.1
pip install pytesseract==0.3.10
pip install imagehash==4.3.1

# Geolocation
pip install geopy==2.4.0
pip install folium==0.15.0
pip install pysolar==0.10
pip install timezonefinder==6.2.0

# Playwright browser install
playwright install chromium

echo "✅ All toolkits installed!"
```

---

## 🎯 Next Steps

1. ✅ **Toolkits Defined** - Complete specification ready
2. 🔨 **Implementation** - Create Python modules
3. 🔨 **Testing** - Test each toolkit
4. 🔨 **Integration** - Connect with agents
5. 🔨 **Documentation** - Usage examples
6. 🔨 **Training** - Agents learn to use tools

---

**Prepared by:** Alex Morgan (Technical) + Elena Volkov (OSINT)  
**Date:** 2025-11-04  
**Status:** Ready for implementation  

**All tools agents need to do world-class investigative work!** 🛠️
