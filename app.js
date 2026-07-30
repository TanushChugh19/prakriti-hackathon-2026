const emotions = {
  joy: { icon: '✦', color: '#c9ef82', description: 'A bright, uplifting emotional state.', scores: [1.2, 96.8, 24.5, 0.8, 1.1, 8.4] },
  love: { icon: '♡', color: '#f49bb6', description: 'Warmth, connection, and affection are present.', scores: [2.1, 33.1, 95.4, 0.6, 0.9, 3.2] },
  anger: { icon: '✹', color: '#ff876b', description: 'A strong signal of frustration or opposition.', scores: [4.5, 1.2, 0.8, 94.6, 9.8, 2.1] },
  fear: { icon: '◒', color: '#b6a2ff', description: 'Concern, uncertainty, or apprehension is present.', scores: [8.2, 1.9, 1.4, 10.8, 93.2, 7.1] },
  sadness: { icon: '☾', color: '#82baf0', description: 'A quieter, reflective emotional state.', scores: [94.1, 3.3, 7.1, 2.2, 13.6, 1.7] },
  surprise: { icon: '✺', color: '#f7cd71', description: 'An unexpected turn has caught attention.', scores: [2.8, 14.5, 1.2, 3.4, 6.7, 92.7] }
};
const labels = ['Sadness','Joy','Love','Anger','Fear','Surprise'];
const input = document.querySelector('#emotionInput');
const count = document.querySelector('#charCount');
const spectrum = document.querySelector('#spectrum');
function classify(text){
  const t = text.toLowerCase();
  const signals = { love:['love','grateful','thank','heart','miss you','together','care','adore'], anger:['angry','frustrat','hate','furious','annoy','unfair','worst','nothing works'], fear:['scared','afraid','anxious','worried','nervous','panic','terrified','uncertain'], sadness:['sad','sorry','alone','lost','hurt','cry','miss','down','grief'], surprise:['surpris','can’t believe','cannot believe','what just','unexpected','wow','never saw','shocked'], joy:['happy','proud','excited','finally','amazing','great','wonderful','made it','joy','delighted'] };
  let best='joy', max=0; Object.entries(signals).forEach(([emotion,words])=>{const n=words.reduce((a,w)=>a+(t.includes(w)?1:0),0);if(n>max){max=n;best=emotion}}); return best;
}
function render(emotion){
  const data=emotions[emotion]; document.querySelector('#emotionIcon').textContent=data.icon; document.querySelector('#emotionIcon').style.background=data.color+'33'; document.querySelector('#emotionIcon').style.color=data.color; document.querySelector('#primaryEmotion').textContent=emotion[0].toUpperCase()+emotion.slice(1); document.querySelector('#emotionDescription').textContent=data.description; document.querySelector('#confidence').textContent=data.scores[labels.indexOf(document.querySelector('#primaryEmotion').textContent)].toFixed(1)+'%'; document.querySelector('#certainty').textContent=data.scores.reduce((a,b)=>Math.max(a,b)).toFixed(0)>90?'High certainty':'Clear signal'; spectrum.innerHTML=''; labels.forEach((label,i)=>{const row=document.createElement('div');row.className='emotion-bar';row.innerHTML=`<span>${label}</span><div class="bar-track"><div class="bar-fill" style="width:0;background:${label.toLowerCase()===emotion?data.color:'#7c7891'}"></div></div><b>${data.scores[i].toFixed(1)}%</b>`;spectrum.append(row);requestAnimationFrame(()=>row.querySelector('.bar-fill').style.width=data.scores[i]+'%')});
}
document.querySelector('#analyzeButton').addEventListener('click',()=>{if(!input.value.trim()) return; const btn=document.querySelector('#analyzeButton'); btn.innerHTML='Reading <span>⌁</span>';setTimeout(()=>{render(classify(input.value));btn.innerHTML='Read emotion <span>→</span>'},350)});
input.addEventListener('input',()=>count.textContent=`${input.value.length} / 500`);
document.querySelectorAll('[data-example]').forEach(btn=>btn.addEventListener('click',()=>{input.value=btn.dataset.example;input.dispatchEvent(new Event('input'));input.focus()}));
const modal=document.querySelector('#modal');const loginButton=document.querySelector('#loginButton');if(modal&&loginButton){loginButton.onclick=()=>modal.classList.add('open');document.querySelector('#closeModal').onclick=()=>modal.classList.remove('open');modal.onclick=e=>{if(e.target===modal)modal.classList.remove('open')};document.querySelector('#loginForm').onsubmit=e=>{e.preventDefault();modal.classList.remove('open');const toast=document.querySelector('#toast');toast.textContent='Welcome to your Emotion Signal workspace';toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),3000)}};
render('joy');
