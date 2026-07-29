import os

import httpx
import pandas as pd
import streamlit as st


SAMPLE_DATA = [
    {"id": 1, "subject": "Python", "score": 100},
    {"id": 2, "subject": "Streamlit", "score": 95},
    {"id": 3, "subject": "FastAPI", "score": 90},
    {"id": 4, "subject": "Python", "score": 88},
    {"id": 5, "subject": "Streamlit", "score": 92},
    {"id": 6, "subject": "FastAPI", "score": 85},
    {"id": 7, "subject": "Python", "score": 97},
    {"id": 8, "subject": "Streamlit", "score": 78},
    {"id": 9, "subject": "FastAPI", "score": 83},
    {"id": 10, "subject": "Python", "score": 94},
]

st.set_page_config(page_title="1반 성적 대시보드", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px;}
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, #ffffff, #f7f9fc);
            border: 1px solid #e8edf5;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 6px 18px rgba(31, 41, 55, 0.05);
        }
        [data-testid="stMetricLabel"] {font-weight: 700;}
        .dashboard-title {
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.2rem;
        }
        .dashboard-subtitle {color: #64748b; margin-bottom: 1.3rem;}
        .status-badge {
            display: inline-block;
            padding: 5px 11px;
            border-radius: 999px;
            background: #eef2ff;
            color: #4338ca;
            font-size: 0.78rem;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=30, show_spinner=False)
def fetch_students(api_url: str) -> list[dict]:
    """class1 API에서 학생 성적 JSON 배열을 가져옵니다."""
    response = httpx.get(api_url, timeout=5.0)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list):
        raise ValueError('응답은 [{"id": 1, "subject": "Python", "score": 100}] 형태의 배열이어야 합니다.')
    if not all(isinstance(student, dict) for student in payload):
        raise ValueError("배열의 각 학생 데이터는 JSON 객체여야 합니다.")
    return payload


def make_dataframe(records: list[dict]) -> pd.DataFrame:
    """JSON 레코드를 화면에서 사용할 안전한 DataFrame으로 변환합니다."""
    frame = pd.DataFrame(records)
    required = {"id", "subject", "score"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"필수 항목이 없습니다: {', '.join(sorted(missing))}")

    frame = frame.loc[:, ["id", "subject", "score"]].copy()
    frame["id"] = pd.to_numeric(frame["id"], errors="coerce")
    frame["score"] = pd.to_numeric(frame["score"], errors="coerce")
    frame["subject"] = frame["subject"].astype(str).str.strip()
    frame = frame.dropna(subset=["id", "score"])
    frame["id"] = frame["id"].astype(int)
    frame["score"] = frame["score"].clip(0, 100)
    return frame.sort_values("id").reset_index(drop=True)


def score_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


default_api_url = os.getenv(
    "CLASS1_API_URL",
    "http://127.0.0.1:8000/class1/students",
)

with st.sidebar:
    st.header("데이터 연결")
    api_url = st.text_input(
        "학생 성적 API 주소",
        value=default_api_url,
        help="class1_sym_service.py 데이터를 반환하는 GET 주소를 입력하세요.",
    )
    use_sample = st.toggle("샘플 데이터로 미리보기", value=True)
    if st.button("데이터 새로고침", use_container_width=True):
        fetch_students.clear()
        st.rerun()

data_source = "샘플 데이터"
if use_sample:
    raw_data = SAMPLE_DATA
else:
    try:
        raw_data = fetch_students(api_url)
        data_source = "API 연결됨"
    except (httpx.HTTPError, ValueError) as error:
        st.error(f"API 데이터를 불러오지 못했습니다: {error}")
        st.info("왼쪽에서 샘플 데이터 미리보기를 켜거나 API 주소를 확인해 주세요.")
        st.stop()

try:
    df = make_dataframe(raw_data)
except ValueError as error:
    st.error(f"데이터 형식을 확인해 주세요. {error}")
    st.stop()

if df.empty:
    st.warning("표시할 학생 성적 데이터가 없습니다.")
    st.stop()

st.markdown('<div class="dashboard-title">1반 성적 대시보드</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dashboard-subtitle">Python · Streamlit · FastAPI 과목 성적을 한눈에 확인하세요.</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<span class="status-badge">● {data_source}</span>', unsafe_allow_html=True)

all_subjects = sorted(df["subject"].unique().tolist())
selected_subjects = st.multiselect(
    "과목 필터",
    options=all_subjects,
    default=all_subjects,
    placeholder="표시할 과목을 선택하세요",
)

filtered_df = df[df["subject"].isin(selected_subjects)].copy()
if filtered_df.empty:
    st.warning("선택한 과목이 없습니다. 한 개 이상의 과목을 선택해 주세요.")
    st.stop()

top_row = filtered_df.loc[filtered_df["score"].idxmax()]
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("응시 학생", f"{filtered_df['id'].nunique()}명")
metric2.metric("전체 평균", f"{filtered_df['score'].mean():.1f}점")
metric3.metric("최고 점수", f"{filtered_df['score'].max():.0f}점", f"학생 {int(top_row['id'])}")
metric4.metric("90점 이상", f"{(filtered_df['score'] >= 90).sum()}명")

st.write("")
chart_tab, table_tab = st.tabs(["📈 성적 차트", "📋 상세 테이블"])

with chart_tab:
    left, right = st.columns([1, 1.45], gap="large")

    with left:
        st.subheader("과목별 평균")
        subject_summary = (
            filtered_df.groupby("subject", as_index=False)
            .agg(평균=("score", "mean"), 최고점=("score", "max"), 응시자=("id", "count"))
            .sort_values("평균", ascending=False)
        )
        st.bar_chart(
            subject_summary,
            x="subject",
            y="평균",
            color="subject",
            horizontal=True,
            height=330,
        )

    with right:
        st.subheader("학생별 점수")
        score_chart_df = filtered_df.copy()
        score_chart_df["학생"] = score_chart_df["id"].map(lambda value: f"{value}번")
        st.line_chart(
            score_chart_df,
            x="학생",
            y="score",
            color="subject",
            height=330,
        )

    st.subheader("과목 요약")
    st.dataframe(
        subject_summary.rename(columns={"subject": "과목"}).style.format(
            {"평균": "{:.1f}점", "최고점": "{:.0f}점", "응시자": "{:.0f}명"}
        ),
        use_container_width=True,
        hide_index=True,
    )

with table_tab:
    display_df = filtered_df.copy()
    display_df["grade"] = display_df["score"].apply(score_grade)
    display_df = display_df.rename(
        columns={"id": "학생 번호", "subject": "과목", "score": "점수", "grade": "등급"}
    )
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "학생 번호": st.column_config.NumberColumn("학생 번호", format="%d번"),
            "과목": st.column_config.TextColumn("과목"),
            "점수": st.column_config.ProgressColumn(
                "점수",
                min_value=0,
                max_value=100,
                format="%d점",
            ),
            "등급": st.column_config.TextColumn("등급"),
        },
    )
    st.caption(f"총 {len(display_df)}건 · 점수 기준 내림차순으로 정렬하려면 열 제목을 클릭하세요.")
