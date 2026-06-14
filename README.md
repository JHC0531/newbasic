# 동사 변화 학습기 🦝 (Streamlit)

중1 영어 동사 변화 학습 웹앱입니다. **Streamlit Community Cloud**로 무료 배포할 수 있어요.
모든 파일명을 영어로 만들어 GitHub 업로드 시 한글 깨짐 문제가 없습니다.

## 📁 파일 구조

```
verbform/
├── app.py                     ← 시작 파일 (배포 시 Main file path에 입력)
├── home_page.py               ← 홈 화면
├── pages/
│   ├── 1_Irregular.py         ← 불규칙 변화
│   ├── 2_Rules.py             ← 규칙 변화 (4탭 + 미니퀴즈)
│   └── 3_Certificate.py       ← 학습 수료증 (이름→15문제→수료증)
├── utils.py                   ← 공통 함수
├── data/
│   ├── irregular_verbs.xlsx   ← 불규칙 동사
│   ├── rules_quiz.csv         ← 규칙변화 미니퀴즈
│   ├── cert_quiz.csv          ← 학습인증 30문항
│   ├── images/                ← 문항 그림 30개 (너구리)
│   └── audio/                 ← 발음 mp3 5개
├── assets/
│   ├── raccoon.png            ← 마스코트
│   └── fonts/                 ← 수료증용 한글 폰트 (NanumGothic)
├── requirements.txt
└── .streamlit/config.toml     ← 초록 테마
```

## 🚀 배포 방법 (Streamlit Community Cloud)

1. 이 폴더 전체를 GitHub 저장소(Public)에 올리기
2. https://share.streamlit.io 접속 → 로그인
3. **New app** → 저장소 선택
4. **Main file path** 에 `app.py` 입력 ← 중요!
5. **Deploy** 클릭

## 💻 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✏️ 데이터 수정

| 수정 내용 | 파일 |
|---|---|
| 불규칙 동사 목록 | `data/irregular_verbs.xlsx` |
| 규칙변화 미니퀴즈 | `data/rules_quiz.csv` |
| 학습인증 문항 | `data/cert_quiz.csv` |
| 발음 mp3 | `data/audio/` (CSV 음성파일이름과 동일하게) |

## 🛠️ 사용 기술

- Streamlit (st.navigation 멀티페이지)
- pandas, openpyxl (데이터)
- Pillow (수료증 PNG 생성)
- NanumGothic 폰트 (OFL)
