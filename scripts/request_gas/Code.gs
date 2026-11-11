/* =========================================================
   シミュラボ リクエスト受付（Google Apps Script・ウェブアプリ）
   - 置き場所：スプレッドシート「シミュラボ リクエスト受付」の 拡張機能 → Apps Script
   - デプロイ：ウェブアプリ／実行ユーザー=自分／アクセス=全員
   - 初回だけエディタで setup() を実行（ADMIN_KEY と編集トリガーを作る）

   ■ サイトから
     POST {action:'submit', idea, genre, why, nick, email, website(罠)} → {ok, id}
     GET  ?list=1          → 掲載OKのリクエスト一覧（メールは出さない）
     GET  ?ids=a,b,c       → 指定した受付番号の状態（本人のブラウザ用）
   ■ 管理（Claude 用）
     GET  ?admin=1&key=KEY → 全件（メール込み）
     POST {action:'update', key, id, status, url, pub, reply} → 状態更新
   ■ 状態が「公開済み」になり公開URLとメールがあれば、依頼者へお知らせメールを自動送信
     （シートを手で書き換えても、編集トリガーで同じように送られる）
   ========================================================= */

const SHEET_NAME = 'リクエスト';
const HEAD = ['受付番号', '受付日時', '見たいシミュ', 'ジャンル', '理由', 'ニックネーム', 'メール',
              '状態', '公開URL', '掲載', 'ひとこと', '通知済み'];
const C = { id: 1, at: 2, idea: 3, genre: 4, why: 5, nick: 6, email: 7, status: 8, url: 9, pub: 10, reply: 11, notified: 12 };
const SITE = 'https://shimulabo.com';
const SHEET_ID = '1VW8aCX_6XL-WupbfdGe8D9rDoRqWvsRsBL2JQtEM1TE';
function ss_() { return SpreadsheetApp.openById(SHEET_ID); }

function sheet_() {
  const ss = ss_();
  let s = ss.getSheetByName(SHEET_NAME);
  if (!s) {
    s = ss.insertSheet(SHEET_NAME);
    s.appendRow(HEAD);
    s.setFrozenRows(1);
    s.getRange(1, 1, 1, HEAD.length).setFontWeight('bold').setBackground('#e0f2f1');
    s.getRange('H2:H').setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['受付', '制作中', '公開済み', '見送り'], true).build());
    s.getRange('J2:J').setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['○', ''], true).build());
  }
  return s;
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function clip_(v, n) {
  let s = (v == null ? '' : String(v)).replace(/\r\n?/g, '\n').trim().slice(0, n);
  if (/^[=+\-@]/.test(s)) s = "'" + s;            // 数式として解釈させない
  return s;
}

function rows_() {
  const s = sheet_();
  const last = s.getLastRow();
  if (last < 2) return [];
  return s.getRange(2, 1, last - 1, HEAD.length).getValues().map((r, i) => ({
    row: i + 2,
    id: String(r[0]),
    at: r[1] instanceof Date ? r[1].toISOString() : String(r[1]),
    idea: String(r[2]), genre: String(r[3]), why: String(r[4]),
    nick: String(r[5]), email: String(r[6]),
    status: String(r[7] || '受付'), url: String(r[8]), pub: String(r[9]),
    reply: String(r[10]), notified: String(r[11])
  })).filter(r => r.id);
}

function public_(r) {
  return { id: r.id, at: r.at, idea: r.idea, genre: r.genre, nick: r.nick,
           status: r.status, url: r.url, reply: r.reply };
}

function isAdmin_(k) {
  const real = PropertiesService.getScriptProperties().getProperty('ADMIN_KEY');
  return !!(k && real && k === real);
}

function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.admin) {
    if (!isAdmin_(p.key)) return out_({ ok: false, error: 'unauthorized' });
    return out_({ ok: true, items: rows_() });
  }
  if (p.ids) {
    const want = String(p.ids).split(',').slice(0, 30);
    const items = rows_().filter(r => want.indexOf(r.id) >= 0).map(public_);
    return out_({ ok: true, items: items });
  }
  // 一覧：掲載OK（○）のものだけ、新しい順
  const items = rows_().filter(r => r.pub === '○').map(public_).reverse();
  return out_({ ok: true, items: items });
}

function doPost(e) {
  let b = {};
  try { b = JSON.parse((e && e.postData && e.postData.contents) || '{}'); } catch (err) {}
  if (b.action === 'update') {
    if (!isAdmin_(b.key)) return out_({ ok: false, error: 'unauthorized' });
    return out_(update_(b));
  }
  return out_(submit_(b));
}

function submit_(b) {
  if (b.website) return { ok: true, id: 'thanks' };               // 罠の欄に入力＝ロボット
  const idea = clip_(b.idea, 1000);
  if (!idea) return { ok: false, error: 'idea required' };

  // 送りすぎ防止（10分で全体40件まで）
  const cache = CacheService.getScriptCache();
  const n = Number(cache.get('n') || 0);
  if (n >= 40) return { ok: false, error: 'busy' };
  cache.put('n', String(n + 1), 600);

  let email = clip_(b.email, 120);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) email = '';
  const rec = {
    id: Utilities.getUuid().replace(/-/g, '').slice(0, 10),
    idea: idea, genre: clip_(b.genre, 50), why: clip_(b.why, 1000),
    nick: clip_(b.nick, 50), email: email
  };

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    sheet_().appendRow([rec.id, new Date(), rec.idea, rec.genre, rec.why, rec.nick, rec.email,
                        '受付', '', '', '', '']);
  } finally { lock.releaseLock(); }

  try { notifyOwner_(rec); } catch (err) {}
  return { ok: true, id: rec.id };
}

function notifyOwner_(rec) {
  const me = Session.getEffectiveUser().getEmail();
  const url = ss_().getUrl();
  MailApp.sendEmail({
    to: me,
    subject: '【シミュラボ】新しいリクエスト：' + rec.idea.replace(/\s+/g, ' ').slice(0, 40),
    name: 'シミュラボ リクエスト受付',
    body:
      'シミュラボに新しいリクエストが届きました。\n\n' +
      '■見たいシミュ\n' + rec.idea + '\n\n' +
      '■ジャンル：' + (rec.genre || '-') + '\n' +
      '■理由\n' + (rec.why || '（未記入）') + '\n\n' +
      '■ニックネーム：' + (rec.nick || '（未記入）') + '\n' +
      '■お知らせ用メール：' + (rec.email ? 'あり' : 'なし') + '\n' +
      '■受付番号：' + rec.id + '\n\n' +
      '一覧（スプレッドシート）：' + url + '\n'
  });
}

function update_(b) {
  const r = rows_().find(x => x.id === String(b.id || ''));
  if (!r) return { ok: false, error: 'not found' };
  const s = sheet_();
  if (b.status != null) s.getRange(r.row, C.status).setValue(String(b.status));
  if (b.url != null) s.getRange(r.row, C.url).setValue(String(b.url));
  if (b.pub != null) s.getRange(r.row, C.pub).setValue(b.pub ? '○' : '');
  if (b.reply != null) s.getRange(r.row, C.reply).setValue(clip_(b.reply, 300));
  SpreadsheetApp.flush();
  const sent = notifyPending_();
  return { ok: true, id: r.id, mailed: sent.indexOf(r.id) >= 0 };
}

/* 「公開済み」＋公開URL＋メールあり＋未通知 の行に、お知らせメールを送る */
function notifyPending_() {
  const s = sheet_();
  const sent = [];
  rows_().forEach(r => {
    if (r.status !== '公開済み' || !r.url || r.notified) return;
    if (!r.email) { s.getRange(r.row, C.notified).setValue('メールなし'); return; }
    const name = r.nick ? r.nick + ' さん' : 'リクエストをくださった方';
    MailApp.sendEmail({
      to: r.email,
      subject: '【シミュラボ】リクエストのシミュレーションができました！',
      name: 'シミュラボ',
      body:
        name + '\n\n' +
        'シミュラボにリクエストをいただき、ありがとうございました。\n' +
        'いただいたアイデアをもとに、シミュレーションを作って公開しました！\n\n' +
        '■リクエスト内容\n' + r.idea + '\n\n' +
        '■できたシミュレーション\n' + r.url + '\n\n' +
        (r.reply ? '■つくり手からひとこと\n' + r.reply + '\n\n' : '') +
        'ほかのリクエストと進み具合はこちら：\n' + SITE + '/board/\n\n' +
        'またいつでもアイデアをお寄せください。\n' + SITE + '/request/\n\n' +
        '――――\nシミュラボ（触って分かるシミュレーター集）\n' + SITE + '/\n' +
        '※このメールは、リクエスト時にお知らせ用のメールアドレスをご記入いただいた方にお送りしています。'
    });
    s.getRange(r.row, C.notified).setValue(Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm'));
    sent.push(r.id);
  });
  return sent;
}

/* シートを手で書き換えたとき（編集トリガー） */
function onEditNotify(e) {
  try { notifyPending_(); } catch (err) {}
}

/* 初回だけ実行：管理キーと編集トリガーを作る */
function setup() {
  sheet_();
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('ADMIN_KEY')) {
    props.setProperty('ADMIN_KEY', Utilities.getUuid().replace(/-/g, ''));
  }
  const ss = ss_();
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'onEditNotify') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('onEditNotify').forSpreadsheet(ss).onEdit().create();
  Logger.log('ADMIN_KEY=' + props.getProperty('ADMIN_KEY'));
  Logger.log('owner=' + Session.getEffectiveUser().getEmail());
}
