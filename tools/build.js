// Builds a self-hostable, SEO-ready static site into ../site
// Usage: node tools/build.js https://your-domain.com
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const SITE=(process.argv[2]||'https://webdesign-hnu.vercel.app').replace(/\/$/,'');
const ROOT=path.join(__dirname,'..'),OUT=path.join(ROOT,'site'),TMP=path.join(ROOT,'.build');
const SRC=fs.readFileSync(path.join(ROOT,'src','index.html'),'utf8');
const AUTHOR={name:'Ahmed Salman',url:'https://dev.uniskills.pro/'};
const PAGES={
 'home':{t:'Web Design Pixel Quest | شرح وحل مادة Web Design',d:'شرح مادة Web Design بالعربي والمصطلحات إنجليزي: 5 محاضرات، كويز تدريبي على كل محاضرة، واختبار شامل 30 سؤال بيتولد مختلف كل مرة من بنك 250 سؤال.',type:'home'},
 'lec-1':{t:'Introduction to Web Design شرح | UI vs UX | Web Design',d:'يعني إيه Web Design، الفرق بينه وبين Development و Graphic Design، UI vs UX، مكونات الموقع، أنواع المواقع، ومراحل التصميم الخمسة.',type:'lesson'},
 'lec-2':{t:'Web Layout & Grid System شرح | 12-column grid | Web Design',d:'الـ Web Layout وأعمدته الخمسة، مكونات الصفحة، الـ Grid System و 12-column grid، أنواع الـ layouts، Visual Hierarchy، وتجهيز الملف في Illustrator.',type:'lesson'},
 'lec-3':{t:'Website Elements & Visual Identity شرح | 8px, Breakpoints | Web Design',d:'طبقات التصميم، عناصر الـ interface، مبادئ التصميم، الـ 8px spacing system، الـ containers والـ breakpoints، والمقارنة بين المواقع التعليمية والمتاحف والبورتفوليو.',type:'lesson'},
 'lec-4':{t:'Logo Design شرح | أنواع اللوجو ومعاييره | Web Design',d:'تعريف اللوجو، استراتيجية التصميم، الـ 10 معايير، الأنواع السبعة (Word Mark, Letter Mark, Emblem, Mascot...)، تحليل لوجوهات المتاحف المصرية، ومراحل التصميم في Illustrator.',type:'lesson'},
 'lec-5':{t:'Designing Website Elements شرح | Buttons, Icons, Cards | Web Design',d:'تصميم الـ navigation والـ buttons والـ icons والـ cards والـ typography، مبادئ الـ visual consistency، وألوان المتاحف وعلم نفس الألوان.',type:'lesson'},
 'quiz-1':{t:'Introduction to Web Design Quiz | كويز محاضرة 1',d:'كويز MCQ تدريبي على مقدمة Web Design مع الإجابات والشرح بعد كل سؤال.',type:'quiz'},
 'quiz-2':{t:'Web Layout Quiz | كويز محاضرة 2 | Web Design',d:'كويز MCQ تدريبي على الـ Web Layout والـ Grid System مع الإجابات والشرح.',type:'quiz'},
 'quiz-3':{t:'Website Elements Quiz | كويز محاضرة 3 | Web Design',d:'كويز MCQ تدريبي على عناصر الموقع والـ spacing والـ breakpoints مع الإجابات والشرح.',type:'quiz'},
 'quiz-4':{t:'Logo Design Quiz | كويز محاضرة 4 | Web Design',d:'كويز MCQ تدريبي على تصميم اللوجو وأدوات Illustrator مع الإجابات والشرح.',type:'quiz'},
 'quiz-5':{t:'Designing Website Elements Quiz | كويز محاضرة 5 | Web Design',d:'كويز MCQ تدريبي على تصميم الـ buttons والـ icons والـ cards والـ typography مع الإجابات والشرح.',type:'quiz'},
 'exam':{t:'Final Exam | اختبار شامل Web Design بيتولد كل مرة',d:'اختبار شامل 30 سؤال على المحاضرات الخمسة، بيتولد مختلف كل مرة من بنك 250 سؤال، مع تحليل الدرجة لكل محاضرة.',type:'quiz'},
};
const url=r=>SITE+(r==='home'?'/':'/'+r+'/');
const esc=s=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
function ld(r,p){
  const base={"@context":"https://schema.org"};
  const course={"@type":"Course",name:"Web Design (Multimedia Software)",description:PAGES.home.d,inLanguage:["ar","en"],url:url('home'),
    provider:{"@type":"Person",name:AUTHOR.name,url:AUTHOR.url},isAccessibleForFree:true};
  if(p.type==='home')return [{...base,"@type":"WebSite",name:"Web Design Pixel Quest",url:url('home'),inLanguage:"ar",author:{"@type":"Person",name:AUTHOR.name,url:AUTHOR.url}},{...base,...course}];
  const crumbs={...base,"@type":"BreadcrumbList",itemListElement:[{"@type":"ListItem",position:1,name:"Web Design",item:url('home')},{"@type":"ListItem",position:2,name:p.t.split(' | ')[0],item:url(r)}]};
  const lr={...base,"@type":p.type==='quiz'?"Quiz":"LearningResource",name:p.t.split(' | ')[0],description:p.d,url:url(r),inLanguage:["ar","en"],
    learningResourceType:p.type==='quiz'?"Practice quiz":"Lesson",educationalLevel:"University, Level 3",isAccessibleForFree:true,
    author:{"@type":"Person",name:AUTHOR.name,url:AUTHOR.url},isPartOf:course};
  return [lr,crumbs];
}
function head(r,p){return `<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(p.t)}</title>
<meta name="description" content="${esc(p.d)}">
<meta name="author" content="${AUTHOR.name}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#05070d">
<link rel="canonical" href="${url(r)}">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="author" href="${AUTHOR.url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Web Design Pixel Quest">
<meta property="og:locale" content="ar_EG">
<meta property="og:title" content="${esc(p.t)}">
<meta property="og:description" content="${esc(p.d)}">
<meta property="og:url" content="${url(r)}">
<meta property="og:image" content="${SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Web Design Pixel Quest - pixel character and title">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(p.t)}">
<meta name="twitter:description" content="${esc(p.d)}">
<meta name="twitter:image" content="${SITE}/og.png">
<meta name="mmd-route" content="${r}">
${ld(r,p).map(o=>`<script type="application/ld+json">${JSON.stringify(o)}</script>`).join('\n')}
<style>:root{padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
`}
(async()=>{
  fs.rmSync(OUT,{recursive:true,force:true});fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(TMP,{recursive:true});
  const body=SRC.replace(/^<title>[\s\S]*?<meta name="author"[^>]*>\n/,'').replace('<meta name="claude:viewport-fit-sides" content="cover">\n','');
  const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1200,height:900}});
  for(const [r,p] of Object.entries(PAGES)){
    const html=head(r,p)+body+'\n</body>\n</html>\n';
    const tmp=path.join(TMP,r+'.html');fs.writeFileSync(tmp,html);
    await pg.goto('file://'+tmp);await pg.waitForTimeout(250);
    const app=await pg.evaluate(()=>document.getElementById('app').innerHTML);
    const out=html.replace('<!--PRERENDER-->',app);
    const dir=r==='home'?OUT:path.join(OUT,r);fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'index.html'),out);
  }
  // images: OG card + icons, drawn with the same character code
  const ahmed=SRC.match(/const AHMED=\(function\(\)[\s\S]*?return X\}\)\(\);/)[0];
  const card=`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=IBM+Plex+Sans+Arabic:wght@600&display=swap"></head>
<body style="margin:0;width:1200px;height:630px;background:#05070d;overflow:hidden;font-family:'Press Start 2P';position:relative">
<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background-image:linear-gradient(#7c88ff55 2px,transparent 2px),linear-gradient(90deg,#7c88ff55 2px,transparent 2px);background-size:40px 40px;-webkit-mask-image:linear-gradient(transparent,#000);border-top:4px solid #ffd23f"></div>
<div style="position:absolute;left:80px;top:90px;color:#7c88ff;font-size:20px;letter-spacing:3px">WEB DESIGN · MULTIMEDIA SOFTWARE</div>
<div style="position:absolute;left:80px;top:150px;color:#dfe3ff;font-size:54px;line-height:1.5;text-shadow:5px 5px 0 #4b55e8">WEB DESIGN<br><span style="color:#ffd23f;text-shadow:5px 5px 0 #a86f00">QUEST</span></div>
<div dir="rtl" style="position:absolute;left:80px;top:360px;color:#eef1f8;font:600 34px 'IBM Plex Sans Arabic'">شرح · كويزات · اختبار شامل</div>
<div style="position:absolute;left:80px;top:440px;color:#8a93a8;font-size:16px">BY AHMED SALMAN</div>
<canvas id="c" width="48" height="72" style="position:absolute;right:120px;top:90px;width:280px;height:420px;image-rendering:pixelated;filter:drop-shadow(0 0 30px rgba(124,136,255,.55))"></canvas>
<script>${ahmed};AHMED.O(document.getElementById('c').getContext('2d'),AHMED.o.cheer)</script></body></html>`;
  fs.writeFileSync(path.join(TMP,'og.html'),card);
  await pg.setViewportSize({width:1200,height:630});await pg.goto('file://'+path.join(TMP,'og.html'));await pg.waitForTimeout(1500);
  await pg.screenshot({path:path.join(OUT,'og.png')});
  for(const [name,size] of [['favicon.png',64],['apple-touch-icon.png',180],['icon-512.png',512]]){
    fs.writeFileSync(path.join(TMP,'ic.html'),`<body style="margin:0;background:#05070d;width:${size}px;height:${size}px;display:grid;place-items:center"><canvas id="c" width="48" height="72" style="height:${Math.round(size*1.25)}px;margin-top:${Math.round(size*.55)}px;image-rendering:pixelated"></canvas><script>${ahmed};AHMED.O(document.getElementById('c').getContext('2d'),AHMED.o.idle)</script></body>`);
    await pg.setViewportSize({width:size,height:size});await pg.goto('file://'+path.join(TMP,'ic.html'));await pg.screenshot({path:path.join(OUT,name)});
  }
  await b.close();
  const today=new Date().toISOString().slice(0,10);
  fs.writeFileSync(path.join(OUT,'sitemap.xml'),`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${Object.keys(PAGES).map(r=>`  <url><loc>${url(r)}</loc><lastmod>${today}</lastmod><priority>${r==='home'?'1.0':r.startsWith('lec')?'0.8':'0.7'}</priority></url>`).join('\n')}\n</urlset>\n`);
  fs.writeFileSync(path.join(OUT,'robots.txt'),`User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`);
  fs.writeFileSync(path.join(OUT,'site.webmanifest'),JSON.stringify({name:'Web Design Pixel Quest',short_name:'Web Design',lang:'ar',dir:'rtl',start_url:'/',display:'standalone',background_color:'#05070d',theme_color:'#05070d',icons:[{src:'/apple-touch-icon.png',sizes:'180x180',type:'image/png'},{src:'/icon-512.png',sizes:'512x512',type:'image/png'}]},null,2));
  fs.writeFileSync(path.join(OUT,'404.html'),fs.readFileSync(path.join(OUT,'index.html'),'utf8').replace('<meta name="robots" content="index, follow, max-image-preview:large">','<meta name="robots" content="noindex">'));
  fs.rmSync(TMP,{recursive:true,force:true});
  console.log('built',Object.keys(PAGES).length,'pages for',SITE);
})();
