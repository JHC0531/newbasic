"""발음 듣기 컴포넌트: 단어 + 3개 스피커 버튼 (가짜철자 TTS)"""
import json


def pron_listen_html(word: str, options: list) -> str:
    """단어 카드 + 3개 스피커 버튼.
    options: [{'label':'1', 'speak':'walkt'}, ...] 순서대로 1,2,3번 버튼.
    듣기 전용 (선택/정답 판정은 Streamlit 쪽에서 라디오/버튼으로)."""
    opts_json = json.dumps(options, ensure_ascii=False)
    html = r"""
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
:root{--green:#2d6a4f;--green-light:#52b788;--green-pale:#d8f3dc;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI','Malgun Gothic',sans-serif;background:transparent;}
.wrap{text-align:center;}
.word-card{background:var(--green);color:#fff;border-radius:16px;padding:20px;margin-bottom:16px;
  box-shadow:0 4px 14px rgba(0,0,0,.12);}
.word-card .sub{font-size:0.85rem;color:#d8f3dc;margin-bottom:4px;}
.word-card .w{font-size:2.4rem;font-weight:800;letter-spacing:1px;}
.spk-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.spk-btn{background:#fff;border:2.5px solid var(--green-light);border-radius:14px;
  padding:16px 22px;font-size:1.4rem;font-weight:800;color:var(--green);cursor:pointer;
  transition:.15s;min-width:90px;box-shadow:0 2px 8px rgba(0,0,0,.07);}
.spk-btn:hover{background:var(--green-pale);transform:translateY(-2px);}
.spk-btn.playing{background:#f8961e;color:#fff;border-color:#f8961e;}
.spk-btn .num{display:block;font-size:1.5rem;margin-bottom:2px;}
.spk-btn .ico{font-size:1.1rem;}
.hint{font-size:0.8rem;color:#888;margin-top:10px;}
</style></head><body>
<div class="wrap">
  <div class="word-card">
    <div class="sub">🦝 이 단어의 알맞은 발음을 골라봐!</div>
    <div class="w" id="word"></div>
  </div>
  <div class="spk-row" id="spkRow"></div>
  <div class="hint">🔊 버튼을 눌러 1·2·3번 소리를 들어보고, 아래에서 정답을 골라줘!</div>
</div>
<script>
const WORD = __WORD__;
const OPTS = __OPTS__;
document.getElementById('word').textContent = WORD;
function speak(text, btn){
  if(!('speechSynthesis' in window)){alert('이 브라우저는 음성을 지원하지 않아요 😢');return;}
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang='en-US';u.rate=0.75;
  if(btn){
    document.querySelectorAll('.spk-btn').forEach(b=>b.classList.remove('playing'));
    btn.classList.add('playing');
    u.onend=()=>btn.classList.remove('playing');
    u.onerror=()=>btn.classList.remove('playing');
  }
  window.speechSynthesis.speak(u);
}
const row=document.getElementById('spkRow');
OPTS.forEach((o,i)=>{
  const btn=document.createElement('button');
  btn.className='spk-btn';
  btn.innerHTML=`<span class="num">${o.label}</span><span class="ico">🔊</span>`;
  btn.onclick=()=>speak(o.speak, btn);
  row.appendChild(btn);
});
</script></body></html>
""".replace("__WORD__", json.dumps(word, ensure_ascii=False)).replace("__OPTS__", opts_json)
    return html
