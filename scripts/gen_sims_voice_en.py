# -*- coding: utf-8 -*-
"""Shimulabo: English (/en/) build of the Voice Input category (10 sims) + /en/ homepage.
   Pages are self-contained for SEO: canonical, hreflang, JSON-LD, GA, breadcrumb baked in,
   so seo_internal.py / add_ga.py skip them. Typeless affiliate CTA on every result page."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
GA = "G-R72MT9H7PT"
CAT = "Voice Input & Time Saved"
GRAD = "linear-gradient(135deg,#eef2ff,#f5f3ff)"
AFF = "https://www.typeless.com/?via=44144c"

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

CTA = '''      <a class="cta-box" href="''' + AFF + '''" target="_blank" rel="noopener" style="display:block;text-decoration:none;text-align:left;margin-top:20px;background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1.5px solid #a5b4fc;border-radius:14px;padding:18px;">
        <div style="font-weight:900;color:#4f46e5;font-size:15px;">🎙️ That time saving is real — with voice input.</div>
        <div style="font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.7;">Talking is far faster than typing. <strong>The best voice-input tool right now is Typeless</strong>: its AI cleans up filler words and turns speech into polished text, so meeting notes, emails and articles get done in a fraction of the time. People stop wanting to go back to the keyboard.</div>
        <div style="margin-top:12px;display:inline-flex;align-items:center;gap:8px;background:#4f46e5;color:#fff;font-weight:800;font-size:14px;padding:11px 22px;border-radius:999px;">Try Typeless for free →</div>
      </a>'''

TYPELESS = '<div class="note" style="margin-top:14px;"><strong>Bottom line: the best voice-input tool right now is Typeless.</strong><br>There are many dictation tools, but Typeless stands out for accuracy and for auto-cleaning filler words into natural written text — turning the savings above into reality.</div>'

PRE = "../../../"  # /en/sims/<id>/ -> root

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__CANON__">
<link rel="alternate" hreflang="ja" href="__JA__">
<link rel="alternate" hreflang="en" href="__CANON__">
<link rel="alternate" hreflang="x-default" href="__JA__">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__OGDESC__">
<meta property="og:type" content="website">
<meta property="og:url" content="__CANON__">
<meta property="og:image" content="__OGIMG__">
<meta property="og:locale" content="en_US">
<meta name="robots" content="index,follow">
<link rel="icon" href="''' + PRE + '''favicon-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="''' + PRE + '''apple-touch-icon.png">
<link rel="stylesheet" href="''' + PRE + '''assets/style.css">
<!-- ga4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=''' + GA + '''"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","''' + GA + '''");</script>
__JSONLD__
<!-- adsense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
     crossorigin="anonymous"></script>
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="''' + PRE + '''en/index.html">
      ''' + LOGO + '''
      <span class="name">Simu<b>Lab</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="''' + PRE + '''en/index.html">← All sims</a>
  </div>
</header>

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="''' + PRE + '''en/index.html">Home</a><span>›</span>''' + CAT + '''<span>›</span><span class="cur">__H1__</span></nav>

  <div class="sim-head">
    <div class="cat">''' + CAT + '''</div>
    <h1>__H1__</h1>
    <p class="lead">__LEAD__</p>
  </div>

  <section class="panel">
__INPUTS__
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
__RESULT__
''' + CTA + '''
      <div style="text-align:center;margin-top:14px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">Share on 𝕏</button>
        <button class="btn btn-ghost" id="copyBtn">Copy result</button>
      </div>
    </div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="''' + PRE + '''en/index.html">← Back to SimuLab home</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 SimuLab (シミュラボ)</p>
  </div>
</footer>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const usd = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const num = (n) => Math.round(n).toLocaleString('en-US');
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('en-US'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  $('calcBtn').addEventListener('click', calc);
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('SimuLab,voiceinput'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='Copied ✓'; setTimeout(()=>$('copyBtn').textContent='Copy result',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="''' + PRE + '''assets/result-fx.js"></script>
<script src="''' + PRE + '''assets/lang-toggle.js"></script>
<script src="''' + PRE + '''assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

def faq_html(pairs):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in pairs) + '</dl>'

SIMS = []
def add(**k): SIMS.append(k)

add(id='input-jitan', emoji='🎙️',
  title='Voice Typing Savings Calculator | How much do you save by switching from typing to voice? | SimuLab',
  desc='Enter your words per day, typing speed (WPM) and hourly rate to see how much time and money you save each year by switching from typing to voice input.',
  ogtitle='Voice Typing Savings Calculator | How much do you save?', ogdesc='See your yearly time and money saved by switching from typing to voice input.',
  h1='Voice Typing Savings Calculator',
  lead='Stop typing, start talking. Enter how much you write per day, your typing speed and your hourly rate to see how much time and money you save per year with voice input.',
  inputs='''    <h2>🎙️ Your numbers</h2>
    <div class="row"><div class="field"><label>Words written per day</label><input type="number" id="words" value="1500" min="0" inputmode="numeric"></div>
    <div class="field"><label>Typing speed <span class="hint">(WPM)</span></label><input type="number" id="wpm" value="40" min="5" inputmode="numeric"></div></div>
    <div class="field"><label>Your hourly rate <span class="hint">($)</span></label><input type="number" id="rate" value="30" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">See my yearly savings</button>''',
  result='''      <div class="label">Money saved per year with voice input</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Time saved / day</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">Hours saved / year</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">Saved over 10 years</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>How much faster is voice?</h2>
    <div class="note"><strong>Formula</strong><br>Speaking (~150 WPM) is about 3× faster than typing (~40 WPM).<br>Time saved/day = words ÷ WPM × (1 − 1/3) · Money saved = hours saved × hourly rate</div>
    <p>People talk far faster than they type. Move your daily writing to voice and, over a year, the saved time and money add up fast — time you can put back into real work or rest.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('What about fixing recognition errors?','Modern AI dictation is highly accurate and even cleans up your text automatically, so editing time drops too.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const wd=Math.max(0,+$('words').value||0),wpm=Math.max(1,+$('wpm').value||1),r=Math.max(0,+$('rate').value||0);
    const typeMin=wd/wpm, voiceMin=wd/(wpm*3), saveDay=typeMin-voiceMin, yearH=saveDay*365/60, money=yearH*r;
    $('sub').textContent=`${num(wd)} words/day · ${wpm} WPM · $${num(r)}/hr`;$('day').textContent=num(saveDay)+' min';$('hours').textContent=num(yearH)+' hrs';$('y10').textContent=usd(money*10);
    SHARE=`Switching from typing to voice input would save me about ${usd(money)} (${num(yearH)} hours) a year 🎙️ What about you?`;show();anim($('big'),0,money,900);}''',
  faqs=[('What about fixing recognition errors?','Modern AI dictation is highly accurate and even cleans up your text automatically, so editing time drops too.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='gijiroku-jitan', emoji='📝',
  title='Meeting Minutes Voice Calculator | How much do you save with auto transcription? | SimuLab',
  desc='From meetings per week and minutes spent writing minutes, see how much working time and payroll cost you save per year by switching to voice input / auto transcription.',
  ogtitle='Meeting Minutes Voice Calculator | Yearly payroll saved', ogdesc='See how much time and payroll cost auto transcription saves on meeting minutes.',
  h1='Meeting Minutes Voice Calculator',
  lead='Writing up meeting minutes eats hours every week. See how much working time and payroll cost you save per year by switching to voice input and auto transcription.',
  inputs='''    <h2>📝 Your numbers</h2>
    <div class="row"><div class="field"><label>Meetings per week</label><input type="number" id="n" value="5" min="0" inputmode="numeric"></div>
    <div class="field"><label>Minutes to write up each</label><input type="number" id="min" value="40" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>Hourly rate <span class="hint">($)</span></label><input type="number" id="rate" value="35" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">See the savings</button>''',
  result='''      <div class="label">Payroll saved per year on minutes</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Hours saved / year</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">Saved per meeting</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">Meetings / year</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>The automation effect</h2>
    <div class="note"><strong>Formula</strong><br>Voice input / transcription cuts write-up time to about 1/3.<br>Yearly saving = minutes per write-up × 2/3 × meetings/week × 52 × hourly rate</div>
    <p>Record the meeting, talk through the summary, and the draft writes itself — you only tidy the key points. Across a whole team the saving is huge.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Is accuracy good enough?','Modern AI learns terminology and is highly accurate; usually only proper nouns need a quick fix.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),r=Math.max(0,+$('rate').value||0);
    const perSave=mi*2/3, yearH=perSave*n*52/60, money=yearH*r;
    $('sub').textContent=`${n}/week · ${mi} min each · $${num(r)}/hr`;$('hours').textContent=num(yearH)+' hrs';$('per').textContent=num(perSave)+' min';$('cnt').textContent=num(n*52);
    SHARE=`Auto transcription for meeting minutes would save about ${usd(money)} (${num(yearH)} hours) a year 📝`;show();anim($('big'),0,money,900);}''',
  faqs=[('Is accuracy good enough?','Modern AI learns terminology and is highly accurate; usually only proper nouns need a quick fix.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='mail-jitan', emoji='✉️',
  title='Email Writing Voice Calculator | How much do you save dictating email? | SimuLab',
  desc='From emails per day and minutes to write each, see how much time and money you save per year by dictating your email with voice input.',
  ogtitle='Email Writing Voice Calculator | Yearly savings', ogdesc='See your yearly savings from dictating email instead of typing it.',
  h1='Email Writing Voice Calculator',
  lead='You write a lot of email. What if you talked it instead? From emails per day and minutes per email, see the time and money voice input frees up each year.',
  inputs='''    <h2>✉️ Your numbers</h2>
    <div class="row"><div class="field"><label>Emails written per day</label><input type="number" id="n" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>Minutes per email</label><input type="number" id="min" value="4" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>Hourly rate <span class="hint">($)</span></label><input type="number" id="rate" value="30" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">See the savings</button>''',
  result='''      <div class="label">Saved per year on email</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Time saved / day</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">Hours saved / year</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">Emails / year</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>Email is made for voice</h2>
    <div class="note"><strong>Formula</strong><br>Voice cuts writing time to about 1/3.<br>Yearly saving = minutes/email × 2/3 × emails/day × 240 workdays × hourly rate</div>
    <p>Routine emails are the fastest to dictate — and AI tidies the tone and formatting, so proofreading shrinks too. The more email you send, the bigger the win.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Will it sound too casual?','AI rewrites speech into a clean professional tone — it won\'t read like a transcript.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),r=Math.max(0,+$('rate').value||0);
    const saveDay=n*mi*2/3, yearH=saveDay*240/60, money=yearH*r;
    $('sub').textContent=`${n}/day · ${mi} min each · $${num(r)}/hr`;$('day').textContent=num(saveDay)+' min';$('hours').textContent=num(yearH)+' hrs';$('cnt').textContent=num(n*240);
    SHARE=`Dictating my email would save about ${usd(money)} (${num(yearH)} hours) a year ✉️`;show();anim($('big'),0,money,900);}''',
  faqs=[('Will it sound too casual?','AI rewrites speech into a clean professional tone — it won\'t read like a transcript.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='blog-shippitsu', emoji='✍️',
  title='Article & Blog Writing Voice Calculator | How much faster with voice? | SimuLab',
  desc='From articles per month and minutes to write each, see how much time and value you gain per year by drafting articles and blog posts with voice input.',
  ogtitle='Article & Blog Writing Voice Calculator', ogdesc='See your yearly time gain from drafting articles by voice.',
  h1='Article & Blog Writing Voice Calculator',
  lead='Draft your articles by talking them through. From posts per month and minutes per post, see the time and value voice input frees up each year. For writers and creators.',
  inputs='''    <h2>✍️ Your numbers</h2>
    <div class="row"><div class="field"><label>Articles per month</label><input type="number" id="n" value="8" min="0" inputmode="numeric"></div>
    <div class="field"><label>Minutes to write each</label><input type="number" id="min" value="120" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>Hourly value <span class="hint">($ — your rate or outsource cost)</span></label><input type="number" id="rate" value="40" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">See the yearly gain</button>''',
  result='''      <div class="label">Yearly value saved on writing</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Hours saved / year</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">Extra articles possible</div><div class="v" id="extra">—</div></div>
      <div class="stat"><div class="k">Articles / year</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>The power of a spoken draft</h2>
    <div class="note"><strong>Formula</strong><br>Voice roughly halves drafting time (you plan in your head, then dictate).<br>Yearly saving = minutes/article × 0.5 × articles/month × 12 × hourly value</div>
    <p>Talking keeps your thoughts flowing where typing stalls them. Outline, dictate, let AI tidy it up — your output speeds up dramatically. Reinvest the time and you can publish even more.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Won\'t it read like spoken word?','AI converts speech into written style, so the final article reads naturally.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),r=Math.max(0,+$('rate').value||0);
    const saveYearMin=mi*0.5*n*12, yearH=saveYearMin/60, money=yearH*r, extra=mi>0?saveYearMin/(mi*0.5):0;
    $('sub').textContent=`${n}/month · ${mi} min each · $${num(r)}/hr`;$('hours').textContent=num(yearH)+' hrs';$('extra').textContent=num(extra);$('cnt').textContent=num(n*12);
    SHARE=`Drafting articles by voice would free up about ${usd(money)} (${num(yearH)} hours) of value a year ✍️`;show();anim($('big'),0,money,900);}''',
  faqs=[('Won\'t it read like spoken word?','AI converts speech into written style, so the final article reads naturally.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='moji-okoshi', emoji='🔊',
  title='Transcription Cost Savings Calculator | How much do you save with AI transcription? | SimuLab',
  desc='From minutes recorded per month and your outsourcing rate, see how much you save per year by switching transcription to AI voice recognition.',
  ogtitle='Transcription Cost Savings Calculator', ogdesc='See yearly savings from switching transcription to AI.',
  h1='Transcription Cost Savings Calculator',
  lead='Outsourced transcription is billed by the minute. See how much you save per year by switching interview and meeting transcription to AI voice recognition.',
  inputs='''    <h2>🔊 Your numbers</h2>
    <div class="row"><div class="field"><label>Minutes recorded per month</label><input type="number" id="min" value="180" min="0" inputmode="numeric"></div>
    <div class="field"><label>Outsourcing rate <span class="hint">($/min)</span></label><input type="number" id="tanka" value="1.5" min="0" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>AI tool monthly cost <span class="hint">($)</span></label><input type="number" id="tool" value="15" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">See the savings</button>''',
  result='''      <div class="label">Transcription saved per year</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Outsourced / year</div><div class="v" id="gai">—</div></div>
      <div class="stat"><div class="k">AI tool / year</div><div class="v" id="toolv">—</div></div>
      <div class="stat"><div class="k">Savings rate</div><div class="v accent" id="rate">—</div></div></div>''',
  article='''    <h2>Outsourced vs AI transcription</h2>
    <div class="note"><strong>Formula</strong><br>Outsourced (year) = minutes × rate/min × 12<br>Savings = outsourced cost − AI tool yearly cost</div>
    <p>Human transcription typically runs $1–2 per recorded minute. AI transcription is often a flat monthly fee with unlimited use — the more you transcribe, the more you save, and it's far faster too.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Is AI accuracy on par?','Modern AI is highly accurate, with speaker separation and custom vocabulary in many tools.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),t=Math.max(0,+$('tanka').value||0),tool=Math.max(0,+$('tool').value||0);
    const gai=mi*t*12, toolY=tool*12, save=Math.max(0,gai-toolY), rate=gai>0?save/gai*100:0;
    $('sub').textContent=`${num(mi)} min/mo · $${t}/min`;$('gai').textContent=usd(gai);$('toolv').textContent=usd(toolY);$('rate').textContent=Math.round(rate)+'%';
    SHARE=`Switching transcription to AI would save about ${usd(save)} a year (${Math.round(rate)}% off) 🔊`;show();anim($('big'),0,save,900);}''',
  faqs=[('Is AI accuracy on par?','Modern AI is highly accurate, with speaker separation and custom vocabulary in many tools.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='shorui-jitan', emoji='📄',
  title='Document & Report Writing Voice Calculator | Yearly time saved | SimuLab',
  desc='From weekly hours spent on documents and reports and your hourly rate, see how much time and money voice input saves you per year.',
  ogtitle='Document & Report Writing Voice Calculator', ogdesc='See yearly time and money saved writing documents by voice.',
  h1='Document & Report Writing Voice Calculator',
  lead='Reports, briefs, proposals — documents devour your week. From your weekly writing hours and hourly rate, see the yearly saving from voice input.',
  inputs='''    <h2>📄 Your numbers</h2>
    <div class="row"><div class="field"><label>Hours writing docs per week</label><input type="number" id="hours" value="5" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>Hourly rate <span class="hint">($)</span></label><input type="number" id="rate" value="35" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">See the savings</button>''',
  result='''      <div class="label">Saved per year on documents</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Hours saved / year</div><div class="v accent" id="hh">—</div></div>
      <div class="stat"><div class="k">Saved per week</div><div class="v" id="wk">—</div></div>
      <div class="stat"><div class="k">Over 10 years</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>Faster documents</h2>
    <div class="note"><strong>Formula</strong><br>Voice cuts document time by about 40% (thinking is included, so we keep it conservative).<br>Yearly saving = weekly hours × 40% × 52 × hourly rate</div>
    <p>Composing while typing is heavy on the brain. Talking lets ideas flow, and AI shapes and summarizes the draft, cutting clean-up time too.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('What about table-heavy docs?','The prose parts speed up most; pair voice with templates for the structured parts.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const h=Math.max(0,+$('hours').value||0),r=Math.max(0,+$('rate').value||0);
    const wk=h*0.4, yearH=wk*52, money=yearH*r;
    $('sub').textContent=`${h} hrs/week · $${num(r)}/hr`;$('hh').textContent=num(yearH)+' hrs';$('wk').textContent=wk.toFixed(1)+' hrs';$('y10').textContent=usd(money*10);
    SHARE=`Writing documents by voice would save about ${usd(money)} (${num(yearH)} hours) a year 📄`;show();anim($('big'),0,money,900);}''',
  faqs=[('What about table-heavy docs?','The prose parts speed up most; pair voice with templates for the structured parts.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='chat-jitan', emoji='💬',
  title='Chat & Messaging Voice Calculator | Yearly time saved | SimuLab',
  desc='From daily minutes spent typing chat and messages and your hourly value, see how much time voice input saves you per year.',
  ogtitle='Chat & Messaging Voice Calculator', ogdesc='See yearly time saved replying by voice instead of typing.',
  h1='Chat & Messaging Voice Calculator',
  lead='Slack, chat, DMs, social replies — they quietly eat your day. From your daily typing time, see the time and value voice input gives back each year.',
  inputs='''    <h2>💬 Your numbers</h2>
    <div class="row"><div class="field"><label>Minutes typing chat per day</label><input type="number" id="min" value="40" min="0" inputmode="numeric"></div>
    <div class="field"><label>Hourly value <span class="hint">($/hr)</span></label><input type="number" id="rate" value="25" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">See the yearly gain</button>''',
  result='''      <div class="label">Yearly value saved on chat</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Time saved / day</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">Hours saved / year</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">In 2-hr movies</div><div class="v" id="movie">—</div></div></div>''',
  article='''    <h2>Short replies, big totals</h2>
    <div class="note"><strong>Formula</strong><br>Voice roughly halves chat typing time.<br>Yearly = daily minutes × 50% × 365 × hourly value</div>
    <p>Even quick replies add up — thumb-typing is slower than you think. Talk to your phone instead and a year of micro-moments becomes real, recoverable time.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Hard to use in public?','Many tools support an earbud mic or quiet dictation; even at home it pays off.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),r=Math.max(0,+$('rate').value||0);
    const saveDay=mi*0.5, yearH=saveDay*365/60, money=yearH*r;
    $('sub').textContent=`${mi} min/day · $${num(r)}/hr`;$('day').textContent=num(saveDay)+' min';$('hours').textContent=num(yearH)+' hrs';$('movie').textContent=num(yearH/2);
    SHARE=`Replying by voice would save about ${usd(money)} (${num(yearH)} hours) a year 💬`;show();anim($('big'),0,money,900);}''',
  faqs=[('Hard to use in public?','Many tools support an earbud mic or quiet dictation; even at home it pays off.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='memo-jitan', emoji='🗒️',
  title='Notes & Journaling Voice Calculator | Yearly time saved | SimuLab',
  desc='From daily minutes spent on notes, logs and journaling, see how much time voice input saves you per year.',
  ogtitle='Notes & Journaling Voice Calculator', ogdesc='See yearly time saved capturing notes by voice.',
  h1='Notes & Journaling Voice Calculator',
  lead='Idea notes, daily logs, journaling, reading notes — capture them by voice. From your daily note-taking time, see the time and value you reclaim each year.',
  inputs='''    <h2>🗒️ Your numbers</h2>
    <div class="row"><div class="field"><label>Minutes on notes per day</label><input type="number" id="min" value="25" min="0" inputmode="numeric"></div>
    <div class="field"><label>Hourly value <span class="hint">($/hr)</span></label><input type="number" id="rate" value="25" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">See the yearly gain</button>''',
  result='''      <div class="label">Yearly value saved on notes</div>
      <div class="big">$<span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Time saved / day</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">Hours saved / year</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">Value over 10 years</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>Never lose the thought</h2>
    <div class="note"><strong>Formula</strong><br>Voice cuts note-taking time to about 1/3.<br>Yearly = daily minutes × 2/3 × 365 × hourly value</div>
    <p>Ideas vanish the moment you try to type them. Speaking captures them instantly — and you're far more likely to keep the habit going.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Can it make bullet lists?','Some tools format bullets when you ask, straight from speech.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),r=Math.max(0,+$('rate').value||0);
    const saveDay=mi*2/3, yearH=saveDay*365/60, money=yearH*r;
    $('sub').textContent=`${mi} min/day · $${num(r)}/hr`;$('day').textContent=num(saveDay)+' min';$('hours').textContent=num(yearH)+' hrs';$('y10').textContent=usd(money*10);
    SHARE=`Capturing notes by voice would save about ${usd(money)} (${num(yearH)} hours) a year 🗒️`;show();anim($('big'),0,money,900);}''',
  faqs=[('Can it make bullet lists?','Some tools format bullets when you ask, straight from speech.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='shogai-typing', emoji='⌨️',
  title='Lifetime Typing Time Calculator | How many days can voice input give you back? | SimuLab',
  desc='From your daily typing hours and the years ahead, see your lifetime hours at the keyboard and how many days of your life voice input could give back.',
  ogtitle='Lifetime Typing Time Calculator | Days you can reclaim', ogdesc='See your lifetime typing hours and the days voice input could give back.',
  h1='Lifetime Typing Time Calculator',
  lead='How many days of your life will you spend at the keyboard? From your daily typing hours, see your lifetime total — and how many days voice input could give back.',
  inputs='''    <h2>⌨️ Your numbers</h2>
    <div class="row"><div class="field"><label>Typing hours per day</label><input type="number" id="h" value="4" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>Years ahead</label><input type="number" id="years" value="40" min="1" max="70" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">See the time I can reclaim</button>''',
  result='''      <div class="label">Time voice input could give back</div>
      <div class="big"><span id="big">0</span><span class="unit"> days</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Lifetime typing</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">Hours reclaimed</div><div class="v accent" id="back">—</div></div>
      <div class="stat"><div class="k">Per day</div><div class="v" id="day">—</div></div></div>''',
  article='''    <h2>Reclaim your time</h2>
    <div class="note"><strong>Formula</strong><br>Lifetime typing = hours/day × 365 × years<br>Reclaimable = lifetime typing × 2/3 (voice ≈ 3× faster)</div>
    <p>Daily keyboard time piles into days — even months — of your life. Reclaim two-thirds of it with voice input, and imagine what that time could become. Time is your most valuable asset.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Can everything go to voice?','Code and fine edits still suit the keyboard, but most prose can be dictated.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),y=Math.max(1,+$('years').value||1);
    const totalH=h*365*y, backH=totalH*2/3, backDays=backH/24;
    $('sub').textContent=`${h} hrs/day × ${y} years`;$('total').textContent=num(totalH)+' hrs';$('back').textContent=num(backH)+' hrs';$('day').textContent=num(h*2/3*60)+' min';
    SHARE=`Switching to voice input could give me back about ${num(backDays)} days of my life ⌨️`;show();anim($('big'),0,backDays,900);}''',
  faqs=[('Can everything go to voice?','Code and fine edits still suit the keyboard, but most prose can be dictated.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])

add(id='kenshouen', emoji='🩹',
  title='Typing Strain Calculator | How much strain does voice input remove? | SimuLab',
  desc='From your daily typing hours, estimate yearly keystrokes and finger travel, and see how much hand strain switching to voice input removes.',
  ogtitle='Typing Strain Calculator | How much does voice remove?', ogdesc='Estimate yearly keystrokes and see how much strain voice input removes.',
  h1='Typing Strain Calculator',
  lead='All that typing is hard on your hands. From your daily typing hours, estimate yearly keystrokes and see how much hand strain switching to voice input removes.',
  inputs='''    <h2>🩹 Your numbers</h2>
    <div class="row"><div class="field"><label>Typing hours per day</label><input type="number" id="h" value="5" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>Share moved to voice <span class="hint">(%)</span></label><input type="number" id="rate" value="60" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">See the strain removed</button>''',
  result='''      <div class="label">Keystrokes removed per year</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">Keystrokes / year</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">Hours hands rested / yr</div><div class="v accent" id="rest">—</div></div>
      <div class="stat"><div class="k">Finger travel / year</div><div class="v" id="dist">—</div></div></div>''',
  article='''    <h2>Hand strain, in numbers</h2>
    <div class="note"><strong>Estimates</strong><br>Typing ≈ 250 keystrokes/min. 5 hrs/day ≈ 75,000 keystrokes/day.<br>Moving a share to voice removes that share of keystrokes and finger travel (≈ 2 cm per stroke).</div>
    <p>Long hours of typing can lead to strain, RSI and fatigue. Cut keystrokes with voice input and you meaningfully ease the load on your hands. Your health is an asset money can't buy — be kind to your body.</p>'''+TYPELESS+'''
    <h2>FAQ</h2>'''+faq_html([('Is this medical advice?','No — these are rough estimates. If you have pain, please see a medical professional.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),r=Math.max(0,Math.min(100,+$('rate').value||0))/100;
    const perDay=h*60*250, yearTotal=perDay*240, reduced=yearTotal*r;
    const restH=h*r*240, distKm=reduced*0.02/1000;
    $('sub').textContent=`${h} hrs/day · ${Math.round(r*100)}% to voice`;$('total').textContent=num(yearTotal);$('rest').textContent=num(restH)+' hrs';$('dist').textContent=num(distKm)+' km';
    SHARE=`Voice input would remove about ${num(reduced)} keystrokes a year for me 🩹 Be kind to your hands.`;show();anim($('big'),0,reduced,900);}''',
  faqs=[('Is this medical advice?','No — these are rough estimates. If you have pain, please see a medical professional.'),('Is my data sent anywhere?','No. This calculator runs entirely in your browser.')])


def jsonld_for(s):
    canon = f"{BASE}/en/sims/{s['id']}/"
    blocks = [{
        "@context": "https://schema.org", "@type": "WebApplication",
        "name": s['h1'], "url": canon, "description": s['ogdesc'],
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
        "inLanguage": "en", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@type": "Organization", "name": "SimuLab", "url": BASE + "/"}
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/en/"},
            {"@type": "ListItem", "position": 2, "name": s['h1'], "item": canon},
        ]
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s['faqs']]
    }]
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + '</script>' for b in blocks)


def render_sims():
    for s in SIMS:
        d = os.path.join(ROOT, 'en', 'sims', s['id']); os.makedirs(d, exist_ok=True)
        canon = f"{BASE}/en/sims/{s['id']}/"
        ja = f"{BASE}/sims/{s['id']}/"
        ogimg = f"{BASE}/ogp/{s['id']}.png"
        html = (TPL.replace('__TITLE__', s['title']).replace('__DESC__', s['desc'])
                .replace('__OGTITLE__', s['ogtitle']).replace('__OGDESC__', s['ogdesc'])
                .replace('__CANON__', canon).replace('__JA__', ja).replace('__OGIMG__', ogimg)
                .replace('__JSONLD__', jsonld_for(s))
                .replace('__H1__', s['h1']).replace('__LEAD__', s['lead'])
                .replace('__INPUTS__', s['inputs']).replace('__RESULT__', s['result'])
                .replace('__ARTICLE__', s['article']).replace('__JS__', s['js']).replace('__ID__', s['id']))
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print('created en/sims/' + s['id'])


HOME_TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SimuLab (English) | Free voice-input savings calculators</title>
<meta name="description" content="Free calculators that show how much time and money you save by switching from typing to voice input — for email, meeting minutes, transcription, writing and more.">
<link rel="canonical" href="''' + BASE + '''/en/">
<link rel="alternate" hreflang="ja" href="''' + BASE + '''/">
<link rel="alternate" hreflang="en" href="''' + BASE + '''/en/">
<link rel="alternate" hreflang="x-default" href="''' + BASE + '''/">
<meta property="og:title" content="SimuLab (English) | Voice-input savings calculators">
<meta property="og:description" content="See how much time and money voice input saves you, with free interactive calculators.">
<meta property="og:type" content="website">
<meta property="og:url" content="''' + BASE + '''/en/">
<meta property="og:image" content="''' + BASE + '''/ogp/default.png">
<meta property="og:locale" content="en_US">
<meta name="robots" content="index,follow">
<link rel="icon" href="../favicon-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="stylesheet" href="../assets/style.css">
<!-- ga4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=''' + GA + '''"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","''' + GA + '''");</script>
<script type="application/ld+json">__WEBSITE__</script>
<!-- adsense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
     crossorigin="anonymous"></script>
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="index.html">
      ''' + LOGO + '''
      <span class="name">Simu<b>Lab</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../index.html">日本語</a>
  </div>
</header>

<main class="wrap">
  <section class="hero" style="text-align:center;padding:30px 0 8px;">
    <h1 style="font-size:30px;margin:0 0 10px;">Turn “I should try voice input” into real numbers.</h1>
    <p class="lead" style="max-width:640px;margin:0 auto;">Free, instant calculators that show how much time and money you save by switching from typing to voice. No sign-up, runs entirely in your browser.</p>
  </section>

  <section style="margin-top:18px;">
    <div class="grid">
__CARDS__
    </div>
  </section>

  <section class="req-banner" style="margin-top:30px;">
    <h2>🎙️ The voice-input tool we recommend</h2>
    <p>Across these calculators, the savings are real — if you actually switch. The tool we recommend right now is <strong>Typeless</strong>: accurate dictation that auto-cleans filler words into polished text.</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="''' + AFF + '''" target="_blank" rel="noopener">Try Typeless for free →</a>
  </section>
</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../index.html">日本語サイトはこちら / Japanese site</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 SimuLab (シミュラボ)</p>
  </div>
</footer>
<script src="../assets/lang-toggle.js"></script>
</body>
</html>
'''

def render_home():
    cards = []
    for s in SIMS:
        cards.append(
f'''      <a class="sim-card" data-cat="voice" href="sims/{s['id']}/index.html">
        <div class="thumb" style="background:{GRAD}"><span class="emoji">{s['emoji']}</span></div>
        <div class="body"><div class="cat">{CAT}</div><h3>{s['h1']}</h3><p>{s['ogdesc'][:60]}</p><span class="go">Try it →</span></div>
      </a>''')
    website = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "SimuLab", "url": BASE + "/en/", "inLanguage": "en",
        "description": "Free calculators that show how much time and money you save with voice input."
    }, ensure_ascii=False)
    d = os.path.join(ROOT, 'en'); os.makedirs(d, exist_ok=True)
    html = HOME_TPL.replace('__CARDS__', "\n".join(cards)).replace('__WEBSITE__', website)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('created en/index.html')


if __name__ == '__main__':
    render_sims()
    render_home()
    print(f'EN voice done. {len(SIMS)} sims + home.')
