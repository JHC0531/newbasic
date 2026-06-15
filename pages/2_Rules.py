import random
import streamlit as st
import streamlit.components.v1 as components
from utils import (
    inject_global_css, MASCOT_PATH, load_rules_quiz,
    get_regular_verbs, ed_fake_spellings, classify_ed_sound,
    RULE_NAMES, SOUND_NAMES, make_homework_cert,
)
from bird_game import bird_game_html
from pron_listen import pron_listen_html

inject_global_css()

st.title("규칙 변화 📝")
st.markdown(
    '<div style="font-size:1.05rem;font-weight:600;color:var(--green);margin-bottom:6px;">'
    '진단평가 → 규칙 학습 → 게임 → 숙제 순서로 master하자! 🚀</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

quiz_df = load_rules_quiz()

# ──────────────────────────────────────────
# 공통 헬퍼
# ──────────────────────────────────────────
def raccoon_bubble(text, border=None):
    style = f"border-left:5px solid {border};" if border else ""
    c1, c2 = st.columns([1, 6])
    with c1:
        st.image(str(MASCOT_PATH), width=88)
    with c2:
        st.markdown(f'<div class="raccoon-bubble" style="margin-top:14px;{style}">{text}</div>',
                    unsafe_allow_html=True)


def feedback_bubble(text, border=None):
    style = f"border-left:5px solid {border};" if border else ""
    st.markdown(f'<div class="raccoon-bubble" style="margin:6px 0;{style}">{text}</div>',
                unsafe_allow_html=True)


def word_card(big_text, sub_text="과거형을 골라봐!"):
    st.markdown(f"""
    <div class="verb-display" style="background:var(--green);">
        <div class="verb-meaning" style="color:#d8f3dc;">{sub_text}</div>
        <div class="verb-base" style="color:#ffffff;">{big_text}</div>
    </div>
    """, unsafe_allow_html=True)


def choice_buttons(choices, key_prefix):
    """큰 카드형 보기 버튼. 클릭된 선택을 반환(없으면 None)."""
    st.markdown('<div class="choice-btn-wrap">', unsafe_allow_html=True)
    picked = None
    bcols = st.columns(len(choices))
    for i, ch in enumerate(choices):
        with bcols[i]:
            if st.button(str(ch), key=f"{key_prefix}_{i}", use_container_width=True):
                picked = ch
    st.markdown('</div>', unsafe_allow_html=True)
    return picked


# ══════════════════════════════════════════════════════════
# 규칙 4개 탭 정의
# ══════════════════════════════════════════════════════════
RULE_TABS = [
    {
        "label": "1️⃣ 동사원형 + -ed", "rule_keys": ["1"],
        "title": "가장 일반적인 경우: 동사원형 + -ed",
        "desc": "대부분의 일반 동사는 동사원형 뒤에 <b>-ed</b>를 붙여요!",
        "examples": ["want → wanted", "talk → talked", "clean → cleaned"],
        "sentence": ("I <b>listened</b> to jazz music last night.", "나는 어젯밤에 재즈 음악을 들었다."),
        "reason": "동사원형 뒤에 그대로 <b>-ed</b>를 붙이는 가장 기본 규칙이야!",
    },
    {
        "label": "2️⃣ 자음 + e → -d", "rule_keys": ["2"],
        "title": "자음 + e로 끝나는 경우: -d만 추가",
        "desc": "이미 <b>e</b>로 끝나니까 <b>d</b>만 붙이면 돼요. 😎",
        "examples": ["like → liked", "live → lived", "love → loved"],
        "sentence": ("Many students <b>liked</b> the new school event.", "많은 학생들이 새 행사를 좋아했다."),
        "reason": "이미 <b>e</b>로 끝나니까 <b>d</b>만 붙여! (ed를 통째로 붙이지 않아)",
    },
    {
        "label": "3️⃣ -y 규칙 🔑", "rule_keys": ["3a", "3b"],
        "title": "-y로 끝나는 경우: 두 가지로 나뉘어요!",
        "desc": ("<b>자음 + y</b> → y를 <b>i</b>로 바꾸고 -ed (study → studied)<br>"
                 "<b>모음 + y</b> → 그대로 -ed (play → played)"),
        "examples": ["study → studied", "try → tried", "play → played", "enjoy → enjoyed"],
        "sentence": ("He <b>studied</b> in the library.", "그는 도서관에서 공부했다."),
        "reason": "y 앞이 <b>자음</b>이면 y→i로 바꾸고 ed, <b>모음</b>이면 그대로 ed!",
    },
    {
        "label": "4️⃣ 단모음+단자음 ✌️", "rule_keys": ["4"],
        "title": "단모음 + 단자음으로 끝나는 경우: 자음을 한 번 더!",
        "desc": "짧은 모음 + 자음 하나로 끝나면, 마지막 자음을 <b>하나 더 쓰고</b> -ed!",
        "examples": ["stop → stopped", "plan → planned", "hug → hugged"],
        "sentence": ("The police <b>stepped</b> into the room.", "경찰이 방 안으로 발을 들여놓았다."),
        "reason": "단모음+단자음이라 마지막 <b>자음을 하나 더 쓰고</b> ed를 붙여!",
    },
]

# 탭 생성: 진단평가 + 규칙4 + 새잡기 + HOMEWORK
tab_labels = ["🩺 진단평가"] + [t["label"] for t in RULE_TABS] + ["🐦 새 잡기 게임", "📒 HOMEWORK"]
tabs = st.tabs(tab_labels)


# ══════════════════════════════════════════════════════════
# 발음 문제 / 규칙 문제 생성 (진단평가·HOMEWORK 공용)
# ══════════════════════════════════════════════════════════
def make_pron_question(verb):
    """발음 듣기 문제 1개 생성"""
    fk = ed_fake_spellings(verb["base"])
    # 3개 보기: 1=/t/, 2=/d/, 3=/ɪd/ 순서 고정 (들어보고 고르기)
    options = [
        {"label": "1", "speak": fk["t"], "sound": "t"},
        {"label": "2", "speak": fk["d"], "sound": "d"},
        {"label": "3", "speak": fk["id"], "sound": "id"},
    ]
    return {
        "type": "pron",
        "word": verb["past"],
        "base": verb["base"],
        "options": options,
        "answer_sound": verb["sound"],
        "rule": verb["rule"],
    }


def make_spell_question(verb, pool):
    """규칙 적용(철자) 문제 1개 생성 — 동사원형 보고 과거형 고르기"""
    correct = verb["past"]
    # 오답: 흔한 실수형
    b = verb["base"]
    wrongs = set()
    if b.endswith("e"):
        wrongs.add(b + "ed")
    else:
        wrongs.add(b + "d")
    wrongs.add(b + "ed" if not b.endswith("e") else b[:-1] + "ed")
    if b.endswith("y"):
        wrongs.add(b + "ed")
    wrongs.discard(correct)
    wrongs = list(wrongs)[:2]
    # 모자라면 다른 동사 과거형으로
    while len(wrongs) < 2:
        cand = random.choice(pool)["past"]
        if cand != correct and cand not in wrongs:
            wrongs.append(cand)
    choices = [correct] + wrongs
    random.shuffle(choices)
    return {
        "type": "spell",
        "word": verb["base"],
        "answer": correct,
        "choices": choices,
        "rule": verb["rule"],
    }


# ══════════════════════════════════════════════════════════
# 탭 0 — 진단평가
# ══════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("#### 🩺 진단평가")
    st.caption("배울 내용을 미리 풀어보고, 어떤 규칙·발음을 공부해야 할지 확인하자! 🦝")

    NUM_DIAG = 10

    def init_diag():
        pool = get_regular_verbs(include_extra=True)
        random.shuffle(pool)
        questions = []
        # 발음 5 + 규칙 5 섞기
        pron_pool = [v for v in pool]
        random.shuffle(pron_pool)
        for v in pron_pool[:5]:
            questions.append(make_pron_question(v))
        for v in pron_pool[5:10]:
            questions.append(make_spell_question(v, pool))
        random.shuffle(questions)
        st.session_state.diag = {
            "questions": questions, "idx": 0, "checked": False, "picked": None,
            "wrong_rules": set(), "wrong_sounds": set(), "score": 0, "finished": False,
        }

    if "diag" not in st.session_state:
        init_diag()
    dg = st.session_state.diag

    if dg["finished"]:
        score = dg["score"]
        total = len(dg["questions"])
        raccoon_bubble(f"진단 끝! <b>{total}문제 중 {score}개</b> 맞았어! 🎉")

        # 학습 처방
        st.markdown("##### 📋 너구리쌤의 학습 처방전")
        known_rules = set(RULE_NAMES) - dg["wrong_rules"]
        if dg["wrong_rules"] or dg["wrong_sounds"]:
            if known_rules:
                ok_txt = ", ".join(RULE_NAMES[r] for r in sorted(known_rules) if r in RULE_NAMES)
                if ok_txt:
                    st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--green);">'
                                f'✅ <b>잘 아는 규칙</b>: {ok_txt}</div>', unsafe_allow_html=True)
            if dg["wrong_rules"]:
                no_txt = ", ".join(RULE_NAMES[r] for r in sorted(dg["wrong_rules"]) if r in RULE_NAMES)
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--red);">'
                            f'📌 <b>다시 공부할 규칙</b>: {no_txt} → 해당 탭에서 복습하자!</div>',
                            unsafe_allow_html=True)
            if dg["wrong_sounds"]:
                snd_txt = ", ".join(SOUND_NAMES[s] for s in sorted(dg["wrong_sounds"]) if s in SOUND_NAMES)
                st.markdown(f'<div class="raccoon-bubble" style="border-left:5px solid var(--red);">'
                            f'🔊 <b>다시 들어볼 발음</b>: {snd_txt}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="raccoon-bubble" style="border-left:5px solid var(--green);">'
                        '🏆 완벽해! 모든 규칙과 발음을 잘 알고 있어! 그래도 한 번 더 복습하면 더 좋아!</div>',
                        unsafe_allow_html=True)

        if st.button("🔄 다시 진단하기", key="diag_restart"):
            init_diag()
            st.rerun()
    else:
        q = dg["questions"][dg["idx"]]
        q_num = dg["idx"] + 1
        total = len(dg["questions"])
        st.caption(f"문제 {q_num} / {total}")

        if q["type"] == "pron":
            # 발음 듣기 문제
            html = pron_listen_html(q["word"], q["options"])
            components.html(html, height=290, scrolling=False)
            st.markdown('<div style="font-weight:700;color:var(--green);margin:6px 0;">'
                        '🦝 위 단어의 알맞은 발음은 몇 번일까?</div>', unsafe_allow_html=True)
            if not dg["checked"]:
                picked = choice_buttons(["1번 /t/", "2번 /d/", "3번 /ɪd/"], f"diag_pron_{dg['idx']}")
                if picked:
                    sound_map = {"1번 /t/": "t", "2번 /d/": "d", "3번 /ɪd/": "id"}
                    dg["picked"] = sound_map[picked]
                    dg["checked"] = True
                    if dg["picked"] == q["answer_sound"]:
                        dg["score"] += 1
                    else:
                        dg["wrong_sounds"].add(q["answer_sound"])
                    st.rerun()
            else:
                if dg["picked"] == q["answer_sound"]:
                    feedback_bubble(f"정답이에요! 🎉 <b>{q['word']}</b>는 {SOUND_NAMES[q['answer_sound']]}!",
                                    border="var(--green)")
                else:
                    feedback_bubble(f"틀렸어! 🦝 <b>{q['word']}</b>의 발음은 {SOUND_NAMES[q['answer_sound']]}(이)야.",
                                    border="var(--red)")
        else:
            # 규칙 적용 문제
            word_card(q["word"], "이 동사의 과거형은?")
            if not dg["checked"]:
                picked = choice_buttons(q["choices"], f"diag_spell_{dg['idx']}")
                if picked:
                    dg["picked"] = picked
                    dg["checked"] = True
                    if picked == q["answer"]:
                        dg["score"] += 1
                    else:
                        dg["wrong_rules"].add(q["rule"])
                    st.rerun()
            else:
                if dg["picked"] == q["answer"]:
                    feedback_bubble(f"정답이에요! 🎉 <b>{q['word']} → {q['answer']}</b>", border="var(--green)")
                else:
                    rule_name = RULE_NAMES.get(q["rule"], "")
                    feedback_bubble(f"틀렸어! 🦝 답은 <b>{q['answer']}</b>(이)야. "
                                    f"<br><span style='font-size:0.9rem;color:#555;'>👉 규칙: {rule_name}</span>",
                                    border="var(--red)")

        if dg["checked"]:
            is_last = dg["idx"] + 1 >= total
            label = "진단 결과 보기 →" if is_last else "다음 문제 →"
            if st.button(label, key=f"diag_next_{dg['idx']}", type="primary"):
                if is_last:
                    dg["finished"] = True
                else:
                    dg["idx"] += 1
                    dg["checked"] = False
                    dg["picked"] = None
                st.rerun()


# ══════════════════════════════════════════════════════════
# 탭 1~4 — 규칙 학습 + 미니퀴즈
# ══════════════════════════════════════════════════════════
QUESTIONS_PER_QUIZ = 3


def init_rule_quiz(tab_idx, rule_keys):
    pool = quiz_df[quiz_df["규칙번호"].isin(rule_keys)].to_dict("records")
    random.shuffle(pool)
    st.session_state[f"rq_{tab_idx}"] = {
        "questions": pool[:QUESTIONS_PER_QUIZ], "idx": 0, "score": 0,
        "checked": False, "picked": None, "finished": False,
    }
    for k in list(st.session_state.keys()):
        if k.startswith(f"rqchoices_{tab_idx}_"):
            del st.session_state[k]


def render_rule_quiz(tab_idx, rule_keys, reason):
    sk = f"rq_{tab_idx}"
    if sk not in st.session_state:
        init_rule_quiz(tab_idx, rule_keys)
    qs = st.session_state[sk]

    if qs["finished"]:
        score, total = qs["score"], len(qs["questions"])
        msg = "완벽해! 🏆" if score == total else "잘했어! 🦝"
        feedback_bubble(f"{total}문제 중 <b>{score}개</b> 맞았어! {msg}")
        if st.button("🔄 복습하기", key=f"rqreview_{tab_idx}"):
            init_rule_quiz(tab_idx, rule_keys)
            st.rerun()
        return

    q = qs["questions"][qs["idx"]]
    total = len(qs["questions"])
    st.caption(f"문제 {qs['idx']+1} / {total}")

    ckey = f"rqchoices_{tab_idx}_{qs['idx']}"
    if ckey not in st.session_state:
        ch = [q["정답"], q["오답1"], q["오답2"]]
        random.shuffle(ch)
        st.session_state[ckey] = ch
    choices = st.session_state[ckey]

    word_card(q["동사원형"], "이 동사의 과거형은?")
    raccoon_bubble("정답을 골라봐! 🦝")

    if not qs["checked"]:
        picked = choice_buttons(choices, f"rqpick_{tab_idx}_{qs['idx']}")
        if picked:
            qs["checked"] = True
            qs["picked"] = picked
            if picked == q["정답"]:
                qs["score"] += 1
            st.rerun()
    else:
        if qs["picked"] == q["정답"]:
            feedback_bubble(f"정답이에요! 🎉 <b>{q['동사원형']} → {q['정답']}</b>", border="var(--green)")
        else:
            feedback_bubble(f"틀렸어! 🦝 답은 <b>{q['동사원형']} → {q['정답']}</b>(이)야.<br>"
                            f"<span style='font-size:0.92rem;color:#555;'>👉 {reason}</span>",
                            border="var(--red)")
        sentence = str(q.get("예문", "")).strip()
        if sentence and sentence.lower() != "nan":
            hl = sentence.replace(q["정답"], f"<b style='color:var(--green)'>{q['정답']}</b>")
            st.markdown(f"<div style='margin:10px 0;color:#555;'>📖 {hl}</div>", unsafe_allow_html=True)
        is_last = qs["idx"] + 1 >= total
        if st.button("결과 보기 →" if is_last else "계속하기 →", key=f"rqnext_{tab_idx}", type="primary"):
            if is_last:
                qs["finished"] = True
            else:
                qs["idx"] += 1
                qs["checked"] = False
                qs["picked"] = None
            st.rerun()


for i, tab_def in enumerate(RULE_TABS):
    with tabs[i + 1]:
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
        render_rule_quiz(i + 1, tab_def["rule_keys"], tab_def["reason"])


# ══════════════════════════════════════════════════════════
# 탭 5 — 새 잡기 게임 (규칙 동사, 현재형→과거형)
# ══════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("#### 🐦 새 잡기 게임")
    st.caption("현재형을 보고, 과거형이 등에 적힌 새를 60초 안에 잡아! 🦝")
    reg_verbs = get_regular_verbs(include_extra=True)
    # bird_game은 {base, past, pp, meaning} 형식 필요 → 맞춰주기
    game_verbs = [{"base": v["base"], "past": v["past"], "pp": v["past"],
                   "meaning": ""} for v in reg_verbs]
    html = bird_game_html(game_verbs, num_birds=5, game_time=60)
    components.html(html, height=560, scrolling=False)

    # ── 반 전체 순위표 (규칙 동사 전용) ──
    import leaderboard as lb

    if lb.is_online_ranking_available():
        # 자동 수신: URL 쿼리로 들어온 점수를 시트에 저장
        components.html("""
        <script>
        const seen = new Set();
        window.addEventListener('message', (ev)=>{
          const d = ev.data;
          if(!d || d.type!=='bird_score') return;
          const key = d.ts || (d.name+'_'+d.score);
          if(seen.has(key)) return;
          seen.add(key);
          try{
            const top = window.parent;
            const url = new URL(top.location.href);
            url.searchParams.set('rbird_name', d.name||'');
            url.searchParams.set('rbird_score', d.score||0);
            url.searchParams.set('rbird_ts', d.ts||Date.now());
            top.location.href = url.toString();
          }catch(e){}
        });
        </script>
        """, height=0)

        qp = st.query_params
        if "rbird_score" in qp and "rbird_name" in qp:
            ts = qp.get("rbird_ts", "")
            if ts != st.session_state.get("last_saved_rbird"):
                nm = qp.get("rbird_name", "").strip()
                try:
                    sc = int(qp.get("rbird_score", 0))
                except (ValueError, TypeError):
                    sc = 0
                if nm:
                    if lb.add_score(nm, sc, game="regular"):
                        lb.get_ranking.clear()
                        st.session_state.last_saved_rbird = ts
                        st.success(f"🎉 {nm}님의 {sc}점이 규칙 순위표에 등록됐어!")
            st.query_params.clear()

        st.markdown("---")
        st.markdown("### 🏆 우리 반 순위표 (규칙 동사)")
        st.caption("게임이 끝나면 점수가 자동으로 등록돼요! 안 되면 아래에 직접 입력해도 돼 🦝")

        with st.expander("✍️ 점수 직접 등록하기 (자동 등록이 안 될 때)"):
            rc1, rc2, rc3 = st.columns([2, 1, 1])
            with rc1:
                reg_name = st.text_input("이름", key="rlb_name", placeholder="예: 김지현")
            with rc2:
                reg_score = st.number_input("점수", min_value=0, max_value=999, step=1, key="rlb_score")
            with rc3:
                st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                if st.button("순위 등록 🏅", key="rlb_submit", use_container_width=True):
                    if reg_name.strip():
                        if lb.add_score(reg_name.strip(), int(reg_score), game="regular"):
                            lb.get_ranking.clear()
                            st.success(f"🎉 {reg_name.strip()}님, {int(reg_score)}점 등록 완료!")
                        else:
                            st.error("등록에 실패했어요. 잠시 후 다시 시도해줘.")
                    else:
                        st.warning("이름을 입력해줘!")

        ranking = lb.get_ranking(top_n=20, game="regular")
        if ranking:
            medals = ["🥇", "🥈", "🥉"]
            rows = ""
            for i, e in enumerate(ranking):
                rank = medals[i] if i < 3 else f"<b>{i+1}</b>"
                bg = "#fff8e1" if i < 3 else "#f1f6f2"
                rows += (
                    f'<div style="display:flex;align-items:center;justify-content:space-between;'
                    f'background:{bg};padding:9px 16px;border-radius:10px;margin-bottom:5px;font-weight:700;">'
                    f'<span style="width:46px;font-size:1.1rem;">{rank}</span>'
                    f'<span style="flex:1;color:#333;">{e["name"]}</span>'
                    f'<span style="color:var(--green);font-weight:800;">{e["score"]}점</span></div>'
                )
            st.markdown(f'<div style="max-width:480px;">{rows}</div>', unsafe_allow_html=True)
            if st.button("🔄 순위표 새로고침", key="rlb_refresh"):
                lb.get_ranking.clear()
                st.rerun()
        else:
            st.info("아직 등록된 점수가 없어요. 첫 번째 도전자가 되어보자! 🦝")
    else:
        st.caption("💡 게임 안에서 같은 기기 순위가 표시돼요. (반 전체 순위표는 준비 중)")


# ══════════════════════════════════════════════════════════
# 탭 6 — HOMEWORK
# ══════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("#### 📒 HOMEWORK")
    st.caption("발음 5문제 + 과거형 5문제! 다 풀면 숙제 확인증을 받을 수 있어! 🦝✨")

    NUM_HW = 10

    def init_hw():
        pool = get_regular_verbs(include_extra=True)
        random.shuffle(pool)
        questions = []
        for v in pool[:5]:
            questions.append(make_pron_question(v))
        for v in pool[5:10]:
            questions.append(make_spell_question(v, pool))
        random.shuffle(questions)
        st.session_state.hw = {
            "questions": questions, "idx": 0, "checked": False, "picked": None,
            "score": 0, "finished": False, "name": "",
        }

    if "hw" not in st.session_state:
        init_hw()
    hw = st.session_state.hw

    if hw["finished"]:
        score = hw["score"]
        total = len(hw["questions"])
        raccoon_bubble(f"숙제 완료! <b>{total}문제 중 {score}개</b> 맞았어! 🎉")

        name = st.text_input("이름을 입력하면 숙제 확인증을 만들어줄게! ✍️", key="hw_name")
        if name.strip():
            cert = make_homework_cert(name.strip(), score, total)
            st.image(cert, caption="숙제 확인증 🦝", use_container_width=True)
            st.download_button("📥 숙제 확인증 저장하기", data=cert,
                               file_name=f"homework_{name.strip()}.png", mime="image/png")

        if st.button("🔄 숙제 다시 풀기", key="hw_restart"):
            init_hw()
            st.rerun()
    else:
        q = hw["questions"][hw["idx"]]
        q_num = hw["idx"] + 1
        total = len(hw["questions"])
        st.caption(f"문제 {q_num} / {total}")

        if q["type"] == "pron":
            html = pron_listen_html(q["word"], q["options"])
            components.html(html, height=290, scrolling=False)
            st.markdown('<div style="font-weight:700;color:var(--green);margin:6px 0;">'
                        '🦝 위 단어의 알맞은 발음은?</div>', unsafe_allow_html=True)
            if not hw["checked"]:
                picked = choice_buttons(["1번 /t/", "2번 /d/", "3번 /ɪd/"], f"hw_pron_{hw['idx']}")
                if picked:
                    sound_map = {"1번 /t/": "t", "2번 /d/": "d", "3번 /ɪd/": "id"}
                    hw["picked"] = sound_map[picked]
                    hw["checked"] = True
                    if hw["picked"] == q["answer_sound"]:
                        hw["score"] += 1
                    st.rerun()
            else:
                if hw["picked"] == q["answer_sound"]:
                    feedback_bubble(f"정답이에요! 🎉 <b>{q['word']}</b>는 {SOUND_NAMES[q['answer_sound']]}!",
                                    border="var(--green)")
                else:
                    feedback_bubble(f"틀렸어! 🦝 <b>{q['word']}</b>의 발음은 {SOUND_NAMES[q['answer_sound']]}(이)야.",
                                    border="var(--red)")
        else:
            word_card(q["word"], "이 동사의 과거형은?")
            if not hw["checked"]:
                picked = choice_buttons(q["choices"], f"hw_spell_{hw['idx']}")
                if picked:
                    hw["picked"] = picked
                    hw["checked"] = True
                    if picked == q["answer"]:
                        hw["score"] += 1
                    st.rerun()
            else:
                if hw["picked"] == q["answer"]:
                    feedback_bubble(f"정답이에요! 🎉 <b>{q['word']} → {q['answer']}</b>", border="var(--green)")
                else:
                    rule_name = RULE_NAMES.get(q["rule"], "")
                    feedback_bubble(f"틀렸어! 🦝 답은 <b>{q['answer']}</b>(이)야. "
                                    f"<br><span style='font-size:0.9rem;color:#555;'>👉 규칙: {rule_name}</span>",
                                    border="var(--red)")

        if hw["checked"]:
            is_last = hw["idx"] + 1 >= total
            label = "숙제 끝내기 →" if is_last else "다음 문제 →"
            if st.button(label, key=f"hw_next_{hw['idx']}", type="primary"):
                if is_last:
                    hw["finished"] = True
                else:
                    hw["idx"] += 1
                    hw["checked"] = False
                    hw["picked"] = None
                st.rerun()
