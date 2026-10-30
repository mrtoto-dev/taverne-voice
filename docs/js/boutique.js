// Boutique : choisir une formule, être connecté, payer sur Ko-fi, puis attendre l'activation.
"use strict";
(() => {
  const $ = (s) => document.querySelector(s);
  const K = window.TAVERNE.kofi;
  const LIENS = { mensuel: K.mensuel, trimestre: K.trimestre, annuel: K.annuel };
  let formule = new URLSearchParams(location.search).get("formule");
  if (!LIENS.hasOwnProperty(formule)) formule = "mensuel";
  let infos = null;
  let finAvant = 0;
  let attente = null;

  function afficherFormules() {
    for (const b of document.querySelectorAll("[data-formule]")) b.setAttribute("aria-pressed", String(b.dataset.formule === formule));
    const f = TV.FORMULES[formule];
    $("#b-payer").textContent = TV.t(`Payer ${f.prix} sur Ko-fi`, `Pay ${f.prix} on Ko-fi`);
    $("#b-detail").textContent = formule === "mensuel"
      ? TV.t("Abonnement mensuel Ko-fi : tu peux l'arrêter quand tu veux depuis ton compte Ko-fi, l'accès reste jusqu'à la fin du mois payé.",
        "Monthly Ko-fi subscription: you can stop it anytime from your Ko-fi account, and access stays until the end of the paid month.")
      : TV.t(`Passe ${f.nom} payé une seule fois, sans renouvellement automatique. S'il te reste du temps, il s'ajoute à la suite.`,
        `${f.nom} pass paid once, no automatic renewal. If you have time left, it's added on top.`);
    const ouvert = !!LIENS[formule];
    $("#b-payer").hidden = !ouvert;
    $("#b-bientot").hidden = ouvert;
    majBouton();
  }

  function majBouton() {
    $("#b-payer").classList.toggle("desactive", !$("#b-accord").checked || !infos);
  }

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-formule]");
    if (b) { formule = b.dataset.formule; history.replaceState(null, "", "?formule=" + formule); afficherFormules(); }
  });
  $("#b-accord").addEventListener("change", majBouton);

  async function chargerCompte() {
    if (!TV.jeton()) return afficherCompte(null);
    try { infos = await TV.moi(); } catch (e) { infos = null; }
    afficherCompte(infos);
  }

  function afficherCompte(i) {
    const etape = $("#etape-compte");
    etape.classList.toggle("faite", !!i);
    if (i) {
      $("#b-compte").innerHTML = TV.t(`Connecté avec <strong>${TV.echapper(i.email)}</strong>. <a href="compte.html">Mon compte</a>`, `Signed in as <strong>${TV.echapper(i.email)}</strong>. <a href="compte.html">My account</a>`);
      $("#b-email").textContent = i.email;
      $("#b-email-zone").hidden = false;
      finAvant = i.abonnement.fin || 0;
      if (i.abonnement.actif) {
        $("#b-deja").hidden = false;
        $("#b-deja").textContent = i.abonnement.formule === "essai"
          ? TV.t(`Ton essai gratuit dure jusqu'au ${TV.date(i.abonnement.fin)}. Ton achat s'ajoutera à la suite : tu ne perds aucun jour.`, `Your free trial lasts until ${TV.date(i.abonnement.fin)}. Your purchase will be added on top: you don't lose a single day.`)
          : TV.t(`Tu as déjà accès jusqu'au ${TV.date(i.abonnement.fin)}. Un nouvel achat s'ajoute à la suite.`, `You already have access until ${TV.date(i.abonnement.fin)}. A new purchase is added on top.`);
      }
    } else {
      const r = encodeURIComponent(formule);
      $("#b-compte").innerHTML = `<a class="bouton petit" href="compte.html?vue=inscription&retour=boutique&formule=${r}>${TV.t("Créer mon compte", "Create my account")}</a>
        <a class="bouton second petit" href="compte.html?vue=connexion&retour=boutique&formule=${r}>${TV.t("J'ai déjà un compte", "I already have an account")}</a>`;
      $("#b-email-zone").hidden = true;
    }
    majBouton();
  }

  $("#b-copier").addEventListener("click", async (ev) => {
    try { await navigator.clipboard.writeText(infos.email); ev.target.textContent = TV.t("Copié", "Copied"); setTimeout(() => (ev.target.textContent = TV.t("Copier", "Copy")), 1400); } catch (e) {}
  });

  $("#b-payer").addEventListener("click", (ev) => {
    if (!infos) { ev.preventDefault(); $("#etape-compte").scrollIntoView({ behavior: "smooth", block: "center" }); return; }
    if (!$("#b-accord").checked) { ev.preventDefault(); $("#b-accord").focus(); $("#b-accord-zone").classList.add("a-cocher"); return; }
    ev.preventDefault();
    if (window.taverneMesure) window.taverneMesure("evenement", { type: "kofi", detail: formule, page: location.pathname });
    window.open(LIENS[formule], "kofi", "width=520,height=820");
    attendrePaiement();
  });

  // vérifie le compte toutes les 8 secondes jusqu'à ce que le paiement Ko-fi arrive
  function attendrePaiement() {
    $("#etape-activation").hidden = false;
    $("#b-attente").hidden = false;
    $("#b-active").hidden = true;
    $("#etape-activation").scrollIntoView({ behavior: "smooth", block: "center" });
    clearInterval(attente);
    let essais = 0;
    attente = setInterval(async () => {
      if (++essais > 150) { clearInterval(attente); return; } // 20 minutes
      try {
        const i = await TV.moi();
        if (i.abonnement.actif && i.abonnement.fin > finAvant + 3600000) {
          clearInterval(attente);
          $("#b-attente").hidden = true;
          $("#b-active").hidden = false;
          $("#b-fin").textContent = TV.date(i.abonnement.fin);
          $("#etape-activation").classList.add("faite");
        }
      } catch (e) {}
    }, 8000);
  }

  afficherFormules();
  chargerCompte();
})();
