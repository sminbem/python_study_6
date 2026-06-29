import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')


region_mask = df["통합 분류1"].notna() & df["통합 분류1"].str.contains("지역")
# 지역 관련 뉴스만 추출
df_region = df[region_mask].copy()
# 복사본 생성

df_region['상세지역'] = df_region['통합 분류1'].apply(
    lambda x: x.split('-')[-1].strip() if '-' in str(x) else x.strip()
)
# 1회용 함수 람다
# lambda x: [조건이 참일 때 매수] if [조건식] else [조건이 거짓일 때 매수]

print("=== [콘솔 확인] 1. 추출된 상세지역 상위 빈도수 ===")
print(df_region['상세지역'].value_counts(),
      f"\n 상세지역은 총 {len(df_region['상세지역'].value_counts())}개")
print("====================================================\n")


df_region['키워드'] = df_region['키워드'].fillna('')
# 빈문자열이라도 삽입 


from collections import Counter
# 어떤 요소가 몇 개씩 들어있는지 계산하여 딕셔너리 형태로 반환

# 키워드 칼럼에서 키워드 순위 10
# 정의 순서 주의
def get_top_10_keywords(series):
   
    all_text = " ".join(series.astype(str))    
    words = [word.strip() for word in all_text.replace(',', ' ').split() if word.strip()]
    
  
    top_10 = [item[0] for item in Counter(words).most_common(10)]
    
    return top_10


summary_df = df_region.groupby('상세지역').agg(
    뉴스빈도수=('상세지역', 'count'),
    키워드순=('키워드', get_top_10_keywords)
).sort_values(by='뉴스빈도수', ascending=False)


"""
print("=== [콘솔 확인] 4. 상세지역별 통합 키워드 순위  ===")
print(summary_df)
print("\n----------------------------------------------------")
print("데이터프레임 정보 및 타입 확인:")
print(summary_df.info())
print("====================================================\n")
"""

stopwords = ['노인', '노인들', '지역', '주민', '사회', 
             '사업', '행사', '전달', '지원', '추진', '시설', '운영', '회장', '참석', '활동', 
             '사랑']

#지역명도 제거
regions = set(df_region['상세지역'].unique())
stopwords.update(regions)

print(stopwords)