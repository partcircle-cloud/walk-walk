from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import httpx
import os

from database import init_db, get_db, WalkRecord
from models import WalkCreate, WalkResponse, WeatherResponse

app = FastAPI(title="산책산책 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 초기화
@app.on_event("startup")
def startup_event():
    init_db()

# 날씨 API
@app.get("/api/weather", response_model=WeatherResponse)
async def get_weather(lat: float = 37.5665, lng: float = 126.9780):
    """OpenWeatherMap API 호출"""
    API_KEY = '0f50d979150498a3e3da7a6b2daea2f5'
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://api.openweathermap.org/data/2.5/weather',
                params={
                    'lat': lat,
                    'lon': lng,
                    'appid': API_KEY,
                    'units': 'metric',
                    'lang': 'kr'
                },
                timeout=5.0
            )
            
            if response.status_code == 200:
                data = response.json()
                temp = round(data['main']['temp'], 1)
                condition = data['weather'][0]['description']
                
                # 날씨 아이콘 매핑
                weather_id = data['weather'][0]['id']
                if weather_id < 300:
                    icon = '⛈️'
                elif weather_id < 600:
                    icon = '🌧️'
                elif weather_id < 700:
                    icon = '❄️'
                elif weather_id < 800:
                    icon = '🌫️'
                elif weather_id == 800:
                    icon = '☀️'
                else:
                    icon = '☁️'
                
                return WeatherResponse(temp=temp, condition=condition, icon=icon)
    except Exception as e:
        print(f'날씨 API 에러: {e}')
    
    # 기본값 반환
    return WeatherResponse(temp=18.0, condition='맑음', icon='☀️')

# 산책 기록 생성
@app.post("/api/walks", response_model=WalkResponse)
def create_walk(walk: WalkCreate, db: Session = Depends(get_db)):
    """새로운 산책 기록 저장"""
    db_walk = WalkRecord(
        duration=walk.duration,
        distance=walk.distance,
        steps=walk.steps
    )
    db.add(db_walk)
    db.commit()
    db.refresh(db_walk)
    return db_walk

# 산책 기록 전체 조회
@app.get("/api/walks", response_model=List[WalkResponse])
def get_walks(db: Session = Depends(get_db)):
    """모든 산책 기록 조회 (최신순)"""
    walks = db.query(WalkRecord).order_by(WalkRecord.date.desc()).all()
    return walks

# 산책 기록 삭제
@app.delete("/api/walks/{walk_id}")
def delete_walk(walk_id: int, db: Session = Depends(get_db)):
    """특정 산책 기록 삭제"""
    walk = db.query(WalkRecord).filter(WalkRecord.id == walk_id).first()
    if not walk:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
    
    db.delete(walk)
    db.commit()
    return {"message": "삭제되었습니다", "id": walk_id}

# 최근 기록 1개
@app.get("/api/walks/recent", response_model=WalkResponse)
def get_recent_walk(db: Session = Depends(get_db)):
    """가장 최근 산책 기록"""
    walk = db.query(WalkRecord).order_by(WalkRecord.date.desc()).first()
    if not walk:
        raise HTTPException(status_code=404, detail="기록이 없습니다")
    return walk

@app.get("/")
def root():
    return {"message": "산책산책 API 🌿", "status": "running"}