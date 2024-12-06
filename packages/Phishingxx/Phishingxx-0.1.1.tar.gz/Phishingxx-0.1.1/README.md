# Phishingxx - Phishing Detection Library

`Phishingxx`는 URL 피싱 여부를 탐지하는 Python 라이브러리입니다. 동적 크롤링 및 머신러닝 모델을 기반으로 피싱 사이트를 판별합니다.

## 주요 기능
- URL 유효성 검사
- 도메인/IP 정보 및 WHOIS 데이터 분석
- iframe, AJAX 호출 등 동적 분석
- XGBoost 기반 피싱 판별
- SHAP 기여도 분석

## 설치 방법
아래 명령어로 라이브러리를 설치할 수 있습니다:
```bash
pip install Phishingxx
```

## 설치 방법
아래 명령어로 라이브러리를 설치할 수 있습니다:
```python
from bisanggu.analyzer import crawl_website

headers = {'User Agent 기입'}

url = "검증 URL 기입"
result = crawl_website(url, headers)

# 예측 수행
if result:
    print(f'URL: {url}, RESULT: 피싱 사이트')
else:
    print(f'URL: {url}, RESULT: 안전 사이트')
```

## 개발자
중부대학교 정보보안S/W융합전공 정진호, 박우경, 이하영, 최수민, 홍준희
