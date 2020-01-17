import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

if __name__ == '__main__':
    # pandas의 read_csv 함수를 이용하여 DTM 파일을 불러온다.
    dataset = pd.read_csv('D:\crawling\DTM.csv')

    # 각 단어의 빈도수를 나타내는 dictionary를 선언한다. key: 단어, value: 등장 횟수
    frequency = {}

    for word in dataset.columns[1:]:        # columns를 사용하면 0번째 열에 해당하는 값들을 반환해준다.
        frequency[word] = sum(dataset[word])        # sum 함수를 통해 모든 문서를 통틀어 해당 단어가 몇 번 출현했는지 빈도수를 저장할 수 있다.

    black_mage_mask = np.array(Image.open("D:\crawling\Black_Mage.jpg"))

    # 워드 클라우드의 기본 설정을 해준다.
    fp = './utils/NanumGothic.ttf'      # 설정해줄 폰트의 경로 (C:/Windows/Fonts/ 를 참고)
    wc = WordCloud(background_color="white", max_words=100, width=1000, height=800, font_path=fp, mask=black_mage_mask)
    plt.figure(figsize=(15, 15))        # 워드 클라우드 이미지 사이즈를 조절한다.

    wc = wc.generate_from_frequencies(frequency)        # 빈도수에 따라 각 단어의 크기가 결정된다.
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
