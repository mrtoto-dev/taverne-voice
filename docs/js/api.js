// Accès au serveur des comptes (api.tavernevoice.fr) pour les pages du site.
"use strict";
window.TV = (() => {
  const API = window.TAVERNE.api;
  const CLE = "taverne-jeton";
  const lireJeton = () => { try { return localStorage.getItem(CLE) || ""; } catch (e) { return ""; } };
  const ecrireJeton = (j) => { try { j ? localStorage.setItem(CLE, j) : localStorage.removeItem(CLE); } catch (e) {} };

  async function appel(chemin, corps, avecJeton) {
    const h = { "Content-Type": "application/json" };
    if (avecJeton) h.Authorization = "Bearer " + lireJeton();
    let r;
    try {
      r = await fetch(API + chemin, corps === undefined ? { headers: h } : { method: "POST", headers: h, body: JSON.stringify(corps) });
    } catch (e) {
      throw Object.assign(new Error("Le serveur ne répond pas. Vérifie ta connexion et réessaie."), { statut: 0 });
    }
    const d = await r.json().catch(() => ({}));
    if (!r.ok) {
      if (r.status === 401 && avecJeton) ecrireJeton("");
      throw Object.assign(new Error(d.erreur || "Erreur " + r.status), { statut: r.status, extra: d });
    }
    return d;
  }

  const FORMULES = {
    mensuel: { nom: "Mensuel", prix: "4,99 €", detail: "par mois, renouvelé tout seul" },
    trimestre: { nom: "3 mois", prix: "14,99 €", detail: "payé une fois" },
    annuel: { nom: "1 an", prix: "59,99 €", detail: "payé une fois" },
    offert: { nom: "Accès offert", prix: "", detail: "" },
    essai: { nom: "Essai gratuit", prix: "0 €", detail: "14 jours" },
  };

  const date = (ms) => new Date(ms).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
  const echapper = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  return { appel, jeton: lireJeton, ecrireJeton, moi: () => appel("/compte", undefined, true), FORMULES, date, echapper };
})();
