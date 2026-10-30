// Accès au serveur des comptes (api.tavernevoice.fr) pour les pages du site.
"use strict";
window.TV = (() => {
  const API = window.TAVERNE.api;
  // pages anglaises (/en/) : <html lang="en">
  const EN = document.documentElement.lang === "en";
  const t = (fr, en) => (EN ? en : fr);
  const CLE = "taverne-jeton";
  const lireJeton = () => { try { return localStorage.getItem(CLE) || ""; } catch (e) { return ""; } };
  const ecrireJeton = (j) => { try { j ? localStorage.setItem(CLE, j) : localStorage.removeItem(CLE); } catch (e) {} };

  async function appel(chemin, corps, avecJeton) {
    const h = { "Content-Type": "application/json" };
    if (EN) h["X-Langue"] = "en";
    if (avecJeton) h.Authorization = "Bearer " + lireJeton();
    let r;
    try {
      r = await fetch(API + chemin, corps === undefined ? { headers: h } : { method: "POST", headers: h, body: JSON.stringify(corps) });
    } catch (e) {
      throw Object.assign(new Error(t("Le serveur ne répond pas. Vérifie ta connexion et réessaie.", "The server isn't responding. Check your connection and try again.")), { statut: 0 });
    }
    const d = await r.json().catch(() => ({}));
    if (!r.ok) {
      if (r.status === 401 && avecJeton) ecrireJeton("");
      throw Object.assign(new Error(d.erreur || t("Erreur ", "Error ") + r.status), { statut: r.status, extra: d });
    }
    return d;
  }

  const FORMULES = EN ? {
    mensuel: { nom: "Monthly", prix: "€4.99", detail: "per month, renews automatically" },
    trimestre: { nom: "3 months", prix: "€14.99", detail: "paid once" },
    annuel: { nom: "1 year", prix: "€59.99", detail: "paid once" },
    offert: { nom: "Free access", prix: "", detail: "" },
    essai: { nom: "Free trial", prix: "€0", detail: "14 days" },
  } : {
    mensuel: { nom: "Mensuel", prix: "4,99 €", detail: "par mois, renouvelé tout seul" },
    trimestre: { nom: "3 mois", prix: "14,99 €", detail: "payé une fois" },
    annuel: { nom: "1 an", prix: "59,99 €", detail: "payé une fois" },
    offert: { nom: "Accès offert", prix: "", detail: "" },
    essai: { nom: "Essai gratuit", prix: "0 €", detail: "14 jours" },
  };

  const date = (ms) => new Date(ms).toLocaleDateString(EN ? "en-GB" : "fr-FR", { day: "numeric", month: "long", year: "numeric" });
  const echapper = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  return { t, en: EN, appel, jeton: lireJeton, ecrireJeton, moi: () => appel("/compte", undefined, true), FORMULES, date, echapper };
})();
