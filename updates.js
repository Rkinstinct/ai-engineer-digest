/* Supplemental transcript-based cards. Existing cards remain in the HTML. */
(async function () {
  const files = ['lectures-2026-11-extra.json', 'lectures-2026-11-extra2.json'];
  const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const months = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'];
  const label = d => {const [y,m,day]=d.split('-'); return `${Number(day)} ב${months[Number(m)-1]} ${y}`;};
  const main = document.querySelector('main');
  const toc = main.querySelector('.toc');
  const data = (await Promise.all(files.map(async f => {const r=await fetch(new URL(f,document.baseURI));if(!r.ok)throw Error('Supplement unavailable');return r.json();}))).flat();
  data.sort((a,b)=>b.published_est.localeCompare(a.published_est)||b.added.localeCompare(a.added));
  const sections = new Map();
  for (const x of data) {
    if(document.getElementById('v'+x.id)) continue;
    const d=x.published_est;
    let section=document.getElementById('d'+d);
    if(!section){
      section=document.createElement('section'); section.className='section';section.id='d'+d;
      section.innerHTML=`<div class="wrap"><h2 class="daytitle">${label(d)} <span class="note">(תאריך משוער)</span></h2></div>`;
      const next=[...main.querySelectorAll(':scope > section.section')].find(s=>s.id.slice(1)<d);
      main.insertBefore(section,next||null);
    }
    if(!sections.has(d))sections.set(d,{section,cards:[]});
    const s=x.summary_he, a=document.createElement('article');a.className='lec';a.id='v'+x.id;
    a.innerHTML=`<h3>${escape(x.title)}</h3><p class="meta">${escape(x.speaker)}${x.org?' · '+escape(x.org):''} · ${Math.floor(x.duration_sec/60)}:${String(x.duration_sec%60).padStart(2,'0')} דקות</p><p><strong>בקצרה:</strong> ${escape(s.tldr)}</p><ul>${s.points.map(p=>'<li>'+escape(p)+'</li>').join('')}</ul><p class="aud"><strong>למי זה מתאים:</strong> ${escape(s.audience)}</p><div class="tags">${s.tags.map(t=>'<span>'+escape(t)+'</span>').join('')}</div><a class="src" href="https://www.youtube.com/watch?v=${encodeURIComponent(x.id)}" rel="noopener" target="_blank">צפייה בהרצאה ביוטיוב ←</a>`;
    sections.get(d).cards.push(a);
  }
  for(const {section,cards} of sections.values())section.querySelector('.daytitle').after(...cards);
  toc.replaceChildren(...[...main.querySelectorAll(':scope > section.section')].map(section=>{const a=document.createElement('a');a.href='#'+section.id;a.textContent=`${label(section.id.slice(1))} (${section.querySelectorAll('article.lec').length})`;return a;}));
  main.querySelector('.hero p.note').textContent=main.querySelector('.hero p.note').textContent.replace(/^\d+/,String(main.querySelectorAll('article.lec').length));
  if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target)target.scrollIntoView();}
})().catch(error=>console.error('Additional lecture cards could not be loaded:',error));
