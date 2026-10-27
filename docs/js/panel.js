// Panel créateur : clients, abonnements et paiements. Chaque requête est signée
// avec la clé du créateur (déchiffrée par le mot de passe sur cette page).
import * as ed from "../createur/ed25519.js";

const $ = (s) => document.querySelector(s);
const API = window.TAVERNE.api;
const hex = (b) => [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
const echapper = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const date = (ms) => ms ? new Date(ms).toLocaleDateString("fr-FR") : "—";
const FORMULES = { mensuel: "Mensuel", trimestre: "3 mois", annuel: "1 an", offert: "Offert", essai: "Essai" };

let graine = null;
let clientOuvert = null;

async function admin(action, donnees = {}) {
  const charge = JSON.stringify({ action, donnees, horodatage: Date.now() });
  const signature = hex(await ed.signAsync(new TextEncoder().encode(charge), graine));
  let r;
  try {
    r = await fetch(API + "/createur", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ charge, signature }) });
  } catch (e) {
    throw new Error("Le serveur ne répond pas (api.tavernevoice.fr).");
  }
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.erreur || "Erreur " + r.status);
  return d;
}

function statutAbo(a) {
  if (a.actif) return `<span class="pastille-statut ok">${FORMULES[a.formule] || "actif"}${a.mensuel ? "" : " jusqu'au " + date(a.fin)}</span>`;
  if (a.fin) return `<span class="pastille-statut">terminé le ${date(a.fin)}</span>`;
  return `<span class="pastille-statut">aucun</span>`;
}

async function chargerStats() {
  const s = await admin("stats");
  const somme = (l) => l.map((x) => `${(x.total || 0).toFixed(2).replace(".", ",")} ${x.devise || "€"}`).join(" + ") || "0 €";
  const actifs = s.actifs.reduce((n, x) => n + x.n, 0);
  $("#p-tuiles").innerHTML = `
    <div class="tuile"><b>${s.comptes}</b><span>comptes</span></div>
    <div class="tuile"><b>${actifs}</b><span>accès actifs${s.actifs.length ? " (" + s.actifs.map((x) => `${x.n} ${(FORMULES[x.formule] || x.formule).toLowerCase()}`).join(", ") + ")" : ""}</span></div>
    <div class="tuile"><b>${somme(s.mois)}</b><span>encaissés ce mois-ci</span></div>
    <div class="tuile"><b>${somme(s.total)}</b><span>depuis le début</span></div>`;
  const alertes = [];
  if (!s.kofi) alertes.push("Le jeton Ko-fi (KOFI_TOKEN) n'est pas réglé sur le serveur : les paiements ne seront pas reçus.");
  if (!s.emails) alertes.push("Les e-mails (Brevo) ne sont pas réglés : les adresses ne sont pas vérifiées et « mot de passe oublié » ne marche pas.");
  if (s.enAttente) alertes.push(`${s.enAttente} paiement(s) Ko-fi n'ont pas encore de compte : voir « Paiements sans compte ».`);
  $("#p-alertes").innerHTML = alertes.map((a) => `<p class="msg erreur">${echapper(a)}</p>`).join("");
}

async function chercher() {
  const r = await admin("clients", { recherche: $("#p-recherche").value.trim() });
  $("#p-clients").innerHTML = r.clients.map((c) => `<tr>
      <td>${echapper(c.pseudo || "—")}<small>${echapper(c.email)}</small></td>
      <td>${date(c.cree)}</td>
      <td>${statutAbo(c.abonnement)}</td>
      <td>${c.pcs}</td>
      <td>${c.bloque ? '<span class="pastille-statut ko">bloqué</span>' : c.verifie ? "" : '<span class="pastille-statut">adresse à vérifier</span>'}</td>
      <td><button class="lien-bouton" type="button" data-client="${echapper(c.id)}">Ouvrir</button></td></tr>`).join("")
    || `<tr><td colspan="6">Aucun client${$("#p-recherche").value ? " pour cette recherche" : " pour l'instant"}.</td></tr>`;
}

async function ouvrirClient(id) {
  clientOuvert = id;
  const r = await admin("client", { id });
  const c = r.client;
  $("#f-titre").textContent = c.pseudo || c.email;
  $("#f-infos").innerHTML = `<p>${echapper(c.email)}, inscrit le ${date(c.cree)}. ${statutAbo(c.abonnement)}
      ${c.bloque ? '<span class="pastille-statut ko">bloqué</span>' : ""} ${c.verifie ? "" : '<span class="pastille-statut">adresse non vérifiée</span>'}</p>`;
  $("#f-note").value = c.note || "";
  $("#f-bloquer").textContent = c.bloque ? "Débloquer le compte" : "Bloquer le compte";
  $("#f-bloquer").dataset.bloque = c.bloque ? "" : "1";
  $("#f-verifier").hidden = c.verifie;
  $("#f-pcs").innerHTML = r.pcs.map((p) => `<li><span>${echapper(p.nom || p.pc)}<small>${echapper(p.pc)}, vu le ${date(p.vu)}</small></span></li>`).join("") || "<li><span>Aucun PC.</span></li>";
  $("#f-paiements").innerHTML = r.paiements.map((p) => `<li><span>${echapper(FORMULES[p.formule] || p.type)}<small>${date(p.quand)}${p.email !== c.email ? ", payé avec " + echapper(p.email) : ""}</small></span>
      <span>${p.montant ? echapper(p.montant + " " + p.devise) : ""}</span></li>`).join("") || "<li><span>Aucun paiement.</span></li>";
  $("#f-journal").innerHTML = r.journal.slice(0, 30).map((j) => `<li><span>${echapper(j.quoi)}<small>${new Date(j.quand).toLocaleString("fr-FR")}</small></span></li>`).join("");
  $("#f-msg").hidden = true;
  if (!$("#fiche").open) $("#fiche").showModal();
}

async function action(nom, donnees, confirmation) {
  if (confirmation && !confirm(confirmation)) return;
  const m = $("#f-msg");
  try {
    await admin(nom, { id: clientOuvert, ...donnees });
    m.className = "msg ok"; m.textContent = "C'est fait."; m.hidden = false;
    await Promise.all([ouvrirClient(clientOuvert), chercher(), chargerStats()]);
    m.hidden = false;
  } catch (e) { m.className = "msg erreur"; m.textContent = e.message; m.hidden = false; }
}

async function chargerAttente() {
  const r = await admin("attente");
  $("#p-attente-zone").hidden = !r.paiements.length;
  $("#p-attente").innerHTML = r.paiements.map((p) => `<li><span>${echapper(p.email || "(sans adresse)")}<small>${echapper(FORMULES[p.formule] || p.type)}, ${date(p.quand)}${p.nom ? ", " + echapper(p.nom) : ""}</small></span>
      <span>${echapper(p.montant + " " + p.devise)} <button class="lien-bouton" type="button" data-rattacher="${echapper(p.id)}">Rattacher à un compte</button></span></li>`).join("");
}

async function tout() {
  $("#p-erreur").hidden = true;
  try { await Promise.all([chargerStats(), chercher(), chargerAttente()]); }
  catch (e) { $("#p-erreur").textContent = e.message; $("#p-erreur").hidden = false; }
}

window.addEventListener("createur", (ev) => {
  graine = ev.detail && ev.detail.graine;
  if (graine) tout();
});

$("#p-actualiser").addEventListener("click", tout);
let minuterie = null;
$("#p-recherche").addEventListener("input", () => { clearTimeout(minuterie); minuterie = setTimeout(() => chercher().catch(() => {}), 300); });
$("#p-clients").addEventListener("click", (ev) => { const b = ev.target.closest("[data-client]"); if (b) ouvrirClient(b.dataset.client).catch((e) => alert(e.message)); });
$("#p-attente").addEventListener("click", async (ev) => {
  const b = ev.target.closest("[data-rattacher]");
  if (!b) return;
  const email = prompt("Adresse e-mail du compte Taverne Voice à qui donner ce paiement :");
  if (!email) return;
  try {
    const r = await admin("clients", { recherche: email.trim().toLowerCase() });
    const c = r.clients.find((x) => x.email === email.trim().toLowerCase());
    if (!c) return alert("Aucun compte avec cette adresse. Le client doit d'abord créer son compte.");
    await admin("rattacher", { id: c.id, paiement: b.dataset.rattacher });
    tout();
  } catch (e) { alert(e.message); }
});

$("#f-offrir").addEventListener("click", () => {
  const j = Number($("#f-jours").value);
  action("offrir", { jours: j }, `Offrir ${j} jours d'accès à ce client ?`);
});
$("#f-arreter").addEventListener("click", () => action("arreter", {}, "Arrêter l'accès de ce client maintenant ? (il ne sera pas remboursé)"));
$("#f-pcs-raz").addEventListener("click", () => action("pcs", {}, "Déconnecter tous les PC de ce client ? Il devra se reconnecter dans le logiciel."));
$("#f-bloquer").addEventListener("click", (ev) => action("bloquer", { bloque: !!ev.target.dataset.bloque }, ev.target.dataset.bloque ? "Bloquer ce compte ? Le client ne pourra plus se connecter." : ""));
$("#f-verifier").addEventListener("click", () => action("verifier", {}));
$("#f-note-enregistrer").addEventListener("click", () => action("note", { note: $("#f-note").value }));
$("#f-supprimer").addEventListener("click", async () => {
  if (!confirm("Supprimer définitivement ce compte ? Ses paiements restent dans la comptabilité.")) return;
  try { await admin("supprimer", { id: clientOuvert }); $("#fiche").close(); tout(); } catch (e) { alert(e.message); }
});
$("#f-fermer").addEventListener("click", () => $("#fiche").close());
