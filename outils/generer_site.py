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
CONTACT = "https://github.com/mrtoto-dev"
CONTACT_TEXTE = "écris au créateur sur GitHub"

VOIX = json.loads((RACINE / "outils" / "voix.json").read_text(encoding="utf-8"))
VOIX_DEMO = ["normal", "chipmunk", "robot", "demon", "telephone"]
SYMBOLES = (RACINE / "outils" / "symboles.svg").read_text(encoding="utf-8")

e = html.escape

def icone(nom):
    return f'<svg class="ic" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-{nom}"/></svg>'

ICONE_TELECHARGER = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" style="stroke-width:2.2"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'

MENU = [
    ("index.html", "Accueil"),
    ("installation.html", "Guide"),
    ("stream-deck.html", "Stream Deck"),
    ("licence.html", "Version complète"),
    ("faq.html", "Questions"),
]

GUIDE = [
    ("installation.html", "Installer"),
    ("obs-discord.html", "OBS et Discord"),
    ("voix.html", "Les voix"),
    ("soundboard.html", "Soundboard"),
    ("stream-deck.html", "Stream Deck"),
    ("licence.html", "Version complète"),
    ("faq.html", "Questions"),
]


def page(fichier, titre, description, corps, guide=False, noindex=False):
    actif = fichier if fichier != "obs-discord.html" and fichier not in ("voix.html", "soundboard.html") else "installation.html"
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == actif else ""}>{t}</a>' for h, t in MENU
    )
    if guide:
        sommaire = "".join(
            f'<a href="{h}"{" aria-current=\"page\"" if h == fichier else ""}>{t}</a>' for h, t in GUIDE
        )
        corps = f'<div class="enveloppe guide"><nav class="sommaire" aria-label="Guide"><p>Le guide</p>{sommaire}</nav><article>{corps}</article></div>'
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ""
    titre_complet = "Taverne Voice" if fichier == "index.html" else f"{titre} – Taverne Voice"
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre_complet)}</title>
<meta name="description" content="{e(description)}">
{robots}
<link rel="icon" href="img/icone.png">
<link rel="stylesheet" href="site.css">
</head>
<body>
{SYMBOLES}
<header class="entete">
  <div class="enveloppe">
    <a class="marque" href="index.html"><img src="img/icone.png" alt=""><span>Taverne Voice</span></a>
    <nav class="nav" aria-label="Menu">{nav}</nav>
    <a class="bouton petit" href="{TELECHARGER}Taverne-Voice-Setup.exe">Télécharger</a>
  </div>
</header>
<main>
{corps}
</main>
<footer class="pied">
  <div class="enveloppe">
    <span>Taverne Voice, changeur de voix pour Windows. <span id="version-site"></span></span>
    <span class="liens-pied"><a href="{DEPOT}/releases">Toutes les versions</a> <a href="faq.html">Aide</a></span>
  </div>
</footer>
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
    return page("index.html", "Accueil",
        "Change ta voix en direct sur Twitch et Discord : 33 voix, un soundboard Myinstants et un plugin pour ton Stream Deck.", f"""
<div class="enveloppe heros">
  <div>
    <h1>Taverne Voice</h1>
    <p class="chapo">Change ta voix en direct sur Twitch et Discord. 33 voix, un soundboard et des plugins pour ton Stream Deck.</p>
    <div class="actions">
      <a class="bouton" href="{TELECHARGER}Taverne-Voice-Setup.exe">{ICONE_TELECHARGER}Télécharger pour Windows</a>
      <a class="bouton second" href="installation.html">Lire le guide</a>
    </div>
    <p class="petit-texte">Gratuit en démo. Windows 10 et 11.</p>
  </div>
  <div>
    <div class="mur" aria-label="Les 33 voix">{mur}</div>
    <p class="legende-mur"><span class="l-libre">5 voix dans la démo</span><span class="l-complete">28 de plus avec une clé</span></p>
  </div>
</div>

<section class="section">
  <div class="enveloppe">
    <h2>Prêt en trois minutes</h2>
    <p class="intro">Taverne Voice transforme ta voix et l'envoie dans un câble audio virtuel. OBS et Discord écoutent ce câble au lieu de ton micro.</p>
    <ol class="etapes">
      <li><h3>Installe</h3><p>L'installateur ajoute le logiciel, le câble audio gratuit de VB-Audio et le plugin de ton Stream Deck.</p></li>
      <li><h3>Branche</h3><p>Dans OBS et Discord, choisis <strong>CABLE Output</strong> comme micro. <a href="obs-discord.html">Voir comment</a>.</p></li>
      <li><h3>Choisis ta voix</h3><p>Un clic sur un sous-bock et tout le monde t'entend avec. <kbd>F8</kbd> coupe l'effet, même en jeu.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Démo ou version complète</h2>
    <p class="intro">La démo n'a pas de limite de temps. Une clé débloque tout le reste, sur ce PC, sans compte à créer.</p>
    <div class="offres">
      <div class="offre">
        <h3>Démo</h3>
        <ul>
          <li><strong>5 voix</strong> : Normal, Chipmunk, Robot, Démon, Téléphone</li>
          <li><strong>3 sons</strong> dans le soundboard</li>
          <li>La touche <kbd>F8</kbd> et les mises à jour automatiques</li>
        </ul>
      </div>
      <div class="offre">
        <h3>Version complète</h3>
        <ul>
          <li><strong>Les 33 voix</strong>, dont l'autotune, la French Touch et les créatures</li>
          <li><strong>Les curseurs</strong> pour régler chaque voix et enregistrer les tiennes</li>
          <li><strong>Un soundboard sans limite</strong>, avec Myinstants et tes MP3</li>
          <li><strong>Les plugins Stream Deck</strong> pour toutes les marques</li>
        </ul>
        <p style="margin:18px 0 0"><a class="bouton petit" href="licence.html">Obtenir une clé</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Ton Stream Deck, quelle que soit la marque</h2>
    <p class="intro">Une touche pour chaque son, une touche pour chaque voix. Les touches s'allument quand le son joue ou quand la voix est active.</p>
    <div class="marques">
      <div class="carte-marque"><h3>Elgato</h3><p>Stream Deck, MK.2, XL, Mini, +, Neo.</p><a class="bouton second petit" href="stream-deck.html#elgato">Installer</a></div>
      <div class="carte-marque"><h3>StreamDock</h3><p>Mars Gaming, Mirabox, Ajazz, Soomfon.</p><a class="bouton second petit" href="stream-deck.html#streamdock">Installer</a></div>
      <div class="carte-marque"><h3>Ulanzi</h3><p>Stream Controller D200, D200H, D200X.</p><a class="bouton second petit" href="stream-deck.html#ulanzi">Installer</a></div>
      <div class="carte-marque"><h3>Les autres</h3><p>Razer, Loupedeck, Touch Portal : avec des raccourcis.</p><a class="bouton second petit" href="stream-deck.html#autres">Voir comment</a></div>
    </div>
  </div>
</section>
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


def licence():
    return page("licence.html", "Version complète", "Débloquer la version complète de Taverne Voice avec une clé.", f"""
<h1>Version complète</h1>
<p class="chapo">La démo marche sans limite de temps. Une clé débloque tout le reste.</p>

<div class="tableau"><table>
  <tr><th></th><th>Démo</th><th>Version complète</th></tr>
  <tr><td>Voix</td><td>5</td><td>33, plus les tiennes</td></tr>
  <tr><td>Curseurs de réglage</td><td>non</td><td>oui</td></tr>
  <tr><td>Sons dans le soundboard</td><td>3</td><td>sans limite</td></tr>
  <tr><td>Raccourcis clavier et <kbd>F8</kbd></td><td>oui</td><td>oui</td></tr>
  <tr><td>Plugins Stream Deck</td><td>non</td><td>toutes les marques</td></tr>
  <tr><td>Mises à jour</td><td>oui</td><td>oui</td></tr>
</table></div>

<h2>Obtenir une clé</h2>
<p>Les clés sont données par le créateur de Taverne Voice : <a href="{CONTACT}">{CONTACT_TEXTE}</a>. Une clé peut être à vie ou valable pour une durée limitée.</p>

<h2>Activer ta clé</h2>
<ol>
  <li>Dans Taverne Voice, clique sur <strong>Démo · Débloquer</strong> à côté du nom, en haut.</li>
  <li>Colle ta clé (elle commence par <code>TV1-</code>) et clique sur <strong>Activer la clé</strong>.</li>
</ol>
<p>Pas besoin d'internet ni de compte. La clé est gardée sur ce PC, même après une mise à jour.</p>

<h2>Changer de PC</h2>
<p>Sur l'ancien PC : <strong>Réglages → Licence → Retirer la clé de ce PC</strong>. Puis active la même clé sur le nouveau.</p>

<div class="encadre"><p>Une clé est personnelle. Si elle est partagée, le créateur peut la désactiver : le logiciel repasse alors en démo.</p></div>
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
    "index.html": accueil, "installation.html": installation, "obs-discord.html": obs_discord,
    "voix.html": voix, "soundboard.html": soundboard, "stream-deck.html": stream_deck,
    "licence.html": licence, "faq.html": faq, "createur.html": createur, "404.html": page404,
}

if __name__ == "__main__":
    for nom, f in PAGES.items():
        (DOCS / nom).write_text(f(), encoding="utf-8")
        print("écrit", nom)
