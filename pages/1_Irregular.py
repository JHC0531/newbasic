import random
import streamlit as st
import streamlit.components.v1 as components
from utils import inject_global_css, MASCOT_PATH, get_irregular_verbs, get_game_verbs
from bird_game import bird_game_html

inject_global_css()

st.title("불규칙 변화 📖")
st.markdown(
    '<div style="font-size:1.05rem;font-weight:600;color:var(--green);margin-bottom:6px;">'
    '패턴을 배우고, 게임으로 익히고, 리스트로 확인하자! 🎮✨</div>',
    unsafe_allow_html=True,
)

st.markdown("---")

# ── 난이도 선택 (게임 공통) ──
if "irr_hard" not in st.session_state:
    st.session_state.irr_hard = False

tab1, tab2, tab3, tab4 = st.tabs([
    "📖 패턴 학습",
    "🐦 새 잡기 게임",
    "🧩 3단 변화 완성",
    "📋 동사 리스트",
])

# ══════════════════════════════════════════
# 탭 1 — 패턴 학습
# ══════════════════════════════════════════
with tab1:
    st.markdown("""
    <div style="font-size:1.1rem;line-height:1.7;background:#fff;border-radius:14px;
    padding:18px 22px;box-shadow:0 4px 15px rgba(0,0,0,0.08);margin-bottom:18px;">
    앞에서 배운 <b>규칙 동사</b>는 뒤에 <b>-ed</b>만 붙이면 됐죠? 🟢<br>
    하지만 <b style="color:var(--green);">불규칙 동사</b>는 모양이 완전히 달라지거나,
    아예 안 바뀌기도 해요! 🤯<br>아래에서 5가지 패턴을 살펴보자! 🦝
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 불규칙 동사 패턴 5가지 🔍")

    PATTERNS = [
        {
            "cls": "t-aaa", "code": "A-A-A", "emoji": "🟰",
            "big": "세 형태가 모두 같아요!",
            "examples": [("cut", "cut", "cut", "자르다"), ("put", "put", "put", "두다"), ("hit", "hit", "hit", "치다")],
            "sentence": ("I <b>cut</b> the paper yesterday.", "나는 어제 종이를 잘랐다."),
        },
        {
            "cls": "t-aab", "code": "A-A-B", "emoji": "✌️",
            "big": "과거형은 같고, 과거분사만 달라요!",
            "examples": [("beat", "beat", "beaten", "이기다")],
            "sentence": ("Our team has <b>beaten</b> them before.", "우리 팀은 전에 그들을 이긴 적 있다."),
        },
        {
            "cls": "t-aba", "code": "A-B-A", "emoji": "🔄",
            "big": "원형과 과거분사가 같아요!",
            "examples": [("come", "came", "come", "오다"), ("run", "ran", "run", "달리다"), ("become", "became", "become", "~이 되다")],
            "sentence": ("She has <b>come</b> back home.", "그녀는 집에 돌아왔다."),
        },
        {
            "cls": "t-abb", "code": "A-B-B", "emoji": "👯",
            "big": "과거형과 과거분사가 같아요!",
            "examples": [("buy", "bought", "bought", "사다"), ("make", "made", "made", "만들다"), ("feel", "felt", "felt", "느끼다")],
            "sentence": ("I have <b>made</b> a cake.", "나는 케이크를 만들었다."),
        },
        {
            "cls": "t-abc", "code": "A-B-C", "emoji": "🌈",
            "big": "세 형태가 모두 달라요! (제일 중요)",
            "examples": [("go", "went", "gone", "가다"), ("eat", "ate", "eaten", "먹다"), ("write", "wrote", "written", "쓰다")],
            "sentence": ("He has <b>written</b> a letter.", "그는 편지를 썼다."),
        },
    ]

    cols = st.columns(2)
    for i, p in enumerate(PATTERNS):
        with cols[i % 2]:
            ex_html = ""
            for base, past, pp, ko in p["examples"]:
                ex_html += (
                    f'<div style="margin:3px 0;">'
                    f'<b style="color:var(--green);">{base}</b> → {past} → {pp} '
                    f'<span style="color:#888;font-size:0.85rem;">({ko})</span></div>'
                )
            eng, kor = p["sentence"]
            st.markdown(f"""
            <div class="vb-card {p['cls']}">
                <div style="font-size:1.35rem;font-weight:800;color:var(--green);margin-bottom:2px;">
                {p['emoji']} {p['big']}</div>
                <div style="font-size:0.85rem;color:#999;font-weight:700;letter-spacing:1px;margin-bottom:10px;">
                {p['code']}</div>
                <div class="example">{ex_html}</div>
                <div style="background:#fff;border-radius:8px;padding:8px 12px;margin-top:10px;
                font-size:0.9rem;border:1px dashed var(--green-light);">
                📖 {eng}<br><span style="color:#6b7280;font-size:0.82rem;">{kor}</span></div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# 난이도 토글 (게임 탭 공통 안내)
# ══════════════════════════════════════════
def difficulty_toggle(key):
    c1, c2 = st.columns([3, 1])
    with c1:
        level_txt = "⭐⭐⭐ Hard (어려운 단어 포함)" if st.session_state.irr_hard else "⭐ Easy (쉬운 단어만)"
        st.markdown(f"**현재 난이도: {level_txt}**")
    with c2:
        label = "Easy로 바꾸기" if st.session_state.irr_hard else "Hard 도전! 🔥"
        if st.button(label, key=key, use_container_width=True):
            st.session_state.irr_hard = not st.session_state.irr_hard
            st.rerun()

# ══════════════════════════════════════════
# 탭 2 — 새 잡기 게임
# ══════════════════════════════════════════
with tab2:
    st.markdown("#### 🐦 새 잡기 게임")
    st.caption("현재형을 보고, 과거형이 등에 적힌 새를 60초 안에 잡아! 🦝")
    difficulty_toggle("bird_diff")

    verbs = get_game_verbs(st.session_state.irr_hard)
    html = bird_game_html(verbs, num_birds=5, game_time=60)
    components.html(html, height=560, scrolling=False)

# ══════════════════════════════════════════
# 탭 3 — 3단 변화 완성 게임
# ══════════════════════════════════════════
with tab3:
    st.markdown("#### 🧩 3단 변화 완성")
    st.caption("원형을 보고 과거형·과거분사형을 채워보자! 10문제 🦝")
    difficulty_toggle("form_diff")

    NUM_Q = 10

    def init_form_game():
        pool = get_game_verbs(st.session_state.irr_hard)
        # 3단 변화가 한 글자라도 다른 동사 위주로 (A-A-A는 너무 쉬워서 일부만)
        random.shuffle(pool)
        selected = pool[:NUM_Q]
        st.session_state.form_game = {
            "questions": selected,
            "idx": 0,
            "score": 0,
            "stage": "past",   # past → pp
            "checked": False,
            "picked": None,
            "history": [],
            "raccoon": "원형을 보고 과거형부터 골라봐! 🦝",
            "finished": False,
        }
        for k in list(st.session_state.keys()):
            if k.startswith("form_choices_"):
                del st.session_state[k]

    if "form_game" not in st.session_state:
        init_form_game()

    fg = st.session_state.form_game

    def form_choices(q, stage, pool):
        correct = q[stage]
        others = [v[stage] for v in pool if v[stage] != correct]
        random.shuffle(others)
        opts = [correct] + others[:3]
        random.shuffle(opts)
        return opts

    # ── 결과 화면 ──
    if fg["finished"]:
        score = fg["score"]
        total = len(fg["questions"]) * 2  # 과거형+과거분사
        st.markdown(f"""
        <div class="raccoon-bubble" style="margin-bottom:12px;">
        🦝 끝났어! <b>{total}개 중 {score}개</b> 맞았어! {"완벽해! 🏆" if score==total else "잘했어! 🎉"}<br>
        아래에서 정답을 확인하자! 👇
        </div>
        """, unsafe_allow_html=True)

        rows = ""
        for h in fg["history"]:
            cls = "ok" if h["ok"] else "no"
            mark = "✅" if h["ok"] else "❌"
            bg = "#d1fae5" if h["ok"] else "#fee2e2"
            color = "var(--green)" if h["ok"] else "var(--red)"
            rows += (
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'background:{bg};color:{color};padding:8px 14px;border-radius:10px;'
                f'margin-bottom:5px;font-weight:700;">'
                f'<span>{mark} {h["base"]} → {h["past"]} → {h["pp"]}</span>'
                f'<span style="font-weight:500;font-size:0.85rem;opacity:.8;">{h["meaning"]}</span></div>'
            )
        st.markdown(f'<div style="max-height:300px;overflow-y:auto;">{rows}</div>',
                    unsafe_allow_html=True)

        if st.button("🔄 다시 도전", key="form_restart"):
            init_form_game()
            st.rerun()
    else:
        q = fg["questions"][fg["idx"]]
        pool = get_game_verbs(st.session_state.irr_hard)
        q_num = fg["idx"] + 1
        total = len(fg["questions"])

        st.caption(f"문제 {q_num} / {total}")

        # 진행 카드: 원형 + (과거형/과거분사 빈칸)
        past_show = q["past"] if (fg["stage"] == "pp" or fg["checked"]) else "???"
        pp_show = q["pp"] if fg["checked"] and fg["stage"] == "pp" else "???"
        # 단계별 강조
        past_hl = "var(--yellow)" if fg["stage"] == "past" else "var(--green-pale)"
        pp_hl = "var(--yellow)" if fg["stage"] == "pp" else "var(--green-pale)"

        st.markdown(f"""
        <div class="verb-display" style="background:var(--green);">
            <div class="verb-meaning" style="color:#d8f3dc;">뜻: {q['meaning']}</div>
            <div class="verb-base" style="color:#fff;">{q['base']}</div>
            <div style="display:flex;justify-content:center;gap:12px;margin-top:8px;flex-wrap:wrap;">
                <div style="background:{past_hl};border-radius:10px;padding:6px 18px;">
                    <div style="font-size:0.72rem;color:#444;font-weight:600;">과거형</div>
                    <div style="font-size:1.1rem;font-weight:800;color:var(--green);">{past_show}</div>
                </div>
                <div style="background:{pp_hl};border-radius:10px;padding:6px 18px;">
                    <div style="font-size:0.72rem;color:#444;font-weight:600;">과거분사형</div>
                    <div style="font-size:1.1rem;font-weight:800;color:var(--green);">{pp_show}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 너구리 질문
        st.markdown(f"""
        <div class="raccoon-row">
            <div class="raccoon-bubble">{fg['raccoon']}</div>
        </div>
        """, unsafe_allow_html=True)

        # 보기 카드 버튼
        ckey = f"form_choices_{fg['idx']}_{fg['stage']}"
        if ckey not in st.session_state:
            st.session_state[ckey] = form_choices(q, fg["stage"], pool)
        choices = st.session_state[ckey]

        if not fg["checked"]:
            st.markdown('<div class="choice-btn-wrap">', unsafe_allow_html=True)
            bcols = st.columns(len(choices))
            for i, ch in enumerate(choices):
                with bcols[i]:
                    if st.button(ch, key=f"form_pick_{fg['idx']}_{fg['stage']}_{i}", use_container_width=True):
                        fg["checked"] = True
                        fg["picked"] = ch
                        correct = q[fg["stage"]]
                        if ch == correct:
                            fg["score"] += 1
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            correct = q[fg["stage"]]
            stage_ko = "과거형" if fg["stage"] == "past" else "과거분사형"
            if fg["picked"] == correct:
                st.markdown(f"""
                <div class="raccoon-bubble" style="border-left:5px solid var(--green);">
                정답이야! 🎉 {stage_ko}은 <b>{correct}</b> 맞아!</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="raccoon-bubble" style="border-left:5px solid var(--red);">
                틀렸어! 🦝 {stage_ko}은 <b>{correct}</b>(이)야. 기억해두자! 💪</div>
                """, unsafe_allow_html=True)

            nxt_label = "다음 →"
            if fg["stage"] == "past":
                nxt_label = "과거분사형 풀기 →"
            elif fg["idx"] + 1 >= total:
                nxt_label = "결과 보기 →"

            if st.button(nxt_label, key=f"form_next_{fg['idx']}_{fg['stage']}", type="primary"):
                if fg["stage"] == "past":
                    # 과거형 단계 결과 임시 저장
                    fg["_past_ok"] = (fg["picked"] == q["past"])
                    fg["stage"] = "pp"
                    fg["checked"] = False
                    fg["picked"] = None
                    fg["raccoon"] = "이번엔 과거분사형을 골라봐! 🧩"
                else:
                    pp_ok = (fg["picked"] == q["pp"])
                    fg["history"].append({
                        "base": q["base"], "past": q["past"], "pp": q["pp"],
                        "meaning": q["meaning"],
                        "ok": fg.get("_past_ok", False) and pp_ok,
                    })
                    if fg["idx"] + 1 >= total:
                        fg["finished"] = True
                    else:
                        fg["idx"] += 1
                        fg["stage"] = "past"
                        fg["checked"] = False
                        fg["picked"] = None
                        fg["raccoon"] = "다음 동사! 과거형부터 골라봐! 🦝"
                st.rerun()

# ══════════════════════════════════════════
# 탭 4 — 동사 리스트
# ══════════════════════════════════════════
with tab4:
    st.markdown("#### 📋 불규칙 동사 리스트")
    st.caption("유형을 골라서 동사를 찾아봐! 🔍")

    df = get_irregular_verbs()
    type_options = ["전체"] + sorted(df["type"].unique().tolist())
    type_choice = st.selectbox("유형 선택", type_options, key="list_type")

    filtered = df if type_choice == "전체" else df[df["type"] == type_choice]
    display_df = filtered[["base", "past", "pp", "meaning", "type"]].rename(columns={
        "base": "원형", "past": "과거형", "pp": "과거분사", "meaning": "뜻", "type": "유형",
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"총 {len(display_df)}개")
