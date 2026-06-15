"""구글시트 기반 반 전체 순위표 (점수 저장/불러오기)"""
from datetime import datetime

import streamlit as st


def _get_sheet(_debug=False):
    """구글시트 워크시트 객체 반환. 설정 안 됐으면 None.
    _debug=True면 실패 이유를 문자열로 반환 (진단용)."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as e:
        return f"라이브러리 없음: {e}" if _debug else None

    try:
        if "gcp_service_account" not in st.secrets:
            return "secrets에 gcp_service_account 없음" if _debug else None
    except Exception as e:
        return f"secrets 읽기 실패: {e}" if _debug else None

    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]), scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet_url = st.secrets.get("sheet_url")
        if not sheet_url:
            return "secrets에 sheet_url 없음" if _debug else None
        return client.open_by_url(sheet_url).sheet1
    except Exception as e:
        return f"시트 연결 실패: {type(e).__name__}: {e}" if _debug else None


def debug_reason() -> str:
    """진단용: 연결 실패 이유를 문자열로 반환"""
    result = _get_sheet(_debug=True)
    if isinstance(result, str):
        return result
    return "연결 성공 ✓"


def is_online_ranking_available() -> bool:
    """온라인 순위표 사용 가능 여부"""
    return _get_sheet() is not None


def add_score(name: str, score: int, game: str = "irregular") -> bool:
    """점수를 시트에 추가. 성공하면 True.
    game: 'regular' 또는 'irregular' (게임 종류 구분)"""
    sheet = _get_sheet()
    if sheet is None:
        return False
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.append_row([name, int(score), ts, game])
        return True
    except Exception:
        return False


@st.cache_data(ttl=10)
def get_ranking(top_n: int = 20, game: str = "irregular") -> list:
    """순위표 불러오기 (점수 높은 순). [{name, score, time}, ...]
    game: 'regular' 또는 'irregular'. 게임 종류가 없는 옛 기록은 'irregular'로 간주."""
    sheet = _get_sheet()
    if sheet is None:
        return []
    try:
        records = sheet.get_all_records()  # 헤더(name/score/time/game) 기준 dict 리스트
        cleaned = []
        for r in records:
            try:
                # game 칸이 없거나 비어있으면 'irregular'로 간주 (옛 기록 호환)
                g = str(r.get("game", "")).strip().lower() or "irregular"
                if g != game:
                    continue
                cleaned.append({
                    "name": str(r.get("name", "")).strip(),
                    "score": int(r.get("score", 0)),
                    "time": str(r.get("time", "")),
                })
            except (ValueError, TypeError):
                continue
        cleaned.sort(key=lambda x: x["score"], reverse=True)
        return cleaned[:top_n]
    except Exception:
        return []
