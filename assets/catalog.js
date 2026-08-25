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

  const el = document.createElement('article');
  el.className = 'card';
  el.style.position = 'relative';
  el.innerHTML = `
    <div class="card-media">
      <img src="${p.img}" alt="${p.name} DIY kit" loading="lazy" width="800" height="800">
      ${sibs.length > 1 ? `<span class="badge card-flag">${sibs.length} colours</span>` : ''}
    </div>
    <div class="card-body">
      <div>
        <p class="t-label subtle" style="margin:0 0 6px;letter-spacing:.06em">${p.typeLabel}</p>
        <h3 class="t-title"><a class="stretched" href="product.html?id=${p.id}">${p.name}</a></h3>
      </div>
      <div class="card-meta">
        <span class="badge badge-${p.difficulty.toLowerCase()}">${icoGauge}${p.difficulty}</span>
        <span class="badge">${icoClock}${p.lead} days</span>
      </div>
      <div class="card-foot">
        <span class="t-price">${money(p.price)}</span>
        ${swatches}
      </div>
    </div>`;
  return el;
}

/* ---------- filter + render ---------- */
function matches(p) {
  if (state.type.length       && !state.type.includes(p.type))             return false;
  if (state.colour.length     && !state.colour.includes(p.colour))         return false;
  if (state.difficulty.length && !state.difficulty.includes(p.difficulty)) return false;
  if (state.size.length       && !state.size.includes(p.size))             return false;
  if (state.lead.length       && !state.lead.includes(String(p.lead)))     return false;
  if (state.q) {
    const hay = (p.name + ' ' + p.typeLabel + ' ' + COLOURS[p.colour].label).toLowerCase();
    if (!hay.includes(state.q.toLowerCase())) return false;
  }
  return true;
}

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
    b.setAttribute('aria-label', `Remove filter ${label}`);
    b.addEventListener('click', () => { clear(); syncInputs(); apply(); });
    chipsEl.appendChild(b);
  };
  state.type.forEach(v       => add(v === 'table' ? 'Tables' : 'Carpets', () => toggle(state.type, v)));
  state.colour.forEach(v     => add(COLOURS[v].label,        () => toggle(state.colour, v)));
  state.difficulty.forEach(v => add(v,                       () => toggle(state.difficulty, v)));
  state.size.forEach(v       => add(v,                       () => toggle(state.size, v)));
  state.lead.forEach(v       => add(`${v}-day lead time`,    () => toggle(state.lead, v)));
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

function writeUrl() {
  const q = new URLSearchParams();
  ['type','colour','difficulty','size','lead'].forEach(k => { if (state[k].length) q.set(k, state[k].join(',')); });
  if (state.q) q.set('q', state.q);
  if (state.sort !== 'featured') q.set('sort', state.sort);
  const s = q.toString();
  history.replaceState(null, '', s ? '?' + s : location.pathname);
}

function readUrl() {
  const q = new URLSearchParams(location.search);
  ['type','colour','difficulty','size','lead'].forEach(k => {
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
  countEl.textContent = `${list.length} ${list.length === 1 ? 'kit' : 'kits'}`;
  empty.hidden = list.length > 0;
  grid.hidden = list.length === 0;
  renderChips();
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
  ['type','colour','difficulty','size','lead'].forEach(k => state[k] = []);
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

const ft = document.getElementById('filterToggle');
if (window.matchMedia('(max-width:1023px)').matches) filters.hidden = true;
ft.addEventListener('click', () => {
  filters.hidden = !filters.hidden;
  ft.setAttribute('aria-expanded', String(!filters.hidden));
});

/* cart badge shared with the PDP */
const cartCount = document.getElementById('cartCount');
function readCart() { try { return +(sessionStorage.getItem('cart') || 0); } catch { return 0; } }
cartCount.textContent = readCart();
document.getElementById('cartBtn').setAttribute('aria-label', `Cart, ${readCart()} items`);

readUrl();
syncInputs();
apply();
