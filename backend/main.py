import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Receipt Expense Tracker API",
    description="Upstage Vision LLM 기반 영수증 OCR 지출 관리 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uploads 디렉토리 자동 생성
os.makedirs("uploads", exist_ok=True)

# 라우터 등록 (Phase 2~3에서 구현)
# from routers import upload, expenses, summary
# app.include_router(upload.router, prefix="/api")
# app.include_router(expenses.router, prefix="/api")
# app.include_router(summary.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "Receipt Expense Tracker API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
