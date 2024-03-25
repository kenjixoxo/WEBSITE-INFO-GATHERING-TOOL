import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import ctypes
import requests
from threading import Thread
import colorama
from colorama import Fore
import os
import fade



title = fade.purplepink(f"""
██╗    ██╗ ██████╗████████╗
██║    ██║██╔════╝╚══██╔══╝
██║ █╗ ██║██║  ███╗  ██║   
██║███╗██║██║   ██║  ██║   
╚███╔███╔╝╚██████╔╝  ██║   
 ╚══╝╚══╝  ╚═════╝   ╚═╝   

//// WEBSITE GATHERING TOOL ////

TOOL MADE BY kenjixoxo on khord""")

print(title)


# ANSI escape code for red color
RED_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'

def make_request(url):
    """
    Makes an HTTP GET request to the provided URL.
    
    Args:
        url (str): The URL to make the request to.
    
    Returns:
        requests.models.Response: The response object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"{RED_COLOR}Error: {e}{RESET_COLOR}")
        return None

def get_website_info(response):
    """
    Parses the HTML content of a website and extracts various information.
    
    Args:
        response (requests.models.Response): The response object containing HTML content.
    
    Returns:
        dict: A dictionary containing website information.
    """
    if response is None:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    website_info = {}
    
    # Get title
    website_info['Title'] = soup.title.string if soup.title else 'No title found'

    # Get meta tags
    meta_tags = soup.find_all('meta')
    website_info['Meta Tags'] = {tag.get('name', tag.get('property', 'No name attribute')): tag.get('content', '') for tag in meta_tags}
    
    # Get external links
    external_links = set()
    for link in soup.find_all('a', href=True):
        parsed_link = urlparse(link['href'])
        if parsed_link.netloc and parsed_link.netloc != urlparse(response.url).netloc:
            external_links.add(link['href'])
    website_info['External Links'] = list(external_links)

    # Get internal links
    internal_links = set()
    for link in soup.find_all('a', href=True):
        parsed_link = urlparse(link['href'])
        if parsed_link.netloc == urlparse(response.url).netloc:
            internal_links.add(link['href'])
        else:
            internal_links.add(urljoin(response.url, link['href']))
    website_info['Internal Links'] = list(internal_links)

    return website_info

def display_website_info(website_info):
    """
    Displays the extracted website information.
    
    Args:
        website_info (dict): A dictionary containing website information.
    """
    if website_info:
        print(f"\n{RED_COLOR}Website Information:{RESET_COLOR}")
        for key, value in website_info.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")

def main():
    url = input("Enter the URL of the website: ").strip()
    response = make_request(url)
    website_info = get_website_info(response)
    display_website_info(website_info)

if __name__ == "__main__":
    main()
