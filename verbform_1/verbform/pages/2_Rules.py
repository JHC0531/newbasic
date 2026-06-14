import random
import streamlit as st
from utils import inject_global_css, MASCOT_PATH, load_rules_quiz, random_message

inject_global_css()

col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(MASCOT_PATH), width=80)
with col2:
    st.title("규칙 변화 📝")
    st.caption("규칙을 배우고 바로 퀴즈로 확인해봐요!")

st.markdown("---")

quiz_df = load_rules_quiz()

# ──────────────────────────────────────────
# 탭별 규칙 설명 정의
# rule_keys: 이 탭의 퀴즈에 사용할 규칙번호(들)
# ──────────────────────────────────────────
TABS = [
    {
        "label": "1. 동사원형 + -ed",
        "rule_keys": ["1"],
        "title": "가장 일반적인 경우: 동사원형 + -ed",
        "desc": "대부분의 일반 동사는 정해진 규칙에 따라 변해요. 가장 기본은 동사원형 뒤에 **-ed**를 붙이는 거예요!",
        "examples": ["want → wanted", "talk → talked", "stay → stayed"],
        "sentence": ("I <b>listened</b> to jazz music last night.", "나는 어젯밤에 재즈 음악을 들었다."),
    },
    {
        "label": "2. 자음 + e → -d",
        "rule_keys": ["2"],
        "title": "자음 + e로 끝나는 경우: -d만 추가",
        "desc": "이미 **e**로 끝나니까, **d**만 붙이면 돼요. 편하죠? 😎",
        "examples": ["like → liked", "live → lived", "love → loved"],
        "sentence": ("Many students <b>liked</b> the new school event.", "많은 학생들이 새 학교 행사를 좋아했다."),
    },
    {
        "label": "3. -y 규칙",
        "rule_keys": ["3a", "3b"],
        "title": "-y로 끝나는 경우: 두 가지로 나뉘어요!",
        "desc": (
            "**자음 + y**로 끝나면 → y를 **i**로 바꾸고 **-ed** (study → studied)<br>"
            "**모음 + y**로 끝나면 → 그대로 **-ed** (play → played)<br><br>"
            "y 앞에 있는 글자가 자음이냐 모음이냐가 핵심이에요! 🔑"
        ),
        "examples": ["study → studied", "try → tried", "play → played", "enjoy → enjoyed"],
        "sentence": ("He <b>studied</b> in the library.", "그는 도서관에서 공부했다."),
    },
    {
        "label": "4. 단모음+단자음 → 자음 겹침",
        "rule_keys": ["4"],
        "title": "단모음 + 단자음으로 끝나는 경우: 자음을 한 번 더!",
        "desc": "짧은 모음 소리 + 자음 하나로 끝나면, 마지막 자음을 **하나 더 쓰고** -ed를 붙여요.",
        "examples": ["stop → stopped", "plan → planned", "chat → chatted"],
        "sentence": ("The police <b>stepped</b> into the room carefully.", "경찰이 조심스럽게 방 안으로 발을 들여놓았다."),
    },
]

QUESTIONS_PER_QUIZ = 3


def make_quiz_pool(rule_keys):
    """해당 규칙번호들의 문제를 합쳐 dict 리스트로 반환"""
    pool = quiz_df[quiz_df["규칙번호"].isin(rule_keys)]
    return pool.to_dict("records")


def init_quiz(tab_idx, rule_keys):
    """탭별 퀴즈 상태 초기화 (3문제 랜덤 추출)"""
    pool = make_quiz_pool(rule_keys)
    random.shuffle(pool)
    selected = pool[:QUESTIONS_PER_QUIZ]
    st.session_state[f"quiz_{tab_idx}"] = {
        "questions": selected,
        "idx": 0,
        "score": 0,
        "checked": False,
        "selected_answer": None,
        "raccoon": random_message("start"),
        "finished": False,
    }


def build_choices(q):
    """정답+오답2개 셔플"""
    choices = [q["정답"], q["오답1"], q["오답2"]]
    random.shuffle(choices)
    return choices


def render_quiz(tab_idx, rule_keys):
    state_key = f"quiz_{tab_idx}"
    if state_key not in st.session_state:
        init_quiz(tab_idx, rule_keys)

    qs = st.session_state[state_key]

    # ── 결과 화면 ──
    if qs["finished"]:
        score = qs["score"]
        total = len(qs["questions"])
        st.markdown(f"""
        <div class="raccoon-row">
            <div class="raccoon-bubble">{total}문제 중 <b>{score}개</b> 맞았어! {"완벽해! 🏆" if score==total else "잘했어! 🦝"}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 복습하기 (다른 문제)", key=f"review_{tab_idx}"):
            init_quiz(tab_idx, rule_keys)
            st.rerun()
        return

    q = qs["questions"][qs["idx"]]
    q_num = qs["idx"] + 1
    total = len(qs["questions"])

    # 선택지 빌드 (문제별로 고정 — 세션에 저장)
    choice_key = f"choices_{tab_idx}_{qs['idx']}"
    if choice_key not in st.session_state:
        st.session_state[choice_key] = build_choices(q)
    choices = st.session_state[choice_key]

    # ── 너구리 + 진행 ──
    st.markdown(f"""
    <div class="raccoon-row">
        <div class="raccoon-bubble">{qs['raccoon']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"문제 {q_num} / {total}")

    # ── 문제 카드 ──
    st.markdown(f"""
    <div class="verb-display">
        <div class="verb-meaning">다음 동사의 과거형은?</div>
        <div class="verb-base">{q['동사원형']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 보기 (라디오) ──
    picked = st.radio(
        "정답을 골라봐!",
        choices,
        key=f"radio_{tab_idx}_{qs['idx']}",
        index=None,
        horizontal=True,
        disabled=qs["checked"],
    )

    # ── 확인하기 / 계속하기 ──
    if not qs["checked"]:
        if st.button("확인하기 ✅", key=f"check_{tab_idx}", type="primary"):
            if picked is None:
                st.warning("먼저 보기를 골라줘!")
            else:
                qs["checked"] = True
                qs["selected_answer"] = picked
                if picked == q["정답"]:
                    qs["score"] += 1
                st.rerun()
    else:
        # 정답/오답 피드백
        if qs["selected_answer"] == q["정답"]:
            st.markdown(f"""
            <div class="raccoon-row">
                <div class="raccoon-bubble" style="border-left:5px solid var(--green);">
                정답이에요! 🎉 <b>{q['동사원형']} → {q['정답']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="raccoon-row">
                <div class="raccoon-bubble" style="border-left:5px solid var(--red);">
                오답이에요! 🦝 네가 고른 건 <b>{qs['selected_answer']}</b>,
                정답은 <b>{q['정답']}</b>(이)야!
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 예문 표시
        sentence = str(q.get("예문", "")).strip()
        if sentence and sentence.lower() != "nan":
            highlighted = sentence.replace(q["정답"], f"<b style='color:var(--green)'>{q['정답']}</b>")
            st.markdown(f"<div style='margin:8px 0;color:#555;'>📖 {highlighted}</div>", unsafe_allow_html=True)

        is_last = qs["idx"] + 1 >= total
        btn_label = "결과 보기 →" if is_last else "계속하기 →"
        if st.button(btn_label, key=f"next_{tab_idx}", type="primary"):
            if is_last:
                qs["finished"] = True
            else:
                qs["idx"] += 1
                qs["checked"] = False
                qs["selected_answer"] = None
                qs["raccoon"] = random_message("start")
            st.rerun()


# ──────────────────────────────────────────
# 탭 렌더링
# ──────────────────────────────────────────
tabs = st.tabs([t["label"] for t in TABS])

for tab_idx, (tab, tab_def) in enumerate(zip(tabs, TABS)):
    with tab:
        # 규칙 설명
        examples_html = "".join(f'<span class="rule-ex">{ex}</span>' for ex in tab_def["examples"])
        eng, kor = tab_def["sentence"]
        st.markdown(f"""
        <div class="vb-card">
        <h3>{tab_def['title']}</h3>
        <p>{tab_def['desc']}</p>
        <div style="margin:10px 0;">{examples_html}</div>
        <div style="background:var(--green-pale);border-radius:8px;padding:10px 14px;margin-top:10px;">
        📖 {eng}<br><span style="color:#6b7280;font-size:0.88rem;">{kor}</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎯 바로 풀어보기")
        render_quiz(tab_idx, tab_def["rule_keys"])
