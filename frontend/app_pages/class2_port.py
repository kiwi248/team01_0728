import httpx
import pandas as pd
import streamlit as st


CLASS2_URL = "http://127.0.0.1:8000/student2"
SUBJECTS = ["Korean", "Math", "English"]


st.title("2반 성적 Data")

try:
    with st.spinner("2반 성적 데이터를 불러오는 중입니다..."):
        response = httpx.get(CLASS2_URL, timeout=10.0)
        response.raise_for_status()
        student_data = response.json()

    student_df = pd.DataFrame(student_data)

    required_columns = ["id", "name", *SUBJECTS]
    if student_df.empty or not all(
        column in student_df.columns for column in required_columns
    ):
        raise ValueError

    student_df[SUBJECTS] = student_df[SUBJECTS].apply(
        pd.to_numeric,
        errors="raise",
    )

    st.success(f"{len(student_df)}명의 성적 데이터를 불러왔습니다.")

    st.subheader("과목별 성적")
    selected_subject = st.selectbox(
        "과목을 선택하세요.",
        SUBJECTS,
    )

    subject_df = student_df[["name", selected_subject]].copy()
    subject_df = subject_df.sort_values(
        by=selected_subject,
        ascending=True,
    )
    subject_df["순위"] = subject_df[selected_subject].rank(
        method="min",
        ascending=False,
    ).astype(int)
    subject_df = subject_df.rename(
        columns={
            "name": "이름",
            selected_subject: "점수",
        }
    )

    st.dataframe(
        subject_df[["순위", "이름", "점수"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(f"{selected_subject} 학생별 점수")
    subject_chart_df = subject_df.set_index("이름")[["점수"]]
    st.bar_chart(subject_chart_df)

    st.subheader("학생별 과목 점수")
    all_subject_chart_df = student_df.set_index("name")[SUBJECTS]
    st.bar_chart(all_subject_chart_df)

    student_df["평균"] = student_df[SUBJECTS].mean(axis=1).round(1)

    st.subheader("평균 점수별 학생 조회")
    average_range = st.slider(
        "평균 점수 범위를 선택하세요.",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=10,
    )

    filtered_df = student_df[
        student_df["평균"].between(
            average_range[0],
            average_range[1],
            inclusive="both",
        )
    ][["name", "Korean", "Math", "English", "평균"]]
    filtered_df = filtered_df.sort_values(by="평균", ascending=True)
    filtered_df = filtered_df.rename(
        columns={
            "name": "이름",
        }
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )
    st.write("해당 학생 수:", len(filtered_df))

    st.subheader("학생별 평균 점수")
    if filtered_df.empty:
        st.info("선택한 평균 점수 범위에 해당하는 학생이 없습니다.")
    else:
        average_chart_df = filtered_df.set_index("이름")[["평균"]]
        st.bar_chart(average_chart_df)

except httpx.TimeoutException:
    st.error("성적 API 응답 시간이 초과되었습니다.")

except httpx.HTTPStatusError as error:
    st.error(f"성적 API 오류: {error.response.status_code}")

except httpx.RequestError:
    st.error("성적 API 서버에 연결할 수 없습니다.")

except (KeyError, TypeError, ValueError):
    st.error("API 응답을 성적 데이터로 변환할 수 없습니다.")
