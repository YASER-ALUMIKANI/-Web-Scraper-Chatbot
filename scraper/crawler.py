import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

def scrape_page(soup):
    """Extracts and cleans text from a parsed HTML page."""
    return ' '.join(p.get_text().strip() for p in soup.find_all('p'))

def get_all_links(base_url, soup):
    """Extracts and normalizes internal links from a page."""
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = urljoin(base_url, a_tag['href'])
        parsed_href = urlparse(href)
        
        if parsed_href.netloc == urlparse(base_url).netloc:
            clean_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            links.add(clean_url)
    return links

def crawl_and_scrape(base_url, max_pages=None):
    visited_urls = set()
    queue = [base_url]
    all_text = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    def process_url(url):
        """Fetches and processes a single page."""
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = scrape_page(soup)
            return (url, content, get_all_links(base_url, soup))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return (url, None, set())

    with ThreadPoolExecutor(max_workers=5) as executor:
        while queue and len(visited_urls) < max_pages:
            current_batch = queue[:5]
            queue = queue[5:]

            future_results = {executor.submit(process_url, url): url for url in current_batch}
            
            for future in future_results:
                url, content, new_links = future.result()
                if content and url not in visited_urls:
                    visited_urls.add(url)
                    all_text.append(content)
                    queue.extend(new_links - visited_urls)

            time.sleep(0.5)
    
    return "\n".join(all_text)
