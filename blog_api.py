import os
import urllib.request
import json
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")


def search_blog(keywords: list[str], length: int = 20, sort='sim'):
    """
    Args:
        keyword (list(str)): 검색어 리스트
        length (int): 검색 결과 개수 (max = 100)
        sort (str): 정렬 기준  (sim: 정확도순으로 내림차순 정렬 / date: 날짜순으로 내림차순 정렬)
    """
    keyword_query = " ".join([f"+{keyword}" for keyword in keywords]) # 해당 키워드들을 모두 포함하는 검색 결과
    encText = urllib.parse.quote(keyword_query)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + str(length) + "&sort=" + sort 
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read().decode('utf-8')
        search_results = json.loads(response_body)
        
        # JSON 형식으로 저장
        # with open('search_results.json', 'w', encoding='utf-8') as file:
        #     json.dump(search_results, file, ensure_ascii=False, indent=4)
        
        return search_results
    else:
        print("Error Code:" + rescode)
        return None
    
def crawl_blog(url: str):
    m_url = "https://m." + url.replace("https://","")
    response = urllib.request.urlopen(m_url)
    soup = BeautifulSoup(response, 'html.parser')
    p_tags = soup.find_all('p', class_=re.compile('se-text-paragraph'))

    result=""
    for p_tag in p_tags:
        text = p_tag.get_text(strip=True)
        if text:  
            result += text
    return result