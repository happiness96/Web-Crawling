# -*- encoding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re
from tqdm import tqdm


# 문자열에서 원하는 문자만 필터링하는 함수이다.
def filtering(string: str, regular_expression: str) -> str:
    # 필터링을 위해 re 모듈을 사용하였으며
    # 해당 정규 표현식은 한글만 추출한다.
    # findall 함수는 string에서 정규 표현식에 해당하는 부분을 추출해내며
    # compile 함수를 통해 list 형식으로 반환시켜준다.
    string = re.compile(regular_expression).findall(string)

    # join 함수를 통해 list의 모든 요소들을 공백으로 구분하여 하나의 문자열로 반환한다.
    return ' '.join(string)


# 웹 페이지로부터 데이터를 크롤링한 후 데이터를 csv파일로 저장하는 함수
def get_csv() -> None:
    # 크롤링 후 저장할 csv 파일을 경로로 지정
    # mode를 'w' (write)로 선언
    # newline을 사용하지 않으면 열과 열 사이의 비어있는 열이 하나 생긴다.
    file_name = open('D:\crawling\crawling_data.csv', 'w', encoding='utf-8-sig', newline='')

    # csv 모듈을 사용하여 지정한 파일의 writer 객체를 가져온다.
    wr = csv.writer(file_name)

    for page_num in tqdm(range(1, 6771), desc='문서 크롤링 진행중'):
        # 크롤링 할 홈페이지의 주소를 url 변수에 담는다.
        url = 'https://icis.me.go.kr/chmCls/chmClsView.do?hlhsn_sn=' + str(page_num)
        
        # BeautifulSoup 객체 생성
        # urlopen 함수를 통해 지정한 주소에 접근할 수 있다.
        # parser의 종류는 기본적으로 BeautifulSoup에서 제공하는 html.paser을 사용한다.
        # 별도의 설치를 통해 웹 페이지의 해석 속도가 매우 빠른 lxml을 사용할 수 있다.
        obj = BeautifulSoup(urlopen(url), 'lxml')

        if page_num == 1:
            row_list = []           # csv 파일에 들어갈 열(row) 하나의 리스트이다.

            # find_all 함수에 두 개의 파라미터가 들어가있다.
            # 첫 번째 파라미터는 메타 태그, 두 번째 파라미터는 class name이다.
            for item in obj.find_all('div', 's_title'):
                row_list.append(filtering(str(item.find_all(text=True)), '[A-Za-z0-9가-힣]+'))

            # writerow 함수를 통해 열(row)를 삽입한다.
            wr.writerow(row_list)

        row_list = []
        for item in obj.find_all('td', 'td_left td_wrap_max'):
            row_list.append(filtering(str(item.find_all(text=True)), '[가-힣]+'))

        wr.writerow(row_list)

    file_name.close()


if __name__ == '__main__':
    get_csv()
