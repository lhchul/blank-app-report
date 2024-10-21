import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# matplotlib 및 scikit-learn 라이브러리 오류 처리
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    st.error("❌ 'matplotlib' 라이브러리가 설치되지 않았습니다. "
             "아래 명령어를 실행해 설치하세요:\n\n"
             "`pip install matplotlib`")
    st.stop()  # 앱 실행 중단

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer
except ModuleNotFoundError:
    st.error("❌ 'scikit-learn' 라이브러리가 설치되지 않았습니다. "
             "아래 명령어를 실행해 설치하세요:\n\n"
             "`pip install scikit-learn`")
    st.stop()  # 앱 실행 중단

# 유사한 통합국명 찾기 함수
def find_similar_location(input_name, locations):
    vectorizer = CountVectorizer().fit_transform([input_name] + list(locations))
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    most_similar_index = cosine_sim.argmax()
    return locations[most_similar_index]

# Streamlit 앱 타이틀
st.title("온도 데이터 대시보드")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요:", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기
    data = pd.read_csv(uploaded_file)

    # 통합국명 입력받기
    user_input = st.text_input("통합국명을 입력하세요:")

    if user_input:
        # 유사한 통합국명 찾기
        unique_locations = data['통합국명'].unique()
        most_similar_location = find_similar_location(user_input, unique_locations)

        # 해당 통합국명의 데이터 필터링
        filtered_data = data[data['통합국명'] == most_similar_location]

        # 가장 최근 온도와 날짜 추출
        latest_record = filtered_data.sort_values(by='날짜', ascending=False).iloc[0]
        latest_temp = latest_record['온도']
        latest_date = latest_record['날짜']

        # 일주일 전 데이터 필터링
        one_week_ago = datetime.now() - timedelta(days=7)
        week_ago_data = filtered_data[pd.to_datetime(filtered_data['날짜']) >= one_week_ago]

        # 일주일 최고/최저 온도 계산
        max_temp = week_ago_data['온도'].max

