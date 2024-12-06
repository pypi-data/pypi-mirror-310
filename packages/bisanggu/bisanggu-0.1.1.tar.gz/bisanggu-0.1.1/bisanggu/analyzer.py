from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import requests
import time
import socket
import dns.resolver
from .utils import clean_url, is_valid_url, ensure_url_scheme, is_obfuscated_script, get_country_by_ip, get_user_country, get_domain_age

# 셀레니움 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def analyze_dynamic_content(url):
    """Analyze dynamic content using Selenium."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    dynamic_analysis = {
        'redirection_count': 0,
        'external_domain_requests': 0,
        'malicious_file_downloads': 0,
        'script_execution_count': 0,
        'iframe_present': False,
        'ajax_calls': 0,
        'cookie_settings': 0
    }
    try:
        driver.get(url)

        # iFrame 감지
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        dynamic_analysis['iframe_present'] = len(iframes) > 0

        # AJAX 호출 감지
        dynamic_analysis['ajax_calls'] = len(driver.find_elements(By.XPATH, "//script[contains(text(), 'XMLHttpRequest')]"))

        # 쿠키 설정 감지
        if 'document.cookie' in driver.page_source:
            dynamic_analysis['cookie_settings'] += 1

        # 스크립트 실행 감지
        dynamic_analysis['script_execution_count'] = len(driver.find_elements(By.TAG_NAME, 'script'))

    except Exception as e:
        print(f"Dynamic content analysis failed for {url}: {e}")
    finally:
        driver.quit()
    return dynamic_analysis

def crawl_website(url, headers):
    url = clean_url(url)
    if not is_valid_url(url):
        print(f"Invalid URL: {url}. Skipping this URL.")
        return None

    try:
        url = ensure_url_scheme(url)
        start_time = time.time()

        response = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
        redirect_count = 0
        final_url = url

        if 300 <= response.status_code < 400:
            final_url = response.headers['Location']
            redirect_count = 1
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        loading_time = time.time() - start_time
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # 1. IP 주소 확인
        ip_address = socket.gethostbyname(domain) if domain else None
        country = get_country_by_ip(ip_address) if ip_address else 'Unknown'
        user_ip, user_country = get_user_country()
        countries_match = 'Yes' if user_country == country else 'No'

        # 2. 도메인 연령 및 등록자 정보
        creation_date, expiration_date, domain_age, registrant_name = get_domain_age(domain)

        # 3. 서브 도메인 수
        subdomain_count = len(domain.split('.')) - 2 if domain else 0

        # 4. iframe 태그 분석 및 콘텐츠 크기
        hidden_iframe_count = len(soup.find_all('iframe', style=lambda x: 'display:none' in x or 'width:0' in x)) if soup else 0
        content_size = len(response.content)

        # 5. 스크립트 태그 분석
        script_tags = soup.find_all('script')
        total_script_length = sum(len(script.text) for script in script_tags)
        obfuscated_script_length = sum(len(script.text) for script in script_tags if is_obfuscated_script(script.text))
        obfuscation_ratio = (obfuscated_script_length / total_script_length) if total_script_length > 0 else 0
        is_obfuscated = any(is_obfuscated_script(script.text) for script in script_tags)
        script_count = len(script_tags)

        # 6. 기타 요소 분석
        meta_redirect = len(soup.find_all('meta', attrs={"http-equiv": "refresh"}))
        window_redirect = any('window.location' in script.text for script in script_tags)
        ajax_calls = sum(1 for script in script_tags if 'XMLHttpRequest' in script.text or 'fetch' in script.text)
        ssl_used = url.startswith('https')
        cookie_access = any('document.cookie' in script.text for script in script_tags)
        favicon = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
        x_frame_options = response.headers.get('X-Frame-Options', None)

        # SPF 설정 확인
        spf = False
        try:
            spf_records = dns.resolver.resolve(domain, 'TXT')
            spf = any("v=spf1" in str(record) for record in spf_records)
        except Exception:
            pass

        # TXT 레코드 확인
        txt = False
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            txt = len(txt_records) > 0
        except Exception:
            pass

        # HTML 언어 설정
        html_tag = soup.find("html")
        lang = bool(html_tag.get("lang")) if html_tag else False

        # 텍스트와 이미지 비율
        images = soup.find_all("img")
        texts = soup.get_text().strip().split()
        text_image_ratio = len(texts) / len(images) if len(images) > 0 else len(texts)

        # 동적 분석
        dynamic_analysis = analyze_dynamic_content(url)

        result = {
            'URL': url,
            'IP Address': ip_address,
            'Country': country,
            'User Country': user_country,
            'Countries Match': countries_match,
            'Domain Age (days)': domain_age,
            'Creation Date': creation_date,
            'Expiration Date': expiration_date,
            'Registrant Name': registrant_name,
            'Subdomain Count': subdomain_count,
            'Hidden Iframe Count': hidden_iframe_count,
            'Total Script Length': total_script_length,
            'Obfuscated Script Length': obfuscated_script_length,
            'Obfuscation Ratio': obfuscation_ratio,
            'Is Obfuscated': is_obfuscated,
            'Script Count': script_count,
            'Meta Redirect': meta_redirect,
            'Window Location Redirect': window_redirect,
            'AJAX Call Count': ajax_calls,
            'SSL Used': ssl_used,
            'Cookie Access': cookie_access,
            'Loading Time (s)': loading_time,
            'Content Size (bytes)': content_size,
            'Redirect Count': redirect_count,
            'Final URL': final_url,
            'redirection_count': dynamic_analysis['redirection_count'],
            'external_domain_requests': dynamic_analysis['external_domain_requests'],
            'malicious_file_downloads': dynamic_analysis['malicious_file_downloads'],
            'script_execution_count': dynamic_analysis['script_execution_count'],
            'iframe_present': dynamic_analysis['iframe_present'],
            'ajax_calls_dynamic': dynamic_analysis['ajax_calls'],
            'cookie_settings': dynamic_analysis['cookie_settings'],
            'favicon': bool(favicon),
            'x_frame_option': bool(x_frame_options),
            'spf': spf,
            'txt': txt,
            'lang': lang,
            'img_and_text_ratio': text_image_ratio,
        }
        return result
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
