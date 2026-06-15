import streamlit as st
from utils import inject_global_css, MASCOT_PATH, make_app_qr

inject_global_css()

# ── Intro ──
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image(str(MASCOT_PATH), width=140)
with col2:
    st.title("동사 변화 학습기 🦝")
    st.markdown("""
    ### 안녕! 나는 동사 선생님 너구리야!

    영어 동사의 과거형·과거분사형을 함께 공부해보자!  
    왼쪽 사이드바 또는 아래 메뉴에서 원하는 학습 방법을 골라봐.
    """)
with col3:
    st.markdown(
        '<div style="text-align:center;font-size:0.8rem;color:var(--green);'
        'font-weight:700;margin-bottom:4px;">📱 앱 바로가기</div>',
        unsafe_allow_html=True,
    )
    st.image(make_app_qr(), width=110)

st.markdown("---")

# ── 동사 변화형이란? ──
st.markdown("### 🤔 동사 변화형이란?")
st.markdown("""
<div style="background:#fff;border-radius:14px;padding:18px 22px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);font-size:1.05rem;line-height:1.7;margin-bottom:18px;">
영어 동사는 시제에 따라 모양이 바뀌어요. 그래서 한 동사마다
<b style="color:var(--green);">3가지 형태</b>를 알아야 해요! 👇<br><br>
<div style="text-align:center;font-size:1.2rem;font-weight:800;">
<span style="color:#6c757d;">원형</span>
&nbsp;→&nbsp;
<span style="color:var(--orange);">과거형</span>
&nbsp;→&nbsp;
<span style="color:var(--red);">과거분사형</span></div>
<div style="text-align:center;font-size:0.88rem;color:#888;margin-top:4px;">
(base form) &nbsp; (past) &nbsp; (past participle)</div>
</div>
""", unsafe_allow_html=True)

# ── 왜/언제 쓰는지 ──
st.markdown("### 💡 그런데 이걸 왜 배워요? 언제 써요?")
st.markdown("""
<div style="background:var(--green-pale);border-radius:14px;padding:16px 20px;
font-size:1rem;line-height:1.6;margin-bottom:14px;">
과거형과 과거분사형은 <b>쓰는 곳이 정해져 있어요.</b> 아래 예문에서
<span style="color:var(--orange);font-weight:800;">과거형</span>과
<span style="color:var(--red);font-weight:800;">과거분사형</span>을 잘 봐! 👀
</div>
""", unsafe_allow_html=True)

u1, u2 = st.columns(2)
with u1:
    st.markdown("""
    <div class="vb-card" style="border-top-color:var(--orange);">
    <h3 style="color:var(--orange);">⏰ 과거형</h3>
    <div class="tag">과거에 있었던 일을 말할 때</div>
    <div style="margin-top:8px;font-size:0.98rem;line-height:1.8;">
    • I <b style="color:var(--orange);">played</b> soccer yesterday.<br>
    <span style="color:#777;font-size:0.85rem;">나는 어제 축구를 <b>했다</b>.</span><br>
    • She <b style="color:var(--orange);">went</b> to school.<br>
    <span style="color:#777;font-size:0.85rem;">그녀는 학교에 <b>갔다</b>.</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

with u2:
    st.markdown("""
    <div class="vb-card" style="border-top-color:var(--red);">
    <h3 style="color:var(--red);">✅ 과거분사형</h3>
    <div class="tag">현재완료·수동태에 쓸 때</div>
    <div style="margin-top:8px;font-size:0.98rem;line-height:1.8;">
    • I have <b style="color:var(--red);">eaten</b> lunch. (현재완료)<br>
    <span style="color:#777;font-size:0.85rem;">나는 점심을 (막) <b>먹었다</b>.</span><br>
    • The cake was <b style="color:var(--red);">made</b> by mom. (수동태)<br>
    <span style="color:#777;font-size:0.85rem;">그 케이크는 엄마가 <b>만들었다</b>.</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;font-size:1.05rem;font-weight:700;color:var(--green);
margin:14px 0 4px;">그래서 3단 변화를 알아야 영어 문장을 자유롭게 쓸 수 있어! 🚀</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── 학습 메뉴 ──
st.markdown("### 🎮 자, 이제 시작해볼까?")

# ── Menu cards ──
c1, c2, c3 = st.columns(3)

with c1:
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

with c2:
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
