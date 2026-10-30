// Page « Mon compte » : connexion, inscription, vérification, mot de passe oublié, tableau de bord.
"use strict";
(() => {
  const $ = (s) => document.querySelector(s);
  const params = new URLSearchParams(location.search);
  const retour = params.get("retour") === "boutique" ? "boutique.html" + (params.get("formule") ? "?formule=" + encodeURIComponent(params.get("formule")) : "") : "";
  let emailEnCours = "";

  const VUES = ["connexion", "inscription", "verif", "oubli", "oubli2", "tableau", "chargement"];
  function vue(nom) {
    for (const v of VUES) $("#vue-" + v).hidden = v !== nom;
    const premier = $("#vue-" + nom + " input");
    if (premier) premier.focus();
    window.scrollTo(0, 0);
  }

  function message(id, texte, ok) {
    const m = $(id);
    m.textContent = texte || "";
    m.className = "msg " + (ok ? "ok" : "erreur");
    m.hidden = !texte;
  }

  async function envoyer(form, fn) {
    const b = form.querySelector("button[type=submit]");
    const t = b.textContent;
    b.disabled = true; b.textContent = TV.t("Un instant…", "One moment…");
    try { await fn(); } finally { b.disabled = false; b.textContent = t; }
  }

  function connecte(jeton) {
    TV.ecrireJeton(jeton);
    if (retour) { location.href = retour; return; }
    afficherTableau();
  }

  // ---------------------------------------------------------------- formulaires
  $("#form-connexion").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      message("#msg-connexion", "");
      const email = $("#c-email").value.trim();
      try {
        const r = await TV.appel("/connexion", { email, mdp: $("#c-mdp").value });
        connecte(r.jeton);
      } catch (e) {
        if (e.extra && e.extra.aVerifier) { emailEnCours = email; $("#verif-email").textContent = email; vue("verif"); message("#msg-verif", e.message, true); return; }
        message("#msg-connexion", e.message);
      }
    });
  });

  $("#form-inscription").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      message("#msg-inscription", "");
      if ($("#i-mdp").value !== $("#i-mdp2").value) return message("#msg-inscription", TV.t("Les deux mots de passe ne sont pas pareils.", "The two passwords don't match."));
      if (!$("#i-accord").checked) return message("#msg-inscription", TV.t("Coche la case pour accepter les conditions.", "Check the box to accept the terms."));
      const email = $("#i-email").value.trim();
      try {
        const r = await TV.appel("/inscription", { email, mdp: $("#i-mdp").value, pseudo: $("#i-pseudo").value.trim() });
        if (r.aVerifier) { emailEnCours = email; $("#verif-email").textContent = email; vue("verif"); return; }
        connecte(r.jeton);
      } catch (e) { message("#msg-inscription", e.message); }
    });
  });

  $("#form-verif").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      try {
        const r = await TV.appel("/verifier", { email: emailEnCours, code: $("#v-code").value.trim() });
        connecte(r.jeton);
      } catch (e) { message("#msg-verif", e.message); }
    });
  });
  $("#renvoyer").addEventListener("click", async () => {
    await TV.appel("/renvoyer-code", { email: emailEnCours }).catch(() => {});
    message("#msg-verif", TV.t("Un nouveau code vient de partir. Regarde aussi dans tes spams.", "A new code is on its way. Check your spam folder too."), true);
  });

  $("#form-oubli").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      emailEnCours = $("#o-email").value.trim();
      try {
        await TV.appel("/oubli", { email: emailEnCours });
        $("#oubli-email").textContent = emailEnCours;
        vue("oubli2");
      } catch (e) { message("#msg-oubli", e.message); }
    });
  });
  $("#form-oubli2").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      try {
        const r = await TV.appel("/nouveau-mdp", { email: emailEnCours, code: $("#o-code").value.trim(), mdp: $("#o-mdp").value });
        connecte(r.jeton);
      } catch (e) { message("#msg-oubli2", e.message); }
    });
  });

  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("[data-vue]");
    if (a) { ev.preventDefault(); vue(a.dataset.vue); }
  });

  // ---------------------------------------------------------------- tableau de bord
  let infos = null;
  async function afficherTableau() {
    vue("chargement");
    try { infos = await TV.moi(); } catch (e) {
      if (e.statut === 401) { vue("connexion"); return; }
      $("#vue-chargement").innerHTML = `<p class="msg erreur">${TV.echapper(e.message)}</p>`;
      return;
    }
    const a = infos.abonnement;
    $("#t-nom").textContent = infos.pseudo || infos.email;
    $("#t-email").textContent = infos.email;
    $("#t-pseudo").value = infos.pseudo || "";
    const f = TV.FORMULES[a.formule] || { nom: "" };
    const statut = $("#t-statut");
    statut.classList.toggle("actif", a.actif);
    const essai = infos.essai || {};
    $("#t-essai").hidden = !essai.disponible;
    $("#t-essai-jours").textContent = (essai.jours || 14) + TV.t(" jours", " days");
    if (a.actif && a.formule === "essai") {
      const reste = Math.max(0, Math.ceil((a.fin - Date.now()) / 86400000));
      $("#t-statut-titre").textContent = TV.t(`Essai gratuit : encore ${reste} jour${reste > 1 ? "s" : ""}`, `Free trial: ${reste} day${reste > 1 ? "s" : ""} left`);
      $("#t-statut-detail").textContent = TV.t(`Version complète jusqu'au ${TV.date(a.fin)}. Ensuite, choisis une formule pour continuer : les jours d'essai restants sont gardés.`, `Full version until ${TV.date(a.fin)}. After that, choose a plan to continue: your remaining trial days are kept.`);
    } else if (a.actif) {
      $("#t-statut-titre").textContent = TV.t(`Version complète active${f.nom ? ", " + f.nom.toLowerCase() : ""}`, `Full version active${f.nom ? ", " + f.nom.toLowerCase() : ""}`);
      $("#t-statut-detail").textContent = a.mensuel
        ? TV.t(`Abonnement Ko-fi mensuel. Prochaine échéance vers le ${TV.date(a.fin)}.`, `Monthly Ko-fi subscription. Next payment around ${TV.date(a.fin)}.`)
        : TV.t(`Accès jusqu'au ${TV.date(a.fin)}.`, `Access until ${TV.date(a.fin)}.`);
    } else {
      $("#t-statut-titre").textContent = essai.disponible ? TV.t("Version démo pour l'instant", "Demo version for now") : TV.t("Pas d'abonnement en cours", "No active subscription");
      $("#t-statut-detail").textContent = a.fin ? TV.t(`Ton dernier accès s'est terminé le ${TV.date(a.fin)}.`, `Your last access ended on ${TV.date(a.fin)}.`)
        : essai.disponible ? TV.t("Commence ton essai gratuit dans le logiciel, ou choisis une formule.", "Start your free trial in the app, or choose a plan.") : TV.t("Choisis une formule pour débloquer la version complète.", "Choose a plan to unlock the full version.");
    }
    $("#t-acheter").textContent = a.actif && a.formule !== "essai" ? TV.t("Prolonger ou changer de formule", "Extend or change plan") : TV.t("Choisir une formule", "Choose a plan");
    $("#t-kofi").hidden = !a.mensuel;

    const pcs = infos.pcs.map((p) => `<li><span>${TV.echapper(p.nom || "PC " + p.pc)}<small>${TV.t("Code", "Code")} ${TV.echapper(p.pc)}, ${TV.t("vu le", "last seen")} ${TV.date(p.vu)}</small></span>
      <button class="bouton second petit" type="button" data-retirer="${TV.echapper(p.pc)}">${TV.t("Retirer", "Remove")}</button></li>`).join("");
    $("#t-pcs").innerHTML = pcs || TV.t(`<li><span>Aucun PC pour l'instant.<small>Dans Taverne Voice : « Démo : débloquer » → Mon compte.</small></span></li>`, `<li><span>No PCs yet.<small>In Taverne Voice: “Demo: unlock” → My account.</small></span></li>`);
    $("#t-pcs-compte").textContent = TV.t(`${infos.pcs.length} sur ${infos.pcMax}`, `${infos.pcs.length} of ${infos.pcMax}`);

    const pa = infos.paiements.map((p) => `<li><span>${TV.echapper((TV.FORMULES[p.formule] || { nom: p.type }).nom)}<small>${TV.date(p.quand)}</small></span>
      <span>${p.montant ? TV.echapper(p.montant + " " + p.devise) : TV.t("offert", "free")}</span></li>`).join("");
    $("#t-paiements").innerHTML = pa || TV.t(`<li><span>Aucun paiement pour l'instant.</span></li>`, `<li><span>No payments yet.</span></li>`);
    vue("tableau");
  }

  $("#t-pcs").addEventListener("click", async (ev) => {
    const b = ev.target.closest("[data-retirer]");
    if (!b || !confirm(TV.t("Retirer ce PC ? Taverne Voice y repassera en démo, et sa place se libère pour un autre PC.", "Remove this PC? Taverne Voice will go back to demo there, and its spot frees up for another PC."))) return;
    try { await TV.appel("/compte/pc/retirer", { pc: b.dataset.retirer }, true); afficherTableau(); } catch (e) { alert(e.message); }
  });
  $("#form-pseudo").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      try { await TV.appel("/compte/pseudo", { pseudo: $("#t-pseudo").value.trim() }, true); message("#msg-pseudo", TV.t("Enregistré. Il s'affichera dans le logiciel à la prochaine actualisation.", "Saved. It will show up in the app at the next refresh."), true); }
      catch (e) { message("#msg-pseudo", e.message); }
    });
  });
  $("#form-mdp").addEventListener("submit", (ev) => {
    ev.preventDefault();
    envoyer(ev.target, async () => {
      try {
        await TV.appel("/compte/mdp", { ancien: $("#m-ancien").value, nouveau: $("#m-nouveau").value }, true);
        ev.target.reset();
        message("#msg-mdp", TV.t("Mot de passe changé.", "Password changed."), true);
      } catch (e) { message("#msg-mdp", e.message); }
    });
  });
  $("#t-deconnexion").addEventListener("click", async () => {
    await TV.appel("/compte/deconnexion", {}, true).catch(() => {});
    TV.ecrireJeton("");
    vue("connexion");
  });
  $("#t-supprimer").addEventListener("click", async () => {
    const mdp = prompt(TV.t("Pour supprimer ton compte, tape ton mot de passe. Tes PC seront déconnectés et ton accès s'arrêtera. Ça ne s'annule pas.", "To delete your account, type your password. Your PCs will be signed out and your access will stop. This can't be undone."));
    if (!mdp) return;
    try { await TV.appel("/compte/supprimer", { mdp }, true); TV.ecrireJeton(""); alert(TV.t("Ton compte est supprimé.", "Your account has been deleted.")); vue("connexion"); }
    catch (e) { alert(e.message); }
  });

  // ---------------------------------------------------------------- départ
  const v = params.get("vue");
  if (TV.jeton()) afficherTableau();
  else vue(VUES.includes(v) ? v : "connexion");
})();
