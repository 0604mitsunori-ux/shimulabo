# -*- coding: utf-8 -*-
"""シミュラボ：結婚式・ブライダル 追加3本（既存 slug=wedding に追加）。結婚指輪・婚約指輪の予算/二次会会費/ハネムーン費用。
gen_sims_tool TPL流用。seo_internal.py / gen_images.py のauto-importに 'gen_sims_wedding2' を追加。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '結婚式・ブライダル'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)
ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700);el.textContent=Math.round(v*p).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=Math.round(v).toLocaleString('ja-JP');})(performance.now());}'''

# ============================================================
# 1. 結婚指輪・婚約指輪の予算（結婚指輪 相場 22000/KD1 + 婚約指輪 21000/KD2）★★★
# ============================================================
add(id='yubiwa-yosan', emoji='💍',
  title='結婚指輪・婚約指輪の予算計算機｜相場とお給料からの目安｜シミュラボ',
  desc='手取り月収を入れるだけで、婚約指輪・結婚指輪の予算の目安を計算する無料ツール。世間の相場（婚約指輪・結婚指輪ペア）も表示。無理のない予算決めに。',
  ogtitle='結婚指輪・婚約指輪の予算計算機', ogdesc='月収から婚約指輪・結婚指輪の予算目安を計算。相場も表示。',
  h1='結婚指輪・婚約指輪の予算計算機',
  lead='指輪の予算、いくらが目安?手取り月収を入れると、婚約指輪・結婚指輪の予算の目安を計算します。世間の相場とあわせて、無理のない予算決めに。',
  inputs='''    <h2>💍 手取り月収を入れる</h2>
    <div class="field"><label>手取り月収 <span class="hint">円</span></label><input type="number" id="income" value="250000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">予算の目安を見る</button>''',
  result='''      <div class="label">婚約指輪の予算の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">結婚指輪（2人分・ペア）</div><div class="v accent" id="pair">—</div></div>
      <div class="stat"><div class="k">婚約指輪の相場</div><div class="v" id="seng">約30〜40万円</div></div>
      <div class="stat"><div class="k">結婚指輪の相場（ペア）</div><div class="v" id="marr">約20〜30万円</div></div></div>''',
  article='''    <div class="note"><strong>予算の目安</strong><br>婚約指輪：手取り月収の約1.5ヶ月分（「給料3ヶ月分」は昔の広告コピーで、今は月収1〜2ヶ月が主流）／結婚指輪：2人分（ペア）で20〜30万円が目安。</div>
    <h2>指輪の予算と相場</h2>
    <p>婚約指輪の予算は、かつて「給料の3ヶ月分」と言われましたが、これは古い広告コピー。現在の平均購入額は約30〜40万円で、手取り月収の1〜2ヶ月分を目安にする人が多数派です。結婚指輪は2人分（ペア）で20〜30万円ほどが相場。大切なのは金額より、二人が納得できること。本ツールは月収からの目安と世間の相場を表示します。無理のない範囲で選びましょう。</p>
    <h2>よくある質問</h2>'''+faq([
      ('給料3ヶ月分って本当？','昔の広告コピーで、今は月収1〜2ヶ月分が主流。相場は約30〜40万円です。'),
      ('結婚指輪と婚約指輪の違いは？','婚約指輪はプロポーズ・婚約の証、結婚指輪は日常的に着ける2人おそろいの指輪です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const inc=Math.max(0,+$('income').value||0);
    const seng=Math.round(inc*1.5/10000)*10000;
    const pairV=Math.min(350000,Math.max(200000,200000+Math.round(inc*0.4/10000)*10000));
    $('sub').textContent='手取り月収 '+num(inc)+'円 × 約1.5ヶ月（婚約指輪）';
    $('pair').textContent='約'+num(Math.round(pairV/10000))+'万円';
    SHARE='結婚指輪・婚約指輪の予算、婚約指輪は約'+num(Math.round(seng/10000))+'万円が目安でした💍';show();anim(seng);}
'''+ANIM)

# ============================================================
# 2. 二次会会費シミュ（結婚式 二次会 会費 1800/KD0）
# ============================================================
add(id='nijikai-kaihi', emoji='🥂',
  title='結婚式 二次会の会費シミュレーター｜赤字にならない会費はいくら？｜シミュラボ',
  desc='参加人数・会場費・1人あたりの飲食費・景品代を入れると、赤字にならない1人あたりの会費の目安を計算する無料ツール。幹事の予算づくりに。',
  ogtitle='二次会の会費シミュレーター｜適正な会費は？', ogdesc='人数・会場費・飲食費・景品代から必要な会費を計算。',
  h1='結婚式 二次会の会費シミュレーター',
  lead='二次会の会費、いくらに設定する?参加人数・会場費・飲食費・景品代を入れると、赤字にならない1人あたりの会費の目安を計算します。幹事さん必見。',
  inputs='''    <h2>🥂 二次会の条件を入れる</h2>
    <div class="row"><div class="field"><label>参加人数 <span class="hint">人</span></label><input type="number" id="n" value="40" min="1" inputmode="numeric"></div>
    <div class="field"><label>1人あたり飲食費 <span class="hint">円</span></label><input type="number" id="food" value="4000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>会場費・その他固定費 <span class="hint">円</span></label><input type="number" id="venue" value="30000" min="0" inputmode="numeric"></div>
    <div class="field"><label>景品・装飾・備品 <span class="hint">円</span></label><input type="number" id="prize" value="50000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要な会費を計算</button>''',
  result='''      <div class="label">必要な1人あたり会費（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総費用</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">一般的な会費との比較</div><div class="v accent" id="hikaku">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>必要会費 ＝（飲食費×人数 ＋ 会場費 ＋ 景品代）÷ 人数<br>※会費は500円単位で切り上げると集金がスムーズです。</div>
    <h2>二次会の会費の決め方</h2>
    <p>二次会の会費は「総費用 ÷ 参加人数」で求めた金額を、500円単位で切り上げて設定するのが基本です。一般的な相場は、男性6,000〜7,000円、女性5,000〜6,000円ほど（男女で差をつけるケースも）。会場費・飲食費・景品代・装飾などの総費用を見積もり、赤字にならない会費を設定しましょう。会費が相場より高すぎると参加のハードルが上がるので、景品代や演出費とのバランスが大切です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('会費の相場は？','男性6,000〜7,000円、女性5,000〜6,000円ほどが一般的です。'),
      ('男女で差をつける？','景品やドレスコードに配慮し、女性をやや安く設定することもあります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const n=Math.max(1,+$('n').value||1),food=Math.max(0,+$('food').value||0),venue=Math.max(0,+$('venue').value||0),prize=Math.max(0,+$('prize').value||0);
    const total=food*n+venue+prize;const fee=Math.ceil(total/n/500)*500;
    $('sub').textContent=n+'人・総費用'+num(total)+'円 ÷ 人数（500円単位で切上げ）';
    $('total').textContent=yen(total);
    const cmp= fee<=5500?'相場よりお手頃':fee<=7000?'一般的な相場の範囲':'相場より高め（景品代を見直すと◎）';
    $('hikaku').textContent=cmp;
    SHARE='二次会の会費シミュ、必要な会費は1人 約'+yen(fee)+'でした🥂';show();anim(fee);}
'''+ANIM)

# ============================================================
# 3. ハネムーン費用シミュ（ハネムーン 費用 100/TP3900）
# ============================================================
add(id='honeymoon-hiyou', emoji='✈️',
  title='ハネムーン費用シミュレーター｜行き先・日数から新婚旅行の予算｜シミュラボ',
  desc='行き先・日数・人数を選ぶと、ハネムーン（新婚旅行）の費用の目安を計算する無料ツール。国内・アジア・ハワイ・ヨーロッパ別の相場で、2人分の総額をチェック。',
  ogtitle='ハネムーン費用シミュレーター｜新婚旅行の予算', ogdesc='行き先・日数からハネムーンの費用の目安を計算。',
  h1='ハネムーン費用シミュレーター',
  lead='新婚旅行、いくらかかる?行き先・日数を選ぶと、ハネムーン費用の目安（2人分の総額）を計算します。旅行先選びと予算づくりに。',
  inputs='''    <h2>✈️ 行き先と日数を選ぶ</h2>
    <div class="field"><label>行き先</label><select id="dest">
      <option value="35000">国内（沖縄・北海道など）</option><option value="55000" selected>近場アジア（韓国・台湾・東南アジア）</option>
      <option value="80000">ハワイ・グアム</option><option value="100000">ヨーロッパ・モルディブ・タヒチ</option></select></div>
    <div class="field"><label>日数 <span class="hint">日</span></label><input type="number" id="days" value="5" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">費用の目安を見る</button>''',
  result='''      <div class="label">ハネムーン費用の目安（2人分）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1人あたり</div><div class="v" id="one">—</div></div>
      <div class="stat"><div class="k">お土産・現地費の目安(別途)</div><div class="v accent" id="extra">—</div></div></div>''',
  article='''    <div class="note"><strong>目安について</strong><br>渡航先別の1人1日あたりの費用 × 日数 × 2人で概算。航空券・ホテル・現地費を含む大まかな目安で、時期（GW・年末年始は高騰）やグレードで変わります。</div>
    <h2>ハネムーンの費用相場</h2>
    <p>ハネムーンの費用は行き先と日数で大きく変わります。目安は、国内なら2人で15〜25万円、近場アジアで25〜40万円、ハワイ・グアムで40〜70万円、ヨーロッパやモルディブなどの遠方・リゾートで60〜100万円ほど。航空券とホテルが大半を占め、ゴールデンウィークや年末年始は高騰します。これとは別に、お土産代・現地での食事や観光の費用がかかります。ご祝儀や結婚資金とのバランスで予算を決めましょう。</p>
    <h2>よくある質問</h2>'''+faq([
      ('安く行くには？','繁忙期（GW・年末年始・お盆）を避け、早割やパッケージツアーを使うと抑えられます。'),
      ('お土産代は別？','はい。本ツールの目安とは別に、お土産・現地費を見込んでおきましょう。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const per=+$('dest').value||0,days=Math.max(1,+$('days').value||1);
    const oneTotal=per*days;const total=oneTotal*2;const extra=Math.round(total*0.15/1000)*1000;
    $('sub').textContent=sel('dest').text.split('（')[0]+'・'+days+'日間・2人分';
    $('one').textContent=yen(oneTotal);$('extra').textContent='約'+yen(extra);
    SHARE='ハネムーン費用シミュ、'+sel('dest').text.split('（')[0]+'・'+days+'日間で2人 約'+yen(total)+'でした✈️';show();anim(total);}
'''+ANIM)

if __name__=='__main__':
    render()
    print(f'wedding2 done. {len(SIMS)} sims.')
