import random
import streamlit as st
from utils import (
    inject_global_css, MASCOT_PATH, IMAGES_DIR, AUDIO_DIR,
    load_cert_quiz, random_message, make_certificate,
)

inject_global_css()

col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(MASCOT_PATH), width=80)
with col2:
    st.title("학습 수료증 🏅")
    st.caption("배운 걸 모두 모아서 도전! 수료증을 받아보자!")

st.markdown("---")

NUM_QUESTIONS = 15
df = load_cert_quiz()


def pick_questions():
    """30문항 중 15개를 유형별로 골고루 섞어 추출"""
    by_type = {}
    for rec in df.to_dict("records"):
        by_type.setdefault(rec["유형"], []).append(rec)

    types = list(by_type.keys())
    for t in types:
        random.shuffle(by_type[t])

    selected = []
    # 라운드로빈으로 유형 골고루 뽑기
    ti = 0
    while len(selected) < NUM_QUESTIONS and any(by_type[t] for t in types):
        t = types[ti % len(types)]
        if by_type[t]:
            selected.append(by_type[t].pop())
        ti += 1
    random.shuffle(selected)
    return selected


def init_cert(name):
    st.session_state.cert = {
        "name": name.strip(),
        "questions": pick_questions(),
        "idx": 0,
        "score": 0,
        "checked": False,
        "selected": None,
        "raccoon": f"{name.strip()}아, 준비됐지? 같이 시작해보자! 🦝",
        "finished": False,
        "started": True,
    }


def build_choices(q):
    """A/B/C 보기를 셔플 (정답 위치 랜덤화)"""
    opts = [q["A"], q["B"], q["C"]]
    random.shuffle(opts)
    return opts


# ──────────────────────────────────────────
# 시작 화면 — 이름 입력
# ──────────────────────────────────────────
if "cert" not in st.session_state or not st.session_state.cert.get("started"):
    rc1, rc2 = st.columns([1, 6])
    with rc1:
        st.image(str(MASCOT_PATH), width=90)
    with rc2:
        st.markdown("""
        <div class="raccoon-bubble" style="margin-top:10px;">
        안녕! 나는 너구리 선생님이야. 🦝<br>
        이름을 알려주면, 너만을 위한 학습인증을 시작할게!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    name = st.text_input("이름을 입력해줘", placeholder="예: 김지현", max_chars=20)

    if st.button("학습 시작하기 →", type="primary", disabled=not name.strip()):
        init_cert(name)
        st.rerun()
    st.stop()


# ──────────────────────────────────────────
# 결과 + 수료증
# ──────────────────────────────────────────
cert = st.session_state.cert

if cert["finished"]:
    score = cert["score"]
    total = len(cert["questions"])
    pct = round(score / total * 100) if total else 0

    st.balloons()

    rc1, rc2 = st.columns([1, 6])
    with rc1:
        st.image(str(MASCOT_PATH), width=90)
    with rc2:
        if pct >= 80:
            msg = f"{cert['name']}아, 정말 대단해! 🏆 동사 마스터구나!"
        elif pct >= 60:
            msg = f"{cert['name']}아, 잘했어! 🦝 조금만 더 하면 완벽해!"
        else:
            msg = f"{cert['name']}아, 수고했어! 💪 복습하면 더 잘할 수 있어!"
        st.markdown(f'<div class="raccoon-bubble" style="margin-top:10px;">{msg}</div>',
                    unsafe_allow_html=True)

    st.markdown(f"## 🎉 학습 완료!  {score} / {total}  ({pct}점)")

    # 수료증 생성
    cert_png = make_certificate(cert["name"], score, total)
    st.image(cert_png, caption="너의 학습 수료증 🏅", use_container_width=True)

    st.download_button(
        "📥 수료증 다운로드 (PNG)",
        data=cert_png,
        file_name=f"수료증_{cert['name']}.png",
        mime="image/png",
        type="primary",
    )

    st.markdown("---")
    if st.button("🔄 다시 도전하기"):
        del st.session_state.cert
        st.rerun()
    st.stop()


# ──────────────────────────────────────────
# 퀴즈 진행
# ──────────────────────────────────────────
q = cert["questions"][cert["idx"]]
q_num = cert["idx"] + 1
total = len(cert["questions"])

# 진행 바 + 점수
colA, colB = st.columns([4, 1])
with colA:
    st.progress(cert["idx"] / total)
with colB:
    st.markdown(f"**점수: {cert['score']} / {total}**")

# 너구리 멘트
rc1, rc2 = st.columns([1, 6])
with rc1:
    st.image(str(MASCOT_PATH), width=70)
with rc2:
    st.markdown(f'<div class="raccoon-bubble" style="margin-top:6px;">{cert["raccoon"]}</div>',
                unsafe_allow_html=True)

st.caption(f"문제 {q_num} / {total}")

# 그림 표시
img_name = str(q.get("그림파일이름", "")).strip()
if img_name and img_name.lower() != "nan":
    img_path = IMAGES_DIR / img_name
    if img_path.exists():
        st.image(str(img_path), width=320)

# audio 유형 — 음성 재생
if q["유형"] == "audio":
    audio_name = str(q.get("음성파일이름", "")).strip()
    audio_path = AUDIO_DIR / audio_name
    if audio_path.exists():
        st.markdown("🔊 **음성을 듣고 답을 골라봐!**")
        st.audio(str(audio_path))
    else:
        st.warning(f"⚠️ 음성 파일이 없어요: data/audio/{audio_name} (선생님이 넣어주세요)")

# 질문
st.markdown(f"""
<div class="vb-card">
<h3 style="font-size:1.15rem;">{q['질문']}</h3>
</div>
""", unsafe_allow_html=True)

# 보기 (문제별 셔플 고정)
choice_key = f"cert_choices_{cert['idx']}"
if choice_key not in st.session_state:
    st.session_state[choice_key] = build_choices(q)
choices = st.session_state[choice_key]

picked = st.radio(
    "정답을 골라봐!",
    choices,
    key=f"cert_radio_{cert['idx']}",
    index=None,
    disabled=cert["checked"],
)

# 확인하기 / 계속하기
if not cert["checked"]:
    if st.button("확인하기 ✅", type="primary"):
        if picked is None:
            st.warning("먼저 보기를 골라줘!")
        else:
            cert["checked"] = True
            cert["selected"] = picked
            if picked == q["정답"]:
                cert["score"] += 1
            st.rerun()
else:
    if cert["selected"] == q["정답"]:
        st.markdown(f"""
        <div class="raccoon-row">
            <div class="raccoon-bubble" style="border-left:5px solid var(--green);">
            정답이에요! 🎉 잘했어, {cert['name']}아!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="raccoon-row">
            <div class="raccoon-bubble" style="border-left:5px solid var(--red);">
            오답이에요! 🦝 정답은 <b>{q['정답']}</b>(이)야. 기억해두자!
            </div>
        </div>
        """, unsafe_allow_html=True)

    is_last = cert["idx"] + 1 >= total
    btn_label = "결과 보기 →" if is_last else "계속하기 →"
    if st.button(btn_label, type="primary"):
        if is_last:
            cert["finished"] = True
        else:
            cert["idx"] += 1
            cert["checked"] = False
            cert["selected"] = None
            cert["raccoon"] = random_message("start")
        st.rerun()
