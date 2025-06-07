from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import os, requests
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
API_KEY = os.getenv("GEMINI_API_KEY")

# 현재 건강 상태 평가용 모델
class DogDailyStatus(BaseModel):
    breed: str
    age_months: int
    weight_kg: float
    walk_km: float  # 오늘 산책 거리

# 월말 리포트 평가용 모델 (나이 포함)
class DogMonthlyStatus(BaseModel):
    breed: str
    age_months: int
    weights: List[float] = Field(..., min_items=31, max_items=31)
    walk_distances: List[float] = Field(..., min_items=31, max_items=31)
    anxiety_scores: List[float] = Field(..., min_items=31, max_items=31)

# Gemini 호출 함수 (3~4줄 요약 요청 포함)
def call_gemini(prompt: str):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    body = {
        "contents": [{"parts": [{"text": prompt + "\n\n결과는 핵심만 3~4줄로 요약해줘."}]}]
    }
    response = requests.post(url, headers=headers, params=params, json=body)
    return {
        "solution": response.json()["candidates"][0]["content"]["parts"][0]["text"]
    }

# 현재 건강 상태 평가 API
@app.post("/check_health")
def check_health(info: DogDailyStatus):
    prompt = f"""
    다음은 오늘 강아지의 건강 상태입니다:

    - 품종: {info.breed}
    - 나이: {info.age_months}개월
    - 체중: {info.weight_kg}kg
    - 오늘 산책 거리: {info.walk_km}km

    위 정보를 바탕으로 현재 건강 상태를 평가하고, 관리 팁을 제시해줘.
    """
    return call_gemini(prompt)

# 월말 평가 API
@app.post("/monthly_report")
def monthly_report(data: DogMonthlyStatus):
    prompt = f"""
    다음은 나이 {data.age_months}개월 된 강아지 {data.breed}의 한 달간 건강 기록입니다:

    - 하루별 체중 변화 (kg): {data.weights}
    - 하루별 산책 거리 변화 (km): {data.walk_distances}
    - 하루별 불안도 변화 (0.0 ~ 1.0): {data.anxiety_scores}

    이 정보를 기반으로 한 달간의 변화 경향을 분석하고, 건강 상태를 평가해줘.
    """
    return call_gemini(prompt)

