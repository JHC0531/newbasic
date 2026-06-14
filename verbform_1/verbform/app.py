import streamlit as st

st.set_page_config(
    page_title="동사 변화 학습기 🦝",
    page_icon="🦝",
    layout="wide",
)

# 사이드바에 한글 이름으로 페이지 표시 (파일명은 영어라 GitHub에서 안 깨짐)
home = st.Page("home_page.py", title="홈", icon="🏠", default=True)
irregular = st.Page("pages/1_Irregular.py", title="불규칙 변화", icon="📖")
rules = st.Page("pages/2_Rules.py", title="규칙 변화", icon="📝")
cert = st.Page("pages/3_Certificate.py", title="학습 수료증", icon="🏅")

nav = st.navigation([home, irregular, rules, cert])
nav.run()
