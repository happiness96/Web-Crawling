# -*- encoding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
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
def get_text() -> None:
    # pandas 모듈을 사용하게 되면 pandas에서 제공하는 DataFrame 객체의 형태로 저장하고 읽어들일 수 있다.
    # DataFrame에 저장할 각 행을 리스트 형태로 df_list에 담는다.
    df_list = []

    # 첫 번째 행에 해당하는 요소들을 title_list에 담을 것이다.
    title_list = []

    for page_num in tqdm(range(1, 6771), desc='문서 크롤링 진행중'):
        # 크롤링 할 홈페이지의 주소를 url 변수에 담는다.
        url = 'https://icis.me.go.kr/chmCls/chmClsView.do?hlhsn_sn=' + str(page_num)

        # BeautifulSoup 객체 생성
        # urlopen 함수를 통해 지정한 주소에 접근할 수 있다.
        # parser의 종류는 기본적으로 BeautifulSoup에서 제공하는 html.paser을 사용한다.
        # 별도의 설치를 통해 웹 페이지의 해석 속도가 매우 빠른 lxml을 사용할 수 있다.
        obj = BeautifulSoup(urlopen(url), 'lxml')

        if page_num == 1:
            # find_all 함수에 두 개의 파라미터가 들어가있다.
            # 첫 번째 파라미터는 메타 태그, 두 번째 파라미터는 class name이다.
            for item in obj.find_all('div', 's_title'):
                title_list.append(filtering(str(item.find_all(text=True)), '[A-Za-z0-9가-힣]+'))

        row_list = []
        for item in obj.find_all('td', 'td_left td_wrap_max'):
            row_list.append(filtering(str(item.find_all(text=True)), '[가-힣]+'))

        df_list.append(row_list)

    # pandas 모듈의 DataFrame 객체를 통해 csv 파일에 입력할 데이터 프레임을 만든다.
    # 이 때, 첫 행은 columns로 각 열에 대한 정보를 표시할 수 있다.
    df = pd.DataFrame(df_list, columns=title_list)

    # 간단하게 to_csv 함수로 경로를 지정해주면 csv 파일로 변환시켜준다.
    # 그냥 변환시키면 자동으로 각 행에 대한 인덱스가 0부터 지정된다.
    # 이를 제거하려면 index 속성을 False로 준다. 필요에 따라 True 혹은 리스트로 지정해줄 수 있다.
    df.to_csv('D:\crawling\crawling_pandas_data.csv', index=False, encoding='utf-16', sep='\t')


if __name__ == '__main__':
    get_text()
