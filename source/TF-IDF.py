# -*- encoding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
# TFIDF를 확인하기 위해 TfidfTransformer을 선언해준다.


if __name__ == '__main__':
    # TFIDF는 DTM으로 확인이 가능하기 때문에 앞전에 만들었던 DTM.csv 파일을 불러온다.
    dataset = pd.read_csv('D:\crawling\DTM.csv')

    # 0번째 열에는 문서 번호가 들어있기 때문에 0번째 열은 pop해준다.
    dataset.pop(dataset.columns[0])

    # fit_transform 함수를 통해 DTM을 TFIDF로 변환할 수 있다.
    tfidf = TfidfTransformer().fit(dataset)

    tf = tfidf.transform(dataset)

    tfidf_array = tf.toarray()       # toarray 함수를 통해 2차원 배열로 만든다.

    # tfidf 배열을 DataFrame 형식으로 변환시킨다.
    tfidf_data_frame = pd.DataFrame(tfidf_array, columns=dataset.columns)

    tfidf_data_frame.to_csv('D:\crawling\TF-IDF.csv', encoding='utf-8-sig')
