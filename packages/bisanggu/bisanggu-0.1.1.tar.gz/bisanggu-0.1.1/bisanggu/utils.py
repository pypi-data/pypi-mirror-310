import re
from urllib.parse import urlparse
import requests
from whois import whois

def clean_url(url):
    return re.sub(r'[^\x00-\x7F]+', '', url)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def ensure_url_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def get_country_by_ip(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        if response.status_code == 200:
            return response.json().get("country_name", "Unknown")
        return "Unknown"
    except requests.RequestException:
        return "Unknown"

def get_user_country():
    try:
        response = requests.get("https://ipapi.co/json/")
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("ip", "Unknown"), user_data.get("country_name", "Unknown")
        return "Unknown", "Unknown"
    except requests.RequestException:
        return "Unknown", "Unknown"

def is_obfuscated_script(script_content):
    return bool(re.search(r"[a-zA-Z$_]\s*=\s*function\s*\(.*\)", script_content))

def get_domain_age(domain):
    try:
        w = whois(domain)
        creation_date = w.creation_date
        expiration_date = w.expiration_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        
        domain_age = (expiration_date - creation_date).days
        return creation_date, expiration_date, domain_age, w.get('name', 'Unknown')
    except Exception:
        return None, None, None, 'Unknown'
