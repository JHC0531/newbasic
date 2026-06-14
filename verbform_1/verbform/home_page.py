import streamlit as st
from utils import inject_global_css, MASCOT_PATH

inject_global_css()

# ── Intro ──
col1, col2 = st.columns([1, 4])
with col1:
    st.image(str(MASCOT_PATH), width=140)
with col2:
    st.title("동사 변화 학습기 🦝")
    st.markdown("""
    ### 안녕! 나는 동사 선생님 너구리야!

    영어 동사의 과거형·과거분사형을 함께 공부해보자!  
    왼쪽 사이드바 또는 아래 메뉴에서 원하는 학습 방법을 골라봐.
    """)

st.markdown("---")

# ── Menu cards ──
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="vb-card t-aaa">
    <h3>📖 불규칙 변화</h3>
    <div class="tag">A-B-C 등 패턴별로 불규칙 동사 익히기</div>
    <div class="example">
    원형 → 과거형 → 과거분사 변화 패턴 5가지를 그림과 표로 한눈에 정리했어요.
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Irregular.py", label="불규칙 변화 보러가기 →", icon="📖")

with c2:
    st.markdown("""
    <div class="vb-card t-abb">
    <h3>📝 규칙 변화</h3>
    <div class="tag">-ed 붙이는 규칙 4가지 정리</div>
    <div class="example">
    일반 규칙부터 자음을 겹치는 규칙까지, 예시와 예문과 함께 차근차근 배워요.
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Rules.py", label="규칙 변화 보러가기 →", icon="📝")

with c3:
    st.markdown("""
    <div class="vb-card t-abc">
    <h3>🏅 학습 수료증</h3>
    <div class="tag">배운 걸 모두 모아 도전! 수료증 받기</div>
    <div class="example">
    이름을 입력하면 너구리가 함께해요. 불규칙·규칙을 섞은 15문제를 풀고,
    내 이름이 들어간 수료증을 받아보세요!
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Certificate.py", label="학습 수료증 받으러 가기 →", icon="🏅")
