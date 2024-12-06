import re
from urllib.parse import urlparse
import requests
from whois import whois
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 셀레니움 설정 (헤드리스 모드로 브라우저 실행)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# URL에서 특수 문자가 있는지 확인하고 제거하는 함수
def clean_url(url):
    # 유효하지 않은 문자를 제거
    url = re.sub(r'[^\x00-\x7F]+', '', url)
    return url

# URL 유효성 검사 함수
def is_valid_url(url):
    try:
        result = urlparse(url)
        # URL에 scheme(http/https)과 netloc이 있어야 유효
        if not all([result.scheme, result.netloc]):
            return False
        # 도메인 길이 체크
        domain = result.netloc
        if len(domain) > 253:  # 도메인 길이 제한 (IDNA 인코딩 시 한계)
            return False
        # 유효하지 않은 문자를 제거
        if re.search(r'[^\x00-\x7F]', url):
            return False
        # 두 개 이상의 점을 포함하는 URL 무효화
        if '..' in domain:
            print(f"Skipping URL due to consecutive dots: {url}")
            return False
        return True
    except ValueError:
        return False

def ensure_url_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def get_country_by_ip(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/23228bdbb77b8b")
        if response.status_code == 200:
            country = response.json().get("country_name", "Unknown")
            return country
        else:
            return "Unknown"
    except requests.RequestException as e:
        print(f"Error retrieving country for IP {ip_address}: {e}")
        return "Unknown"

def get_user_country():
    try:
        response = requests.get("https://ipapi.co/json/")
        if response.status_code == 200:
            user_data = response.json()
            user_ip = user_data.get("ip", "Unknown")
            user_country = user_data.get("country_name", "Unknown")
            return user_ip, user_country
        else:
            return "Unknown", "Unknown"
    except requests.RequestException as e:
        print(f"Error retrieving user IP and country: {e}")
        return "Unknown", "Unknown"

def is_obfuscated_script(script_content):
    return bool(re.search(r"[a-zA-Z$_]\s*=\s*function\s*\(.*\)", script_content))

# 도메인 만료일과 생성일을 확인하는 함수 (WHOIS 데이터 기반)
def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        expiration_date = w.expiration_date
        registrant_name = w.get('name', 'Unknown')  # 등록자 정보

        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if creation_date is None or expiration_date is None:
            return None, None, None, registrant_name

        domain_age_days = (expiration_date - creation_date).days
        return creation_date, expiration_date, domain_age_days, registrant_name

    except Exception as e:
        print(f"Error retrieving WHOIS information for {domain}: {e}")
        return None, None, None, 'Unknown'

# 난독화된 JavaScript 코드 확인 함수
def is_obfuscated_script(script_content):
    return bool(re.search(r"[a-zA-Z$_]\s*=\s*function\s*\(.*\)", script_content))

# URL이 스킴(프로토콜)을 포함하는지 확인하고 없으면 https:// 추가
def ensure_url_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

# 동적 iframe 크롤링
def crawl_website_with_selenium(url):
    try:
        # 셀레니움으로 브라우저 실행
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        # 자바스크립트가 실행된 후의 DOM을 가져옴
        page_source = driver.page_source
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(page_source, 'html.parser')

        # iframe 태그 분석 (동적으로 추가된 iframe 포함)
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        hidden_iframes = sum(1 for iframe in iframes if iframe.get_attribute('style') == 'display:none;' or iframe.get_attribute('width') == '0')

        # 콘텐츠 크기 계산 (HTML 크기)
        content_size = len(page_source)

        # 브라우저 종료
        driver.quit()

        return hidden_iframes, content_size

    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return None, None

# 웹사이트 동적 분석 (AJAX, 쿠키 설정, 스크립트 실행 등 확인)
def analyze_website(url):
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
        driver.set_page_load_timeout(10)
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
        print(f"Error analyzing {url}: {e}")
    finally:
        driver.quit()

    return dynamic_analysis
