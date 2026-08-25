/* Atelier DIY — prototype catalogue data.
   Mirrors the live staging catalogue (34 listings), minus the "TEST Title"
   placeholder which is a data defect, not a product. See 02-catalog-page.md §1. */

const COLOURS = {
  'off-white':  { label: 'Off-White',  hex: '#efeae2' },
  'oker':       { label: 'Oker',       hex: '#bfa24c' },
  'sand':       { label: 'Sand',       hex: '#d8cdbb' },
  'terra':      { label: 'Terra',      hex: '#b5573e' },
  'deep-black': { label: 'Deep Black', hex: '#2a2a28' },
  'brown':      { label: 'Brown',      hex: '#6b4a33' },
  'white':      { label: 'White',      hex: '#f2efe9' }
};

const MODELS = ['HB', 'AV', 'RV', 'SH', 'EH'];
const TABLE_COLOURS = ['off-white', 'oker', 'sand', 'terra', 'deep-black'];

const PRODUCTS = [];

/* — Carpets — */
const carpetSizes = [
  { size: '3m²', price: 399.99 },
  { size: '4m²', price: 549.99 },
  { size: '6m²', price: 749.99 },
  { size: '9m²', price: 999.99 }
];
[['brown', 'Brown'], ['white', 'White']].forEach(([slug, label]) => {
  carpetSizes.forEach(({ size, price }) => {
    const n = size.replace('m²', '');
    PRODUCTS.push({
      id: `${slug}-carpet-${n}`,
      name: `${label} Carpet ${size}`,
      type: 'carpet',
      typeLabel: 'Carpet',
      colour: slug,
      size,
      price,
      difficulty: slug === 'brown' && (n === '3' || n === '4') ? 'Advanced' : 'Basis',
      lead: n === '4' && slug === 'brown' ? 5 : 3,
      img: `img/${slug}-carpet-${n}.jpg`,
      dims: { width: `${n === '3' ? 150 : n === '4' ? 200 : n === '6' ? 240 : 300}cm`,
              length: `${n === '3' ? 200 : n === '4' ? 200 : n === '6' ? 250 : 300}cm` },
      blurb: `Our DIY ${label.toLowerCase()} rugs bring warmth and natural elegance to your home. The soft, earthy tone fits modern and rustic interiors alike, and instantly adds a serene atmosphere.`,
      body: `This rug has a generous size of ${size}, ideal for larger spaces or to make a statement in a smaller room. Everything you need to make your own rug is included, from high-quality materials to clear instructions that guide you step by step. Quality and durability — this rug is designed to last for years. Easy to make: even with no experience, you can make this rug yourself.`
    });
  });
});

/* — Tables — */
const slugMap = { 'off-white': 'offwhite', 'deep-black': 'deepblack', oker: 'oker', sand: 'sand', terra: 'terra' };
MODELS.forEach(model => {
  TABLE_COLOURS.forEach(colour => {
    PRODUCTS.push({
      id: `model-${model.toLowerCase()}-${colour}`,
      name: `Model ${model} ${COLOURS[colour].label}`,
      type: 'table',
      typeLabel: 'Table',
      model,
      colour,
      size: null,
      price: 399.99,
      difficulty: 'Advanced',
      // the live catalogue shows Model SH Deep Black at 5 days; every other table is 3
      lead: (model === 'SH' && colour === 'deep-black') ? 5 : 3,
      img: `img/${model.toLowerCase()}-${slugMap[colour]}.jpg`,
      dims: { height: '38cm', width: '110cm', length: '70cm' },
      blurb: `Model ${model} is a hand-finished Mortex coffee table with a soft, organic silhouette. Every piece is finished by you, so no two are identical.`,
      body: `The kit contains the shaped core, the Mortex system, pigments in ${COLOURS[colour].label}, and every tool needed to finish it. Follow the step-by-step manual and video tutorial from first coat to final seal. Expect around a weekend of work, spread over three days of curing.`
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
