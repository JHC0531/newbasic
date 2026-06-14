import random
import streamlit as st
import streamlit.components.v1 as components
from utils import (
    inject_global_css, MASCOT_PATH, get_irregular_verbs,
    get_game_verbs, get_verbs_by_type, check_answer,
)
from bird_game import bird_game_html
from word_cards import word_cards_html

inject_global_css()

st.title("불규칙 변화 📖")
st.markdown(
    '<div style="font-size:1.05rem;font-weight:600;color:var(--green);margin-bottom:6px;">'
    '유형별로 듣고 익힌 다음, 게임으로 마스터하자! 🎧🎮</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# 난이도 상태 (게임 공통)
if "irr_hard" not in st.session_state:
    st.session_state.irr_hard = False

# 유형별 탭 정의 (special 포함)
TYPE_TABS = [
    ("A-A-A", "🟰 A-A-A", "세 형태가 모두 같아요!"),
    ("A-A-B", "✌️ A-A-B", "과거형은 같고 과거분사만 달라요!"),
    ("A-B-A", "🔄 A-B-A", "원형과 과거분사가 같아요!"),
    ("A-B-B", "👯 A-B-B", "과거형과 과거분사가 같아요!"),
    ("A-B-C", "🌈 A-B-C", "세 형태가 모두 달라요!"),
    ("special", "⭐ special", "be동사·조동사 등 특별한 동사!"),
]

tab_labels = [t[1] for t in TYPE_TABS] + ["🐦 새 잡기 게임", "🧩 3단 변화 마스터"]
tabs = st.tabs(tab_labels)

# ══════════════════════════════════════════
# 유형별 학습 탭 (TTS 단어 카드)
# ══════════════════════════════════════════
for i, (vtype, label, desc) in enumerate(TYPE_TABS):
    with tabs[i]:
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:12px 18px;
        box-shadow:0 3px 10px rgba(0,0,0,0.06);margin-bottom:12px;">
        <span style="font-size:1.15rem;font-weight:800;color:var(--green);">{label}</span>
        &nbsp;<span style="color:#666;">{desc}</span><br>
        <span style="font-size:0.85rem;color:#999;">🔊 버튼을 누르면 발음을 들을 수 있어! 🦝</span>
        </div>
        """, unsafe_allow_html=True)

        verbs = get_verbs_by_type(vtype)
        if not verbs:
            st.info("이 유형에는 동사가 없어요.")
        else:
            html, height = word_cards_html(verbs)
            components.html(html, height=height, scrolling=True)

# ══════════════════════════════════════════
# 난이도 토글
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
# 새 잡기 게임
# ══════════════════════════════════════════
with tabs[len(TYPE_TABS)]:
    st.markdown("#### 🐦 새 잡기 게임")
    st.caption("현재형을 보고, 과거형이 등에 적힌 새를 60초 안에 잡아! 🦝")
    difficulty_toggle("bird_diff")
    verbs = get_game_verbs(st.session_state.irr_hard)
    html = bird_game_html(verbs, num_birds=5, game_time=60)
    components.html(html, height=560, scrolling=False)

# ══════════════════════════════════════════
# 3단 변화 마스터 (주관식)
# ══════════════════════════════════════════
with tabs[len(TYPE_TABS) + 1]:
    st.markdown("#### 🧩 3단 변화 마스터")
    st.caption("원형을 보고 과거형·과거분사형을 직접 입력해보자! 10문제 ✍️🦝")
    difficulty_toggle("master_diff")

    NUM_Q = 10

    def init_master():
        pool = get_game_verbs(st.session_state.irr_hard)
        random.shuffle(pool)
        st.session_state.master = {
            "questions": pool[:NUM_Q],
            "idx": 0,
            "score": 0,
            "checked": False,
            "history": [],
            "finished": False,
        }

    if "master" not in st.session_state:
        init_master()

    mg = st.session_state.master

    # ── 결과 화면 ──
    if mg["finished"]:
        score = mg["score"]
        total = len(mg["questions"]) * 2
        st.markdown(f"""
        <div class="raccoon-row">
            <div class="raccoon-bubble">
            🦝 끝났어! <b>{total}개 중 {score}개</b> 맞았어! {"완벽해! 🏆" if score==total else "잘했어! 🎉"}<br>
            아래에서 정답을 확인하자! 👇</div>
        </div>
        """, unsafe_allow_html=True)

        rows = ""
        for h in mg["history"]:
            ok = h["past_ok"] and h["pp_ok"]
            bg = "#d1fae5" if ok else "#fee2e2"
            color = "var(--green)" if ok else "var(--red)"
            mark = "✅" if ok else "❌"
            # 틀린 부분 표시
            past_disp = h["past"] if h["past_ok"] else f'<s style="color:#999;">{h["past_in"] or "—"}</s> → {h["past"]}'
            pp_disp = h["pp"] if h["pp_ok"] else f'<s style="color:#999;">{h["pp_in"] or "—"}</s> → {h["pp"]}'
            rows += (
                f'<div style="background:{bg};color:{color};padding:9px 14px;border-radius:10px;'
                f'margin-bottom:6px;font-weight:700;">'
                f'{mark} <b>{h["base"]}</b> → {past_disp} → {pp_disp} '
                f'<span style="font-weight:500;font-size:0.83rem;opacity:.75;">({h["meaning"]})</span></div>'
            )
        st.markdown(f'<div style="max-height:340px;overflow-y:auto;">{rows}</div>',
                    unsafe_allow_html=True)

        if st.button("🔄 다시 도전", key="master_restart"):
            init_master()
            st.rerun()
    else:
        q = mg["questions"][mg["idx"]]
        q_num = mg["idx"] + 1
        total = len(mg["questions"])
        st.caption(f"문제 {q_num} / {total}  ·  점수 {mg['score']}")

        # 문제 카드
        st.markdown(f"""
        <div class="verb-display" style="background:var(--green);">
            <div class="verb-meaning" style="color:#d8f3dc;">뜻: {q['meaning']}</div>
            <div class="verb-base" style="color:#fff;">{q['base']}</div>
        </div>
        """, unsafe_allow_html=True)

        # 너구리 질문
        st.markdown("""
        <div class="raccoon-row">
            <div class="raccoon-bubble">과거형과 과거분사형을 입력해봐! ✍️🦝</div>
        </div>
        """, unsafe_allow_html=True)

        if not mg["checked"]:
            ci1, ci2 = st.columns(2)
            with ci1:
                past_in = st.text_input("과거형 (past)", key=f"past_in_{mg['idx']}", placeholder="예: went")
            with ci2:
                pp_in = st.text_input("과거분사형 (past participle)", key=f"pp_in_{mg['idx']}", placeholder="예: gone")

            if st.button("정답 확인 ✅", key=f"master_check_{mg['idx']}", type="primary"):
                past_ok = check_answer(past_in, q["past"])
                pp_ok = check_answer(pp_in, q["pp"])
                if past_ok:
                    mg["score"] += 1
                if pp_ok:
                    mg["score"] += 1
                mg["history"].append({
                    "base": q["base"], "past": q["past"], "pp": q["pp"], "meaning": q["meaning"],
                    "past_in": past_in.strip(), "pp_in": pp_in.strip(),
                    "past_ok": past_ok, "pp_ok": pp_ok,
                })
                mg["checked"] = True
                st.rerun()
        else:
            h = mg["history"][-1]
            # 과거형 피드백
            if h["past_ok"]:
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--green);">'
                            f'과거형 정답! 🎉 <b>{q["past"]}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--red);">'
                            f'과거형은 <b>{q["past"]}</b>(이)야! 💪 (네 답: {h["past_in"] or "—"})</div>',
                            unsafe_allow_html=True)
            # 과거분사 피드백
            if h["pp_ok"]:
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--green);">'
                            f'과거분사형 정답! 🎉 <b>{q["pp"]}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--red);">'
                            f'과거분사형은 <b>{q["pp"]}</b>(이)야! 💪 (네 답: {h["pp_in"] or "—"})</div>',
                            unsafe_allow_html=True)

            is_last = mg["idx"] + 1 >= total
            label = "결과 보기 →" if is_last else "다음 문제 →"
            if st.button(label, key=f"master_next_{mg['idx']}", type="primary"):
                if is_last:
                    mg["finished"] = True
                else:
                    mg["idx"] += 1
                    mg["checked"] = False
                st.rerun()
