# 🗓️ Keystone Schedule

> 수강 스타일을 분석해 최적의 시간표를 자동으로 추천해주는 스마트 시간표 생성기

![Static Badge](https://img.shields.io/badge/version-1.0.0-indigo)
![Static Badge](https://img.shields.io/badge/license-MIT-green)

---

## 📌 프로젝트 소개

Keystone Schedule은 단순한 강의 선택을 넘어, **비선호 교시 · 공강 희망 요일 · 목표 학점 · 수업 배치 스타일**을 입력하면 개인 맞춤 시간표를 자동으로 추천해주는 웹 애플리케이션입니다.

---

## ✨ 주요 기능

- **3단계 위자드 UI** — 스타일 설정 → 강의 선택 → 시간표 추천
- **스마트 추천 알고리즘** — 비선호 교시, 공강, 연강, 목표 학점 등을 종합 점수화
- **충돌 감지** — 시간이 겹치는 강의 조합 자동 제외
- **상위 3개 시간표 비교** — 점수 · 수업일 수 · 공강 현황 한눈에 확인
- **사이버 강의 지원** — 시간 충돌 없이 자유롭게 조합

---

## 🛠️ 기술 스택

| 영역 | 사용 기술 |
|------|-----------|
| Frontend | HTML / CSS / Vanilla JS |
| Backend | Python · FastAPI |
| Data | JSON (부산대학교 강의 데이터) |

---

## 📂 파일 구조

```
keystone-schedule/
├── index.html        # 프론트엔드 (UI + 클라이언트 로직)
├── main.py           # FastAPI 백엔드 서버
├── final_data.json   # 강의 데이터
└── README.md
```

---

## 🚀 실행 방법

### 백엔드 없이 (index.html 단독 실행)
```bash
# index.html과 final_data.json을 같은 폴더에 두고
python -m http.server 8080
# 브라우저에서 http://localhost:8080 접속
```

### 백엔드 포함 실행
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

---

## 👥 팀원

| 이름 | GitHub | 역할 |
|------|--------|------|
| 이선욱 | [@SUNWOOKLEE04](https://github.com/SUNWOOKLEE04) | 추천 알고리즘 설계 및 구현 |
| 이정훈 | [@Irisvt127](https://github.com/Irisvt127) | 데이터 수집 및 정제 |
| 배수진 | [@sinju1021](https://github.com/sinju1021) | 웹 개발 · UI/UX 디자인 |

---

## 📄 라이선스

MIT License
