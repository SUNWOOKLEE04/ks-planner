import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Set
from pathlib import Path

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "final_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

course_dict: dict = {}
for item in raw_data:
    cid = item.get("class_id")
    if cid and cid not in course_dict:
        course_dict[cid] = item

PDY = 15  # t = day*15 + period  (period 1~14)


class Prefs(BaseModel):
    disliked_periods: List[int] = []  # 1~14
    free_days: List[int] = []         # 0=월 ~ 4=금
    target_credits: int = 18
    style: str = "cluster"            # "cluster" | "spread" | "none"


class Req(BaseModel):
    courses: List[str]
    prefs: Prefs = Prefs()


def estimate_credits(course: dict) -> int:
    return len(course.get("times", []))


def score_schedule(schedule: list, prefs: Prefs) -> dict:
    sc = 100
    used_days: Set[int] = set()
    day_periods: dict = {}
    credits = 0

    disliked = set(prefs.disliked_periods)
    free_days = set(prefs.free_days)

    for course in schedule:
        credits += estimate_credits(course)
        for t in course.get("times", []):
            day    = t // PDY       # ← 수정됨 (기존 t//9 오류)
            period = t % PDY        # ← 수정됨 (기존 t%9 오류)
            used_days.add(day)
            day_periods.setdefault(day, []).append(period)

            if period in disliked:
                sc -= 20

    # 공강 희망 요일
    for d in free_days:
        if d not in used_days:
            sc += 35
        else:
            sc -= 15

    # 목표 학점 근접
    cdiff = abs(credits - prefs.target_credits)
    sc += max(0, 40 - cdiff * 8)

    # 수업일 수 기반 스타일
    if prefs.style == "cluster":
        sc += (5 - len(used_days)) * 18
    elif prefs.style == "spread":
        sc += len(used_days) * 10

    # 연강 보너스
    for periods in day_periods.values():
        periods.sort()
        consecutive = sum(1 for i in range(1, len(periods)) if periods[i] == periods[i-1]+1)
        sc += consecutive * 5

    return {"score": sc, "credits": credits, "day_count": len(used_days)}


@app.get("/api/courses")
def get_courses():
    return {"courses": raw_data}


@app.post("/api/schedule")
def make_schedule(req: Req):
    ids = req.courses
    result = []

    def bt(i, sch, used):
        if len(result) >= 80:
            return
        if i == len(ids):
            info = score_schedule(sch, req.prefs)
            result.append({"schedule": list(sch), **info})
            return

        course = course_dict.get(ids[i])
        if not course:
            bt(i + 1, sch, used)
            return

        times = set(course.get("times", []))
        if not course.get("is_cyber") and not times.isdisjoint(used):
            return

        sch.append(course)
        bt(i + 1, sch, used | times)
        sch.pop()

    bt(0, [], set())
    result.sort(key=lambda x: x["score"], reverse=True)
    return {"data": result[:3]}
