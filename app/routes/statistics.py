from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.connection import get_db, engine_url
from sqlalchemy import Table, MetaData
from ..schemas.statistics import UserStatisticsResponse

from sqlmodel import select
from ..models import UserStatistics  # 실제 뷰 모델 import (적절히 수정)


# Define the metadata and UserStatistics table for querying the view
# metadata = MetaData()
# UserStatistics = Table('UserStatistics', metadata, autoload_with=engine_url)

statistics_router = APIRouter(prefix='/statistics', tags=["Statistics"])

# # 사용자 통계 API
# @statistics_router.get("/get_user_statistics/{user_id}", response_model=UserStatisticsResponse)
# async def get_user_statistics(user_id: str, db: Session = Depends(get_db)):
#     # UserStatistics 뷰를 직접 쿼리하여 결과를 가져옴
#     user_stat = db.execute(
#         UserStatistics.select().where(UserStatistics.c.user_id == user_id)
#     ).fetchone()

#     if not user_stat:
#         raise HTTPException(status_code=404, detail="User not found")

#     # 튜플에서 값을 인덱스로 접근
#     return {
#         "user_id": user_stat[0],  # user_id는 첫 번째 요소
#         "average_rating": float(user_stat[1]),  # Decimal 값을 float로 변환하여 반환
#         "total_reviews": user_stat[2]  # total_reviews는 세 번째 요소
#     }

@statistics_router.get("/get_user_review_statistics/{user_id}", response_model=UserStatisticsResponse)
async def get_user_review_statistics(user_id: str, db: Session = Depends(get_db)):
    # 총 사용자 통계 조회 후 리뷰 수 기준으로 내림차순 정렬
    query = select(UserStatistics).order_by(UserStatistics.total_reviews.desc())  # UserStatistics의 컬럼을 명시적으로 선택
    total_reviews = db.execute(query).fetchall()  # 모든 사용자의 통계를 가져옵니다

    # 특정 사용자 통계 조회
    user_stat_query = select(UserStatistics).where(UserStatistics.user_id == user_id)  # 'user_id'를 정확히 필드로 사용
    user_stat_tuple = db.execute(user_stat_query).fetchone()
    print(user_stat_tuple)
    if not user_stat_tuple:
        raise HTTPException(status_code=404, detail="User not found")

    user_stat = user_stat_tuple[0]

    print(user_stat)
    # user_stat을 튜플에서 값을 추출 (인덱스로 접근)
    user_stat_dict = {
        "user_id": user_stat.user_id,  # 튜플에서 첫 번째 값(user_id)
        "average_rating": float(user_stat.average_rating),  # 두 번째 값(average_rating)
        "total_reviews": user_stat.total_reviews  # 세 번째 값(total_reviews)
    }

    # 사용자 순위 계산
    user_rank = next((index for index, value in enumerate(total_reviews) if value[0] == user_id), -1)

    if user_rank == -1:
        raise HTTPException(status_code=404, detail="User not found in total reviews")

    total_users = len(total_reviews)
    percentile = (user_rank / total_users) * 100

    # 로그 출력 (디버깅)
    print({
        "user_id": user_stat_dict["user_id"],
        "average_rating": user_stat_dict["average_rating"],
        "total_reviews": user_stat_dict["total_reviews"],
        "percentile": percentile
    })

    return {
        "user_id": user_stat_dict["user_id"],
        "average_rating": user_stat_dict["average_rating"],
        "total_reviews": user_stat_dict["total_reviews"],
        "percentile": percentile
    }
