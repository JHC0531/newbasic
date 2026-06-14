import streamlit as st
from utils import inject_global_css, get_irregular_verbs, MASCOT_PATH, LEVEL_LABELS

inject_global_css()

col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(MASCOT_PATH), width=80)
with col2:
    st.title("불규칙 변화 📖")
    st.caption("패턴을 알면 쉬워져요!")

st.markdown("---")

# ── 동사 변화형이란? ──
st.markdown("### 동사 변화형이란?")
st.markdown("""
영어 동사는 시제에 따라 모양이 바뀌어요.

**원형(base form)** → **과거형(past)** → **과거분사(past participle)**  
이렇게 3가지 형태를 꼭 알아야 해요!

규칙 동사는 뒤에 **-ed**만 붙이면 되지만, 불규칙 동사는 모양이 완전히 달라지거나
아예 안 바뀌기도 해요. 아래에서 패턴별로 살펴볼게요! 🦝
""")

st.markdown("---")

# ── 패턴 5가지 ──
st.markdown("### 불규칙 동사 패턴 5가지")

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)
c5, _ = st.columns(2)

with c1:
    st.markdown("""
    <div class="vb-card t-aaa">
    <h3>A – A – A</h3>
    <div class="tag">세 형태가 모두 같아요!</div>
    <div class="example">
    <b>cut</b> → cut → cut (자르다)<br>
    <b>put</b> → put → put (두다)<br>
    <b>hit</b> → hit → hit (치다)<br>
    <b>read</b> → read → read (읽다)
    </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="vb-card t-aab">
    <h3>A – A – B</h3>
    <div class="tag">과거형은 같고, 과거분사만 달라요!</div>
    <div class="example">
    <b>beat</b> → beat → <b>beaten</b> (이기다)
    </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="vb-card t-aba">
    <h3>A – B – A</h3>
    <div class="tag">원형 = 과거분사, 과거형만 달라요!</div>
    <div class="example">
    <b>come</b> → <b>came</b> → come (오다)<br>
    <b>run</b> → <b>ran</b> → run (달리다)<br>
    <b>become</b> → <b>became</b> → become (~이 되다)
    </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="vb-card t-abb">
    <h3>A – B – B</h3>
    <div class="tag">과거형 = 과거분사, 원형만 달라요!</div>
    <div class="example">
    <b>bring</b> → brought → brought (가져오다)<br>
    <b>buy</b> → bought → bought (사다)<br>
    <b>feel</b> → felt → felt (느끼다)<br>
    <b>make</b> → made → made (만들다)
    </div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="vb-card t-abc">
    <h3>A – B – C</h3>
    <div class="tag">세 형태가 모두 달라요! 제일 중요!</div>
    <div class="example">
    <b>go</b> → went → gone (가다)<br>
    <b>see</b> → saw → seen (보다)<br>
    <b>eat</b> → ate → eaten (먹다)<br>
    <b>write</b> → wrote → written (쓰다)
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── 동사 목록 표 ──
st.markdown("### 🔥 불규칙 동사 전체 목록")

df = get_irregular_verbs()

col1, col2 = st.columns(2)
with col1:
    level_options = ["전체"] + list(LEVEL_LABELS.values())
    level_choice = st.selectbox("레벨", level_options)
with col2:
    type_options = ["전체"] + sorted(df["type"].unique().tolist())
    type_choice = st.selectbox("유형", type_options)

filtered = df.copy()
if level_choice != "전체":
    level_key = [k for k, v in LEVEL_LABELS.items() if v == level_choice][0]
    filtered = filtered[filtered["level"] == level_key]
if type_choice != "전체":
    filtered = filtered[filtered["type"] == type_choice]

display_df = filtered[["base", "past", "pp", "meaning", "type", "level"]].rename(columns={
    "base": "원형",
    "past": "과거형",
    "pp": "과거분사",
    "meaning": "뜻",
    "type": "유형",
    "level": "레벨",
})
display_df["레벨"] = display_df["레벨"].map(LEVEL_LABELS).fillna(display_df["레벨"])

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.caption(f"총 {len(display_df)}개")
