"""
Tool for scraping job descriptions from URLs
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_job_description(url: str) -> dict:
    """
    Scrape job description from URL
    Returns dict with title, company, and description
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        # Note: This is a generic scraper - may need customization per site
        text = soup.get_text(separator='\n', strip=True)
        
        return {
            'success': True,
            'url': url,
            'content': text,
            'title': soup.find('title').text if soup.find('title') else 'N/A',
        }
    
    except Exception as e:
        return {
            'success': False,
            'url': url,
            'error': str(e),
            'content': ''
        }


def extract_from_text(text: str) -> dict:
    """Handle plain text job descriptions"""
    return {
        'success': True,
        'content': text,
        'title': 'N/A',
        'url': 'manual_input'
    }

