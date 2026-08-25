/* Atelier DIY — prototype catalogue data.
   Mirrors the live staging catalogue (34 listings), minus the "TEST Title"
   placeholder which is a data defect, not a product. See 02-catalog-page.md §1.
   Slugs, ids and image names stay English — only customer-facing copy is Dutch. */

const COLOURS = {
  'off-white':  { label: 'Off-White',  hex: '#efeae2' },
  'oker':       { label: 'Oker',       hex: '#bfa24c' },
  'sand':       { label: 'Zand',       hex: '#d8cdbb' },
  'terra':      { label: 'Terra',      hex: '#b5573e' },
  'deep-black': { label: 'Diepzwart',  hex: '#2a2a28' },
  'brown':      { label: 'Bruin',      hex: '#6b4a33' },
  'white':      { label: 'Wit',        hex: '#f2efe9' }
};

const MODELS = ['HB', 'AV', 'RV', 'SH', 'EH'];
const TABLE_COLOURS = ['off-white', 'oker', 'sand', 'terra', 'deep-black'];

const PRODUCTS = [];

/* — Tapijten — */
const carpetSizes = [
  { size: '3m²', price: 399.99 },
  { size: '4m²', price: 549.99 },
  { size: '6m²', price: 749.99 },
  { size: '9m²', price: 999.99 }
];
[['brown', 'Bruin'], ['white', 'Wit']].forEach(([slug, label]) => {
  carpetSizes.forEach(({ size, price }) => {
    const n = size.replace('m²', '');
    PRODUCTS.push({
      id: `${slug}-carpet-${n}`,
      name: `${label} Tapijt ${size}`,
      type: 'carpet',
      typeLabel: 'Tapijt',
      typePlural: 'Tapijten',
      colour: slug,
      size,
      price,
      difficulty: slug === 'brown' && (n === '3' || n === '4') ? 'Gevorderd' : 'Basis',
      lead: n === '4' && slug === 'brown' ? 5 : 3,
      img: `img/${slug}-carpet-${n}.jpg`,
      dims: { width: `${n === '3' ? 150 : n === '4' ? 200 : n === '6' ? 240 : 300}cm`,
              length: `${n === '3' ? 200 : n === '4' ? 200 : n === '6' ? 250 : 300}cm` },
      blurb: `Onze DIY-tapijten in ${label.toLowerCase()} brengen warmte en natuurlijke elegantie in je interieur. De zachte, aardse tint past even goed in een moderne als in een landelijke woning en zorgt meteen voor een serene sfeer.`,
      body: `Dit tapijt heeft een royale afmeting van ${size}, ideaal voor grotere ruimtes of als blikvanger in een kleinere kamer. Alles om je eigen tapijt te maken zit in het pakket, van hoogwaardige materialen tot een duidelijke handleiding die je stap voor stap begeleidt. Kwaliteit en duurzaamheid — dit tapijt gaat jarenlang mee. Eenvoudig te maken: ook zonder ervaring maak je dit tapijt helemaal zelf.`
    });
  });
});

/* — Tafels — */
const slugMap = { 'off-white': 'offwhite', 'deep-black': 'deepblack', oker: 'oker', sand: 'sand', terra: 'terra' };
MODELS.forEach(model => {
  TABLE_COLOURS.forEach(colour => {
    PRODUCTS.push({
      id: `model-${model.toLowerCase()}-${colour}`,
      name: `Model ${model} ${COLOURS[colour].label}`,
      type: 'table',
      typeLabel: 'Tafel',
      typePlural: 'Tafels',
      model,
      colour,
      size: null,
      price: 399.99,
      difficulty: 'Gevorderd',
      // the live catalogue shows Model SH Diepzwart at 5 days; every other table is 3
      lead: (model === 'SH' && colour === 'deep-black') ? 5 : 3,
      img: `img/${model.toLowerCase()}-${slugMap[colour]}.jpg`,
      dims: { height: '38cm', width: '110cm', length: '70cm' },
      blurb: `Model ${model} is een handafgewerkte salontafel in Mortex met een zachte, organische vorm. Elk exemplaar werk je zelf af, dus geen twee tafels zijn identiek.`,
      body: `Het pakket bevat de gevormde kern, het Mortex-systeem, pigmenten in ${COLOURS[colour].label} en al het gereedschap dat je nodig hebt om de tafel af te werken. Volg de stap-voor-stap handleiding en de videotutorial, van de eerste laag tot de finale verzegeling. Reken op ongeveer een weekend werk, verspreid over drie dagen uitharden.`
    });
  });
});

/* Sibling colourways for a given table model */
function siblings(p) {
  if (p.type !== 'table') return [];
  return PRODUCTS.filter(x => x.type === 'table' && x.model === p.model);
}
function sizeSiblings(p) {
  if (p.type !== 'carpet') return [];
  return PRODUCTS.filter(x => x.type === 'carpet' && x.colour === p.colour);
}
function money(n) {
  return '€ ' + n.toFixed(2).replace('.', ',');
}
function byId(id) {
  return PRODUCTS.find(p => p.id === id);
}
