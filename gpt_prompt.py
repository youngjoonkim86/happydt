import openai
import os
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(df: pd.DataFrame) -> str:
    prompt = (
        "당신은 로또 분석 전문가입니다. 최근 20회차 로또 데이터를 기반으로 "
        "100가지 분석 로직을 종합하여 다음 회차에 추천 가능한 번호 5세트를 제시해주세요.\n\n"
        "아래는 최근 20회차 로또 번호입니다:\n\n"
    )
    recent = df.sort_values("회차", ascending=False).head(20)
    prompt += recent[["회차", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]].to_string(index=False)
    prompt += "\n\n결과 형식은 다음과 같아야 합니다:\n1) 3, 11, 22, 30, 33, 41\n..."
    return prompt

def get_recommendations(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']
