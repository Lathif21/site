/* Catalog behaviour: facets, search, sort, active-filter chips, empty state.
   All state lives in the URL query string so a filtered view is shareable and
   the back button works — see 02-catalog-page.md §5. */

const grid   = document.getElementById('grid');
const empty  = document.getElementById('empty');
const countEl= document.getElementById('count');
const chipsEl= document.getElementById('activeChips');
const form   = document.getElementById('filterForm');
const search = document.getElementById('search');
const sortEl = document.getElementById('sort');
const filters= document.getElementById('filters');

const state = { type: [], colour: [], difficulty: [], size: [], lead: [], q: '', sort: 'featured' };

/* ---------- icons ---------- */
const icoGauge = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-4"/></svg>`;
const icoClock = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/></svg>`;

/* ---------- build colour facet ---------- */
const colourFacet = document.getElementById('colourFacet');
Object.entries(COLOURS).forEach(([slug, c]) => {
  const n = PRODUCTS.filter(p => p.colour === slug).length;
  if (!n) return;
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'chip'; b.dataset.colour = slug;
  b.setAttribute('aria-pressed', 'false');
  b.innerHTML = `<span class="sw" style="background:${c.hex};pointer-events:none;width:16px;height:16px"></span>${c.label}`;
  b.addEventListener('click', () => {
    toggle(state.colour, slug);
    b.setAttribute('aria-pressed', String(state.colour.includes(slug)));
    apply();
  });
  colourFacet.appendChild(b);
});

function toggle(arr, v) {
  const i = arr.indexOf(v);
  if (i > -1) arr.splice(i, 1); else arr.push(v);
}

/* ---------- card ---------- */
function card(p) {
  const sibs = siblings(p);
  const swatches = sibs.length > 1
    ? `<div style="display:flex;gap:6px;position:relative;z-index:2">
         ${sibs.map(s => `<a class="sw" href="product.html?id=${s.id}" title="${COLOURS[s.colour].label}"
              style="background:${COLOURS[s.colour].hex}" ${s.id === p.id ? 'aria-current="true"' : ''}
              aria-label="${p.name.replace(/ \S+$/, '')} in ${COLOURS[s.colour].label}"></a>`).join('')}
       </div>` : '';

  /* Hover crossfades to the next colourway of the same model. There is no
     product footage, and this does the job a hover-video would: it shows the
     range without a click. Decorative, so alt="" and aria-hidden. */
  const next = sibs.length > 1 ? sibs[(sibs.indexOf(p) + 1) % sibs.length] : null;
  const swapImg = next
    ? `<img class="swap" src="${next.img}" alt="" aria-hidden="true" loading="lazy">`
    : '';

  const el = document.createElement('article');
  el.className = 'card';
  el.style.position = 'relative';
  el.innerHTML = `
    <div class="card-media">
      <img class="base" src="${p.img}" alt="${p.name} DIY-pakket" loading="lazy">
      ${swapImg}
      ${sibs.length > 1 ? `<span class="badge card-flag">${sibs.length} kleuren</span>` : ''}
    </div>
    <div class="card-body">
      <div>
        <p class="t-label subtle" style="margin:0 0 6px;letter-spacing:.06em">${p.typeLabel}</p>
        <h3 class="t-title"><a class="stretched" href="product.html?id=${p.id}">${p.name}</a></h3>
      </div>
      <div class="card-meta">
        <span class="badge badge-${p.difficulty.toLowerCase()}">${icoGauge}${p.difficulty}</span>
        <span class="badge">${icoClock}${p.lead} dagen</span>
      </div>
      <div class="card-foot">
        <span class="t-price">${money(p.price)}</span>
        ${swatches}
      </div>
    </div>`;
  return el;
}

/* ---------- filter + render ---------- */
/* One predicate per facet so a single facet can be left out of the pass — the
   facet counts below need an "everything except me" view of the catalogue. */
const FACETS = {
  type:       (p, v) => p.type === v,
  colour:     (p, v) => p.colour === v,
  difficulty: (p, v) => p.difficulty === v,
  size:       (p, v) => p.size === v,
  lead:       (p, v) => String(p.lead) === v
};
const FACET_KEYS = Object.keys(FACETS);

function matchesQuery(p) {
  if (!state.q) return true;
  const hay = (p.name + ' ' + p.typeLabel + ' ' + COLOURS[p.colour].label).toLowerCase();
  return hay.includes(state.q.toLowerCase());
}

/* Passes every active facet except `skip`; values within one facet OR together. */
function matchesExcept(p, skip) {
  for (const k in FACETS) {
    if (k === skip || !state[k].length) continue;
    if (!state[k].some(v => FACETS[k](p, v))) return false;
  }
  return matchesQuery(p);
}

function matches(p) { return matchesExcept(p, null); }

const sorters = {
  featured:  (a, b) => PRODUCTS.indexOf(a) - PRODUCTS.indexOf(b),
  'price-asc':  (a, b) => a.price - b.price,
  'price-desc': (a, b) => b.price - a.price,
  name: (a, b) => a.name.localeCompare(b.name),
  lead: (a, b) => a.lead - b.lead || a.price - b.price
};

function renderChips() {
  chipsEl.innerHTML = '';
  const add = (label, clear) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'chip-active';
    b.innerHTML = `${label}<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>`;
    b.setAttribute('aria-label', `Filter ${label} verwijderen`);
    b.addEventListener('click', () => { clear(); syncInputs(); apply(); });
    chipsEl.appendChild(b);
  };
  state.type.forEach(v       => add(v === "table" ? "Tafels" : "Tapijten", () => toggle(state.type, v)));
  state.colour.forEach(v     => add(COLOURS[v].label,        () => toggle(state.colour, v)));
  state.difficulty.forEach(v => add(v,                       () => toggle(state.difficulty, v)));
  state.size.forEach(v       => add(v,                       () => toggle(state.size, v)));
  state.lead.forEach(v       => add(`levering in ${v} dagen`, () => toggle(state.lead, v)));
  if (state.q) add(`“${state.q}”`, () => { state.q = ''; search.value = ''; });
}

function syncInputs() {
  form.querySelectorAll('input[type=checkbox]').forEach(i => {
    i.checked = state[i.name] && state[i.name].includes(i.value);
  });
  colourFacet.querySelectorAll('.chip').forEach(c => {
    c.setAttribute('aria-pressed', String(state.colour.includes(c.dataset.colour)));
  });
}

/* ---------- facet counts ----------
   Each option reports how many kits it would leave *given the other facets*,
   so Type / Difficulty / Carpet size / Delivery react to one another as you
   tick. The facet is excluded from its own count because its values OR
   together. An option nothing can reach any more is dimmed and disabled —
   unless it is the ticked one, which has to stay clickable to untick. */
const facetInputs = [...form.querySelectorAll('input[type=checkbox]')];

function updateCounts() {
  const pools = {};
  facetInputs.forEach(i => {
    const pool = pools[i.name] || (pools[i.name] = PRODUCTS.filter(p => matchesExcept(p, i.name)));
    const n = pool.filter(p => FACETS[i.name](p, i.value)).length;
    const row = i.closest('.check');
    row.querySelector('.count').textContent = n;
    row.classList.toggle('is-zero', n === 0 && !i.checked);
    i.disabled = n === 0 && !i.checked;
  });
}

/* Sheet chrome: how many filters are on (badge on the toggle, readable without
   opening the sheet) and what ticking them yields (the foot button). */
function updateSheetChrome(n) {
  const on = FACET_KEYS.reduce((sum, k) => sum + state[k].length, 0);
  ftPill.textContent = on;
  ftPill.hidden = on === 0;
  applyBtn.textContent = n ? `Toon ${n} ${n === 1 ? 'pakket' : 'pakketten'}` : 'Geen pakketten';
  applyBtn.disabled = n === 0;
}

function writeUrl() {
  const q = new URLSearchParams();
  FACET_KEYS.forEach(k => { if (state[k].length) q.set(k, state[k].join(',')); });
  if (state.q) q.set('q', state.q);
  if (state.sort !== 'featured') q.set('sort', state.sort);
  const s = q.toString();
  history.replaceState(null, '', s ? '?' + s : location.pathname);
}

function readUrl() {
  const q = new URLSearchParams(location.search);
  FACET_KEYS.forEach(k => {
    if (q.get(k)) state[k] = q.get(k).split(',');
  });
  state.q = q.get('q') || '';
  state.sort = q.get('sort') || 'featured';
  search.value = state.q;
  sortEl.value = state.sort;
}

function apply() {
  const list = PRODUCTS.filter(matches).sort(sorters[state.sort]);
  grid.innerHTML = '';
  list.forEach(p => grid.appendChild(card(p)));
  countEl.textContent = `${list.length} ${list.length === 1 ? "pakket" : "pakketten"}`;
  empty.hidden = list.length > 0;
  grid.hidden = list.length === 0;
  renderChips();
  updateCounts();
  updateSheetChrome(list.length);
  writeUrl();
}

/* ---------- wiring ---------- */
form.addEventListener('change', e => {
  const i = e.target;
  if (i.type !== 'checkbox') return;
  toggle(state[i.name], i.value);
  apply();
});
sortEl.addEventListener('change', () => { state.sort = sortEl.value; apply(); });

let t;
search.addEventListener('input', () => {
  clearTimeout(t);
  t = setTimeout(() => { state.q = search.value.trim(); apply(); }, 180);
});

function clearAll() {
  FACET_KEYS.forEach(k => state[k] = []);
  state.q = ''; search.value = '';
  syncInputs(); apply();
}
document.getElementById('clearAll').addEventListener('click', clearAll);
document.getElementById('clearAll2').addEventListener('click', clearAll);

document.querySelectorAll('.catTile').forEach(tile => {
  tile.addEventListener('click', () => {
    const c = tile.dataset.cat;
    state.type = c === 'all' ? [] : [c];
    syncInputs(); apply();
    document.getElementById('catalog').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

/* ---------- mobile filter sheet ----------
   Below 1024px the aside is a modal bottom sheet. The results keep their
   scroll position behind it, and the foot button carries the live result
   count so the outcome of a tick is visible without closing anything. */
const ft       = document.getElementById('filterToggle');
const ftPill   = document.getElementById('filterCount');
const backdrop = document.getElementById('filterBackdrop');
const applyBtn = document.getElementById('filterApply');
const closeBtn = document.getElementById('filterClose');
const mqMobile = window.matchMedia('(max-width:1023px)');

/* MediaQueryList.addEventListener is Safari 14+; addListener is the fallback. */
function onMediaChange(mq, fn) {
  if (!mq) return;
  if (mq.addEventListener) mq.addEventListener('change', fn);
  else if (mq.addListener) mq.addListener(fn);
}

const sheetIsOpen = () => !filters.hidden;

function openSheet() {
  filters.hidden = backdrop.hidden = false;
  filters.setAttribute('role', 'dialog');
  filters.setAttribute('aria-modal', 'true');
  document.body.classList.add('filters-open');
  requestAnimationFrame(() => {
    filters.classList.add('open');
    backdrop.classList.add('open');
  });
  ft.setAttribute('aria-expanded', 'true');
  closeBtn.focus();
}

function closeSheet(refocus = true) {
  filters.classList.remove('open');
  backdrop.classList.remove('open');
  document.body.classList.remove('filters-open');
  filters.removeAttribute('role');
  filters.removeAttribute('aria-modal');
  ft.setAttribute('aria-expanded', 'false');
  /* wait out the slide-down before pulling it from the a11y tree; the timeout
     covers reduced-motion and any browser that skips the transition */
  const settle = () => {
    backdrop.hidden = true;
    if (mqMobile.matches) filters.hidden = true;   // desktop must never hide it
  };
  filters.addEventListener('transitionend', settle, { once: true });
  setTimeout(settle, 400);
  if (refocus) ft.focus();
}

if (mqMobile.matches) filters.hidden = true;

ft.addEventListener('click', () => (sheetIsOpen() ? closeSheet() : openSheet()));
closeBtn.addEventListener('click', () => closeSheet());
backdrop.addEventListener('click', () => closeSheet());
applyBtn.addEventListener('click', () => {
  closeSheet(false);
  document.getElementById('catalog').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && mqMobile.matches && sheetIsOpen()) closeSheet();
});

/* crossing the breakpoint with the sheet open would leave the body locked.
   Safari < 14 exposes matchMedia but not addEventListener on MediaQueryList; a
   throw here would abort the rest of this file, and the initial apply() at the
   bottom is what paints the grid — so the catalogue would come up empty. */
onMediaChange(mqMobile, e => {
  if (e.matches) { filters.hidden = true; return; }
  filters.classList.remove('open');
  backdrop.classList.remove('open');
  backdrop.hidden = true;
  document.body.classList.remove('filters-open');
  filters.removeAttribute('role');
  filters.removeAttribute('aria-modal');
  ft.setAttribute('aria-expanded', 'false');
  filters.hidden = false;
});

/* cart badge shared with the PDP */
const cartCount = document.getElementById('cartCount');
function readCart() { try { return +(sessionStorage.getItem('cart') || 0); } catch { return 0; } }
cartCount.textContent = readCart();
document.getElementById('cartBtn').setAttribute('aria-label', `Winkelmandje, ${readCart()} artikelen`);

readUrl();
syncInputs();
apply();
