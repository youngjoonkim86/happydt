import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# API Key는 보안상 .env로 옮겨도 좋음
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="🎯 로또 전문가 GPT", layout="centered")
st.title("💡 로또 번호 추천 by Groq LLM")

prompt = (
    "너는 한국 로또 분석 전문가야. 지금부터 1000가지 분석 기준과 전략을 종합해서 "
    "다음 회차에 추천할 6자리 로또 번호 조합 5세트를 제시해줘.\n\n"
    "분석 기준 예시:\n"
    "1. 최근 20회차 출현 빈도\n"
    "2. 미출현 번호\n"
    "3. 연속 번호 여부\n"
    "4. 홀짝 비율 (3:3 등)\n"
    "5. 구간 분포\n"
    "6. 고정수/제외수\n"
    "7. 번호 간 거리\n"
    "8. 평균값/중앙값 등 통계\n"
    "...\n"
    "그리고 나머지 약 1000가지 조건도 함께 고려해줘.\n\n"
    "출력 형식은 아래와 같아야 해:\n"
    "1) 5, 12, 19, 27, 34, 41\n"
    "2) 3, 7, 18, 25, 36, 43\n"
    "..."
)

if st.button("🎲 번호 추천받기"):
    with st.spinner("AI가 분석 중입니다..."):
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # 또는 llama3-8b-8192 등
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500,
            stream=False,
        )
        result = completion.choices[0].message.content
        st.success("추천이 완료되었습니다!")
        st.markdown(f"### 🧠 GPT 추천 번호\n{result}")
