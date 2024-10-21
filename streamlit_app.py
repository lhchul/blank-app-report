import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 유사한 통합국명 찾기 함수
def find_similar_location(input_name, locations):
    vectorizer = CountVectorizer().fit_transform([input_name] + 
    vectorizer = CountVectorizer().fit_transform([input_name] + lis

    vectorizer = CountVectorizer
list(locations))
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors[
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similari

    vectors = vectorizer.toarray()
    cosin

    vectors = vectorizer.toarray

    vectors = vect

   
0:1], vectors[1:]).flatten()
    most_similar_index = cosine_sim.argmax()
    
    most_similar_index = cosine_sim.argmax()
    

    most_similar_index = cosine_sim.argma

    most_similar_index =

    most_simila
return locations[most_similar_index]

# Streamlit 인터페이스 구성
st.title(
st.title(

st
"온도 데이터 대시보드")

# CSV 파일 업로드
uploaded_file = st.file_uploader(
uploaded_file = st.file_upl

uploaded_file = st.fi

uploade

u
"CSV 파일을 업로드하세요:", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기
    data = pd.read_csv(uploaded_file)

    
    data = pd.read_csv(uploaded

    data = pd.read_c

    data = pd

 
# 통합국명 입력받기
    user_input = st.text_input(
    user_input = st.text_i

    user_input = st

    user_in
"통합국명을 입력하세요:")

    

  
if user_input:
        # 유사한 통합국명 찾기
        unique_locations = data[
        unique_locat

     
'통합국명'].unique()
        most_similar_location = find_similar_location(user_input, unique_locations)

        
        most_similar_location = find_similar_location(user_input, unique_locatio

        most_similar_location = find_similar_location(user_input, unique_loc

        most_similar_location = find_similar_location(user_input, u

        most_similar_location = find_similar_location(user_inpu

        most_similar_location = find_similar_location(

        most_similar_location = find_simila

        most_similar_location = find_s

        most_similar_locat

        most_similar_

        most_sim

        mo
# 해당 통합국명의 데이터 필터링
        filtered_data = data[data[
        filtered_data = da

        filtere
'통합국명'] == most_similar_location]

        

     
# 가장 최근 온도와 날짜 추출
        latest_record = filtered_data.sort_values(by=
        latest_record = filtered_da

        latest_record = filtered

        latest_record = filte

        latest_record = fi

        latest_record 

        latest

        la

      

  
'날짜', ascending=False).iloc[0]
        latest_temp = latest_record[
        latest_temp = latest_record

        latest_te

        latest
'온도']
        latest_date = latest_record[
        latest_date = latest_record

        latest_date
'날짜']

        

       
# 일주일 전 데이터 필터링
        one_week_ago = datetime.now() - timedelta(days=
        one_week_ago = datetime.now() - timedelta(d

        one_week_ago = datetime.now() -

        one_week_ago = datetime.

        one_week_ago

        one_week

     
7)
        week_ago_data = filtered_data[pd.to_datetime(filtered_data[
        week_ago_data = filtered_data[pd.to_datetime(filtered_data

        week_ago_data = filtered_data[pd.to_dat

        week_ago_data = filtered_data[p

        week_ago_data 

        week_ago

        w

 
'날짜']) >= one_week_ago]

        # 일주일 최고/최저 온도 계산
        max_temp = week_ago_data[
        max_temp = week_ago_data

        max_temp = week_ag

        max_temp = 

     
'온도'].max()
        min_temp = week_ago_data[
        min_temp = week_ago_dat

        min_temp = week_ago_

        min_temp = week_

       
'온도'].min()

        # 일주일 최고 온도 트렌드 계산
        max_temp_trend = week_ago_data.groupby(
        max_temp_trend = wee

        max_temp_trend
'dt')['온도'].max()

        # 결과 출력
        st.write(f"📍 가장 유사한 통합국명: {most_similar_location}")
        st.write(
  
f"🌡️ 가장 최근 온도: {latest_temp}°C (측정일: {latest_date})")
        st.write(
        st.writ
f"🔺 일주일 최고 온도: {max_temp}°C")
        st.write(
        st.w

    
f"🔻 일주일 최저 온도: {min_temp}°C")

        

       
# 일주일 최고 온도 트렌드 그래프 시각화
        fig, ax = plt.subplots(figsize=(
        fig, ax = plt.subplots(figsize=(

        fig, ax = plt.subplots(

        fig, ax = plt
10, 5))
        ax.plot(max_temp_trend.index.astype(
        ax.plot(max_temp_trend.index.astype(

        ax.plot(max_temp_trend.index.a

        ax.plot(max_temp

        ax.plot(m
str), max_temp_trend.values, marker='o', linestyle='-', linewidth=2)
        ax.set_title(
        ax.set_title

        ax.s

 
f"'{most_similar_location}' 지역의 일주일 최고 온도 추이", fontsize=15)
        ax.set_xlabel(
        ax.set_xla

        a
'날짜', fontsize=12)
        ax.set_ylabel(
       
'최고 온도 (°C)', fontsize=12)
        plt.xticks(rotation=
        plt.xticks(rotat

        plt.xti
45)  # 날짜 보기 좋게 회전
        plt.grid(
        plt.g
True)

        # 그래프 출력
        st.pyplot(fig)

        st.pyplot(fig

        st.pyp
