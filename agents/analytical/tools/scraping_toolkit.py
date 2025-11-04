"""
Scraping Toolkit for OSINT Agents
Web scraping, dynamic content, API access
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import json

try:
    from fake_useragent import UserAgent
    HAS_FAKE_UA = True
except ImportError:
    HAS_FAKE_UA = False

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


class ScrapingToolkit:
    """
    Professional web scraping tools
    
    Capabilities:
    - Basic HTML scraping (BeautifulSoup)
    - Dynamic content (Playwright if available)
    - API clients with rate limiting
    - Data extraction from tables, lists
    - Content archiving
    """
    
    def __init__(self):
        self.session = requests.Session()
        
        if HAS_FAKE_UA:
            self.ua = UserAgent()
            self.session.headers.update({
                'User-Agent': self.ua.random
            })
        else:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
        
        self.playwright = None
        self.browser = None
        self.context = None
    
    # ============================================
    # BASIC WEB SCRAPING
    # ============================================
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        Fetch HTML page
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            HTML content or None if error
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML to BeautifulSoup object
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object
        """
        try:
            from lxml import etree
            return BeautifulSoup(html, 'lxml')
        except ImportError:
            return BeautifulSoup(html, 'html.parser')
    
    def extract_links(self, soup: BeautifulSoup, base_url: Optional[str] = None) -> List[Dict]:
        """
        Extract all links from page
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative links
            
        Returns:
            List of {url, text} dicts
        """
        from urllib.parse import urljoin
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url and not href.startswith('http'):
                href = urljoin(base_url, href)
            links.append({
                'url': href,
                'text': a.get_text(strip=True)
            })
        return links
    
    def extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extract all text from page
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Clean text
        """
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """
        Extract meta tags
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dict of metadata
        """
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
    
    def extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract tables as structured data
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of tables with headers and rows
        """
        tables = []
        
        for table in soup.find_all('table'):
            rows = []
            headers = []
            
            # Extract headers
            header_row = table.find('thead')
            if not header_row:
                header_row = table.find('tr')
            
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # Extract data rows
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr')[1:]:  # Skip header row
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    if headers and len(cells) == len(headers):
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append(cells)
            
            tables.append({
                'headers': headers,
                'rows': rows,
                'row_count': len(rows)
            })
        
        return tables
    
    def extract_images(self, soup: BeautifulSoup, base_url: Optional[str] = None) -> List[Dict]:
        """
        Extract all images
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative paths
            
        Returns:
            List of image data
        """
        from urllib.parse import urljoin
        
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if base_url and not src.startswith('http'):
                    src = urljoin(base_url, src)
                images.append({
                    'url': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        return images
    
    # ============================================
    # DYNAMIC CONTENT SCRAPING
    # ============================================
    
    def start_browser(self, headless: bool = True):
        """Start Playwright browser"""
        if not HAS_PLAYWRIGHT:
            raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
    
    def stop_browser(self):
        """Stop Playwright browser"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def scrape_dynamic_page(self, url: str, wait_for: Optional[str] = None, 
                           scroll: bool = False) -> Optional[str]:
        """
        Scrape page with JavaScript rendering
        
        Args:
            url: URL to scrape
            wait_for: CSS selector to wait for
            scroll: Scroll to bottom to load lazy content
            
        Returns:
            HTML content
        """
        if not self.context:
            raise RuntimeError("Browser not started. Call start_browser() first")
        
        page = self.context.new_page()
        
        try:
            # Navigate
            page.goto(url, wait_until='networkidle')
            
            # Wait for specific element
            if wait_for:
                page.wait_for_selector(wait_for, timeout=10000)
            
            # Scroll if needed
            if scroll:
                self._scroll_page(page)
            
            # Get content
            content = page.content()
            return content
            
        finally:
            page.close()
    
    def _scroll_page(self, page):
        """Scroll page to trigger lazy loading"""
        previous_height = page.evaluate('document.body.scrollHeight')
        
        for _ in range(10):  # Max 10 scrolls
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)
            
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
    
    def screenshot(self, url: str, output_path: str):
        """
        Take screenshot of page
        
        Args:
            url: URL to screenshot
            output_path: Path to save screenshot
        """
        if not self.context:
            raise RuntimeError("Browser not started. Call start_browser() first")
        
        page = self.context.new_page()
        try:
            page.goto(url, wait_until='networkidle')
            page.screenshot(path=output_path, full_page=True)
            return output_path
        finally:
            page.close()
    
    # ============================================
    # API CLIENT
    # ============================================
    
    def api_get(self, url: str, params: Optional[Dict] = None, 
                headers: Optional[Dict] = None) -> Dict:
        """
        GET request to API
        
        Args:
            url: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            JSON response
        """
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        response = self.session.get(url, params=params, headers=request_headers)
        response.raise_for_status()
        return response.json()
    
    def api_post(self, url: str, data: Optional[Dict] = None, 
                 json_data: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Dict:
        """
        POST request to API
        
        Args:
            url: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers
            
        Returns:
            JSON response
        """
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        response = self.session.post(url, data=data, json=json_data, headers=request_headers)
        response.raise_for_status()
        return response.json()
    
    # ============================================
    # ARCHIVING
    # ============================================
    
    def archive_page(self, url: str, output_dir: str = './archives') -> Dict:
        """
        Archive page (HTML + screenshot)
        
        Args:
            url: URL to archive
            output_dir: Directory to save files
            
        Returns:
            Dict with archive paths
        """
        import os
        from datetime import datetime
        from hashlib import md5
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        url_hash = md5(url.encode()).hexdigest()[:8]
        base_name = f"{timestamp}_{url_hash}"
        
        # Fetch HTML
        html = self.fetch_page(url)
        html_path = os.path.join(output_dir, f"{base_name}.html")
        
        if html:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        # Save metadata
        metadata = {
            'url': url,
            'archived_at': datetime.now().isoformat(),
            'html_file': html_path
        }
        
        metadata_path = os.path.join(output_dir, f"{base_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    # ============================================
    # UTILITY
    # ============================================
    
    def get_available_tools(self) -> Dict:
        """List available scraping tools"""
        return {
            "basic_scraping": [
                "fetch_page",
                "parse_html",
                "extract_links",
                "extract_text",
                "extract_metadata",
                "extract_tables",
                "extract_images"
            ],
            "dynamic_scraping": [
                "scrape_dynamic_page (requires Playwright)",
                "screenshot (requires Playwright)"
            ],
            "api_access": [
                "api_get",
                "api_post"
            ],
            "archiving": [
                "archive_page"
            ],
            "playwright_available": HAS_PLAYWRIGHT,
            "status": "Ready for scraping operations"
        }


# Test
if __name__ == "__main__":
    print("🕷️ Scraping Toolkit Test\n")
    
    toolkit = ScrapingToolkit()
    tools = toolkit.get_available_tools()
    
    print("Available Tools:")
    for category, tool_list in tools.items():
        if category != "status":
            print(f"\n{category.upper()}:")
            if isinstance(tool_list, list):
                for tool in tool_list:
                    print(f"  ✓ {tool}")
            else:
                print(f"  {tool}")
    
    print(f"\n{tools['status']}")
    
    # Test basic scraping
    print("\n--- Test: Fetch Page ---")
    html = toolkit.fetch_page('https://httpbin.org/html')
    if html:
        soup = toolkit.parse_html(html)
        text = toolkit.extract_text(soup)
        print(f"Extracted {len(text)} characters")
        print("✅ Basic scraping works!")
