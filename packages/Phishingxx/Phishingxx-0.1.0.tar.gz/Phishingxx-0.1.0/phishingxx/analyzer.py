from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import socket
import dns.resolver
import pandas as pd
import tldextract
from requests.exceptions import SSLError, ConnectionError, Timeout, HTTPError
from selenium import webdriver
import xgboost as xgb
import dns.resolver  # DNS 레코드 조회를 위한 라이브러리
import joblib
from .utils import clean_url, is_valid_url, ensure_url_scheme, is_obfuscated_script, get_country_by_ip, get_user_country, get_domain_age, is_obfuscated_script, ensure_url_scheme, crawl_website_with_selenium, analyze_website
from .models import preprocess_data

# User-Agent 헤더 설정 (403 오류 방지)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15'
}

# 셀레니움 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

model_path = './phishingxx/Phishing_model_02.pkl'
loaded_model = joblib.load(model_path)

def analyze_dynamic_content(url):
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

def crawl_website(url):
    # URL 유효성 검사 및 특수 문자 제거
    url = clean_url(url)
    if not is_valid_url(url):
        print(f"Invalid URL: {url}. Skipping this URL.")
        return

    try:
        url = ensure_url_scheme(url)
        start_time = time.time()  # 로딩 시간 측정 시작

        # 리디렉션을 따라가지 않고 리디렉션 발생 여부 기록
        try:
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
        except UnicodeError as e:
            print(f"Skipping URL due to UnicodeError: {url}. Error: {e}")
            return

        redirect_count = 0
        final_url = url

        # 리디렉션 여부를 감지하고 리디렉션된 URL 기록
        if 300 <= response.status_code < 400:
            final_url = response.headers['Location']
            redirect_count = 1  # 리디렉션 발생한 것으로 간주

        response.raise_for_status()  # HTTP 에러 코드 체크

        # 크롤링 로직
        soup = BeautifulSoup(response.text, 'html.parser')
        loading_time = time.time() - start_time  # 로딩 시간 측정 종료

        parsed_url = tldextract.extract(url)
        domain = parsed_url.domain + '.' + parsed_url.suffix

        # 1. IP 주소 확인
        try:
            ip_address = socket.gethostbyname(domain)
            country = get_country_by_ip(ip_address)  # IP로부터 국가 정보 확인
        except socket.error:
            ip_address = None
            country = 'Unknown'

        # 사용자 국가 정보 가져오기
        user_ip, user_country = get_user_country()

        # 국가 일치 여부 확인
        countries_match = 'Yes' if user_country == country else 'No'

        # 2. 도메인 연령 및 등록자 정보 확인
        creation_date, expiration_date, domain_age, registrant_name = get_domain_age(domain)

        # 3. 서브 도메인 수
        subdomain_count = len(parsed_url.subdomain.split('.')) if parsed_url.subdomain else 0

        # 4. iframe 태그 분석 및 콘텐츠 크기 확인
        hidden_iframe_count, content_size = crawl_website_with_selenium(url)

        # 5. 스크립트 태그 개수 및 난독화 비율 계산
        script_tags = soup.find_all('script')
        total_script_length = sum(len(script.text) for script in script_tags)
        obfuscated_script_length = sum(len(script.text) for script in script_tags if is_obfuscated_script(script.text))

        obfuscation_ratio = (obfuscated_script_length / total_script_length) if total_script_length > 0 else 0
        is_obfuscated = any(is_obfuscated_script(script.text) for script in script_tags)
        script_count = len(script_tags)

        # 리디렉션 기록
        meta_redirect = len(soup.find_all('meta', attrs={"http-equiv": "refresh"}))
        window_redirect = any('window.location' in script.text for script in script_tags)

        # AJAX 호출 확인
        ajax_calls = sum(1 for script in script_tags if 'XMLHttpRequest' in script.text or 'fetch' in script.text)

        # SSL 사용 여부
        ssl_used = url.startswith('https')

        # 쿠키 접근 여부
        cookie_access = any('document.cookie' in script.text for script in script_tags)
        
        # 1. 파비콘 유무
        favicon = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
        
        # 2. X-Frame-Options 헤더의 설정 여부
        x_frame_options = response.headers.get('X-Frame-Options', None)
        
        # 3. SPF(Sender Policy Framework) 설정 여부
        try:
            domain = url.split('//')[-1].split('/')[0]  # 도메인 추출
            spf_records = dns.resolver.resolve(domain, 'TXT')
            spf = any("v=spf1" in str(record) for record in spf_records)
        except Exception:
            spf = False
        
        # 4. TXT 레코드 존재 여부 (DNS 레코드 분석)
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            txt = len(txt_records) > 0
        except Exception:
            txt = False
        
        # 7. 문서 언어 설정 (HTML lang 속성) 유무
        html_tag = soup.find("html")
        if html_tag:
            lang_attr = html_tag.get("lang")
            lang = bool(lang_attr)
        else:
            lang = False  # If no <html> tag is found, we assume the lang attribute is not present
        
        # 8. 페이지 내 텍스트와 이미지 비율
        images = soup.find_all("img")
        texts = soup.get_text().strip().split()
        if texts:
            text_image_ratio = len(texts) / len(images) if len(images) > 0 else len(texts)
        else:
            text_image_ratio = 0

        # 동적 분석 추가
        dynamic_analysis = analyze_website(url)

        # 결과 저장
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
            'x frame option': bool(x_frame_options),
            'spf': spf,
            'txt': txt,
            'lang': lang,
            'img and texts': text_image_ratio,
        }
        
        # 데이터 전처리 후 예측
        df_single_result = pd.DataFrame([result])
        df_processed = preprocess_data(df_single_result)

        # XGBoost 모델 로드 및 예측
        dmatrix = xgb.DMatrix(df_processed)
        prediction = loaded_model.predict(dmatrix)
        
        # 결과 출력
        blocked = bool(prediction[0] > 0.5)  # 0.5 이상의 확률이면 피싱으로 간주
        return blocked
    except (SSLError, ConnectionError, Timeout, HTTPError) as e:
        print(f"Error crawling {url}: {e}")
        return None
