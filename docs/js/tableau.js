// Tableau de bord du créateur : visites du site, logiciel et ventes.
// Les requêtes sont signées avec la clé du créateur, comme le panel des clients.
import * as ed from "../createur/ed25519.js";

const $ = (s) => document.querySelector(s);
const API = window.TAVERNE.api;
const hex = (b) => [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
const echapper = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nf = new Intl.NumberFormat("fr-FR");
const nfCompact = new Intl.NumberFormat("fr-FR", { notation: "compact", maximumFractionDigits: 1 });
const euros = new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" });
const paysNom = (() => { try { const d = new Intl.DisplayNames(["fr"], { type: "region" }); return (c) => { try { return c ? d.of(c) : "Inconnu"; } catch (e) { return c; } }; } catch (e) { return (c) => c || "Inconnu"; } })();
const VOIX = window.VOIX_NOMS || {};

// Palette catégorielle validée (fond #241913, mode sombre) : ambre, violet, sarcelle, braise.
const SERIE = ["#c98500", "#9085e9", "#199e70", "#d95926"];
const ACCENT = "#f2a93b";      // série unique (barres, colonnes)
const DISCRET = "#6b5545";     // tendance hors période courante
// rampe ordinale ambre (entonnoir) et séquentielle (affluence), du fond vers la lanterne
const RAMPE = ["#5c3d14", "#7d531a", "#9d6a1f", "#c48523", "#f2a93b"];
// entonnoir : steps assez clairs pour rester lisibles sur le fond (≥ 2:1)
const RAMPE_ORDINALE = ["#9d6a1f", "#b37822", "#c98827", "#de9830", "#f2a93b"];

let graine = null;
let donnees = null;
let jours = Number(localStorage.getItem("tdb-jours") || 30) || 30;
let mesure = localStorage.getItem("tdb-mesure") || "visiteurs";
const vuesTableau = new Set();

async function admin(action, d = {}) {
  const charge = JSON.stringify({ action, donnees: d, horodatage: Date.now() });
  const signature = hex(await ed.signAsync(new TextEncoder().encode(charge), graine));
  const r = await fetch(API + "/createur", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ charge, signature }) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.erreur || "Erreur " + r.status);
  return j;
}

// ------------------------------------------------------------ navigation de l'accès créateur
function montrerVue(v) {
  for (const b of document.querySelectorAll("[data-adm]")) b.toggleAttribute("aria-current", b.dataset.adm === v) || b.removeAttribute("aria-current");
  for (const b of document.querySelectorAll("[data-adm]")) { if (b.dataset.adm === v) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current"); }
  for (const z of document.querySelectorAll("[data-vue-adm]")) z.hidden = z.dataset.vueAdm !== v;
  document.querySelector(".createur").classList.toggle("large", v === "tableau");
  try { localStorage.setItem("tdb-vue", v); } catch (e) {}
}
$("#adm-nav").addEventListener("click", (ev) => { const b = ev.target.closest("[data-adm]"); if (b) montrerVue(b.dataset.adm); });
$("#deconnexion-haut").addEventListener("click", () => $("#deconnexion").click());

let minuterie = null;
window.addEventListener("createur", (ev) => {
  graine = ev.detail && ev.detail.graine;
  clearInterval(minuterie);
  if (!graine) { document.querySelector(".createur").classList.remove("large"); return; }
  montrerVue(localStorage.getItem("tdb-vue") || "tableau");
  charger();
  minuterie = setInterval(() => { if (!document.hidden && !$("#tdb").hidden) charger(true); }, 60000);
});

// ------------------------------------------------------------ chargement
async function charger(discret) {
  const zone = $("#tdb-contenu");
  zone.setAttribute("aria-busy", "true");
  if (donnees) zone.classList.add("rafraichit"); // on garde l'ancien rendu, atténué
  try {
    donnees = await admin("tableau", { jours });
    $("#tdb-erreur").hidden = true;
    rendu();
  } catch (e) {
    if (!discret) { $("#tdb-erreur").textContent = e.message; $("#tdb-erreur").hidden = false; }
  } finally {
    zone.setAttribute("aria-busy", "false");
    zone.classList.remove("rafraichit");
  }
}

$("#tdb-periode").addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-jours]");
  if (!b) return;
  jours = Number(b.dataset.jours);
  try { localStorage.setItem("tdb-jours", jours); } catch (e) {}
  majSegments();
  charger();
});
$("#tdb-mesure").addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-mesure]");
  if (!b) return;
  mesure = b.dataset.mesure;
  try { localStorage.setItem("tdb-mesure", mesure); } catch (e) {}
  majSegments();
  if (donnees) grapheJours();
});
document.addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-tableau]");
  if (!b || !donnees) return;
  const k = b.dataset.tableau;
  if (vuesTableau.has(k)) vuesTableau.delete(k); else vuesTableau.add(k);
  b.textContent = vuesTableau.has(k) ? "Graphique" : "Tableau";
  rendu();
});
$("#tdb-objectif-changer").addEventListener("click", async () => {
  const v = prompt("Objectif de revenus pour le mois (en euros) :", donnees ? donnees.ventes.objectif : 100);
  if (!v) return;
  try { await admin("objectif", { valeur: Number(String(v).replace(",", ".")) }); charger(); } catch (e) { alert(e.message); }
});
function majSegments() {
  for (const b of document.querySelectorAll("#tdb-periode [data-jours]")) b.setAttribute("aria-checked", String(Number(b.dataset.jours) === jours));
  for (const b of document.querySelectorAll("#tdb-mesure [data-mesure]")) b.setAttribute("aria-checked", String(b.dataset.mesure === mesure));
}
majSegments();

// ------------------------------------------------------------ bulle d'info (survol et clavier)
const bulle = $("#tdb-bulle");
function montrerBulle(html, x, y) {
  bulle.innerHTML = html;
  bulle.hidden = false;
  const r = bulle.getBoundingClientRect();
  let gx = x + 14, gy = y - r.height - 12;
  if (gx + r.width > innerWidth - 8) gx = x - r.width - 14;
  if (gy < 8) gy = y + 16;
  bulle.style.left = gx + "px";
  bulle.style.top = gy + "px";
}
function cacherBulle() { bulle.hidden = true; }
document.addEventListener("pointermove", (ev) => {
  const c = ev.target.closest("[data-bulle]");
  if (c) montrerBulle(c.dataset.bulle, ev.clientX, ev.clientY); else cacherBulle();
});
document.addEventListener("focusin", (ev) => {
  const c = ev.target.closest("[data-bulle]");
  if (!c) return cacherBulle();
  const r = c.getBoundingClientRect();
  montrerBulle(c.dataset.bulle, r.left + r.width / 2, r.top);
});
document.addEventListener("focusout", cacherBulle);

// ------------------------------------------------------------ outils de rendu
const jourCourt = (j) => { const [a, m, d] = j.split("-"); return `${Number(d)}/${Number(m)}`; };
const jourLong = (j) => new Date(j + "T12:00:00").toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
const formater = (m, v) => m === "revenus" ? euros.format(v) : nf.format(v);
const pourcent = (a, b) => new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1 }).format(b ? Math.round(a / b * 1000) / 10 : 0);

function variation(v, avant, bonQuandMonte = true) {
  if (!avant && !v) return `<span class="delta neutre">—</span>`;
  if (!avant) return `<span class="delta monte">nouveau</span>`;
  const p = Math.round((v - avant) / avant * 100);
  if (p === 0) return `<span class="delta neutre">= période d'avant</span>`;
  const bien = (p > 0) === bonQuandMonte;
  return `<span class="delta ${bien ? "bien" : "mal"}" title="Période précédente : ${nf.format(avant)}"><span aria-hidden="true">${p > 0 ? "▲" : "▼"}</span> ${p > 0 ? "+" : ""}${p} %</span>`;
}

// tendance : petite courbe, période en cours dans l'accent
function tendance(valeurs) {
  if (valeurs.length < 2) return "";
  const l = 120, h = 30, max = Math.max(1, ...valeurs);
  const pts = valeurs.map((v, i) => [i / (valeurs.length - 1) * l, h - 3 - v / max * (h - 6)]);
  const d = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join("");
  const dernier = pts[pts.length - 1];
  return `<svg class="tendance" viewBox="0 0 ${l} ${h}" aria-hidden="true"><path d="${d}" fill="none" stroke="${DISCRET}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="${dernier[0]}" cy="${dernier[1]}" r="4" fill="${ACCENT}" stroke="#241913" stroke-width="2"/></svg>`;
}

// liste en barres (une seule série → une seule couleur)
function barres(lignes, opts = {}) {
  if (!lignes.length) return `<p class="tdb-vide">${opts.vide || "Rien pour l'instant."}</p>`;
  const max = Math.max(...lignes.map((l) => l.n));
  const total = opts.total || lignes.reduce((s, l) => s + l.n, 0);
  return `<ul class="barres">${lignes.map((l) => `<li tabindex="0" data-bulle="${echapper(`<strong>${echapper(l.nom)}</strong><br>${nf.format(l.n)} ${opts.unite || ""} · ${pourcent(l.n, total)} %`)}">
      <span class="barre-nom">${l.pastille ? `<i class="pastille-voix" style="--c:${l.pastille}"></i>` : ""}${echapper(l.nom)}</span>
      <span class="barre-piste"><i style="width:${Math.max(2, l.n / max * 100)}%"></i></span>
      <span class="barre-valeur">${nf.format(l.n)}</span></li>`).join("")}</ul>`;
}

// barre de répartition (catégories, ≤ 4 couleurs + « Autres »), avec légende
function repartition(lignes, libelle) {
  if (!lignes.length) return `<p class="tdb-vide">Rien pour l'instant.</p>`;
  let l = [...lignes].sort((a, b) => b.n - a.n);
  if (l.length > 4) l = [...l.slice(0, 3), { nom: "Autres", n: l.slice(3).reduce((s, x) => s + x.n, 0) }];
  const total = l.reduce((s, x) => s + x.n, 0) || 1;
  const segs = l.map((x, i) => `<i tabindex="0" style="flex:${x.n};background:${x.nom === "Autres" ? DISCRET : SERIE[i]}" data-bulle="${echapper(`<strong>${echapper(x.nom)}</strong><br>${nf.format(x.n)} · ${pourcent(x.n, total)} %`)}"></i>`).join("");
  const legende = l.map((x, i) => `<li><i style="background:${x.nom === "Autres" ? DISCRET : SERIE[i]}"></i>${echapper(x.nom)} <strong>${pourcent(x.n, total)} %</strong></li>`).join("");
  return `<div class="repartition" role="img" aria-label="${echapper(libelle)}">${segs}</div><ul class="legende">${legende}</ul>`;
}

function tableauHTML(entetes, lignes) {
  return `<div class="tdb-table"><table><thead><tr>${entetes.map((e) => `<th>${e}</th>`).join("")}</tr></thead>
    <tbody>${lignes.map((l) => `<tr>${l.map((c, i) => `<td${i ? ' class="nb"' : ""}>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

// ------------------------------------------------------------ rendu
function rendu() {
  const d = donnees;
  const quand = new Date(d.genere);
  $("#tdb-maj").textContent = `${d.jours} derniers jours comparés aux ${d.jours} d'avant · mis à jour à ${quand.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}`;
  const dir = d.direct.cinqMinutes;
  $("#tdb-direct").classList.toggle("vivant", dir > 0);
  $("#tdb-direct span").textContent = dir ? `${dir} visiteur${dir > 1 ? "s" : ""} en ce moment` : `${d.direct.trenteMinutes} dans la dernière demi-heure`;
  heros();
  chope();
  tuiles();
  grapheJours();
  journal();
  entonnoir();
  affluence();
  $("#tdb-sources").innerHTML = barres(d.sources.map((s) => ({ nom: nomSource(s.cle), n: s.n })), { unite: "visites", vide: "Pas encore de visite." });
  $("#tdb-pays").innerHTML = barres(d.pays.map((s) => ({ nom: paysNom(s.cle), n: s.n })), { unite: "visites", vide: "Pas encore de visite." });
  $("#tdb-pages").innerHTML = barres(d.pages.map((s) => ({ nom: s.cle.replace(/^\//, "").replace(/\.html$/, "") || "accueil", n: s.n })), { unite: "vues", vide: "Pas encore de visite." });
  $("#tdb-appareils").innerHTML = repartition(d.appareils.map((a) => ({ nom: { mobile: "Mobile", ordinateur: "Ordinateur", tablette: "Tablette" }[a.cle] || a.cle, n: a.n })), "Visiteurs par appareil");
  appli();
  ventes();
}

const SOURCES = { direct: "Direct (lien tapé, favori)", tiktok: "TikTok", twitch: "Twitch", google: "Google", youtube: "YouTube", discord: "Discord", x: "X (Twitter)", instagram: "Instagram", facebook: "Facebook", reddit: "Reddit", "ko-fi": "Ko-fi", github: "GitHub", bing: "Bing", duckduckgo: "DuckDuckGo", qwant: "Qwant" };
const nomSource = (s) => SOURCES[s] || s;

function heros() {
  const v = donnees.ventes;
  $("#tdb-revenu").textContent = euros.format(v.revenuMois);
  const p = Math.min(100, v.revenuMois / v.objectif * 100);
  $("#tdb-jauge").style.width = p + "%";
  $("#tdb-objectif-texte").textContent = `${Math.round(v.revenuMois / v.objectif * 100)} % de l'objectif de ${euros.format(v.objectif)}`;
  const nb = (f) => (v.actifs.find((a) => a.formule === f) || { n: 0 }).n;
  const payants = nb("mensuel") + nb("trimestre") + nb("annuel");
  $("#tdb-ventes-mini").innerHTML = `<div><dt>Revenu mensuel estimé</dt><dd>${euros.format(v.mrr)}</dd></div>
    <div><dt>Abonnés payants</dt><dd>${nf.format(payants)}</dd></div>
    <div><dt>Essais en cours</dt><dd>${nf.format(nb("essai"))}</dd></div>`;
}

// La chope : la bière monte avec les revenus du mois, la mousse déborde quand l'objectif est dépassé
function chope() {
  const v = donnees.ventes;
  const p = Math.max(0, Math.min(1.08, v.revenuMois / v.objectif));
  const haut = 40, bas = 196, niveau = bas - (bas - haut) * Math.min(1, p);
  const deborde = p >= 1;
  const bulles = Array.from({ length: 9 }, (_, i) => {
    const x = 44 + (i * 37) % 92, r = 2 + (i % 3), du = 2.6 + (i % 4) * 0.7, delai = (i * 0.45) % 3;
    return `<circle cx="${x}" cy="${bas - 6}" r="${r}" fill="#fff6" style="animation-duration:${du}s;animation-delay:-${delai}s"/>`;
  }).join("");
  $("#chope").innerHTML = `<svg viewBox="0 0 220 230" role="img" aria-label="Chope remplie à ${Math.round(p * 100)} %">
    <defs><clipPath id="interieur"><rect x="34" y="40" width="112" height="156" rx="10"/></clipPath>
      <linearGradient id="biere" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f7bd4f"/><stop offset="1" stop-color="#c47812"/></linearGradient></defs>
    <rect x="34" y="40" width="112" height="156" rx="10" fill="#1a120d"/>
    <g clip-path="url(#interieur)">
      <rect class="chope-biere" x="30" y="${niveau}" width="120" height="${bas - niveau + 10}" fill="url(#biere)"/>
      <g class="chope-bulles" style="--niveau:${niveau}px">${p > 0.05 ? bulles : ""}</g>
      ${p > 0.02 ? `<path class="chope-mousse" d="M30 ${niveau} q10 -12 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 v14 h-120 z" fill="#f3e7d3"/>` : ""}
    </g>
    ${deborde ? `<path d="M30 38 q12 -22 30 -10 q14 -18 32 -4 q16 -16 32 0 q16 -10 26 8 q6 12 -6 18 h-108 q-12 -2 -6 -12z" fill="#f3e7d3"/><path d="M142 46 q10 10 4 30" stroke="#f3e7d3" stroke-width="7" stroke-linecap="round" fill="none"/>` : ""}
    <rect x="34" y="40" width="112" height="156" rx="10" fill="none" stroke="#f3e7d3" stroke-width="7"/>
    <path d="M146 72 h22 a24 24 0 0 1 24 24 v36 a24 24 0 0 1 -24 24 h-22" fill="none" stroke="#f3e7d3" stroke-width="7"/>
    <path d="M62 62 v112 M90 62 v112 M118 62 v112" stroke="#f3e7d322" stroke-width="5" stroke-linecap="round"/>
  </svg>`;
  $("#chope-texte").textContent = deborde
    ? `Objectif atteint : ${euros.format(v.revenuMois)} sur ${euros.format(v.objectif)}. Tournée générale !`
    : `Encore ${euros.format(Math.max(0, v.objectif - v.revenuMois))} pour la remplir (objectif ${euros.format(v.objectif)}).`;
}

function tuiles() {
  const d = donnees, r = d.resume;
  const t = [
    ["visiteurs", "Visiteurs"], ["vues", "Pages vues"], ["telechargements", "Téléchargements"],
    ["comptes", "Comptes créés"], ["essais", "Essais lancés"], ["achats", "Achats"],
  ];
  $("#tdb-tuiles").innerHTML = t.map(([k, nom]) => `<section class="tdb-tuile">
      <span class="tdb-etiquette">${nom}</span>
      <strong>${nf.format(r[k].valeur)}</strong>
      ${variation(r[k].valeur, r[k].avant)}
      ${tendance(d.serie.map((s) => s[k === "vues" ? "vues" : k]))}
    </section>`).join("");
}

const NOMS_MESURE = { visiteurs: "Visiteurs par jour", telechargements: "Téléchargements par jour", comptes: "Comptes créés par jour", revenus: "Revenus par jour", appli: "Logiciels ouverts par jour" };

// colonnes : une seule série, barres fines arrondies au bout, grille discrète
function grapheJours() {
  const d = donnees, s = d.serie, m = mesure;
  $("#tdb-graphe-titre").textContent = NOMS_MESURE[m];
  const z = $("#tdb-graphe");
  if (vuesTableau.has("graphe")) {
    z.innerHTML = tableauHTML(["Jour", "Visiteurs", "Pages vues", "Téléch.", "Comptes", "Essais", "Achats", "Revenus", "Logiciels"],
      [...s].reverse().map((x) => [jourCourt(x.jour), nf.format(x.visiteurs), nf.format(x.vues), nf.format(x.telechargements), nf.format(x.comptes), nf.format(x.essais), nf.format(x.achats), euros.format(x.revenus), nf.format(x.appli)]));
    return;
  }
  // agrégation par semaine sur l'année (sinon 365 colonnes illisibles)
  let pts = s.map((x) => ({ lib: jourCourt(x.jour), long: jourLong(x.jour), v: x[m] }));
  if (s.length > 120) {
    pts = [];
    for (let i = 0; i < s.length; i += 7) {
      const g = s.slice(i, i + 7);
      pts.push({ lib: jourCourt(g[0].jour), long: `semaine du ${jourLong(g[0].jour)}`, v: g.reduce((a, x) => a + x[m], 0) });
    }
  }
  const L = Math.max(320, z.clientWidth || 700), H = 230, g = 44, dr = 12, ht = 16, bas = 28;
  const max = Math.max(1, ...pts.map((p) => p.v));
  const pas = niceStep(max / 4);
  const yMax = Math.ceil(max / pas) * pas;
  const larg = (L - g - dr) / pts.length;
  const barre = Math.min(24, Math.max(2, larg - 2));
  const y = (v) => ht + (H - ht - bas) * (1 - v / yMax);
  let grille = "";
  for (let v = 0; v <= yMax + 1e-9; v += pas) {
    grille += `<line x1="${g}" x2="${L - dr}" y1="${y(v)}" y2="${y(v)}" class="grille"/><text x="${g - 8}" y="${y(v) + 4}" class="axe" text-anchor="end">${m === "revenus" ? nfCompact.format(v) + " €" : nfCompact.format(v)}</text>`;
  }
  const chaque = Math.ceil(pts.length / Math.floor((L - g) / 46));
  const cols = pts.map((p, i) => {
    const x = g + i * larg + (larg - barre) / 2, yy = y(p.v), hh = Math.max(0, y(0) - yy);
    const r = Math.min(4, barre / 2, hh);
    const chemin = hh > 0 ? `M${x} ${y(0)} V${yy + r} Q${x} ${yy} ${x + r} ${yy} H${x + barre - r} Q${x + barre} ${yy} ${x + barre} ${yy + r} V${y(0)} Z` : "";
    const info = `<strong>${echapper(p.long)}</strong><br>${NOMS_MESURE[m].replace(" par jour", "")} : ${formater(m, p.v)}`;
    return `<g class="colonne" tabindex="0" data-bulle="${echapper(info)}"><rect x="${g + i * larg}" y="${ht}" width="${larg}" height="${H - ht - bas}" fill="transparent"/>${chemin ? `<path d="${chemin}" fill="${ACCENT}"/>` : ""}</g>
      ${i % chaque === 0 ? `<text x="${g + i * larg + larg / 2}" y="${H - 8}" class="axe" text-anchor="middle">${p.lib}</text>` : ""}`;
  }).join("");
  // valeur la plus haute étiquetée (une seule étiquette directe)
  const iMax = pts.reduce((b, p, i) => (p.v > pts[b].v ? i : b), 0);
  const etiq = pts[iMax].v > 0 ? `<text x="${g + iMax * larg + larg / 2}" y="${y(pts[iMax].v) - 6}" class="valeur" text-anchor="middle">${formater(m, pts[iMax].v)}</text>` : "";
  z.innerHTML = `<svg viewBox="0 0 ${L} ${H}" width="100%" height="${H}" role="img" aria-label="${NOMS_MESURE[m]}">${grille}<line x1="${g}" x2="${L - dr}" y1="${y(0)}" y2="${y(0)}" class="base"/>${cols}${etiq}</svg>`;
}
function niceStep(x) {
  const p = Math.pow(10, Math.floor(Math.log10(Math.max(x, 1e-9))));
  const n = x / p;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p || 1;
}
new ResizeObserver(() => { if (donnees && !$("#tdb").hidden) grapheJours(); }).observe($("#tdb-graphe"));

const ICONES_JOURNAL = { compte: "👤", essai: "⏳", achat: "💰", telechargement: "⬇", installation: "🖥" };
const TYPES_JOURNAL = { compte: "Compte", essai: "Essai", achat: "Achat", telechargement: "Téléchargement", installation: "Installation" };
function depuis(ms) {
  const s = (Date.now() - ms) / 1000;
  if (s < 60) return "à l'instant";
  if (s < 3600) return `il y a ${Math.floor(s / 60)} min`;
  if (s < 86400) return `il y a ${Math.floor(s / 3600)} h`;
  return new Date(ms).toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
}
function journal() {
  const l = donnees.journal;
  $("#tdb-journal").innerHTML = l.length ? l.map((j) => `<li class="j-${j.type}"><span class="j-icone" aria-hidden="true">${ICONES_JOURNAL[j.type] || "•"}</span>
      <span><strong>${TYPES_JOURNAL[j.type] || j.type}</strong> ${echapper(j.texte)}<small>${depuis(j.quand)}</small></span></li>`).join("")
    : `<li class="tdb-vide">La taverne est calme pour l'instant.</li>`;
}

// entonnoir : une rampe ordinale (une seule teinte qui s'éclaire vers l'achat)
function entonnoir() {
  const e = donnees.entonnoir;
  const z = $("#tdb-entonnoir");
  if (vuesTableau.has("entonnoir")) {
    z.innerHTML = tableauHTML(["Étape", "Nombre", "Par rapport à l'étape d'avant"], e.map((x, i) => [x.etape, nf.format(x.n), i ? pourcent(x.n, e[i - 1].n) + " %" : "—"]));
    return;
  }
  const max = Math.max(1, e[0].n);
  z.innerHTML = `<ol class="entonnoir">${e.map((x, i) => `<li tabindex="0" data-bulle="${echapper(`<strong>${x.etape}</strong><br>${nf.format(x.n)}${i ? ` · ${pourcent(x.n, e[i - 1].n)} % de l'étape d'avant` : ""}`)}">
      <span class="e-nom">${x.etape}</span>
      <span class="e-piste"><i style="width:${Math.max(1.5, x.n / max * 100)}%;background:${RAMPE_ORDINALE[i]}"></i></span>
      <span class="e-valeur">${nf.format(x.n)}</span>
      ${i ? `<span class="e-taux">${pourcent(x.n, e[i - 1].n)} %</span>` : `<span class="e-taux"></span>`}</li>`).join("")}</ol>
    <p class="tdb-note">${donnees.boutique} visiteurs ont regardé la boutique, ${donnees.kofi} ont ouvert Ko-fi.</p>`;
}

// affluence : grille jour × heure, une seule teinte du fond vers l'ambre
const JOURS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."];
function affluence() {
  const a = donnees.affluence;
  const z = $("#tdb-affluence");
  if (vuesTableau.has("affluence")) {
    z.innerHTML = tableauHTML(["Jour", ...Array.from({ length: 24 }, (_, h) => h + "h")], a.map((l, i) => [JOURS[i], ...l.map((n) => nf.format(n))]));
    return;
  }
  const max = Math.max(1, ...a.flat());
  const couleur = (n) => n === 0 ? "#2c2018" : RAMPE[Math.min(RAMPE.length - 1, Math.floor(n / max * (RAMPE.length - 0.001)))];
  let meilleur = { n: 0 };
  a.forEach((l, i) => l.forEach((n, h) => { if (n > meilleur.n) meilleur = { n, i, h }; }));
  z.innerHTML = `<div class="affluence">
    ${a.map((l, i) => `<span class="a-jour">${JOURS[i]}</span>${l.map((n, h) => `<i tabindex="0" style="background:${couleur(n)}" data-bulle="${echapper(`<strong>${JOURS[i]} ${h} h – ${h + 1} h</strong><br>${nf.format(n)} pages vues`)}"></i>`).join("")}`).join("")}
    <span></span>${[0, 6, 12, 18].map((h) => `<span class="a-heure" style="grid-column:${h + 2} / span 6">${h} h</span>`).join("")}
  </div>
  <div class="echelle"><span>moins</span>${["#2c2018", ...RAMPE].map((c) => `<i style="background:${c}"></i>`).join("")}<span>plus</span></div>
  ${meilleur.n ? `<p class="tdb-note">Le plus de monde : le ${JOURS[meilleur.i].replace(".", "")} vers ${meilleur.h} h. Bon moment pour poster sur TikTok.</p>` : ""}`;
}

const FONCTIONS = { son: "Sons joués", roulette: "Roulette", "defi:chaos": "Défi Chaos", "defi:escalade": "Défi Escalade", "defi:cumul": "Défi Cumul", "defi:piege": "Défi Voix piège",
  "automatisme:cri": "Automatisme « cri »", "automatisme:silence": "Automatisme « silence »", "automatisme:voix": "Automatisme « voix »", "automatisme:son": "Automatisme « son »",
  "automatisme:demarrage": "Automatisme « démarrage »", "automatisme:minuteurFini": "Automatisme « minuteur »", "automatisme:defiFini": "Automatisme « fin de défi »" };
const LICENCES = { demo: "Démo", essai: "Essai", mensuel: "Mensuel", trimestre: "3 mois", annuel: "1 an", offert: "Offert", abonnement: "Abonnement", cle: "Clé", inconnue: "Inconnue" };

function appli() {
  const a = donnees.appli, r = donnees.resume;
  const tuile = (nom, v, extra = "") => `<section class="tdb-tuile"><span class="tdb-etiquette">${nom}</span><strong>${nf.format(v)}</strong>${extra}</section>`;
  $("#tdb-appli-tuiles").innerHTML = tuile("Ouverts aujourd'hui", a.aujourdhui) + tuile("Ouverts sur 7 jours", a.semaine) + tuile("Ouverts sur 30 jours", a.mois)
    + tuile("Nouvelles installations", r.installations.valeur, variation(r.installations.valeur, r.installations.avant)) + tuile("Installations au total", a.total) + tuile("Chaînes Twitch reliées", a.twitch);
  $("#tdb-voix").innerHTML = barres(a.voix.map((v) => ({ nom: (VOIX[v.cle] || { nom: v.cle }).nom, n: v.n, pastille: (VOIX[v.cle] || {}).couleur })), { unite: "fois", vide: "Les premières statistiques arrivent avec la version 2.0." });
  $("#tdb-fonctions").innerHTML = barres(a.fonctions.map((f) => ({ nom: FONCTIONS[f.cle] || f.cle, n: f.n })), { unite: "fois", vide: "Les premières statistiques arrivent avec la version 2.0." });
  $("#tdb-versions").innerHTML = barres(a.versions.map((v) => ({ nom: "v" + v.cle, n: v.n })), { unite: "installations", vide: "Aucune installation active." });
  $("#tdb-licences").innerHTML = repartition(a.licences.map((l) => ({ nom: LICENCES[l.cle] || l.cle, n: l.n })), "Installations par licence");
}

function ventes() {
  const v = donnees.ventes;
  const NOMS = { mensuel: "Mensuel (4,99 €/mois)", trimestre: "3 mois (14,99 €)", annuel: "1 an (59,99 €)", Subscription: "Abonnement", "Shop Order": "Boutique", Donation: "Don" };
  const f = Object.entries(v.parFormule).sort((a, b) => b[1].montant - a[1].montant);
  $("#tdb-formules").innerHTML = f.length
    ? tableauHTML(["Formule", "Ventes", "Montant"], f.map(([k, x]) => [NOMS[k] || k, nf.format(x.n), euros.format(x.montant)]))
      + `<p class="tdb-note">Sur la période : ${euros.format(donnees.resume.revenus.valeur)} ${variation(donnees.resume.revenus.valeur, donnees.resume.revenus.avant)}</p>`
    : `<p class="tdb-vide">Pas encore de vente sur cette période.</p>`;
  const actifs = v.actifs.filter((a) => a.formule !== "essai");
  const taux = v.essais ? Math.round(v.convertis / v.essais * 100) : 0;
  $("#tdb-abonnes").innerHTML = repartition(actifs.map((a) => ({ nom: LICENCES[a.formule] || a.formule, n: a.n })), "Accès actifs par formule")
    + `<div class="tdb-taux"><span class="tdb-etiquette">Essais devenus payants</span>
        <div class="tdb-jauge"><i style="width:${taux}%"></i></div>
        <span><strong>${taux} %</strong> (${v.convertis} sur ${v.essais} essais de la période)</span></div>
      <p class="tdb-note">${v.desabonnes ? `${v.desabonnes} abonnement${v.desabonnes > 1 ? "s" : ""} mensuel${v.desabonnes > 1 ? "s" : ""} arrêté${v.desabonnes > 1 ? "s" : ""} sur la période.` : "Aucun abonnement arrêté sur la période."}</p>`;
}
