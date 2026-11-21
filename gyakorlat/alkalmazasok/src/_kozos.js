// Közös segédfüggvények a PE tankönyvsorozat böngészős alkalmazásaihoz (MIT licenc)
const $ = id => document.getElementById(id);
function el(tag, attrs = {}, ...ch) { const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) { if (k === 'class') e.className = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v); }
  for (const c of ch.flat()) e.append(c instanceof Node ? c : document.createTextNode(c)); return e; }
const SUP = {'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function fmt(x, sig = 3) {
  if (x === null || x === undefined || isNaN(x)) return '–';
  if (!isFinite(x)) return '∞';
  if (x === 0) return '0';
  const a = Math.abs(x);
  if (a >= 0.01 && a < 1e5) { let d = Math.max(0, sig - 1 - Math.floor(Math.log10(a))); d = Math.min(d, 6);
    return x.toFixed(d).replace('.', ','); }
  const e = Math.floor(Math.log10(a)); const m = x / Math.pow(10, e);
  return m.toFixed(sig - 1).replace('.', ',') + '·10' + String(e).split('').map(c => SUP[c]).join('');
}
function szam(s) { if (typeof s === 'number') return s; if (s === undefined || s === null) return NaN;
  const t = String(s).trim().replace(/\s/g, '').replace(',', '.'); return t === '' ? NaN : Number(t); }
function ment(kulcs, obj) { try { localStorage.setItem('pe-bkr-' + kulcs, JSON.stringify(obj)); } catch (e) {} }
function betolt(kulcs) { try { const s = localStorage.getItem('pe-bkr-' + kulcs); return s ? JSON.parse(s) : null; } catch (e) { return null; } }
function letolt(nev, szoveg, mime = 'text/plain;charset=utf-8') { const b = new Blob([szoveg], {type: mime});
  const a = el('a', {href: URL.createObjectURL(b), download: nev}); document.body.append(a); a.click(); a.remove(); }
const SZINEK = ['#285780', '#E07B39', '#3E8E63', '#B83A3A', '#7A5C99', '#D9A520', '#4F7FAD', '#6B7280'];
function tengelyLepes(min, max, n = 5) { const r = max - min; if (r <= 0) return [min];
  const nyers = r / n, p = Math.pow(10, Math.floor(Math.log10(nyers))), f = nyers / p;
  const l = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p; const t = []; for (let v = Math.ceil(min / l) * l; v <= max + 1e-12 * r; v += l) t.push(+v.toPrecision(12)); return t; }
// Vonaldiagram SVG-ben. series: [{nev, szin, pontok:[[x,y],...], szaggatott}]
function vonaldiagram(tarolo, o) {
  const W = o.szel || 640, H = o.mag || 300, m = {b: 64, j: 14, f: 14, a: 44};
  const pts = o.sorok.flatMap(s => s.pontok).filter(p => isFinite(p[0]) && isFinite(p[1]) && (!o.logy || p[1] > 0));
  if (!pts.length) { tarolo.innerHTML = '<p class="megj">Nincs megjeleníthető adat.</p>'; return; }
  let xmin = o.xmin ?? Math.min(...pts.map(p => p[0])), xmax = o.xmax ?? Math.max(...pts.map(p => p[0]));
  let ymin = o.ymin ?? Math.min(...pts.map(p => p[1])), ymax = o.ymax ?? Math.max(...pts.map(p => p[1]));
  if (o.logy) { ymin = Math.log10(ymin); ymax = Math.log10(ymax); ymin = Math.floor(ymin); ymax = Math.ceil(ymax); if (ymax === ymin) ymax++; }
  else { if (ymax === ymin) { ymax += 1; } if (o.ymin === undefined && ymin > 0 && ymin < 0.3 * ymax) ymin = 0; }
  const X = x => m.b + (x - xmin) / (xmax - xmin) * (W - m.b - m.j);
  const Y = y => { const v = o.logy ? Math.log10(y) : y; return H - m.a - (v - ymin) / (ymax - ymin) * (H - m.a - m.f); };
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px" role="img">`;
  const xt = tengelyLepes(xmin, xmax, 6);
  const yt = o.logy ? Array.from({length: ymax - ymin + 1}, (_, i) => ymin + i) : tengelyLepes(ymin, ymax, 5);
  for (const t of yt) { const yy = o.logy ? H - m.a - (t - ymin) / (ymax - ymin) * (H - m.a - m.f) : Y(t);
    s += `<line x1="${m.b}" x2="${W - m.j}" y1="${yy}" y2="${yy}" stroke="#e6e9ee"/><text x="${m.b - 6}" y="${yy + 4}" font-size="11" text-anchor="end" fill="#4b5563">${o.logy ? '10' + String(t).split('').map(c => SUP[c]).join('') : fmt(t, 3)}</text>`; }
  for (const t of xt) { const xx = X(t); s += `<line x1="${xx}" x2="${xx}" y1="${m.f}" y2="${H - m.a}" stroke="#f0f2f5"/><text x="${xx}" y="${H - m.a + 15}" font-size="11" text-anchor="middle" fill="#4b5563">${fmt(t, 3)}</text>`; }
  s += `<line x1="${m.b}" x2="${W - m.j}" y1="${H - m.a}" y2="${H - m.a}" stroke="#1B3A57"/><line x1="${m.b}" x2="${m.b}" y1="${m.f}" y2="${H - m.a}" stroke="#1B3A57"/>`;
  s += `<text x="${(W + m.b) / 2}" y="${H - 8}" font-size="12" text-anchor="middle" fill="#1B3A57">${o.xcimke || ''}</text>`;
  s += `<text transform="translate(14,${(H - m.a) / 2}) rotate(-90)" font-size="12" text-anchor="middle" fill="#1B3A57">${o.ycimke || ''}</text>`;
  o.sorok.forEach((sr, i) => { const szin = sr.szin || SZINEK[i % SZINEK.length];
    const d = sr.pontok.filter(p => isFinite(p[1]) && (!o.logy || p[1] > 0)).map((p, k) => (k ? 'L' : 'M') + X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1)).join('');
    s += `<path d="${d}" fill="none" stroke="${szin}" stroke-width="${sr.vastag || 2}" ${sr.szaggatott ? 'stroke-dasharray="6 4"' : ''}/>`; });
  let ly = m.f + 4; o.sorok.forEach((sr, i) => { if (!sr.nev) return; const szin = sr.szin || SZINEK[i % SZINEK.length];
    s += `<line x1="${W - m.j - 190}" x2="${W - m.j - 170}" y1="${ly + 6}" y2="${ly + 6}" stroke="${szin}" stroke-width="2.5" ${sr.szaggatott ? 'stroke-dasharray="6 4"' : ''}/><text x="${W - m.j - 165}" y="${ly + 10}" font-size="11" fill="#1F2933">${sr.nev}</text>`; ly += 16; });
  tarolo.innerHTML = s + '</svg>';
}
// Vízszintes oszlopdiagram. adatok: [{nev, ertek, szin}], log: logaritmikus tengely
function oszlopdiagram(tarolo, adatok, o = {}) {
  const W = o.szel || 640, sor = 26, m = {b: o.balmargo || 190, j: 70, f: 8}; const H = m.f * 2 + sor * adatok.length + 22;
  const ert = adatok.map(a => a.ertek).filter(v => v > 0); if (!ert.length) { tarolo.innerHTML = ''; return; }
  let lo = o.log ? Math.floor(Math.log10(Math.min(...ert))) : 0, hi = o.log ? Math.ceil(Math.log10(Math.max(...ert))) : Math.max(...ert) * 1.05;
  if (o.log && hi === lo) hi++;
  const X = v => m.b + ((o.log ? Math.log10(v) : v) - lo) / (hi - lo) * (W - m.b - m.j);
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px">`;
  adatok.forEach((a, i) => { const y = m.f + i * sor; const x1 = X(Math.max(a.ertek, o.log ? Math.pow(10, lo) : 0));
    s += `<text x="${m.b - 6}" y="${y + 16}" font-size="11.5" text-anchor="end" fill="#1F2933">${a.nev}</text>`;
    s += `<rect x="${m.b}" y="${y + 4}" width="${Math.max(0, x1 - m.b)}" height="${sor - 8}" fill="${a.szin || '#285780'}" rx="2"/>`;
    s += `<text x="${x1 + 5}" y="${y + 16}" font-size="11" fill="#1F2933">${a.felirat ?? fmt(a.ertek)}</text>`; });
  if (o.vonal !== undefined) { const xv = X(o.vonal); s += `<line x1="${xv}" x2="${xv}" y1="${m.f}" y2="${H - 20}" stroke="#B83A3A" stroke-width="1.5" stroke-dasharray="5 3"/><text x="${xv}" y="${H - 6}" font-size="11" text-anchor="middle" fill="#B83A3A">${o.vonalcimke || ''}</text>`; }
  tarolo.innerHTML = s + '</svg>';
}
function osszegzes(ertekek) { return ertekek.reduce((a, b) => a + b, 0); }
