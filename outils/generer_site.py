#!/usr/bin/env python3
"""Génère le site de Taverne Voice dans docs/ (publié par GitHub Pages).

Utilisation : python3 outils/generer_site.py
Les pages sont écrites ici en HTML ; ce script ajoute l'en-tête, le menu et le pied.
"""
import html
import json
import random
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
DEPOT = "https://github.com/mrtoto-dev/taverne-voice"
TELECHARGER = DEPOT + "/releases/latest/download/"
# Où les gens demandent une clé : remplace par ton Discord, ta chaîne Twitch, un formulaire…
CONTACT = "mailto:contact@tavernevoice.fr"
CONTACT_TEXTE = "contact@tavernevoice.fr"
SITE = "https://tavernevoice.fr"

# Identité du vendeur, obligatoire sur un site qui vend (mentions légales et CGV).
# À compléter : tant qu'une valeur commence par « [ », la page affiche un rappel.
IDENTITE = {
    "nom": "[Prénom Nom ou nom de l'entreprise]",
    "statut": "[Micro-entrepreneur, SIRET 000 000 000 00000]",
    "adresse": "[Adresse postale]",
    "email": "contact@tavernevoice.fr",
}

PARTENAIRES = [
    {"chaine": "mrtoto_of", "nom": "MRTOTO_OF", "texte": "Le créateur de Taverne Voice, en live avec toutes les voix de la taverne."},
    {"chaine": "wapi_twitch", "nom": "Wapi_twitch", "texte": "Streameur partenaire : retrouve Taverne Voice dans ses lives."},
]

VOIX = json.loads((RACINE / "outils" / "voix.json").read_text(encoding="utf-8"))
VOIX_DEMO = ["normal", "chipmunk", "robot", "demon", "telephone"]
SYMBOLES = (RACINE / "outils" / "symboles.svg").read_text(encoding="utf-8")

e = html.escape

def icone(nom):
    return f'<svg class="ic" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-{nom}"/></svg>'

ICONE_TELECHARGER = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" style="stroke-width:2.2"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'
ICONE_TWITCH = '<svg class="ic" viewBox="0 0 48 48" aria-hidden="true" style="width:20px;height:20px"><path d="M10 6h30v20l-8 8h-7l-6 6v-6h-9V12Z"/><path d="M22 14v9M31 14v9"/></svg>'

MENU = [
    ("index.html#fonctions", "Fonctionnalités"),
    ("installation.html", "Guide"),
    ("partenaires.html", "Partenaires"),
    ("boutique.html", "Tarifs"),
]

GUIDE = [
    ("installation.html", "Installer"),
    ("obs-discord.html", "OBS et Discord"),
    ("voix.html", "Les voix"),
    ("soundboard.html", "Soundboard"),
    ("twitch-obs.html", "Twitch et overlay"),
    ("stream-deck.html", "Stream Deck"),
    ("licence.html", "Abonnement et clés"),
    ("faq.html", "Questions"),
]


def page(fichier, titre, description, corps, guide=False, noindex=False, scripts=""):
    actif = "installation.html" if fichier in [h for h, _ in GUIDE] else fichier
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == actif else ""}>{t}</a>' for h, t in MENU
    )
    if guide:
        sommaire = "".join(
            f'<a href="{h}"{" aria-current=\"page\"" if h == fichier else ""}>{t}</a>' for h, t in GUIDE
        )
        corps = f'<div class="enveloppe guide"><nav class="sommaire" aria-label="Guide"><p>Le guide</p>{sommaire}</nav><article>{corps}</article></div>'
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ""
    titre_complet = "Taverne Voice, le changeur de voix des streamers" if fichier == "index.html" else f"{titre} – Taverne Voice"
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre_complet)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(titre_complet)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE}/img/capture-voix.webp">
<link rel="canonical" href="{SITE}/{"" if fichier == "index.html" else fichier}">
{robots}
<link rel="icon" href="img/icone.png">
<link rel="stylesheet" href="site.css">
</head>
<body>
{SYMBOLES}
<header class="entete">
  <div class="enveloppe">
    <a class="marque" href="index.html"><img src="img/icone.png" alt=""><span>Taverne Voice</span></a>
    <nav class="nav" aria-label="Menu">{nav}<a class="bouton-compte" href="compte.html"{" aria-current=\"page\"" if fichier == "compte.html" else ""}>Mon compte</a></nav>
    <a class="bouton petit" href="{TELECHARGER}Taverne-Voice-Setup.exe">Télécharger</a>
  </div>
</header>
<main>
{corps}
</main>
<footer class="pied">
  <div class="enveloppe">
    <span>Taverne Voice, changeur de voix pour Windows. <span id="version-site"></span></span>
    <span class="pied-liens"><a href="faq.html">Aide</a><a href="{DEPOT}/releases">Versions</a><a href="cgv.html">CGV</a><a href="confidentialite.html">Confidentialité</a><a href="mentions-legales.html">Mentions légales</a></span>
  </div>
</footer>
{scripts}
<script>
fetch("https://api.github.com/repos/mrtoto-dev/taverne-voice/releases/latest")
  .then((r) => r.ok ? r.json() : null)
  .then((r) => {{ if (r && r.tag_name) document.querySelector("#version-site").textContent = "Dernière version : " + r.tag_name.replace(/^v/, "") + "."; }})
  .catch(() => {{}});
</script>
</body>
</html>
"""


def bock(v, taille_classe=""):
    libre = v["id"] in VOIX_DEMO
    return (f'<span class="bock{" libre" if libre else ""}{taille_classe}" style="--c:{v["couleur"]};--r:{random.uniform(-9, 9):.1f}deg" '
            f'tabindex="0" aria-label="{e(v["nom"])}{" (démo)" if libre else ""}">{icone(v["icone"])}'
            f'<span class="infobulle">{e(v["nom"])}</span></span>')


def accueil():
    random.seed(7)
    mur = "".join(bock(v) for v in VOIX)
    partenaires = "".join(carte_partenaire(p) for p in PARTENAIRES)
    return page("index.html", "Accueil",
        "Change ta voix en direct sur Twitch et Discord : 33 voix, un soundboard, les points de chaîne Twitch, un overlay OBS et des plugins pour tous les Stream Deck.", f"""
<div class="enveloppe heros2">
  <div>
    <h1>Taverne Voice</h1>
    <p class="chapo">Le changeur de voix des streamers. 33 voix, un soundboard, les points de chaîne Twitch et ton Stream Deck, dans un seul logiciel.</p>
    <div class="actions">
      <a class="bouton" href="{TELECHARGER}Taverne-Voice-Setup.exe">{ICONE_TELECHARGER}Télécharger gratuitement</a>
      <a class="bouton second" href="boutique.html">Voir les formules</a>
    </div>
    <p class="petit-texte">Démo gratuite, sans limite de temps. Windows 10 et 11.</p>
  </div>
  <div class="vitrine">
    <div class="fenetre-app"><img src="img/capture-voix-petit.webp" srcset="img/capture-voix-petit.webp 1360w, img/capture-voix.webp 2720w" sizes="(max-width: 900px) 100vw, 640px" width="1360" height="820" alt="La fenêtre de Taverne Voice : les voix en sous-bocks colorés et les réglages de la voix French Touch"></div>
    <img class="bulle-overlay" src="img/capture-overlay.webp" width="460" height="140" alt="L'overlay OBS : « Wapi_twitch t'a mis la voix Chipmunk », 17 secondes restantes">
  </div>
</div>

<section class="section" id="fonctions">
  <div class="enveloppe">
    <div class="fonction">
      <div>
        <h2>33 voix, réglées pour le live</h2>
        <p>Un clic sur un sous-bock et tout ton chat t'entend avec. <kbd>F8</kbd> coupe l'effet, même en plein jeu.</p>
        <ul>
          <li>Autotune, vocodeur French Touch, robots, démons, ambiances de grotte ou de stade</li>
          <li>Des curseurs pour régler chaque voix et enregistrer les tiennes</li>
          <li>OBS et Discord la reçoivent par un câble audio virtuel, installé avec le logiciel</li>
        </ul>
      </div>
      <div class="capture"><img src="img/capture-voix-petit.webp" loading="lazy" width="1360" height="820" alt="Les voix de Taverne Voice"></div>
    </div>
    <div class="fonction inverse">
      <div>
        <h2>Un soundboard rangé</h2>
        <p>Les sons tendance de Myinstants en un clic, ou tes propres MP3. Range-les par dossiers et donne-leur un raccourci.</p>
        <ul>
          <li>Dossiers : Mèmes, Bruitages, Musiques…</li>
          <li>Ta voix baisse toute seule pendant qu'un son joue</li>
          <li>Un raccourci clavier par son, même en jeu</li>
        </ul>
      </div>
      <div class="capture"><img src="img/capture-soundboard-petit.webp" loading="lazy" width="1360" height="820" alt="Le soundboard de Taverne Voice avec ses dossiers"></div>
    </div>
    <div class="fonction">
      <div>
        <h2>Tes viewers prennent le micro</h2>
        <p>Relie ta chaîne Twitch : tes viewers dépensent leurs points de chaîne pour te mettre une voix pendant 30 secondes ou lancer un son. L'overlay OBS l'affiche dans ton live, avec le compte à rebours.</p>
        <ul>
          <li>Les récompenses se créent depuis le logiciel</li>
          <li>Remboursées toutes seules si le logiciel ne peut pas les jouer</li>
          <li>Overlay en source navigateur, dans le coin de ton choix</li>
        </ul>
        <p><a href="twitch-obs.html">Voir comment ça marche</a></p>
      </div>
      <div class="capture"><img src="img/capture-twitch-petit.webp" loading="lazy" width="1360" height="820" alt="L'onglet Twitch et OBS de Taverne Voice"></div>
    </div>
    <div class="fonction inverse">
      <div>
        <h2>Ton Stream Deck, quelle que soit la marque</h2>
        <p>Une touche par son, une touche par voix. Elles s'allument quand le son joue ou quand la voix est active.</p>
        <p><a class="bouton second petit" href="stream-deck.html">Installer le plugin</a></p>
      </div>
      <div class="marques" style="margin-top:0">
        <div class="carte-marque"><h3>Elgato</h3><p>Stream Deck, MK.2, XL, Mini, +, Neo.</p></div>
        <div class="carte-marque"><h3>StreamDock</h3><p>Mars Gaming, Mirabox, Ajazz, Soomfon.</p></div>
        <div class="carte-marque"><h3>Ulanzi</h3><p>Stream Controller D200, D200H, D200X.</p></div>
        <div class="carte-marque"><h3>Les autres</h3><p>Razer, Loupedeck, Touch Portal, avec des raccourcis.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Toutes les voix de la taverne</h2>
    <p class="intro">Les 5 voix allumées marchent dans la démo. Les 28 autres se débloquent avec un abonnement.</p>
    <div class="mur" aria-label="Les 33 voix" style="margin-top:22px">{mur}</div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Ils streament avec Taverne Voice</h2>
    <p class="intro">Les streamers partenaires de la taverne. Passe leur dire bonjour.</p>
    <div class="partenaires">{partenaires}</div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Les formules</h2>
    <p class="intro">La démo est gratuite et sans limite de temps. Un abonnement débloque tout, sur 2 PC.</p>
    {cartes_formules()}
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Prêt en trois minutes</h2>
    <ol class="etapes">
      <li><h3>Installe</h3><p>L'installateur ajoute le logiciel, le câble audio gratuit de VB-Audio et le plugin de ton Stream Deck.</p></li>
      <li><h3>Branche</h3><p>Dans OBS et Discord, choisis <strong>CABLE Output</strong> comme micro. <a href="obs-discord.html">Voir comment</a>.</p></li>
      <li><h3>Choisis ta voix</h3><p>Un clic sur un sous-bock et tout le monde t'entend avec.</p></li>
    </ol>
  </div>
</section>
""", scripts=SCRIPT_PARTENAIRES)


SCRIPT_PARTENAIRES = """<script>
// le lecteur Twitch ne se charge qu'au clic (la page reste légère)
document.addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-chaine]");
  if (!b) return;
  const parents = ["tavernevoice.fr", "www.tavernevoice.fr", location.hostname].filter((v, i, a) => a.indexOf(v) === i).map((p) => "&parent=" + p).join("");
  const f = document.createElement("iframe");
  f.src = "https://player.twitch.tv/?channel=" + encodeURIComponent(b.dataset.chaine) + parents + "&muted=false&autoplay=true";
  f.allow = "autoplay; fullscreen";
  f.allowFullscreen = true;
  f.title = "Live Twitch de " + b.dataset.chaine;
  b.parentElement.replaceChildren(f);
});
</script>"""


def carte_partenaire(p):
    return f"""<article class="partenaire">
  <div class="ecran"><button type="button" data-chaine="{e(p["chaine"])}">{ICONE_TWITCH}Regarder le live</button></div>
  <div class="infos">
    <span class="pastille-p">{e(p["nom"][0])}</span>
    <div><h3>{e(p["nom"])}</h3><p>{e(p["texte"])}</p></div>
    <a class="bouton second petit" href="https://www.twitch.tv/{e(p["chaine"])}" target="_blank" rel="noopener">Suivre</a>
  </div>
</article>"""


def cartes_formules(lien=True):
    def carte(id_, nom, prix, unite, texte, mise=False, etiquette=""):
        bouton = f'<a class="bouton{"" if mise else " second"}" href="boutique.html?formule={id_}">Choisir</a>' if lien else ""
        return f"""<div class="formule{" mise-en-avant" if mise else ""}">
      {f'<span class="etiquette-f">{etiquette}</span>' if etiquette else ""}
      <h3>{nom}</h3>
      <div class="prix">{prix} <small>{unite}</small></div>
      <p>{texte}</p>
      {bouton}
    </div>"""
    return f"""<div class="formules">
    {carte("mensuel", "Mensuel", "4,99 €", "par mois", "Renouvelé tout seul. Tu l'arrêtes quand tu veux depuis Ko-fi.", True, "Le plus souple")}
    {carte("trimestre", "3 mois", "14,99 €", "une fois", "Trois mois d'accès, sans renouvellement automatique.")}
    {carte("annuel", "1 an", "59,99 €", "une fois", "Une année entière, payée une seule fois, sans renouvellement.")}
  </div>
  <p class="note-formules">Chaque formule débloque les 33 voix, les réglages, le soundboard sans limite, les points de chaîne Twitch, l'overlay OBS et les plugins Stream Deck. Paiement sécurisé par Ko-fi (carte ou PayPal).</p>"""


def partenaires_page():
    return page("partenaires.html", "Partenaires", "Les streamers partenaires de Taverne Voice : MRTOTO_OF et Wapi_twitch.", f"""
<div class="enveloppe page-etroite">
  <h1>Partenaires</h1>
  <p class="chapo">Les streamers qui font vivre la taverne. Lance leur live directement ici.</p>
  <div class="partenaires">{"".join(carte_partenaire(p) for p in PARTENAIRES)}</div>
  <div class="carte" style="margin-top:28px">
    <h2>Devenir partenaire</h2>
    <p>Tu streames avec Taverne Voice et tu veux apparaître ici ? Écris à <a href="{CONTACT}">{CONTACT_TEXTE}</a> avec le lien de ta chaîne.</p>
  </div>
</div>
""", scripts=SCRIPT_PARTENAIRES)


def boutique():
    return page("boutique.html", "Tarifs", "Les formules de Taverne Voice : 4,99 € par mois, 14,99 € pour 3 mois ou 59,99 € pour un an.", f"""
<div class="enveloppe page-etroite">
  <h1>Débloquer Taverne Voice</h1>
  <p class="chapo">Choisis ta formule, crée ton compte, paie sur Ko-fi : ton logiciel se débloque tout seul.</p>
  {cartes_formules(lien=False).replace('<div class="formules">', '<div class="formules" hidden>')}
  <ol class="etapes-achat">
    <li>
      <h3>Choisis ta formule</h3>
      <div class="choix-formule">
        <button type="button" data-formule="mensuel" aria-pressed="true"><strong>4,99 €</strong>par mois</button>
        <button type="button" data-formule="trimestre" aria-pressed="false"><strong>14,99 €</strong>pour 3 mois</button>
        <button type="button" data-formule="annuel" aria-pressed="false"><strong>59,99 €</strong>pour 1 an</button>
      </div>
      <p id="b-detail"></p>
    </li>
    <li id="etape-compte">
      <h3>Ton compte Taverne Voice</h3>
      <p>Il relie ton paiement à ton logiciel, sur 2 PC maximum.</p>
      <div class="ligne-actions" id="b-compte"></div>
      <p class="msg ok" id="b-deja" hidden></p>
    </li>
    <li>
      <h3>Paie sur Ko-fi</h3>
      <div id="b-email-zone" hidden>
        <p>Sur Ko-fi, utilise <strong>exactement la même adresse e-mail</strong> que ton compte :</p>
        <p class="ligne-actions"><span class="email-rappel" id="b-email"></span><button class="lien-bouton" type="button" id="b-copier">Copier</button></p>
      </div>
      <label class="ligne-actions" id="b-accord-zone" style="margin:12px 0;align-items:flex-start;gap:10px;color:var(--parchemin);font-size:15px">
        <input type="checkbox" id="b-accord" style="margin-top:4px;width:18px;height:18px">
        <span>J'accepte les <a href="cgv.html" target="_blank">conditions de vente</a>. Je demande l'accès tout de suite et je renonce donc à mon droit de rétractation de 14 jours pour ce contenu numérique.</span>
      </label>
      <a class="bouton" id="b-payer" href="#" rel="noopener">Payer sur Ko-fi</a>
      <p class="msg erreur" id="b-bientot" hidden>Le paiement ouvre très bientôt. Reviens dans quelques jours !</p>
    </li>
    <li id="etape-activation" hidden>
      <h3>Activation</h3>
      <div id="b-attente"><p>Dès que Ko-fi confirme ton paiement, ton compte s'active tout seul. Garde cette page ouverte…</p></div>
      <div id="b-active" hidden>
        <p class="msg ok">C'est activé, merci ! Ton accès va jusqu'au <strong id="b-fin"></strong>.</p>
        <p>Dans Taverne Voice, clique sur <strong>Démo : débloquer</strong>, onglet <strong>Mon compte</strong>, et connecte-toi.</p>
        <a class="bouton second petit" href="{TELECHARGER}Taverne-Voice-Setup.exe">{ICONE_TELECHARGER}Télécharger Taverne Voice</a>
      </div>
    </li>
  </ol>
  <p class="note-formules">Paiement sécurisé par Ko-fi, par carte ou PayPal. L'abonnement mensuel s'arrête quand tu veux depuis ton compte Ko-fi ; les passes 3 mois et 1 an ne se renouvellent pas. Une question ? <a href="{CONTACT}">{CONTACT_TEXTE}</a>.</p>
</div>
<style>.formule .bouton{{display:none}} #b-payer.desactive{{opacity:.55}} #b-accord-zone.a-cocher span{{color:var(--lanterne)}}</style>
""", scripts='<script src="config.js"></script><script src="js/api.js"></script><script src="js/boutique.js"></script>')


def compte():
    return page("compte.html", "Mon compte", "Ton compte Taverne Voice : abonnement, PC reliés et paiements.", f"""
<div class="enveloppe page-etroite">
  <div id="vue-chargement" hidden><p>Chargement…</p></div>

  <section class="carte" id="vue-connexion" hidden style="max-width:520px">
    <h2>Connexion</h2>
    <p>Avec ton compte Taverne Voice.</p>
    <form class="formulaire" id="form-connexion">
      <label>Adresse e-mail<input type="email" id="c-email" autocomplete="username" required></label>
      <label>Mot de passe<input type="password" id="c-mdp" autocomplete="current-password" required></label>
      <p class="msg erreur" id="msg-connexion" hidden></p>
      <button class="bouton" type="submit">Me connecter</button>
    </form>
    <p style="margin-top:18px"><a href="#" data-vue="oubli">Mot de passe oublié ?</a></p>
    <p>Pas encore de compte ? <a href="#" data-vue="inscription">Crée-le en une minute</a>.</p>
  </section>

  <section class="carte" id="vue-inscription" hidden style="max-width:520px">
    <h2>Créer mon compte</h2>
    <p>Utilise la même adresse que sur Ko-fi : c'est elle qui relie ton paiement à ton compte.</p>
    <form class="formulaire" id="form-inscription">
      <label>Adresse e-mail<input type="email" id="i-email" autocomplete="email" required></label>
      <label>Pseudo (affiché dans le logiciel)<input id="i-pseudo" maxlength="40" placeholder="Ton pseudo Twitch par exemple"></label>
      <label>Mot de passe (8 caractères minimum)<input type="password" id="i-mdp" autocomplete="new-password" minlength="8" required></label>
      <label>Encore une fois<input type="password" id="i-mdp2" autocomplete="new-password" minlength="8" required></label>
      <label style="flex-direction:row;gap:10px;align-items:flex-start"><input type="checkbox" id="i-accord" style="width:18px;height:18px;margin-top:3px"><span>J'accepte les <a href="cgv.html" target="_blank">conditions de vente</a> et la <a href="confidentialite.html" target="_blank">politique de confidentialité</a>.</span></label>
      <p class="msg erreur" id="msg-inscription" hidden></p>
      <button class="bouton" type="submit">Créer mon compte</button>
    </form>
    <p style="margin-top:18px">Déjà un compte ? <a href="#" data-vue="connexion">Me connecter</a></p>
  </section>

  <section class="carte" id="vue-verif" hidden style="max-width:520px">
    <h2>Confirme ton adresse</h2>
    <p>On vient d'envoyer un code à 6 chiffres à <strong id="verif-email"></strong>. Regarde aussi dans tes spams.</p>
    <form class="formulaire" id="form-verif">
      <label>Code<input id="v-code" class="code-saisie" inputmode="numeric" maxlength="6" autocomplete="one-time-code" required></label>
      <p class="msg" id="msg-verif" hidden></p>
      <button class="bouton" type="submit">Confirmer</button>
    </form>
    <p style="margin-top:18px"><button class="lien-bouton" type="button" id="renvoyer">Renvoyer un code</button></p>
  </section>

  <section class="carte" id="vue-oubli" hidden style="max-width:520px">
    <h2>Mot de passe oublié</h2>
    <p>On t'envoie un code pour en choisir un nouveau.</p>
    <form class="formulaire" id="form-oubli">
      <label>Adresse e-mail<input type="email" id="o-email" autocomplete="email" required></label>
      <p class="msg erreur" id="msg-oubli" hidden></p>
      <button class="bouton" type="submit">Envoyer le code</button>
    </form>
    <p style="margin-top:18px"><a href="#" data-vue="connexion">Retour à la connexion</a></p>
  </section>

  <section class="carte" id="vue-oubli2" hidden style="max-width:520px">
    <h2>Nouveau mot de passe</h2>
    <p>Si un compte existe pour <strong id="oubli-email"></strong>, un code vient de partir.</p>
    <form class="formulaire" id="form-oubli2">
      <label>Code<input id="o-code" class="code-saisie" inputmode="numeric" maxlength="6" autocomplete="one-time-code" required></label>
      <label>Nouveau mot de passe<input type="password" id="o-mdp" autocomplete="new-password" minlength="8" required></label>
      <p class="msg erreur" id="msg-oubli2" hidden></p>
      <button class="bouton" type="submit">Changer mon mot de passe</button>
    </form>
  </section>

  <div id="vue-tableau" hidden>
    <h1 style="font-size:clamp(44px,7vw,72px)">Bonjour <span id="t-nom"></span></h1>
    <p style="color:var(--parchemin)">Connecté avec <span id="t-email"></span>.</p>
    <div class="statut-abo" id="t-statut"><span class="point"></span><div><strong id="t-statut-titre"></strong><span id="t-statut-detail"></span></div></div>
    <div class="ligne-actions">
      <a class="bouton" id="t-acheter" href="boutique.html">Choisir une formule</a>
      <a class="bouton second" id="t-kofi" href="https://ko-fi.com/" target="_blank" rel="noopener" hidden>Gérer mon abonnement sur Ko-fi</a>
      <a class="bouton second" href="{TELECHARGER}Taverne-Voice-Setup.exe">{ICONE_TELECHARGER}Télécharger</a>
    </div>
    <p class="note-formules">Pour arrêter l'abonnement mensuel : sur Ko-fi, menu <em>Account &amp; Billing</em>, puis <em>Subscriptions</em>. Ton accès reste jusqu'à la fin du mois payé.</p>

    <div class="colonnes" style="margin-top:26px">
      <section class="carte">
        <h2>Mes PC <small style="font:500 15px Rubik,sans-serif;color:var(--parchemin)" id="t-pcs-compte"></small></h2>
        <p>Retire un PC pour libérer sa place (nouvel ordinateur, Windows réinstallé…).</p>
        <ul class="liste-simple" id="t-pcs"></ul>
      </section>
      <section class="carte">
        <h2>Mes paiements</h2>
        <ul class="liste-simple" id="t-paiements"></ul>
      </section>
    </div>

    <div class="colonnes" style="margin-top:18px">
      <section class="carte">
        <h2>Mon pseudo</h2>
        <form class="formulaire" id="form-pseudo">
          <label>Affiché dans le logiciel<input id="t-pseudo" maxlength="40"></label>
          <p class="msg" id="msg-pseudo" hidden></p>
          <button class="bouton second petit" type="submit">Enregistrer</button>
        </form>
      </section>
      <section class="carte">
        <h2>Mot de passe</h2>
        <form class="formulaire" id="form-mdp">
          <label>Mot de passe actuel<input type="password" id="m-ancien" autocomplete="current-password" required></label>
          <label>Nouveau mot de passe<input type="password" id="m-nouveau" autocomplete="new-password" minlength="8" required></label>
          <p class="msg" id="msg-mdp" hidden></p>
          <button class="bouton second petit" type="submit">Changer</button>
        </form>
      </section>
    </div>
    <p class="ligne-actions" style="margin-top:24px">
      <button class="bouton second" type="button" id="t-deconnexion">Me déconnecter</button>
      <button class="lien-bouton" type="button" id="t-supprimer" style="color:var(--braise)">Supprimer mon compte</button>
    </p>
  </div>
</div>
""", noindex=True, scripts='<script src="config.js"></script><script src="js/api.js"></script><script src="js/compte.js"></script>')


def twitch_obs():
    return page("twitch-obs.html", "Twitch et overlay", "Les points de chaîne Twitch et l'overlay OBS de Taverne Voice.", """
<h1>Twitch et overlay</h1>
<p class="chapo">Tes viewers dépensent leurs points de chaîne pour te changer la voix ou lancer un son, et l'overlay l'affiche dans ton live.</p>
<div class="encadre"><p>Les points de chaîne et l'overlay font partie de l'<a href="boutique.html">abonnement</a>. Les points de chaîne demandent d'être affilié ou partenaire Twitch.</p></div>

<h2>Relier ta chaîne</h2>
<ol>
  <li>Dans Taverne Voice, ouvre l'onglet <strong>Twitch et OBS</strong>.</li>
  <li>Clique sur <strong>Relier ma chaîne Twitch</strong>. Une page Twitch s'ouvre avec un code.</li>
  <li>Connecte-toi avec le compte de ta chaîne et tape le code affiché dans le logiciel.</li>
</ol>
<p>Taverne Voice ne voit jamais ton mot de passe Twitch. Tu peux délier ta chaîne à tout moment ; les récompenses créées par Taverne Voice sont alors retirées.</p>

<h2>Créer une récompense</h2>
<ol>
  <li>Choisis <strong>Changer ma voix</strong> (avec une durée) ou <strong>Lancer un son</strong>.</li>
  <li>Choisis la voix ou le son, le prix en points et le titre affiché sur Twitch.</li>
  <li>Clique sur <strong>Créer sur Twitch</strong>. La récompense apparaît tout de suite sur ta chaîne.</li>
</ol>
<p><strong>Tester</strong> joue la récompense sans Twitch, pour vérifier le rendu dans ton live. <strong>Mettre en pause</strong> la cache sur Twitch sans la supprimer.</p>
<ul>
  <li>Les voix passent l'une après l'autre : si deux viewers en demandent une en même temps, la deuxième attend son tour.</li>
  <li>À la fin, ta voix d'avant revient toute seule.</li>
  <li>Si le logiciel ne peut pas jouer la récompense (son coupé, voix supprimée…), les points sont rendus au viewer.</li>
</ul>

<h2>L'overlay OBS</h2>
<ol>
  <li>Dans OBS, ajoute une <strong>Source navigateur</strong>.</li>
  <li>Adresse : <code>http://127.0.0.1:47321/overlay</code>, largeur <strong>1920</strong>, hauteur <strong>1080</strong>.</li>
  <li>Dans Taverne Voice, choisis ce qu'il montre (voix active, sons en cours, points de chaîne), le coin de l'écran et la taille. Les changements s'appliquent sans toucher à OBS.</li>
</ol>
<p><img src="img/capture-overlay.webp" width="460" height="140" alt="L'overlay pendant une récompense Twitch" style="max-width:100%"></p>
""", guide=True)


def licence():
    return page("licence.html", "Abonnement et clés", "Débloquer la version complète de Taverne Voice avec un compte ou une clé.", f"""
<h1>Abonnement et clés</h1>
<p class="chapo">La démo marche sans limite de temps. Un abonnement débloque tout le reste.</p>

<div class="tableau"><table>
  <tr><th></th><th>Démo</th><th>Abonnement</th></tr>
  <tr><td>Voix</td><td>5</td><td>33, plus les tiennes</td></tr>
  <tr><td>Curseurs de réglage</td><td>non</td><td>oui</td></tr>
  <tr><td>Sons dans le soundboard</td><td>3</td><td>sans limite, en dossiers</td></tr>
  <tr><td>Points de chaîne et overlay OBS</td><td>non</td><td>oui</td></tr>
  <tr><td>Plugins Stream Deck</td><td>non</td><td>toutes les marques</td></tr>
  <tr><td>Nombre de PC</td><td>sans limite</td><td>2 par compte</td></tr>
</table></div>
<p><a class="bouton" href="boutique.html">Voir les formules</a></p>

<h2>Se connecter dans le logiciel</h2>
<ol>
  <li>Crée ton compte sur <a href="compte.html">Mon compte</a> et choisis ta formule dans la <a href="boutique.html">boutique</a>.</li>
  <li>Dans Taverne Voice, clique sur <strong>Démo : débloquer</strong>, onglet <strong>Mon compte</strong>.</li>
  <li>Entre ton adresse e-mail et ton mot de passe.</li>
</ol>
<p>Ton PC est relié à ton compte (2 PC maximum). La licence se renouvelle toute seule tant que ton abonnement est actif. Le logiciel marche aussi hors ligne pendant plusieurs semaines.</p>

<h2>Changer de PC</h2>
<p>Dans le logiciel : <strong>Réglages → Licence → Se déconnecter de ce PC</strong>. Ou sur le site, dans <a href="compte.html">Mon compte</a>, retire l'ancien PC. Puis connecte-toi sur le nouveau.</p>

<h2>Tu as reçu une clé</h2>
<p>Une clé commence par <code>TV1-</code> et t'a été donnée par le créateur (concours, partenaire…). Dans le logiciel : <strong>Démo : débloquer</strong>, onglet <strong>J'ai une clé</strong>, colle-la et clique sur <strong>Activer la clé</strong>.</p>
<div class="encadre"><p>Une clé ou un compte sont personnels. S'ils sont partagés, le créateur peut les désactiver : le logiciel repasse alors en démo.</p></div>
""", guide=True)


def bandeau_identite():
    manque = any(v.startswith("[") for v in IDENTITE.values())
    return '<div class="encadre alerte"><p>Informations du vendeur à compléter avant d\'ouvrir la boutique.</p></div>' if manque else ""


def mentions():
    i = IDENTITE
    return page("mentions-legales.html", "Mentions légales", "Mentions légales de tavernevoice.fr.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Mentions légales</h1>
{bandeau_identite()}
<h2>Éditeur</h2>
<p>{e(i["nom"])}<br>{e(i["statut"])}<br>{e(i["adresse"])}<br>Contact : <a href="mailto:{e(i["email"])}">{e(i["email"])}</a></p>
<h2>Hébergement</h2>
<p>Site : GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr Street, San Francisco, CA 94107, États-Unis.<br>
Serveur des comptes : Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
<h2>Propriété</h2>
<p>Le logiciel Taverne Voice, ses voix, ses icônes et ce site appartiennent à l'éditeur. Toute copie ou redistribution sans accord est interdite. Les sons Myinstants restent la propriété de leurs auteurs.</p>
</article></div>
""")


def cgv():
    i = IDENTITE
    return page("cgv.html", "Conditions de vente", "Conditions générales de vente de Taverne Voice.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Conditions de vente</h1>
{bandeau_identite()}
<p class="chapo">En vigueur au 27 octobre 2026.</p>
<h2>1. Vendeur</h2>
<p>{e(i["nom"])}, {e(i["statut"])}, {e(i["adresse"])}. Contact : {e(i["email"])}.</p>
<h2>2. Ce qui est vendu</h2>
<p>Un accès à la version complète du logiciel Taverne Voice pour Windows : toutes les voix, les réglages, le soundboard sans limite, les points de chaîne Twitch, l'overlay OBS et les plugins Stream Deck. L'accès est lié à un compte personnel et peut être utilisé sur 2 ordinateurs à la fois. La démo gratuite reste disponible sans achat.</p>
<h2>3. Prix et formules</h2>
<ul>
  <li><strong>Mensuel</strong> : 4,99 € par mois, renouvelé automatiquement chaque mois jusqu'à son arrêt.</li>
  <li><strong>3 mois</strong> : 14,99 €, payé une fois, sans renouvellement.</li>
  <li><strong>1 an</strong> : 59,99 €, payé une fois, sans renouvellement.</li>
</ul>
<p>Les prix sont en euros, toutes taxes comprises{"" if "TVA" in i["statut"] else " (TVA non applicable, article 293 B du CGI, si le vendeur est micro-entrepreneur)"}. Le paiement se fait sur Ko-fi, par carte bancaire ou PayPal. Ko-fi et ses prestataires de paiement traitent les données de paiement ; le vendeur n'y a pas accès.</p>
<h2>4. Accès</h2>
<p>L'accès s'active dès que Ko-fi confirme le paiement, sur le compte qui a la même adresse e-mail. Un nouvel achat s'ajoute à la suite de l'accès en cours.</p>
<h2>5. Arrêt de l'abonnement mensuel</h2>
<p>Le client arrête son abonnement mensuel quand il veut, sans frais, depuis son compte Ko-fi (<em>Account &amp; Billing → Subscriptions</em>). L'accès reste actif jusqu'à la fin de la période payée.</p>
<h2>6. Droit de rétractation</h2>
<p>Il s'agit d'un contenu numérique fourni immédiatement. Au moment de l'achat, le client demande expressément l'accès immédiat et reconnaît perdre son droit de rétractation de 14 jours (article L221-28 13° du Code de la consommation). En cas de problème technique empêchant d'utiliser le logiciel, le client peut écrire au vendeur pour trouver une solution ou obtenir un remboursement.</p>
<h2>7. Utilisation</h2>
<p>Le compte est personnel. Le partage de compte, la revente ou le contournement de la protection du logiciel peuvent entraîner la suspension de l'accès, sans remboursement. Le client respecte les droits d'auteur des sons qu'il diffuse.</p>
<h2>8. Garanties</h2>
<p>Le vendeur fait de son mieux pour que le logiciel fonctionne sur Windows 10 et 11 et soit mis à jour. Les garanties légales de conformité des contenus numériques s'appliquent.</p>
<h2>9. Litiges</h2>
<p>Ces conditions sont soumises au droit français. En cas de litige, le client peut recourir gratuitement à un médiateur de la consommation, ou à la plateforme européenne de règlement en ligne des litiges.</p>
</article></div>
""")


def confidentialite():
    i = IDENTITE
    return page("confidentialite.html", "Confidentialité", "Quelles données Taverne Voice garde, et pourquoi.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Confidentialité</h1>
{bandeau_identite()}
<p class="chapo">Ce que Taverne Voice garde, pourquoi, et comment le supprimer.</p>
<h2>Ce qui est gardé</h2>
<ul>
  <li><strong>Ton compte</strong> : adresse e-mail, pseudo, mot de passe (jamais en clair, seulement une empreinte).</li>
  <li><strong>Tes PC</strong> : un code de 8 caractères calculé à partir de l'identifiant Windows (il ne dit rien de ton PC), le nom de l'ordinateur et la dernière connexion.</li>
  <li><strong>Tes paiements</strong> : formule, montant, date et adresse e-mail envoyés par Ko-fi.</li>
  <li><strong>Un historique</strong> des connexions et des changements du compte, pour la sécurité.</li>
</ul>
<p>Le logiciel ne s'écoute pas : ta voix reste sur ton PC. Ta connexion Twitch reste chiffrée sur ton PC.</p>
<h2>Pourquoi</h2>
<p>Pour faire marcher ton accès (exécution du contrat), envoyer les codes de vérification, et respecter les obligations comptables.</p>
<h2>Qui les traite</h2>
<p>{e(i["nom"])}, responsable du traitement. Hébergement du serveur : Cloudflare. Envoi des e-mails : Brevo. Paiements : Ko-fi.</p>
<h2>Combien de temps</h2>
<p>Tant que ton compte existe. Les paiements sont gardés 10 ans pour la comptabilité.</p>
<h2>Tes droits</h2>
<p>Tu peux supprimer ton compte toi-même dans <a href="compte.html">Mon compte</a>. Pour toute autre demande (accès, correction, effacement) : <a href="mailto:{e(i["email"])}">{e(i["email"])}</a>. Tu peux aussi saisir la CNIL.</p>
<h2>Cookies</h2>
<p>Le site n'utilise pas de cookie publicitaire ni de mesure d'audience. Il garde seulement ta connexion dans ton navigateur. Le lecteur Twitch des partenaires ne se charge que si tu cliques dessus.</p>
</article></div>
""")



def installation():
    return page("installation.html", "Installer", "Installer Taverne Voice et le câble audio virtuel sur Windows.", f"""
<h1>Installer</h1>
<p class="chapo">Tout se fait avec un seul fichier. Il faut Windows 10 ou 11 et un micro.</p>

<h2>1. Télécharger</h2>
<p><a class="bouton" href="{TELECHARGER}Taverne-Voice-Setup.exe">{ICONE_TELECHARGER}Télécharger Taverne-Voice-Setup.exe</a></p>
<p>Tu préfères ne rien installer ? <a href="{TELECHARGER}Taverne-Voice.exe">Taverne-Voice.exe</a> est la version portable : un seul fichier à lancer, mais sans lancement avec Windows ni installation automatique du câble.</p>

<h2>2. Passer l'alerte de Windows</h2>
<p>Au premier lancement, Windows peut afficher « Windows a protégé votre ordinateur ». C'est normal pour un petit logiciel qui n'a pas encore de certificat payant.</p>
<ol>
  <li>Clique sur <strong>Informations complémentaires</strong>.</li>
  <li>Clique sur <strong>Exécuter quand même</strong>.</li>
</ol>

<h2>3. Choisir les options</h2>
<p>L'installateur te propose :</p>
<ul>
  <li><strong>Câble audio VB-Audio</strong> : indispensable, c'est lui qui amène ta voix modifiée dans OBS et Discord. Windows te demande ton accord, puis clique sur <em>Install Driver</em>. Redémarre ton PC après.</li>
  <li><strong>Plugin Stream Deck Elgato</strong>, <strong>plugin StreamDock et Ulanzi</strong> : cochés tout seuls si le logiciel de ton Stream Deck est installé.</li>
  <li><strong>Icône sur le Bureau</strong> et <strong>Lancer avec Windows</strong>.</li>
</ul>
<p>Le logiciel s'installe dans ton dossier utilisateur : pas besoin d'être administrateur.</p>

<h2>4. Premier lancement</h2>
<ol>
  <li>Ouvre <strong>Réglages</strong> (la roue en haut à droite).</li>
  <li><strong>Ton micro</strong> : ton vrai micro. Avec SteelSeries Sonar, choisis « SteelSeries Sonar - Microphone » pour garder ta réduction de bruit.</li>
  <li><strong>Sortie vers OBS et Discord</strong> : <code>CABLE Input</code>.</li>
  <li><strong>Casque</strong> : ton casque, pour t'entendre avec « M'entendre ».</li>
  <li>Clique sur <strong>Appliquer</strong>.</li>
</ol>
<p>Ensuite, <a href="obs-discord.html">branche ta voix dans OBS et Discord</a>.</p>

<h2>Mises à jour</h2>
<p>Le logiciel vérifie toutes les 5 minutes s'il existe une nouvelle version. Quand elle sort, Windows affiche une notification et un bouton <strong>Mettre à jour</strong> apparaît en haut de la fenêtre : un clic, et il se remplace tout seul. Tes réglages, tes voix et tes sons sont gardés.</p>

<h2>Désinstaller</h2>
<p>Paramètres de Windows → Applications → Applications installées → Taverne Voice → Désinstaller. On te demande si tu veux aussi supprimer tes réglages et tes sons.</p>
""", guide=True)


def obs_discord():
    return page("obs-discord.html", "OBS et Discord", "Brancher la voix de Taverne Voice dans OBS et dans Discord.", """
<h1>OBS et Discord</h1>
<p class="chapo">Taverne Voice envoie ta voix transformée dans <code>CABLE Input</code>. De l'autre côté du câble, <code>CABLE Output</code> se comporte comme un micro : c'est lui qu'OBS et Discord doivent écouter.</p>

<h2>OBS Studio</h2>
<ol>
  <li>Dans <strong>Sources</strong>, clique sur <strong>+</strong> puis <strong>Capture d'entrée audio</strong>.</li>
  <li>Appelle-la « Taverne Voice » et choisis le périphérique <code>CABLE Output (VB-Audio Virtual Cable)</code>.</li>
  <li>Coupe ton ancienne source micro (l'icône du haut-parleur dans le mélangeur), sinon on t'entend deux fois : une fois normal, une fois avec l'effet.</li>
</ol>
<div class="encadre"><p>Les sons du soundboard passent dans le même câble : pas besoin d'une autre source pour eux.</p></div>

<h2>Discord</h2>
<ol>
  <li>Paramètres utilisateur → <strong>Voix et vidéo</strong>.</li>
  <li><strong>Périphérique d'entrée</strong> : <code>CABLE Output</code>.</li>
  <li>Désactive la <strong>suppression du bruit</strong> (Krisp) et l'<strong>annulation de l'écho</strong> : elles prennent les effets pour du bruit et les abîment.</li>
  <li>Règle la sensibilité d'entrée à la main si ta voix est coupée par moments.</li>
</ol>

<h2>T'entendre</h2>
<p>Active <strong>M'entendre</strong> en bas de la fenêtre pour écouter ta voix modifiée dans ton casque. Garde-le coupé pendant le live si l'écho te gêne.</p>

<h2>Ça ne marche pas ?</h2>
<ul>
  <li>Le témoin <strong>Sortie</strong> en haut de la fenêtre est rouge : la sortie n'est pas <code>CABLE Input</code>, ou le câble n'est pas installé. Ouvre les Réglages.</li>
  <li>On ne t'entend pas du tout : vérifie que l'effet est actif (<kbd>F8</kbd>) et que le bon micro est choisi dans Taverne Voice.</li>
  <li>Plus de questions dans la <a href="faq.html">FAQ</a>.</li>
</ul>
""", guide=True)


def voix():
    categories = [("classiques", "Classiques"), ("musique", "Musique"), ("robots", "Robots"), ("creatures", "Créatures"), ("ambiances", "Ambiances")]
    blocs = ""
    for cid, cnom in categories:
        items = "".join(
            f'<div class="ligne-voix"><span class="bock{" libre" if v["id"] in VOIX_DEMO else ""}" style="--c:{v["couleur"]}">{icone(v["icone"])}</span>'
            f'<span><b>{e(v["nom"])}{"<span class=\"etiquette\">démo</span>" if v["id"] in VOIX_DEMO else ""}</b><small>{e(v["desc"])}</small></span></div>'
            for v in VOIX if v["cat"] == cid)
        blocs += f"<h2>{cnom}</h2><div class=\"liste-voix\">{items}</div>"
    return page("voix.html", "Les voix", "Les 33 voix de Taverne Voice : autotune, vocodeur, robots, créatures et ambiances.", f"""
<h1>Les voix</h1>
<p class="chapo">33 voix rangées en cinq familles. Les voix marquées « démo » marchent sans clé.</p>
<ul>
  <li>Clique sur une voix pour l'utiliser tout de suite.</li>
  <li><kbd>F8</kbd> coupe ou rallume l'effet, même quand tu es en jeu.</li>
  <li>Avec la version complète, les curseurs règlent la hauteur, l'autotune, le chœur, le vibrato, le vocodeur, le robot, l'écho, la grotte et le grain. <strong>Enregistrer ma voix</strong> la garde dans « Mes voix ».</li>
  <li>L'étoile à côté du nom range la voix dans tes favoris.</li>
</ul>
{blocs}
""", guide=True)


def soundboard():
    return page("soundboard.html", "Soundboard", "Le soundboard de Taverne Voice : sons Myinstants, MP3, raccourcis clavier.", """
<h1>Soundboard</h1>
<p class="chapo">Les sons partent dans OBS et Discord avec ta voix. Tu peux les lancer à la souris, au clavier ou depuis ton Stream Deck.</p>

<h2>Ajouter des sons</h2>
<ul>
  <li><strong>Myinstants</strong> : dans l'onglet Soundboard → Myinstants, écoute les sons tendance ou cherche un son, puis clique sur <strong>Ajouter</strong>.</li>
  <li><strong>Tes fichiers</strong> : <strong>Importer</strong>, ou glisse tes MP3 et WAV sur la fenêtre.</li>
</ul>
<div class="encadre"><p>La démo garde 3 sons. La <a href="licence.html">version complète</a> n'a pas de limite.</p></div>

<h2>Ranger en dossiers</h2>
<p>Clique sur <strong>+ Nouveau dossier</strong> au-dessus de tes sons (Mèmes, Bruitages, Musiques…). Glisse un son sur l'onglet d'un dossier pour l'y ranger, ou choisis son dossier dans son panneau. Les sons ajoutés pendant qu'un dossier est ouvert y vont directement.</p>

<h2>Baisser ta voix pendant les sons</h2>
<p>Dans le panneau de droite, active <strong>Baisser ma voix pendant les sons</strong> : tant qu'un son joue, ta voix baisse au niveau choisi, puis remonte en douceur. Pratique quand tu parles par-dessus un son.</p>

<h2>Régler un son</h2>
<p>Clique sur un son pour ouvrir son panneau : volume, nom, raccourci clavier et lien pour Stream Deck. Le raccourci marche même quand Taverne Voice est en arrière-plan.</p>
<p>« Tout arrêter » coupe tous les sons en cours ; tu peux lui donner un raccourci aussi.</p>

<h2>Droits d'auteur</h2>
<div class="encadre alerte"><p>Sur Twitch, un extrait de musique, de film ou de série peut être signalé et coupé dans tes rediffusions. Préfère les bruitages et les sons courts.</p></div>
""", guide=True)


def stream_deck():
    return page("stream-deck.html", "Stream Deck", "Installer le plugin Taverne Voice sur Elgato Stream Deck, StreamDock (Mars Gaming, Mirabox, Ajazz) et Ulanzi.", f"""
<h1>Stream Deck</h1>
<p class="chapo">Chaque marque a son plugin. Une fois installé, tu glisses une action Taverne Voice sur une touche et tu choisis le son ou la voix dans une liste.</p>
<div class="encadre"><p>Les plugins Stream Deck font partie de la <a href="licence.html">version complète</a>.</p></div>

<h2>Les actions</h2>
<div class="tableau"><table>
  <tr><th>Action</th><th>Ce que fait la touche</th></tr>
  <tr><td>Jouer un son</td><td>Joue le son choisi. La touche s'allume pendant qu'il joue.</td></tr>
  <tr><td>Changer de voix</td><td>Passe à la voix choisie. La touche s'allume quand cette voix est active.</td></tr>
  <tr><td>Changeur de voix on/off</td><td>Comme <kbd>F8</kbd> : active ou coupe l'effet.</td></tr>
  <tr><td>Tout arrêter</td><td>Coupe tous les sons en cours.</td></tr>
</table></div>
<p>Si Taverne Voice est fermé, le plugin le lance tout seul en arrière-plan.</p>

<h2 id="elgato">Elgato Stream Deck</h2>
<ol>
  <li>Dans Taverne Voice : <strong>Réglages → Stream Deck → Elgato Stream Deck → Installer le plugin</strong>.</li>
  <li>L'application Stream Deck s'ouvre et te demande de confirmer.</li>
</ol>
<p>Ou télécharge le plugin et double-clique dessus : <a class="bouton second petit" href="{TELECHARGER}Taverne-Voice.streamDeckPlugin">{ICONE_TELECHARGER}Plugin Elgato</a></p>

<h2 id="streamdock">StreamDock : Mars Gaming, Mirabox, Ajazz</h2>
<p>Les Stream Deck Mars Gaming (MSD-ONE, MSD-PRO…), Mirabox, Ajazz et Soomfon utilisent le logiciel <strong>StreamDock</strong>.</p>
<ol>
  <li>Lance StreamDock une fois, pour qu'il crée son dossier.</li>
  <li>Dans Taverne Voice : <strong>Réglages → Stream Deck → StreamDock → Installer le plugin</strong>.</li>
  <li>Ferme complètement StreamDock (clic droit sur son icône près de l'horloge → Quitter) et rouvre-le. « Taverne Voice » apparaît dans la liste des actions.</li>
</ol>
<details>
  <summary>Installer à la main</summary>
  <p><a class="bouton second petit" href="{TELECHARGER}Taverne-Voice-StreamDock.zip">{ICONE_TELECHARGER}Plugin StreamDock</a></p>
  <ol>
    <li>Ouvre le zip et copie le dossier <code>com.mrtoto.tavernevoice.sdPlugin</code>.</li>
    <li>Appuie sur <kbd>Windows</kbd> + <kbd>R</kbd>, tape <code>%appdata%\\HotSpot\\StreamDock\\plugins</code> et valide.</li>
    <li>Colle le dossier, puis redémarre StreamDock.</li>
  </ol>
</details>

<h2 id="ulanzi">Ulanzi</h2>
<ol>
  <li>Lance Ulanzi Studio une fois.</li>
  <li>Dans Taverne Voice : <strong>Réglages → Stream Deck → Ulanzi → Installer le plugin</strong>.</li>
  <li>Ferme complètement Ulanzi Studio et rouvre-le.</li>
</ol>
<details>
  <summary>Installer à la main</summary>
  <p><a class="bouton second petit" href="{TELECHARGER}Taverne-Voice-Ulanzi.zip">{ICONE_TELECHARGER}Plugin Ulanzi</a></p>
  <ol>
    <li>Ouvre le zip et copie le dossier <code>com.mrtoto.tavernevoice.ulanziPlugin</code>.</li>
    <li>Appuie sur <kbd>Windows</kbd> + <kbd>R</kbd>, tape <code>%appdata%\\Ulanzi\\UlanziDeck\\Plugins</code> et valide.</li>
    <li>Colle le dossier, puis redémarre Ulanzi Studio.</li>
  </ol>
</details>

<h2 id="autres">Les autres marques</h2>
<p>Razer Stream Controller, Loupedeck, Touch Portal ou n'importe quel logiciel qui sait ouvrir un fichier ou un lien :</p>
<ol>
  <li>Dans Taverne Voice : <strong>Réglages → Stream Deck → Créer les raccourcis Stream Deck</strong>.</li>
  <li>Le dossier <code>Documents\\Taverne Voice\\Stream Deck</code> s'ouvre, avec un fichier par son, par voix et par action.</li>
  <li>Dans le logiciel de ton Stream Deck, mets une action « Ouvrir » ou « Lancer un fichier » et choisis le fichier voulu.</li>
</ol>
<p>Tu peux aussi coller un lien dans une action « Site web » ou « URL » :</p>
<div class="tableau"><table>
  <tr><th>Lien</th><th>Effet</th></tr>
  <tr><td><code>taverne://son/Applaudissements</code></td><td>joue un son (par son nom)</td></tr>
  <tr><td><code>taverne://voix/robot</code></td><td>passe à une voix</td></tr>
  <tr><td><code>taverne://effet</code>, <code>/on</code>, <code>/off</code></td><td>active ou coupe l'effet</td></tr>
  <tr><td><code>taverne://stop</code></td><td>arrête tous les sons</td></tr>
  <tr><td><code>taverne://ouvrir</code></td><td>ouvre la fenêtre</td></tr>
</table></div>
<p>Le panneau de chaque son a un bouton <strong>Copier</strong> pour son lien.</p>
""", guide=True)


def faq():
    q = [
        ("Windows dit que le logiciel est dangereux. C'est un virus ?",
         "<p>Non. Windows SmartScreen se méfie de tous les logiciels qui n'ont pas encore de certificat de signature payant. Clique sur <strong>Informations complémentaires</strong> puis <strong>Exécuter quand même</strong>.</p>"),
        ("On ne m'entend pas dans Discord.",
         "<p>Vérifie que le périphérique d'entrée de Discord est <code>CABLE Output</code>, que la sortie de Taverne Voice est <code>CABLE Input</code>, et que la suppression du bruit de Discord est coupée. Le guide <a href=\"obs-discord.html\">OBS et Discord</a> détaille chaque étape.</p>"),
        ("J'entends un décalage dans ma voix.",
         "<p>C'est le casque qui ajoute un retard quand « M'entendre » est actif. Ce que reçoivent OBS et Discord n'est pas retardé. Coupe « M'entendre » pendant le live.</p>"),
        ("Le câble CABLE Input n'apparaît pas.",
         "<p>Le câble VB-Audio demande un redémarrage du PC après l'installation. Sinon, ouvre <strong>Réglages → Câble audio → Réinstaller</strong>.</p>"),
        ("Ma clé est refusée.",
         "<p>Copie-la en entier, de <code>TV1-</code> jusqu'au dernier caractère. Les espaces et retours à la ligne ne gênent pas. Si le message dit que la clé a expiré ou a été désactivée, demande une nouvelle clé au créateur.</p>"),
        ("Mon Stream Deck ne montre pas Taverne Voice.",
         "<p>Ferme complètement le logiciel du Stream Deck (clic droit sur son icône près de l'horloge → Quitter) puis rouvre-le. Les plugins ne sont chargés qu'au démarrage. Voir le <a href=\"stream-deck.html\">guide Stream Deck</a>.</p>"),
        ("Où sont mes réglages et mes sons ?",
         "<p>Dans <code>%APPDATA%\\TaverneVoice</code>. Ils sont gardés pendant les mises à jour.</p>"),
        ("Combien de PC avec un abonnement ?",
         "<p>2 PC à la fois. Pour en changer, retire l'ancien dans <a href=\"compte.html\">Mon compte</a> ou clique sur <strong>Se déconnecter de ce PC</strong> dans les Réglages du logiciel.</p>"),
        ("J'ai payé sur Ko-fi mais rien ne se débloque.",
         "<p>Vérifie que ton compte Taverne Voice a <strong>la même adresse e-mail</strong> que sur Ko-fi. Dans le logiciel, Réglages → Licence → <strong>Actualiser</strong>. Si tu as payé avec une autre adresse, écris à contact@tavernevoice.fr : ton paiement sera rattaché à ton compte.</p>"),
        ("Comment arrêter mon abonnement ?",
         "<p>Sur Ko-fi : menu <em>Account &amp; Billing</em> → <em>Subscriptions</em>. Ton accès reste jusqu'à la fin du mois payé. Les passes 3 mois et 1 an ne se renouvellent pas.</p>"),
        ("Ça marche sur Mac ou Linux ?",
         "<p>Non, Taverne Voice est fait pour Windows 10 et 11.</p>"),
        ("Le logiciel reste ouvert quand je ferme la fenêtre.",
         "<p>Oui : il reste près de l'horloge pour que ta voix et tes raccourcis continuent de marcher. Clic droit sur son icône → <strong>Quitter</strong> pour l'arrêter.</p>"),
    ]
    corps = "".join(f"<details><summary>{e(a)}</summary>{b}</details>" for a, b in q)
    return page("faq.html", "Questions", "Les questions fréquentes sur Taverne Voice.", f"""
<h1>Questions</h1>
<p class="chapo">Les problèmes les plus courants, et comment les régler.</p>
{corps}
""", guide=True)


def createur():
    corps = (RACINE / "outils" / "createur_corps.html").read_text(encoding="utf-8")
    return page("createur.html", "Accès créateur", "Réservé au créateur de Taverne Voice.", corps, noindex=True)


def page404():
    return page("404.html", "Page introuvable", "Cette page n'existe pas.", """
<div class="enveloppe" style="padding:80px 0"><h1>Page introuvable</h1><p class="chapo" style="margin-top:16px">Cette page n'existe pas ou a changé d'adresse.</p><p><a class="bouton" href="index.html">Revenir à l'accueil</a></p></div>
""", noindex=True)


PAGES = {
    "index.html": accueil, "boutique.html": boutique, "compte.html": compte, "partenaires.html": partenaires_page,
    "installation.html": installation, "obs-discord.html": obs_discord, "voix.html": voix, "soundboard.html": soundboard,
    "twitch-obs.html": twitch_obs, "stream-deck.html": stream_deck, "licence.html": licence, "faq.html": faq,
    "createur.html": createur, "mentions-legales.html": mentions, "cgv.html": cgv, "confidentialite.html": confidentialite,
    "404.html": page404,
}

if __name__ == "__main__":
    for nom, f in PAGES.items():
        (DOCS / nom).write_text(f(), encoding="utf-8")
        print("écrit", nom)
