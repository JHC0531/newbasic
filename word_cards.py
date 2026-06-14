"""유형별 학습 탭: TTS 듣기 버튼이 있는 단어 카드 HTML"""
import json


def word_cards_html(verbs: list) -> str:
    """현재·과거·과거분사를 보여주고 각각 TTS로 들을 수 있는 카드 그리드"""
    verbs_json = json.dumps(verbs, ensure_ascii=False)
    height = 140 + (len(verbs) + 1) // 2 * 165
    html = r"""
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
:root{--green:#2d6a4f;--green-light:#52b788;--green-pale:#d8f3dc;--orange:#f8961e;--red:#e63946;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI','Malgun Gothic',sans-serif;background:transparent;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;}
.card{background:#fff;border-radius:16px;padding:16px 18px;box-shadow:0 4px 14px rgba(0,0,0,.08);border-top:5px solid var(--green-light);}
.card .meaning{font-size:0.9rem;color:#888;font-weight:600;margin-bottom:10px;}
.card .meaning b{color:var(--green);font-size:1.05rem;}
.row{display:flex;align-items:center;justify-content:space-between;padding:7px 10px;border-radius:10px;margin-bottom:6px;background:var(--green-pale);}
.row.past{background:#fff3e0;}
.row.pp{background:#ffebee;}
.row .lbl{font-size:0.72rem;font-weight:700;color:#777;width:62px;}
.row .form{flex:1;font-size:1.15rem;font-weight:800;color:var(--green);}
.row.past .form{color:var(--orange);}
.row.pp .form{color:var(--red);}
.row .form.none{color:#bbb;font-size:0.95rem;font-weight:600;}
.spk{background:var(--green);color:#fff;border:none;border-radius:50%;width:38px;height:38px;font-size:1.1rem;cursor:pointer;transition:.15s;flex-shrink:0;}
.spk:hover{background:#1e4d35;transform:scale(1.1);}
.spk:disabled{background:#ccc;cursor:not-allowed;}
.spk.playing{background:var(--orange);animation:pulse .6s infinite;}
@keyframes pulse{50%{transform:scale(1.15);}}
.allbtn{background:var(--green-light);color:#fff;border:none;border-radius:10px;padding:6px 12px;font-size:0.82rem;font-weight:700;cursor:pointer;margin-top:4px;width:100%;}
.allbtn:hover{background:var(--green);}
</style></head><body>
<div class="grid" id="grid"></div>
<script>
const VERBS = __VERBS__;
function speak(text, btn){
  if(!('speechSynthesis' in window)){alert('이 브라우저는 음성을 지원하지 않아요 😢');return;}
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang='en-US';u.rate=0.85;
  if(btn){btn.classList.add('playing');u.onend=()=>btn.classList.remove('playing');u.onerror=()=>btn.classList.remove('playing');}
  window.speechSynthesis.speak(u);
}
function speakAll(base,past,pp){
  if(!('speechSynthesis' in window))return;
  window.speechSynthesis.cancel();
  [base,past,pp].forEach(w=>{
    if(w && w!=='-'){const u=new SpeechSynthesisUtterance(w);u.lang='en-US';u.rate=0.85;window.speechSynthesis.speak(u);}
  });
}
const grid=document.getElementById('grid');
VERBS.forEach(v=>{
  const ppNone = (!v.pp || v.pp==='-');
  const card=document.createElement('div');
  card.className='card';
  card.innerHTML=`
    <div class="meaning">뜻: <b>${v.meaning}</b></div>
    <div class="row">
      <span class="lbl">원형</span>
      <span class="form">${v.base}</span>
      <button class="spk" title="듣기">🔊</button>
    </div>
    <div class="row past">
      <span class="lbl">과거형</span>
      <span class="form">${v.past}</span>
      <button class="spk" title="듣기">🔊</button>
    </div>
    <div class="row pp">
      <span class="lbl">과거분사</span>
      <span class="form ${ppNone?'none':''}">${ppNone?'(없음)':v.pp}</span>
      ${ppNone?'<button class="spk" disabled>🔇</button>':'<button class="spk" title="듣기">🔊</button>'}
    </div>
    <button class="allbtn">🦝 전체 듣기 ▶</button>
  `;
  const btns=card.querySelectorAll('.row .spk');
  btns[0].onclick=()=>speak(v.base,btns[0]);
  btns[1].onclick=()=>speak(v.past,btns[1]);
  if(!ppNone) btns[2].onclick=()=>speak(v.pp,btns[2]);
  card.querySelector('.allbtn').onclick=()=>speakAll(v.base,v.past,ppNone?'':v.pp);
  grid.appendChild(card);
});
</script></body></html>
""".replace("__VERBS__", verbs_json)
    return html, height
