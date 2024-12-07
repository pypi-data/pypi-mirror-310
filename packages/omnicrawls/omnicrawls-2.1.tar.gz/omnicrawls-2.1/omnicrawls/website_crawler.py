import requests
from bs4 import BeautifulSoup

class WebsiteScraper:
    def __init__(self):
        pass 

    def clean_text(self, text):
        """Remove unnecessary whitespace and ensure clean text."""
        return ' '.join(text.split())  
    def extract(self, website_url):
        try:
            response = requests.get(website_url)
            response.raise_for_status()  

            soup = BeautifulSoup(response.content, 'html.parser')

            elements = soup.find_all(['div', 'p', 'span', 'header', 'footer', 'article'])

            texts = [self.clean_text(element.get_text()) for element in elements]

            combined_text = ' '.join(texts)

            return combined_text  

        except requests.exceptions.RequestException as e:
            return {"error": f"An error occurred: {e}"}


