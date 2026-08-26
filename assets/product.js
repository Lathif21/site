/* PDP behaviour. Reads ?id= so cards link through and the page is shareable. */

const params = new URLSearchParams(location.search);
const p = byId(params.get('id')) || PRODUCTS[9];

const $ = id => document.getElementById(id);

/* ---------- head / breadcrumb ---------- */
document.title = `${p.name} — Atelier DIY`;
$("bcType").textContent = p.typePlural;
$('bcType').href = `webshop.html?type=${p.type}`;
$('bcName').textContent = p.name;
$('eyebrow').textContent = p.typeLabel;
$('title').textContent = p.name;
$('price').textContent = money(p.price);
$('leadInline').textContent = p.lead;
$('blurb').textContent = p.blurb;

/* ---------- gallery ----------
   The live PDP shows a hero plus three thumbnails. We only have one real
   asset per product, so the prototype pads with the sibling colourways —
   which is honest about what exists and still exercises the interaction. */
const gallery = [p.img, ...siblings(p).filter(s => s.id !== p.id).slice(0, 3).map(s => s.img)];
if (gallery.length === 1) {
  gallery.push(...PRODUCTS.filter(x => x.type === p.type && x.id !== p.id).slice(0, 3).map(x => x.img));
}
const hero = $('hero');
hero.src = gallery[0];
hero.alt = `${p.name} DIY-pakket`;

const thumbs = $('thumbs');
gallery.forEach((src, i) => {
  const b = document.createElement('button');
  b.className = 'thumb'; b.type = 'button';
  b.setAttribute('aria-current', String(i === 0));
  b.setAttribute('aria-label', `Toon afbeelding ${i + 1} van ${gallery.length}`);
  b.innerHTML = `<img src="${src}" alt="" aria-hidden="true" style="width:100%;height:100%;object-fit:cover" loading="lazy">`;
  b.addEventListener('click', () => {
    hero.src = src;
    thumbs.querySelectorAll('.thumb').forEach(t => t.setAttribute('aria-current', 'false'));
    b.setAttribute('aria-current', 'true');
  });
  thumbs.appendChild(b);
});

/* ---------- variants ----------
   The live shop lists every colourway as a separate product, so there is no
   selector at all. Here the sibling listings are surfaced as a variant picker
   without changing the data model: each swatch is a link to that product.
   See 03-product-page.md §4. */
const wrap = $('variantWrap');
const sibs = p.type === 'table' ? siblings(p) : sizeSiblings(p);

if (sibs.length > 1) {
  const isTable = p.type === 'table';
  const heading = isTable ? "Kleur" : "Maat";
  const current = isTable ? COLOURS[p.colour].label : p.size;

  wrap.innerHTML = `
    <p class="t-label" style="margin:0 0 var(--sp-3)">
      ${heading}: <span style="font-weight:400;text-transform:none;letter-spacing:0" class="muted" id="vLabel">${current}</span>
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:${isTable ? '10px' : 'var(--sp-2)'}" id="vList"></div>`;

  const list = $('vList');
  sibs.forEach(s => {
    const on = s.id === p.id;
    const a = document.createElement('a');
    a.href = `product.html?id=${s.id}`;
    if (isTable) {
      a.className = 'sw sw-lg';
      a.style.background = COLOURS[s.colour].hex;
      a.title = COLOURS[s.colour].label;
      a.setAttribute('aria-label', `${COLOURS[s.colour].label} — ${money(s.price)}`);
      if (on) a.setAttribute('aria-current', 'true');
      a.addEventListener('mouseenter', () => $('vLabel').textContent = COLOURS[s.colour].label);
      a.addEventListener('mouseleave', () => $('vLabel').textContent = current);
    } else {
      a.className = 'chip';
      a.style.textDecoration = 'none';
      a.textContent = s.size;
      if (on) a.setAttribute('aria-current', 'true');
      a.setAttribute('aria-label', `${s.size} — ${money(s.price)}`);
    }
    list.appendChild(a);
  });
}

/* ---------- specs ---------- */
const specs = $('specs');
const rows = [
  ["Moeilijkheidsgraad", p.difficulty],
  ["Levertijd", `${p.lead} dagen`],
  p.dims.height ? ["Hoogte", p.dims.height] : null,
  ["Breedte", p.dims.width],
  ["Lengte", p.dims.length],
  ["Kleur", COLOURS[p.colour].label],
  ["Afwerking", "Zelf af te werken"]
].filter(Boolean);

specs.innerHTML = rows.map(([k, v]) => `
  <div class="spec-row">
    <dt>${k}</dt>
    <dd>${k === "Kleur"
      ? `<span style="display:inline-flex;align-items:center;gap:8px">
           <span style="width:16px;height:16px;border-radius:999px;background:${COLOURS[p.colour].hex};border:1px solid rgba(28,28,28,.16)"></span>${v}
         </span>`
      : v}</dd>
  </div>`).join('');

/* ---------- description with read-more ---------- */
const desc = $('desc');
desc.innerHTML = `
  <p style="margin:0 0 1em">${p.blurb}</p>
  <div id="more" style="max-height:0;overflow:hidden;transition:max-height var(--dur-slow) var(--ease-out)">
    <p style="margin:0 0 1em">${p.body}</p>
  </div>
  <button class="btn btn-ghost" id="moreBtn" aria-expanded="false" aria-controls="more" style="margin-top:4px">Lees meer</button>`;

$('moreBtn').addEventListener('click', () => {
  const m = $('more'), b = $('moreBtn');
  const open = b.getAttribute('aria-expanded') === 'true';
  b.setAttribute('aria-expanded', String(!open));
  m.style.maxHeight = open ? '0' : m.scrollHeight + 'px';
  b.textContent = open ? "Lees meer" : "Lees minder";
});

/* ---------- related ---------- */
const icoGauge = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-4"/></svg>`;
const icoClock = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/></svg>`;

const related = PRODUCTS
  .filter(x => x.type === p.type && x.id !== p.id && (p.type !== 'table' || x.model !== p.model))
  .slice(0, 4);
$('relTitle').textContent = p.type === "table" ? "Andere tafelmodellen" : "Andere tapijten";

$('related').innerHTML = related.map(r => `
  <article class="card" style="position:relative">
    <div class="card-media"><img src="${r.img}" alt="${r.name} DIY-pakket" loading="lazy" width="800" height="800"></div>
    <div class="card-body">
      <div>
        <p class="t-label subtle" style="margin:0 0 6px;letter-spacing:.06em">${r.typeLabel}</p>
        <h3 class="t-title"><a class="stretched" href="product.html?id=${r.id}">${r.name}</a></h3>
      </div>
      <div class="card-meta">
        <span class="badge badge-${r.difficulty.toLowerCase()}">${icoGauge}${r.difficulty}</span>
        <span class="badge">${icoClock}${r.lead} dagen</span>
      </div>
      <div class="card-foot"><span class="t-price">${money(r.price)}</span></div>
    </div>
  </article>`).join('');

/* ---------- quantity ---------- */
const qty = $('qty');
const clamp = () => { qty.value = Math.min(20, Math.max(1, parseInt(qty.value, 10) || 1)); };
$('minus').addEventListener('click', () => { qty.value = Math.max(1, +qty.value - 1); });
$('plus').addEventListener('click',  () => { qty.value = Math.min(20, +qty.value + 1); });
qty.addEventListener('change', clamp);

/* ---------- cart ---------- */
function readCart() { try { return +(sessionStorage.getItem('cart') || 0); } catch { return 0; } }
function writeCart(n) { try { sessionStorage.setItem('cart', n); } catch {} }
$('cartCount').textContent = readCart();

const toast = $('toast');
let tt;
function addToCart() {
  const n = readCart() + (+qty.value);
  writeCart(n);
  $('cartCount').textContent = n;
  toast.textContent = `${qty.value} × ${p.name} toegevoegd aan je winkelmandje`;
  toast.classList.add('show');
  clearTimeout(tt);
  tt = setTimeout(() => toast.classList.remove('show'), 2600);
}
$('add').addEventListener('click', addToCart);
$('sbAdd').addEventListener('click', addToCart);

/* ---------- sticky bar ---------- */
$('sbName').textContent = p.name;
$('sbPrice').textContent = money(p.price);
