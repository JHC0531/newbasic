"""공유 유틸 함수: 데이터 로딩, 스타일, 너구리 메시지, 수료증 생성"""

import io
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "irregular_verbs.csv"
RULES_CSV_PATH = BASE_DIR / "data" / "rules_quiz.csv"
CERT_CSV_PATH = BASE_DIR / "data" / "cert_quiz.csv"
IMAGES_DIR = BASE_DIR / "data" / "images"
AUDIO_DIR = BASE_DIR / "data" / "audio"
MASCOT_PATH = BASE_DIR / "assets" / "raccoon.png"
FONT_REGULAR = BASE_DIR / "assets" / "fonts" / "NanumGothic-Regular.ttf"
FONT_BOLD = BASE_DIR / "assets" / "fonts" / "NanumGothic-Bold.ttf"

LEVEL_LABELS = {
    "Easy": "⭐ Easy",
    "Average": "⭐⭐ Average",
    "Difficult": "⭐⭐⭐ Hard",
}

RACCOON_MESSAGES = {
    "start": [
        "어서와! 동사 연습 시작해볼까? 🦝",
        "자, 카드를 골라서 빈 칸을 채워봐! 🦝",
        "집중집중! 할 수 있어! 🦝",
    ],
    "correct": [
        "정답! 역시 천재! 🎉",
        "완벽해! 🦝✨",
        "맞았어! 대단해! 🎊",
        "Good job! 계속 가자! 🚀",
    ],
    "wrong": [
        "아이쿠, 틀렸어. 다시 봐봐! 🦝",
        "괜찮아, 다음엔 기억할 거야! 💪",
        "아깝다! 정답은 잘 봐둬! 🔍",
    ],
    "end": [
        "완주했어! 진짜 대단해! 🏆",
        "모든 문제 끝냈어! 🎉",
        "동사 마스터 등극! 🦝👑",
    ],
}


def _read_csv_safe(path):
    """어떤 인코딩으로 저장된 CSV든 안전하게 읽기
    (엑셀에서 저장하면 utf-16/cp949 등으로 바뀌어 깨지는 경우 대비)"""
    df = None
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp949", "euc-kr"):
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if df is None:
        # 마지막 수단: 깨진 문자는 무시하고 읽기
        df = pd.read_csv(path, encoding="utf-8", encoding_errors="ignore")
    # 칼럼명에 붙은 BOM(\ufeff)·앞뒤 공백 제거
    df.columns = [str(c).replace("\ufeff", "").strip() for c in df.columns]
    return df


@st.cache_data
def load_verbs() -> pd.DataFrame:
    """CSV 파일을 읽어서 정제된 DataFrame으로 반환
    (칼럼명이 깨져도 순서로 이름을 다시 붙임)"""
    df = _read_csv_safe(DATA_PATH)
    # 칼럼 순서: 유형, 동사원형, 과거형, 과거분사형, 뜻, 레벨
    df.columns = ["type", "base", "past", "pp", "meaning", "level"][:len(df.columns)]
    df = df.fillna("-")
    for col in ["type", "base", "past", "pp", "meaning", "level"]:
        df[col] = df[col].astype(str).str.strip()
    return df


@st.cache_data
def get_irregular_verbs() -> pd.DataFrame:
    df = load_verbs()
    return df[~df["type"].isin(["Regular (-ed)", "special"])].reset_index(drop=True)


@st.cache_data
def get_game_verbs(include_hard: bool = False) -> list:
    """게임용 불규칙 동사 목록.
    include_hard=False면 Easy만, True면 Average·Difficult까지 포함.
    여러 형태(slash)는 첫 번째 형태만 사용."""
    df = get_irregular_verbs()
    if include_hard:
        pool = df
    else:
        pool = df[df["level"] == "Easy"]

    verbs = []
    for _, r in pool.iterrows():
        past = r["past"].split("/")[0].strip()
        pp = r["pp"].split("/")[0].strip()
        base = r["base"].strip()
        if not base or not past or not pp or past == "-" or pp == "-":
            continue
        verbs.append({
            "base": base,
            "past": past,
            "pp": pp,
            "meaning": r["meaning"],
            "type": r["type"],
            "level": r["level"],
        })
    return verbs


# 규칙변화 미니퀴즈 데이터 (CSV 깨짐 방지를 위해 코드에 직접 내장)
_RULES_QUIZ_DATA = [
    ("1", "walk", "walked", "walkd", "walkt", "We walked along the beach after lunch."),
    ("1", "watch", "watched", "watcht", "watchd", "My brother watched a science program last night."),
    ("1", "help", "helped", "helpped", "helpd", "The students helped an elderly woman cross the street."),
    ("1", "visit", "visited", "visitted", "visitd", "We visited a museum during the school trip."),
    ("1", "clean", "cleaned", "cleened", "cleand", "Mina cleaned her desk before class."),
    ("1", "play", "played", "plaied", "playd", "The boys played basketball after school."),
    ("1", "cook", "cooked", "cookt", "cookked", "My father cooked dinner for the family."),
    ("2", "like", "liked", "likeed", "likt", "Many students liked the new school event."),
    ("2", "live", "lived", "liveed", "livved", "My grandparents lived in a small village."),
    ("2", "hope", "hoped", "hopeed", "hopd", "I hoped for sunny weather on sports day."),
    ("2", "dance", "danced", "danceed", "dancedd", "The children danced happily on the stage."),
    ("2", "use", "used", "useed", "ussed", "She used her phone to take pictures."),
    ("2", "love", "loved", "loveed", "lovved", "The baby loved the colorful toy."),
    ("3a", "study", "studied", "studyed", "studyd", "Jisu studied English for two hours."),
    ("3a", "carry", "carried", "carryed", "carryd", "He carried a heavy box upstairs."),
    ("3a", "try", "tried", "tryed", "tryd", "I tried a new recipe for dinner."),
    ("3a", "cry", "cried", "cryed", "cryd", "The baby cried loudly at night."),
    ("3a", "worry", "worried", "worryed", "worryd", "She worried about the math test."),
    ("3a", "reply", "replied", "replyed", "replyd", "Tom replied to my message quickly."),
    ("3b", "play", "played", "plaied", "playyed", "The team played very well yesterday."),
    ("3b", "enjoy", "enjoyed", "enjoied", "enjoyd", "They enjoyed the school festival."),
    ("3b", "stay", "stayed", "staied", "stayd", "We stayed at a hotel near the lake."),
    ("3b", "obey", "obeyed", "obeied", "obeyd", "The students obeyed the classroom rules."),
    ("3b", "delay", "delayed", "delaied", "delayd", "Heavy rain delayed the baseball game."),
    ("4", "stop", "stopped", "stoped", "stoppped", "The bus stopped in front of the station."),
    ("4", "plan", "planned", "planed", "plannned", "Our class planned a recycling campaign."),
    ("4", "drop", "dropped", "droped", "droppped", "I dropped my pencil during the test."),
    ("4", "shop", "shopped", "shoped", "shoppped", "My parents shopped for groceries yesterday."),
    ("4", "chat", "chatted", "chated", "chattted", "The friends chatted online after school."),
    ("4", "hug", "hugged", "huged", "huggged", "The little girl hugged her puppy."),
]


@st.cache_data
def load_rules_quiz() -> pd.DataFrame:
    """규칙변화 미니퀴즈 데이터 (코드 내장 — CSV 불필요)"""
    return pd.DataFrame(
        _RULES_QUIZ_DATA,
        columns=["규칙번호", "동사원형", "정답", "오답1", "오답2", "예문"],
    )



# 학습인증 30문항 데이터 (CSV 깨짐 방지를 위해 코드에 직접 내장)
_CERT_QUIZ_DATA = [
    (1, 'spelling', '', 'Yesterday, we ______ basketball after school.', 'playyed', 'plaied', 'played', 'played', 'q01_basketball.png'),
    (2, 'spelling', '', 'My sister ______ a beautiful song at the concert.', 'sanged', 'sang', 'songed', 'sang', 'q02_sang.png'),
    (3, 'spelling', '', 'We ______ our homework before dinner.', 'finised', 'finished', 'finish', 'finished', 'q03_homework.png'),
    (4, 'spelling', '', 'He ______ his bike to school yesterday.', 'rode', 'roed', 'rided', 'rode', 'q04_bike.png'),
    (5, 'spelling', '', 'They ______ a new movie last night.', 'watched', 'watch', 'watcheed', 'watched', 'q05_movie.png'),
    (6, 'spelling', '', 'The cat ______ onto the table.', 'jumpted', 'jump', 'jumped', 'jumped', 'q06_jumped.png'),
    (7, 'spelling', '', 'I ______ my room this morning.', 'cleand', 'cleaned', 'clean', 'cleaned', 'q07_cleaned.png'),
    (8, 'spelling', '', 'We ______ in the sea last summer.', 'swummed', 'swimmed', 'swam', 'swam', 'q08_swam.png'),
    (9, 'spelling', '', 'She ______ a letter to her pen pal.', 'written', 'writed', 'wrote', 'wrote', 'q09_wrote.png'),
    (10, 'spelling', '', 'The baby ______ loudly last night.', 'cride', 'cryed', 'cried', 'cried', 'q10_cried.png'),
    (11, 'irregular_past', '', 'Last weekend, I ______ many pictures.', 'took', 'taked', 'taken', 'took', 'q11_pictures.png'),
    (12, 'irregular_past', '', 'She ______ to the beach with her family.', 'gone', 'goed', 'went', 'went', 'q12_beach.png'),
    (13, 'irregular_past', '', 'He ______ his keys on the bus.', 'lost', 'losted', 'loosed', 'lost', 'q13_keys.png'),
    (14, 'irregular_past', '', 'They ______ a big cake for her birthday.', 'made', 'make', 'maked', 'made', 'q14_cake.png'),
    (15, 'irregular_past', '', 'I ______ up early and had breakfast.', 'get', 'got', 'gotten', 'got', 'q15_gotup.png'),
    (16, 'irregular_past', '', 'My brother ______ his toy yesterday.', 'found', 'finded', 'founded', 'found', 'q16_found.png'),
    (17, 'irregular_past', '', 'We ______ dinner at a nice restaurant.', 'haded', 'haved', 'had', 'had', 'q17_dinner.png'),
    (18, 'irregular_past', '', 'The lights ______ out during the storm.', 'went', 'goed', 'gone', 'went', 'q18_storm.png'),
    (19, 'irregular_past', '', 'She ______ the door before leaving.', 'shooted', 'shutted', 'shut', 'shut', 'q19_door.png'),
    (20, 'irregular_past', '', 'He ______ to me last night.', 'spoked', 'spoken', 'spoke', 'spoke', 'q20_spoke.png'),
    (21, 'audio', 'visited.mp3', '음성을 듣고 문맥에 알맞은 철자를 고르시오. We ______ a museum during the school trip.', 'visited', 'visitted', 'visitd', 'visited', 'q21_museum.png'),
    (22, 'audio', 'played.mp3', '음성을 듣고 문맥에 알맞은 철자를 고르시오. I ______ the piano at the recital.', 'playyed', 'played', 'plaied', 'played', 'q22_piano.png'),
    (23, 'audio', 'made.mp3', '음성을 듣고 문맥에 알맞은 단어를 고르시오. My mom ______ a delicious dinner.', 'made', 'makes', 'maded', 'made', 'q23_made_dinner.png'),
    (24, 'audio', 'went.mp3', '음성을 듣고 문맥에 알맞은 단어를 고르시오. We ______ to the mountains last winter.', 'gone', 'goed', 'went', 'went', 'q24_mountain.png'),
    (25, 'audio', 'saw.mp3', '음성을 듣고 문맥에 알맞은 단어를 고르시오. I ______ a shooting star in the sky.', 'saw', 'see', 'seen', 'saw', 'q25_saw_star.png'),
    (26, 'pp_pattern', '', '<보기> I have met him before. 같은 형식으로 문장을 완성하시오. She has ______ the letter back to her mother. (send → sent → ?)', 'sent', 'sending', 'send', 'sent', 'q26_sent_letter.png'),
    (27, 'pp_pattern', '', '<보기> I have eaten lunch already. 같은 형식으로 문장을 완성하시오. He has ______ all of his homework. (finish → finished → ?)', 'finished', 'finishing', 'finish', 'finished', 'q27_finished_hw.png'),
    (28, 'pp_pattern', '', '<보기> They have seen the movie. 같은 형식으로 문장을 완성하시오. We have ______ that show before. (see → saw → ?)', 'see', 'seen', 'seeing', 'seen', 'q28_seen_movie.png'),
    (29, 'pp_pattern', '', '<보기> The window has been cleaned. 같은 형식으로 문장을 완성하시오. The room has been ______ by my brother. (clean → cleaned → ?)', 'cleaning', 'cleaned', 'clean', 'cleaned', 'q29_cleaned_room.png'),
    (30, 'pp_pattern', '', '<보기> The cake has been made by her. 같은 형식으로 문장을 완성하시오. The book has been ______ by my teacher. (write → wrote → ?)', 'wrote', 'write', 'written', 'written', 'q30_written_book.png'),
]


@st.cache_data
def load_cert_quiz() -> pd.DataFrame:
    """학습인증 30문항 데이터 (코드 내장 — CSV 불필요)"""
    return pd.DataFrame(
        _CERT_QUIZ_DATA,
        columns=["문제번호", "유형", "음성파일이름", "질문", "A", "B", "C", "정답", "그림파일이름"],
    )


def random_message(category: str) -> str:
    return random.choice(RACCOON_MESSAGES[category])


def inject_global_css():
    st.markdown("""
    <style>
    :root {
        --green: #2d6a4f;
        --green-light: #52b788;
        --green-pale: #d8f3dc;
        --yellow: #f9c74f;
        --orange: #f8961e;
        --red: #e63946;
    }
    .stApp { background-color: #f1faee; }

    /* Title styling */
    h1, h2, h3 { color: var(--green); }

    /* Card-like containers */
    .vb-card {
        background: white;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.10);
        margin-bottom: 14px;
        border-top: 5px solid var(--green-light);
    }
    .vb-card h3 { font-size: 1.25rem; font-weight: 800; margin-bottom: 4px; }
    .vb-card .tag { font-size: 0.78rem; color: #6b7280; margin-bottom: 8px; }
    .vb-card .example {
        background: var(--green-pale);
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 0.9rem;
        line-height: 1.7;
    }
    .vb-card .example b { color: var(--green); }

    .t-aaa { border-top-color: #6c757d; }
    .t-aab { border-top-color: #457b9d; }
    .t-aba { border-top-color: #9b5de5; }
    .t-abb { border-top-color: var(--orange); }
    .t-abc { border-top-color: var(--red); }

    /* Raccoon bubble */
    .raccoon-row { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
    .raccoon-bubble {
        background: white;
        border-radius: 14px 14px 14px 2px;
        padding: 10px 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.10);
        font-size: 1rem;
        font-weight: 600;
    }

    /* Verb display */
    .verb-display {
        background: white;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.10);
        margin-bottom: 16px;
    }
    .verb-meaning { font-size: 0.9rem; color: #6b7280; margin-bottom: 6px; }
    .verb-base { font-size: 2.6rem; font-weight: 800; color: #1a1a2e; margin-bottom: 10px; }

    .slot-box {
        display: inline-block;
        background: var(--green-pale);
        border-radius: 12px;
        padding: 10px 24px;
        margin: 0 8px;
        min-width: 130px;
    }
    .slot-label { font-size: 0.75rem; color: #6b7280; font-weight: 600; margin-bottom: 4px; }
    .slot-answer { font-size: 1.2rem; font-weight: 700; color: var(--green); }
    .slot-answer.empty { color: #bbb; font-size: 1.6rem; }
    .slot-answer.wrong { color: var(--red); }

    /* rule examples */
    .rule-ex {
        display: inline-block;
        background: var(--green-pale);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--green);
        margin: 3px;
    }

    /* 퀴즈 보기 — 큰 카드형 버튼 */
    .choice-btn-wrap [data-testid="stButton"] > button {
        width: 100%;
        min-height: 90px;
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--green);
        background: #ffffff;
        border: 2.5px solid var(--green-light);
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        transition: all 0.15s;
    }
    .choice-btn-wrap [data-testid="stButton"] > button:hover {
        background: var(--green-pale);
        border-color: var(--green);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)


def make_certificate(name: str, score: int, total: int) -> bytes:
    """이름·점수·날짜가 들어간 수료증 PNG를 만들어 bytes로 반환"""
    W, H = 1000, 700
    bg = (241, 250, 238)       # cream
    green = (45, 106, 79)
    green_light = (82, 183, 136)
    gold = (249, 199, 79)
    dark = (26, 26, 46)
    gray = (107, 114, 128)

    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # 외곽 테두리 (이중)
    draw.rectangle([20, 20, W - 20, H - 20], outline=green, width=6)
    draw.rectangle([34, 34, W - 34, H - 34], outline=gold, width=3)

    def font(bold, size):
        path = str(FONT_BOLD if bold else FONT_REGULAR)
        return ImageFont.truetype(path, size)

    def center(text, y, fnt, fill):
        bbox = draw.textbbox((0, 0), text, font=fnt)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)

    # 제목
    center("학 습 수 료 증", 80, font(True, 56), green)
    center("🦝 동사 변화 학습기 🦝", 165, font(True, 30), green_light)

    # 구분선
    draw.line([180, 230, W - 180, 230], fill=gold, width=3)

    # 본문
    center("위 학생은 영어 동사 변화 학습 과정을", 280, font(False, 28), dark)
    center("성실히 이수하였기에 이 증서를 수여합니다.", 320, font(False, 28), dark)

    # 이름 (강조)
    center(f"{name}", 400, font(True, 64), green)

    # 점수
    pct = round(score / total * 100) if total else 0
    center(f"점수:  {score} / {total}   ({pct}점)", 510, font(True, 38), dark)

    # 날짜
    today = datetime.now().strftime("%Y년 %m월 %d일")
    center(today, 580, font(False, 26), gray)

    # 너구리 마스코트 (오른쪽 하단)
    try:
        mascot = Image.open(MASCOT_PATH).convert("RGBA")
        mascot.thumbnail((120, 120))
        img.paste(mascot, (W - 200, H - 200), mascot)
    except Exception:
        pass

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
