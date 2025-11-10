# Sprint 03 - Menu Generator

AI 기반 메뉴판 자동 생성 시스템

## 프로젝트 개요

음식 사진, 설명, 테마를 입력받아 자동으로 메뉴판을 생성하는 시스템

## 주요 기능

### 1차 목표
- 메뉴 사진 + 설명 + 테마 프롬프트 입력
- PDF 형식 메뉴판 자동 생성
- 카테고리별 그룹핑
- 한글/영문 지원

### 추가 예정
- OCR 기능: 기존 메뉴판 스캔하여 재구성

## 기술 스택

- Frontend: Streamlit
- Backend: FastAPI (예정)
- Server: GCP (34.68.116.93)
- OCR: DeepSeekOCR (예정)

## 프로젝트 구조

```
task/
├── menu_generator_test.py    # Streamlit 테스트 페이지
├── backend/                   # API 서버 (예정)
├── frontend/                  # UI (예정)
└── README.md
```

## 실행 방법

### 테스트 페이지 실행
```bash
streamlit run menu_generator_test.py
```

## API 명세

### Request
```json
{
  "theme": {
    "style": "modern/classic/elegant/casual",
    "color_scheme": "warm/cool/vibrant",
    "language": "ko/en/bilingual"
  },
  "menu_items": [
    {
      "image": "이미지 데이터",
      "category": "Soup/Salad/Spicy/Dessert",
      "name_ko": "한글 이름",
      "name_en": "English Name",
      "description": "설명",
      "highlights": ["키워드1", "키워드2"],
      "price": 15000
    }
  ]
}
```

### Response
```json
{
  "menu_pdf_url": "생성된 PDF URL",
  "status": "success/error",
  "processing_time": 2.5
}
```

## 팀원

- GCP 서버: 34.68.116.93
- 협업 방식: GitHub

## 개발 일정

- Week 1: API 연동 및 기본 기능 구현
- Week 2: UI 개선 및 테스트
- Week 3: OCR 기능 추가 (선택)
