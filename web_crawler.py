import requests
from bs4 import BeautifulSoup
import sys

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            print(f"Extracted text from {url}")
            return text
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None

def crawl_web(seed_url, output_file):
    text = extract_text_from_url(seed_url)
    if text:
        # Remove empty lines
        text_lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(text_lines)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Text extracted from {seed_url} and saved to {output_file}")
    else:
        # create an empty file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")


# test
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python web_crawler.py <seed_url> <output_file>")
    else:
        seed_url = sys.argv[1]
        output_file = sys.argv[2]
        crawl_web(seed_url, output_file)