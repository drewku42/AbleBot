import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from tqdm import tqdm

# Step 1: Get all URLs from the sitemap
SITEMAP_URL = "https://able.co/sitemap.xml"

def get_sitemap_urls(sitemap_url):
    """Fetch URLs from the sitemap."""
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print("Failed to fetch sitemap.")
        return []

    # Parse XML
    root = ET.fromstring(response.content)
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    
    urls = [elem.text for elem in root.findall(f".//{namespace}loc")]
    return urls

# Step 2: Scrape each page's content
def scrape_page(url):
    """Extract text content from a given webpage."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        # Remove navigation, footer, and scripts
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.extract()

        # Extract main text
        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Step 3: Scrape all pages and store data
def scrape_website():
    urls = get_sitemap_urls(SITEMAP_URL)
    
    print(f"Found {len(urls)} URLs. Starting scraping...")
    all_data = []

    for url in tqdm(urls, desc="Scraping pages"):
        text = scrape_page(url)
        if text:
            all_data.append(f"URL: {url}\n{text}\n\n")

        # Let page load
        time.sleep(1)

    # Save scraped data
    with open("company_info.txt", "w", encoding="utf-8") as f:
        f.writelines(all_data)
    
    print("Scraping completed. Data saved to company_info.txt.")

# Run the scraper
scrape_website()
