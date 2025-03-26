from bs4 import BeautifulSoup
import requests

def scrape_website(company_url):
    response = requests.get(company_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text from paragraphs, headings, etc.
    content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
    
    # Save to file (local storage)}"
    with open("company_info.txt", "w") as file:
        file.write(content)
    
    return content

scrape_website("https://able.co")