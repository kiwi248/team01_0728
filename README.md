# TEAM01_0728

## 개요

FastAPI 백엔드와 Streamlit 프론트엔드로 구성된 학생 성적 관리 프로젝트입니다. 반별로 서로 다른 과목의 학생 점수 데이터를 다룹니다.

- **1반**: Python, Streamlit, FastAPI 과목을 시험 본 학생 10명의 점수
- **2반**: Korean, Math, English 과목을 시험 본 학생 10명의 점수

### 구성
- `backend/` — FastAPI 기반 API 서버 (routers / schemas / services 계층 분리)
- `frontend/` — Streamlit 기반 웹 UI (app_pages 별 반 페이지 구성)


## 디렉토리 구조
```

TEAM01_0728/
├── backend/
│   ├── routers/
│   │   ├── class1_sym_router.py
│   │   └── class2_inhye_router.py
│   ├── schemas/
│   │   ├── class1_sym_schema.py
│   │   └── class2_inhye_schema.py
│   ├── services/
│   │   ├── class1_sym_service.py
│   │   └── class2_inhye_service.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app_pages/
│   │   ├── class1_jso.py
│   │   └── class2_port.py
│   └── app.py
├── .gitignore
└── README.md

```

## 환경설정

### 1. 가상환경 생성 및 활성화 (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. 패키지 설치

```powershell
pip install -r backend/requirements.txt
```

### 3. 백엔드 로컬 서버 실행 (FastAPI)

```powershell
cd backend
uvicorn main:app --reload
```

- 실행 후 `http://127.0.0.1:8000` 에서 API 확인 가능
- Swagger 문서: `http://127.0.0.1:8000/docs`

### 4. 프론트엔드 로컬 서버 실행 (Streamlit)

```powershell
cd frontend
streamlit run app.py
```

- 실행 후 자동으로 브라우저에서 `http://localhost:8501` 열림

## 배포

### 백엔드 (Render)

1. GitHub 저장소를 Render에 연결
2. New Web Service 생성 시 아래와 같이 설정
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. 배포 완료 후 발급되는 URL(예: `https://team01-0728.onrender.com`)을 프론트엔드의 API 요청 주소로 사용

### 프론트엔드 (Streamlit Cloud)

1. GitHub 저장소를 Streamlit Cloud에 연결
2. 앱 생성 시 아래와 같이 설정
   - **Repository**: 해당 GitHub 저장소
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
3. 배포 후 프론트엔드에서 백엔드 API를 호출할 때는 로컬 주소(`http://127.0.0.1:8000`) 대신 Render에 배포된 백엔드 URL을 사용하도록 설정