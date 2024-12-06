from phishingxxx.analyzer import crawl_website

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15'
}

url = "https://www.naver.com"
blocked = crawl_website(url, headers)

# 예측 수행
if blocked:
    print(f'URL: {url}, RESULT: 피싱 사이트')
else:
    print(f'URL: {url}, RESULT: 안전 사이트')
