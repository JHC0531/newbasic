"""탭2 새 잡기 게임 HTML 컴포넌트 생성"""
import json
from utils import _make_distractors


def bird_game_html(verbs: list, num_birds: int = 5, game_time: int = 60) -> str:
    # 각 동사에 매력적 오답(흔한 실수형) 부착
    enriched = []
    for v in verbs:
        item = dict(v)
        item["distractors"] = _make_distractors(v["base"], v["past"], num_birds - 1)
        enriched.append(item)
    verbs_json = json.dumps(enriched, ensure_ascii=False)
    return r"""
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
:root{--green:#2d6a4f;--green-light:#52b788;--green-pale:#d8f3dc;--sky1:#bde0fe;--sky2:#a2d2ff;--red:#e63946;--yellow:#f9c74f;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI','Malgun Gothic',sans-serif;}
#game-wrap{position:relative;width:100%;margin:0 auto;}
.hud{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:8px;flex-wrap:wrap;}
.hud .pill{background:var(--green);color:#fff;border-radius:20px;padding:6px 16px;font-weight:800;font-size:1rem;}
.hud .time{background:var(--yellow);color:#5a4030;}
.hud .time.low{background:var(--red);color:#fff;animation:blink .5s infinite;}
@keyframes blink{50%{opacity:.5;}}
.ask{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.ask .bubble{background:#fff;border:2px solid var(--green-pale);border-radius:14px 14px 14px 2px;padding:8px 14px;font-weight:700;font-size:1.05rem;box-shadow:0 3px 10px rgba(0,0,0,.1);}
.ask .word{color:var(--green);font-size:1.3rem;}
#sky{position:relative;width:100%;height:420px;overflow:hidden;background:linear-gradient(180deg,var(--sky1),var(--sky2));border-radius:18px;box-shadow:inset 0 0 30px rgba(255,255,255,.4);cursor:crosshair;}
.cloud{position:absolute;background:#fff;border-radius:50px;opacity:.7;}
.bird{position:absolute;width:96px;height:64px;cursor:pointer;user-select:none;will-change:left,top;}
.bird svg{width:100%;height:100%;overflow:visible;}
.bird .label{position:absolute;top:-4px;left:50%;transform:translateX(-50%);background:#fff;border:2px solid var(--green);border-radius:12px;padding:1px 8px;font-weight:800;font-size:0.95rem;color:var(--green);white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.15);}
.bird.correct-hit .label{background:#d1fae5;border-color:var(--green);}
.bird.wrong-hit .label{background:#fee2e2;border-color:var(--red);color:var(--red);}
.overlay{position:absolute;inset:0;background:rgba(255,255,255,.93);display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:18px;text-align:center;padding:20px;z-index:10;}
.overlay h2{color:var(--green);font-size:1.6rem;margin-bottom:8px;}
.overlay p{color:#555;margin-bottom:16px;line-height:1.6;}
.btn{background:var(--green);color:#fff;border:none;border-radius:25px;padding:12px 30px;font-size:1.1rem;font-weight:800;cursor:pointer;transition:.15s;}
.btn:hover{background:#1e4d35;transform:translateY(-2px);}
.review{max-height:230px;overflow-y:auto;width:100%;max-width:480px;margin:6px 0 16px;text-align:left;}
.review .item{display:flex;justify-content:space-between;align-items:center;padding:7px 14px;border-radius:10px;margin-bottom:5px;font-weight:700;}
.review .ok{background:#d1fae5;color:var(--green);}
.review .no{background:#fee2e2;color:var(--red);}
.review .item .ko{font-weight:500;font-size:0.85rem;opacity:.8;}
.flash{position:absolute;font-weight:900;font-size:2rem;pointer-events:none;animation:floatUp .8s ease-out forwards;z-index:20;}
@keyframes floatUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-50px) scale(1.4);}}
.name-input{padding:10px 16px;font-size:1.05rem;border:2px solid var(--green-light);border-radius:12px;margin-bottom:14px;text-align:center;width:240px;outline:none;}
.name-input:focus{border-color:var(--green);}
.board{width:100%;max-width:420px;margin:4px 0 14px;text-align:left;}
.board .brow{display:flex;align-items:center;justify-content:space-between;padding:8px 14px;border-radius:10px;margin-bottom:5px;font-weight:700;background:#f1f6f2;}
.board .brow.me{background:#fff3cd;border:2px solid var(--yellow);}
.board .brow .rank{font-size:1.1rem;width:42px;}
.board .brow .nm{flex:1;color:#333;}
.board .brow .sc{color:var(--green);font-weight:800;}
.board-title{font-weight:800;color:var(--green);margin:6px 0;font-size:1.1rem;}
</style></head><body>
<div id="game-wrap">
  <div class="hud">
    <div class="pill">🎯 점수 <span id="score">0</span></div>
    <div class="pill">🐦 <span id="qnum">0</span></div>
    <div class="pill time" id="timer">⏱️ __TIME__</div>
  </div>
  <div class="ask" id="askRow" style="visibility:hidden;">
    <div style="font-size:2rem;">🦝</div>
    <div class="bubble"><span id="askText">준비됐니?</span></div>
  </div>
  <div id="sky">
    <div class="overlay" id="startOverlay">
      <h2>🐦 새 잡기 게임</h2>
      <p>현재형 단어를 보고, <b>과거형</b>이 등에 적힌 새를 잡아!<br>__TIME__초 안에 최대한 많이 맞혀보자! 🦝✨</p>
      <input id="nameInput" class="name-input" type="text" maxlength="10" placeholder="이름을 입력하세요 ✍️" />
      <button class="btn" onclick="startGame()">시작하기 🚀</button>
    </div>
  </div>
</div>
<script>
const VERBS = __VERBS__;
const NUM_BIRDS = __NUM__;
const GAME_TIME = __TIME__;
let sky,score,qnum,timeLeft,timerId,animId;
let birds=[],current=null,history=[],playing=false,acceptClick=false;
let leaderboard=[],playerName="";
const BIRD_COLORS=["#ef476f","#ffd166","#06d6a0","#118ab2","#f78c6b","#9b5de5","#00bbf9"];
function rand(a,b){return a+Math.random()*(b-a);}
function shuffle(arr){const a=[...arr];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function shade(hex){const c=hex.replace('#','');const n=parseInt(c,16);let r=Math.max(0,(n>>16)-30),g=Math.max(0,((n>>8)&255)-30),b=Math.max(0,(n&255)-30);return `rgb(${r},${g},${b})`;}
function birdSVG(color){return `<svg viewBox="0 0 96 64"><ellipse cx="46" cy="38" rx="26" ry="17" fill="${color}"/><circle cx="70" cy="28" r="13" fill="${color}"/><circle cx="74" cy="25" r="2.5" fill="#222"/><polygon points="82,28 96,24 82,33" fill="#f9a826"/><path d="M40 32 Q30 8 14 20 Q28 30 40 38 Z" fill="${shade(color)}"/><path d="M20 44 Q6 50 2 44" stroke="${shade(color)}" stroke-width="5" fill="none" stroke-linecap="round"/></svg>`;}
function startGame(){
  sky=document.getElementById('sky');
  // 이름 입력 (시작 화면일 때만)
  const ni=document.getElementById('nameInput');
  if(ni){
    const nm=ni.value.trim();
    if(!nm){ni.style.borderColor='#e63946';ni.placeholder='이름을 먼저 입력해줘! 🦝';return;}
    playerName=nm;
  }
  document.getElementById('startOverlay')?.remove();
  document.getElementById('resultOverlay')?.remove();
  document.getElementById('askRow').style.visibility='visible';
  score=0;qnum=0;timeLeft=GAME_TIME;history=[];playing=true;acceptClick=true;
  document.getElementById('score').textContent=0;
  document.getElementById('qnum').textContent=0;
  updateTimer();addClouds();
  timerId=setInterval(()=>{timeLeft--;updateTimer();if(timeLeft<=0)endGame();},1000);
  nextQuestion();loop();
}
function updateTimer(){const t=document.getElementById('timer');t.textContent='⏱️ '+timeLeft;t.classList.toggle('low',timeLeft<=10);}
function addClouds(){for(let i=0;i<4;i++){const c=document.createElement('div');c.className='cloud';const w=rand(60,120);c.style.width=w+'px';c.style.height=(w*0.5)+'px';c.style.left=rand(0,80)+'%';c.style.top=rand(5,70)+'%';sky.appendChild(c);}}
function nextQuestion(){
  birds.forEach(b=>b.el.remove());birds=[];
  current=VERBS[Math.floor(Math.random()*VERBS.length)];
  qnum++;document.getElementById('qnum').textContent=qnum;
  document.getElementById('askText').innerHTML=`<b class="word">${current.base}</b> 의 과거형은? 🐦`;
  // 매력적 오답(흔한 실수형) 우선, 모자라면 다른 동사 과거형으로 채움
  let seenPast={};seenPast[current.past]=true;
  let wrongs=[];
  for(const d of (current.distractors||[])){
    if(wrongs.length>=NUM_BIRDS-1)break;
    if(d && !seenPast[d]){seenPast[d]=true;wrongs.push(d);}
  }
  for(const v of shuffle(VERBS)){
    if(wrongs.length>=NUM_BIRDS-1)break;
    if(!seenPast[v.past]){seenPast[v.past]=true;wrongs.push(v.past);}
  }
  let labels=shuffle([current.past,...wrongs]);
  const W=sky.clientWidth,H=sky.clientHeight;
  labels.forEach((pastForm,i)=>{
    const el=document.createElement('div');el.className='bird';
    const color=BIRD_COLORS[i%BIRD_COLORS.length];
    el.innerHTML=birdSVG(color)+`<div class="label">${pastForm}</div>`;
    const bx=rand(20,Math.max(40,W-120)),by=rand(20,Math.max(40,H-90));
    el.style.left=bx+'px';el.style.top=by+'px';sky.appendChild(el);
    const b={el,x:bx,y:by,vx:rand(-1.4,1.4)||1,vy:rand(-1.1,1.1)||1,past:pastForm,isAns:(pastForm===current.past)};
    el.addEventListener('click',()=>hitBird(b));birds.push(b);
  });
}
function loop(){
  if(!playing)return;
  const W=sky.clientWidth,H=sky.clientHeight;
  birds.forEach(b=>{
    b.x+=b.vx;b.y+=b.vy;
    if(b.x<0){b.x=0;b.vx*=-1;}if(b.x>W-96){b.x=W-96;b.vx*=-1;}
    if(b.y<0){b.y=0;b.vy*=-1;}if(b.y>H-64){b.y=H-64;b.vy*=-1;}
    b.el.style.left=b.x+'px';b.el.style.top=b.y+'px';
    b.el.style.transform=b.vx<0?'scaleX(-1)':'';
  });
  animId=requestAnimationFrame(loop);
}
function hitBird(b){
  if(!acceptClick)return;
  if(b.isAns){
    score++;document.getElementById('score').textContent=score;
    b.el.classList.add('correct-hit');flash('⭐+1','#06d6a0',b.x,b.y);
    history.push({base:current.base,past:current.past,pp:current.pp,meaning:current.meaning,ok:true});
    acceptClick=false;setTimeout(()=>{acceptClick=true;nextQuestion();},250);
  }else{
    b.el.classList.add('wrong-hit');flash('❌','#e63946',b.x,b.y);
    history.push({base:current.base,past:current.past,pp:current.pp,meaning:current.meaning,ok:false});
    acceptClick=false;setTimeout(()=>{acceptClick=true;nextQuestion();},350);
  }
}
function flash(txt,color,x,y){const f=document.createElement('div');f.className='flash';f.textContent=txt;f.style.color=color;f.style.left=(x+30)+'px';f.style.top=y+'px';sky.appendChild(f);setTimeout(()=>f.remove(),800);}
function endGame(){
  playing=false;clearInterval(timerId);cancelAnimationFrame(animId);
  birds.forEach(b=>b.el.remove());birds=[];
  const seen={};history.forEach(h=>{seen[h.base]={...h};});
  const items=Object.values(seen);
  let listHTML=items.map(h=>{const cls=h.ok?'ok':'no';const mark=h.ok?'✅':'❌';return `<div class="item ${cls}"><span>${mark} ${h.base} → ${h.past} → ${h.pp}</span><span class="ko">${h.meaning||''}</span></div>`;}).join('');
  if(!listHTML)listHTML='<p style="text-align:center;color:#888;">푼 문제가 없어요!</p>';

  // 순위표에 기록 추가 (이번 기록 표시용 id 부여)
  const entryId=Date.now();
  leaderboard.push({name:playerName,score:score,id:entryId});
  leaderboard.sort((a,b)=>b.score-a.score);
  const medals=['🥇','🥈','🥉'];
  let boardHTML=leaderboard.slice(0,10).map((e,i)=>{
    const rank=medals[i]||('<b>'+(i+1)+'</b>');
    const me=e.id===entryId?' me':'';
    return `<div class="brow${me}"><span class="rank">${rank}</span><span class="nm">${e.name}</span><span class="sc">${e.score}점</span></div>`;
  }).join('');

  const ov=document.createElement('div');ov.className='overlay';ov.id='resultOverlay';
  ov.innerHTML=`
    <h2>⏱️ 시간 종료!</h2>
    <p>🦝 <b>${playerName}</b>(이)가 <b>${score}개</b> 잡았어! 🎉</p>
    <div class="board-title">🏆 순위표</div>
    <div class="board">${boardHTML}</div>
    <input id="nameInput" class="name-input" type="text" maxlength="10" placeholder="다음 사람 이름 ✍️" />
    <button class="btn" onclick="startGame()">다음 도전 🔄</button>
    <div style="margin-top:12px;width:100%;max-width:420px;">
      <details><summary style="cursor:pointer;color:#888;font-size:0.9rem;">내가 푼 단어 정답 보기 📖</summary>
      <div class="review" style="margin-top:8px;">${listHTML}</div></details>
    </div>`;
  sky.appendChild(ov);

  // 부모(Streamlit)로 점수 자동 전송 (반 전체 순위표 저장용)
  try{
    const payload={type:'bird_score',name:playerName,score:score,ts:entryId};
    window.parent.postMessage(payload,'*');
    // URL 해시로도 백업 전달 (일부 환경 대비)
    if(window.parent && window.parent.postMessage){
      window.parent.postMessage({isStreamlitMessage:true, ...payload},'*');
    }
  }catch(e){}
}
</script></body></html>
""".replace("__VERBS__", verbs_json).replace("__NUM__", str(num_birds)).replace("__TIME__", str(game_time))
