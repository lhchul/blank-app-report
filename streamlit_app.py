import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 유사한 통합국명 찾기 함수
def find_similar_location(input_name, locations):
    vectorizer = CountVectorizer().fit_transform([input_name] + list(locations))
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    most_similar_index = cosine_sim.argmax()
    return locations[most_similar_index]

# Streamlit 인터페이스 구성
st.title("통합국명 기반 온도 분석 대시보드")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기
    data = pd.read_csv(uploaded_file)

    # 모든 통합국명 리스트 생성
    unique_locations = data['통합국명'].unique()

    # 통합국명 선택 입력 (셀렉트박스 제공)
    user_input = st.selectbox("통합국명을 선택하거나 직접 입력하세요:", unique_locations, index=0)

    # 직접 입력 옵션
    manual_input = st.text_input("직접 입력하려면 여기에 통합국명을 입력하세요:")

    # 입력된 값을 우선 처리
    selected_location = manual_input if manual_input else user_input

    if selected_location:
        # 유사한 통합국명 찾기
        most_similar_location = find_similar_location(selected_location, unique_locations)

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
        max_temp = week_ago_data['온도'].max()
        min_temp = week_ago_data['온도'].min()

        # 일주일 최고 온도 TREND 계산
        max_temp_trend = week_ago_data.groupby('dt')['온도'].max()

        # 결과 출력
        st.write(f"📍 가장 유사한 통합국명: {most_similar_location}")
        st.write(f"🌡️ 가장 최근 온도: {latest_temp}°C (측정일: {latest_date})")
        st.write(f"🔺 일주일 최고 온도: {max_temp}°C")
        st.write(f"🔻 일주일 최저 온도: {min_temp}°C")

        # 일주일 최고 온도 트렌드 그래프 시각화
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(max_temp_trend.index.astype(str), max_temp_trend.values, marker='o', linestyle='-', linewidth=2)
        ax.set_title(f"'{most_similar_location}' 지역의 일주일 최고 온도 추이", fontsize=15)
        ax.set_xlabel('날짜', fontsize=12)
        ax.set_ylabel('최고 온도 (°C)', fontsize=12)
        plt.xticks(rotation=45)  # 날짜 보기 좋게 회전
        plt.grid(True)

        # 그래프 출력
        st.pyplot(fig)

