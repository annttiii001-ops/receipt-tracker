# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

영수증 사진/PDF를 업로드하면 Upstage Vision LLM이 OCR로 파싱하여 지출 내역을 자동 기록하는 웹앱 (1-day sprint MVP).

기획 문서:
- `PRD_영수증_지출관리앱.md` — 기능 요구사항, 인수 기준, 데이터 스키마
- `프로그램개요서_영수증_지출관리앱.md` — 아키텍처, 기술 스택, 구현 계획

## 기술 스택

**Frontend:** React 18 + Vite 5 + TailwindCSS 3 + Axios  
**Backend:** Python FastAPI + LangChain 0.2 + Upstage Document AI (`document-digitization-vision`)  
**Storage:** JSON 파일 (`backend/data/expenses.json`) — DB 없음  
**Deploy:** Vercel (frontend + serverless backend)

## 개발 명령어

### Frontend (`frontend/` 디렉토리)
```bash
npm install
npm run dev      # Vite 개발 서버 (기본 포트 5173)
npm run build    # 프로덕션 빌드
npm run preview  # 빌드 결과 미리보기
```

### Backend (`backend/` 디렉토리)
```bash
pip install -r requirements.txt
uvicorn main:app --reload        # 개발 서버 (기본 포트 8000)
python main.py                   # 또는 직접 실행
```

### 환경 변수
- `UPSTAGE_API_KEY` — Upstage API 인증 키 (`.env` 파일 또는 Vercel 환경 변수)
- `VITE_API_BASE_URL` — 프론트엔드에서 사용할 백엔드 API 주소

## 아키텍처

```
사용자 → React UI → POST /api/upload
                  → FastAPI → Pillow/pdf2image → Base64 변환
                           → LangChain Chain → Upstage Vision LLM
                           → 구조화된 JSON → expenses.json 저장
                  ← 파싱 결과 응답
```

### API 엔드포인트
| Method | Path | 역할 |
|--------|------|------|
| POST | `/api/upload` | 영수증 업로드 → OCR 파싱 |
| GET | `/api/expenses` | 전체 지출 목록 (날짜 필터 선택) |
| GET | `/api/expenses/{id}` | 단건 조회 |
| PUT | `/api/expenses/{id}` | 수정 |
| DELETE | `/api/expenses/{id}` | 삭제 |
| GET | `/api/summary` | 집계 통계 (월별, 카테고리별) |

### 데이터 스키마 (`expenses.json`)
```json
{
  "id": "uuid-v4",
  "created_at": "ISO8601",
  "store_name": "string",
  "receipt_date": "YYYY-MM-DD",
  "receipt_time": "HH:MM",
  "category": "식료품|외식|교통|쇼핑|의료|기타",
  "items": [{ "name", "quantity", "unit_price", "total_price" }],
  "subtotal": number,
  "discount": number,
  "tax": number,
  "total_amount": number,
  "payment_method": "string",
  "raw_image_path": "string"
}
```

## 주요 구현 제약

- **Vercel 서버리스 환경**: 요청 간 파일 유지 불가 → MVP에서는 클라이언트 localStorage 백업 병행
- **파일 업로드 제한**: JPG, PNG, PDF만 허용, 최대 10MB
- **LLM 응답 파싱**: Upstage 응답이 JSON 형식이 아닐 수 있으므로 LangChain OutputParser로 구조화 필수

## 프론트엔드 구조 (구현 예정)

```
frontend/src/
├── pages/         # Dashboard (/), Upload (/upload), Detail (/expense/:id)
├── components/    # DropZone, ExpenseCard, SummaryCard, FilterBar, ParsePreview
└── api/           # Axios 인스턴스 (baseURL = VITE_API_BASE_URL)
```

## 디자인 시스템

- Primary: `indigo-600`, Success: `green-500`, Error: `red-500`
- 카테고리 배지: 식료품=green, 외식=orange, 교통=blue, 쇼핑=purple, 의료=red, 기타=gray
- 폰트: Pretendard (CDN) → Noto Sans KR (fallback)
- 최대 너비: 896px 중앙 정렬, 반응형 1→2→3 컬럼 (mobile→tablet→desktop)
