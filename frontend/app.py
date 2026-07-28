"""초보자를 위한 가장 간단한 Streamlit 멀티페이지 앱입니다."""

import streamlit as st


st.set_page_config(
    page_title="학생점수관리페이지",
    page_icon="🎓",
    layout="wide",
)


class1_jso_page = st.Page("app_pages/class1_jso.py", title="1반", icon="📝", default=True)
class2_port_page = st.Page("app_pages/class2_port.py", title="2반", icon="📝")

pg = st.navigation([class1_jso_page, class2_port_page], position="top")
pg.run()

