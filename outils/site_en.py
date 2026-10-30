"""English version of the Taverne Voice website (docs/en/).

Called by generer_site.py, which passes itself as G so the pages share the same
template, helpers and settings. Pages here mirror the French pages one by one.
"""
import random

MENU_EN = [
    ("index.html#fonctions", "Features"),
    ("installation.html", "Guide"),
    ("partenaires.html", "Partners"),
    ("boutique.html", "Pricing"),
]

GUIDE_EN = [
    ("installation.html", "Install"),
    ("obs-discord.html", "OBS and Discord"),
    ("voix.html", "The voices"),
    ("soundboard.html", "Soundboard"),
    ("interactif.html", "Roulette and challenges"),
    ("atelier.html", "Workshop and profiles"),
    ("twitch-obs.html", "Twitch and overlay"),
    ("stream-deck.html", "Stream Deck"),
    ("reglages.html", "Backups and diagnostics"),
    ("licence.html", "Subscription and keys"),
    ("faq.html", "Questions"),
]

VOIX_EN = {
    "normal": ("Normal", "Your real voice, no effect"),
    "chipmunk": ("Chipmunk", "Tiny, very high-pitched voice"),
    "lutin": ("Elf", "High-pitched and mischievous"),
    "geant": ("Giant", "Deep, slow and imposing"),
    "bebe": ("Baby", "Small voice that shakes a little"),
    "autotune": ("Autotune", "Every note snapped in tune, robotic rapper effect"),
    "autotune-doux": ("Soft autotune", "Fixes your pitch without it being too obvious"),
    "french-touch": ("French Touch", "Disco robot vocoder, French Touch style"),
    "talkbox": ("Talkbox", "A synth that talks with your mouth, funk sound"),
    "chorale": ("Choir", "Your voice sung in chords by several singers"),
    "popstar": ("Pop star", "Autotune, doubled voice and studio reverb"),
    "soiree": ("Party", "Nightclub vibe with echo and doubled voice"),
    "robot": ("Robot", "Metallic machine voice"),
    "alien": ("Alien", "High-pitched with a spacey sound"),
    "cyborg": ("Cyborg", "Half human, half machine"),
    "retro": ("Retro 8-bit", "Like an old video game"),
    "ordinateur": ("Computer", "An AI's synthetic voice"),
    "monstre": ("Monster", "Very deep and raspy"),
    "demon": ("Demon", "Deep, metallic and cavernous"),
    "fantome": ("Ghost", "Distant with echo"),
    "dragon": ("Dragon", "Huge roar"),
    "orc": ("Orc", "Deep, gravelly brute"),
    "gobelin": ("Goblin", "Small, nervous, squeaky voice"),
    "zombie": ("Zombie", "Wavering voice from beyond the grave"),
    "grotte": ("Cave", "Like deep inside a cavern"),
    "cathedrale": ("Cathedral", "Huge stone hall"),
    "radio": ("Radio", "Crackling walkie-talkie"),
    "telephone": ("Phone", "Thin, like on the other end of the line"),
    "megaphone": ("Megaphone", "Announcement shouted through a megaphone"),
    "stade": ("Stadium", "Stadium announcer"),
    "sousleau": ("Underwater", "Muffled and wavy, like underwater"),
    "chuchoteur": ("Whisperer", "Just breath, like a whisper"),
    "ivrogne": ("Drunkard", "The customer who had too much at the tavern"),
}

PARTENAIRES_EN = {
    "mrtoto_of": "The creator of Taverne Voice, live with every voice in the tavern.",
    "wapi_twitch": "Partner streamer: catch Taverne Voice in their streams.",
}

NOTE_TRADUCTION = '<div class="encadre"><p>This English translation is provided for convenience. The <a href="../{}">French version</a> is the one that legally applies.</p></div>'


def pages(G):
    e, icone = G.e, G.icone
    T, DL, TW = G.TELECHARGER, G.ICONE_TELECHARGER, G.ICONE_TWITCH

    def pg(fichier, titre, description, corps, **kw):
        return G.page(fichier, titre, description, corps, L="en", menu=MENU_EN, sommaire_guide=GUIDE_EN, **kw)

    def nom(v):
        return VOIX_EN.get(v["id"], (v["nom"], v["desc"]))[0]

    def desc(v):
        return VOIX_EN.get(v["id"], (v["nom"], v["desc"]))[1]

    def bock(v):
        libre = v["id"] in G.VOIX_DEMO
        return (f'<span class="bock{" libre" if libre else ""}" style="--c:{v["couleur"]};--r:{random.uniform(-9, 9):.1f}deg" '
                f'tabindex="0" aria-label="{e(nom(v))}{" (demo)" if libre else ""}">{icone(v["icone"])}'
                f'<span class="infobulle">{e(nom(v))}</span></span>')

    def carte_partenaire(p):
        return f"""<article class="partenaire">
  <div class="ecran"><button type="button" data-chaine="{e(p["chaine"])}">{TW}Watch the stream</button></div>
  <div class="infos">
    <span class="pastille-p">{e(p["nom"][0])}</span>
    <div><h3>{e(p["nom"])}</h3><p>{e(PARTENAIRES_EN.get(p["chaine"], p["texte"]))}</p></div>
    <a class="bouton second petit" href="https://www.twitch.tv/{e(p["chaine"])}" target="_blank" rel="noopener">Follow</a>
  </div>
</article>"""

    script_partenaires = G.SCRIPT_PARTENAIRES.replace('"Live Twitch de "', '"Twitch stream of "')

    def bandeau_essai():
        return """<div class="bandeau-essai">
    <div class="prix-essai">€0<small>14 days</small></div>
    <div><h3>Free trial</h3><p>The whole full version for 14 days, no credit card and no commitment. Create your account, then sign in from the app: the trial starts on its own.</p></div>
    <a class="bouton" href="compte.html?vue=inscription">Start the trial</a>
  </div>"""

    def cartes_formules(lien=True):
        def carte(id_, nom_, prix, unite, texte, mise=False, etiquette=""):
            bouton = f'<a class="bouton{"" if mise else " second"}" href="boutique.html?formule={id_}">Choose</a>' if lien else ""
            return f"""<div class="formule{" mise-en-avant" if mise else ""}">
      {f'<span class="etiquette-f">{etiquette}</span>' if etiquette else ""}
      <h3>{nom_}</h3>
      <div class="prix">{prix} <small>{unite}</small></div>
      <p>{texte}</p>
      {bouton}
    </div>"""
        return f"""<div class="formules">
    {carte("mensuel", "Monthly", "€4.99", "per month", "Renews automatically. Stop it anytime from Ko-fi.", True, "Most flexible")}
    {carte("trimestre", "3 months", "€14.99", "once", "Three months of access, no automatic renewal.")}
    {carte("annuel", "1 year", "€59.99", "once", "A whole year, paid once, no renewal.")}
  </div>
  <p class="note-formules">Every plan unlocks the 33 voices, fine-tuning, the unlimited soundboard, Twitch channel points, the OBS overlay and the Stream Deck plugins. Secure payment with Ko-fi (card or PayPal).</p>"""

    # ------------------------------------------------------------------ home
    def accueil():
        random.seed(7)
        mur = "".join(bock(v) for v in G.VOIX)
        partenaires = "".join(carte_partenaire(p) for p in G.PARTENAIRES)
        return pg("index.html", "Home",
            "Change your voice live on Twitch and Discord: 33 voices, a soundboard, Twitch channel points, an OBS overlay and plugins for every Stream Deck.", f"""
<div class="enveloppe heros2">
  <div>
    <h1>Taverne Voice</h1>
    <p class="chapo">The voice changer for streamers. 33 voices, a soundboard, Twitch channel points and your Stream Deck, all in one app.</p>
    <div class="actions">
      <a class="bouton" href="{T}Taverne-Voice-Setup.exe">{DL}Download for free</a>
      <a class="bouton second" href="compte.html?vue=inscription">14-day free trial</a>
    </div>
    <p class="petit-texte">14 days of the full version for free, no credit card. After that the demo stays free. Windows 10 and 11.</p>
  </div>
  <div class="vitrine">
    <div class="fenetre-app"><img src="../img/en/capture-voix-petit.webp" srcset="../img/en/capture-voix-petit.webp 1360w, ../img/en/capture-voix.webp 2720w" sizes="(max-width: 900px) 100vw, 640px" width="1360" height="820" alt="The Taverne Voice window: voices as colored coasters and the settings of the French Touch voice"></div>
    <img class="bulle-overlay" src="../img/en/capture-overlay.webp" width="460" height="106" alt="The OBS overlay: a viewer gave the streamer the Chipmunk voice, 17 seconds left">
  </div>
</div>

<section class="section" id="fonctions">
  <div class="enveloppe">
    <div class="fonction">
      <div>
        <h2>33 voices, tuned for streaming</h2>
        <p>One click on a coaster and your whole chat hears it. <kbd>F8</kbd> turns the effect off, even mid-game.</p>
        <ul>
          <li>Autotune, French Touch vocoder, robots, demons, cave or stadium ambiences</li>
          <li>Sliders to fine-tune every voice and save your own</li>
          <li>OBS and Discord get it through a virtual audio cable, installed with the app</li>
        </ul>
      </div>
      <div class="capture"><img src="../img/en/capture-voix-petit.webp" loading="lazy" width="1360" height="820" alt="The Taverne Voice voices"></div>
    </div>
    <div class="fonction inverse">
      <div>
        <h2>A tidy soundboard</h2>
        <p>Trending Myinstants sounds in one click, or your own MP3s. Sort them into folders and give them a shortcut.</p>
        <ul>
          <li>Folders: Memes, Sound effects, Music…</li>
          <li>Your voice ducks on its own while a sound plays</li>
          <li>One keyboard shortcut per sound, even in game</li>
        </ul>
      </div>
      <div class="capture"><img src="../img/en/capture-soundboard-petit.webp" loading="lazy" width="1360" height="820" alt="The Taverne Voice soundboard with its folders"></div>
    </div>
    <div class="fonction">
      <div>
        <h2>Your viewers take the mic</h2>
        <p>Link your Twitch channel: your viewers spend their channel points to give you a voice for 30 seconds or play a sound. The OBS overlay shows it on your stream, with the countdown.</p>
        <ul>
          <li>Rewards are created right from the app</li>
          <li>Refunded automatically if the app can't play them</li>
          <li>Overlay as a browser source, in the corner of your choice</li>
        </ul>
        <p><a href="twitch-obs.html">See how it works</a></p>
      </div>
      <div class="capture"><img src="../img/en/capture-twitch-petit.webp" loading="lazy" width="1360" height="820" alt="The Twitch and OBS tab in Taverne Voice"></div>
    </div>
    <div class="fonction inverse">
      <div>
        <h2>Roulette, challenges and automations</h2>
        <p>Spin the voice roulette, start a “Chaos” challenge where your voice changes on its own, or let Taverne Voice react when you shout.</p>
        <ul>
          <li>4 challenges: Chaos, Escalation, Pile-up, Trap voice</li>
          <li>Timer: every voice goes back on its own after 30 seconds</li>
          <li>Your viewers can spin the roulette or start a challenge with their channel points</li>
        </ul>
        <p><a href="interactif.html">See the challenges</a></p>
      </div>
      <div class="capture"><img src="../img/en/capture-interactif-petit.webp" loading="lazy" width="1360" height="820" alt="The Interactive tab: roulette, a Chaos challenge in progress and the timer"></div>
    </div>
    <div class="fonction">
      <div>
        <h2>Build your own voice in the workshop</h2>
        <p>Stack effects like ingredients, mix two voices with a slider, or let chance invent one. You hear the result live.</p>
        <ul>
          <li>Save your voices with a name, a color and an icon</li>
          <li>Share them with a simple code to paste in Discord</li>
          <li>One keyboard shortcut per voice, even in game</li>
        </ul>
        <p><a href="atelier.html">Discover the workshop</a></p>
      </div>
      <div class="capture"><img src="../img/en/capture-atelier-petit.webp" loading="lazy" width="1360" height="820" alt="The creation workshop: effects, mixing two voices and saving"></div>
    </div>
    <div class="fonction inverse">
      <div>
        <h2>Your Stream Deck, whatever the brand</h2>
        <p>One key per sound, one key per voice. They light up when the sound plays or the voice is active.</p>
        <p><a class="bouton second petit" href="stream-deck.html">Install the plugin</a></p>
      </div>
      <div class="marques" style="margin-top:0">
        <div class="carte-marque"><h3>Elgato</h3><p>Stream Deck, MK.2, XL, Mini, +, Neo.</p></div>
        <div class="carte-marque"><h3>StreamDock</h3><p>Mars Gaming, Mirabox, Ajazz, Soomfon.</p></div>
        <div class="carte-marque"><h3>Ulanzi</h3><p>Stream Controller D200, D200H, D200X.</p></div>
        <div class="carte-marque"><h3>Others</h3><p>Razer, Loupedeck, Touch Portal, with shortcuts.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Every voice in the tavern</h2>
    <p class="intro">The 5 lit voices work in the demo. The other 28 unlock with a subscription.</p>
    <div class="mur" aria-label="The 33 voices" style="margin-top:22px">{mur}</div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>They stream with Taverne Voice</h2>
    <p class="intro">The tavern's partner streamers. Drop by and say hi.</p>
    <div class="partenaires">{partenaires}</div>
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Plans</h2>
    <p class="intro">Try everything for 14 days, for free. After that the demo stays free with no time limit, and a subscription unlocks everything, on 2 PCs.</p>
    {bandeau_essai()}
    {cartes_formules()}
  </div>
</section>

<section class="section">
  <div class="enveloppe">
    <h2>Ready in three minutes</h2>
    <ol class="etapes">
      <li><h3>Install</h3><p>The installer adds the app, VB-Audio's free audio cable and your Stream Deck plugin.</p></li>
      <li><h3>Connect</h3><p>In OBS and Discord, pick <strong>CABLE Output</strong> as your mic. <a href="obs-discord.html">See how</a>.</p></li>
      <li><h3>Pick your voice</h3><p>One click on a coaster and everyone hears it.</p></li>
    </ol>
  </div>
</section>
""", scripts=script_partenaires)

    def partenaires_page():
        return pg("partenaires.html", "Partners", "Taverne Voice partner streamers: MRTOTO_OF and Wapi_twitch.", f"""
<div class="enveloppe page-etroite">
  <h1>Partners</h1>
  <p class="chapo">The streamers who keep the tavern alive. Watch their stream right here.</p>
  <div class="partenaires">{"".join(carte_partenaire(p) for p in G.PARTENAIRES)}</div>
  <div class="carte" style="margin-top:28px">
    <h2>Become a partner</h2>
    <p>You stream with Taverne Voice and want to be listed here? Email <a href="{G.CONTACT}">{G.CONTACT_TEXTE}</a> with your channel link.</p>
  </div>
</div>
""", scripts=script_partenaires)

    # ------------------------------------------------------------------ shop and account
    def boutique():
        return pg("boutique.html", "Pricing", "Taverne Voice plans: €4.99 per month, €14.99 for 3 months or €59.99 for a year.", f"""
<div class="enveloppe page-etroite">
  <h1>Unlock Taverne Voice</h1>
  <p class="chapo">Pick your plan, create your account, pay on Ko-fi: your app unlocks on its own.</p>
  <div class="encadre"><p>Not sure yet? <a href="compte.html?vue=inscription">Create your account</a> and sign in from the app: <strong>14-day free trial</strong>, no payment. If you buy during the trial, your remaining days are kept.</p></div>
  {cartes_formules(lien=False).replace('<div class="formules">', '<div class="formules" hidden>')}
  <ol class="etapes-achat">
    <li>
      <h3>Pick your plan</h3>
      <div class="choix-formule">
        <button type="button" data-formule="mensuel" aria-pressed="true"><strong>€4.99</strong>per month</button>
        <button type="button" data-formule="trimestre" aria-pressed="false"><strong>€14.99</strong>for 3 months</button>
        <button type="button" data-formule="annuel" aria-pressed="false"><strong>€59.99</strong>for 1 year</button>
      </div>
      <p id="b-detail"></p>
    </li>
    <li id="etape-compte">
      <h3>Your Taverne Voice account</h3>
      <p>It links your payment to your app, on up to 2 PCs.</p>
      <div class="ligne-actions" id="b-compte"></div>
      <p class="msg ok" id="b-deja" hidden></p>
    </li>
    <li>
      <h3>Pay on Ko-fi</h3>
      <div id="b-email-zone" hidden>
        <p>On Ko-fi, use <strong>exactly the same email address</strong> as your account:</p>
        <p class="ligne-actions"><span class="email-rappel" id="b-email"></span><button class="lien-bouton" type="button" id="b-copier">Copy</button></p>
      </div>
      <label class="ligne-actions" id="b-accord-zone" style="margin:12px 0;align-items:flex-start;gap:10px;color:var(--parchemin);font-size:15px">
        <input type="checkbox" id="b-accord" style="margin-top:4px;width:18px;height:18px">
        <span>I accept the <a href="cgv.html" target="_blank">terms of sale</a>. I ask for access right away and therefore waive my 14-day right of withdrawal for this digital content.</span>
      </label>
      <a class="bouton" id="b-payer" href="#" rel="noopener">Pay on Ko-fi</a>
      <p class="msg erreur" id="b-bientot" hidden>Payments open very soon. Come back in a few days!</p>
    </li>
    <li id="etape-activation" hidden>
      <h3>Activation</h3>
      <div id="b-attente"><p>As soon as Ko-fi confirms your payment, your account activates on its own. Keep this page open…</p></div>
      <div id="b-active" hidden>
        <p class="msg ok">It's active, thank you! Your access runs until <strong id="b-fin"></strong>.</p>
        <p>In Taverne Voice, click <strong>Demo: unlock</strong>, <strong>My account</strong> tab, and sign in.</p>
        <a class="bouton second petit" href="{T}Taverne-Voice-Setup.exe">{DL}Download Taverne Voice</a>
      </div>
    </li>
  </ol>
  <p class="note-formules">Secure payment with Ko-fi, by card or PayPal. The monthly subscription stops whenever you want from your Ko-fi account; the 3-month and 1-year passes don't renew. A question? <a href="{G.CONTACT}">{G.CONTACT_TEXTE}</a>.</p>
</div>
<style>.formule .bouton{{display:none}} #b-payer.desactive{{opacity:.55}} #b-accord-zone.a-cocher span{{color:var(--lanterne)}}</style>
""", scripts='<script src="../config.js"></script><script src="../js/api.js"></script><script src="../js/boutique.js"></script>')

    def compte():
        return pg("compte.html", "My account", "Your Taverne Voice account: subscription, linked PCs and payments.", f"""
<div class="enveloppe page-etroite">
  <div id="vue-chargement" hidden><p>Loading…</p></div>

  <section class="carte" id="vue-connexion" hidden style="max-width:520px">
    <h2>Sign in</h2>
    <p>With your Taverne Voice account.</p>
    <form class="formulaire" id="form-connexion">
      <label>Email address<input type="email" id="c-email" autocomplete="username" required></label>
      <label>Password<input type="password" id="c-mdp" autocomplete="current-password" required></label>
      <p class="msg erreur" id="msg-connexion" hidden></p>
      <button class="bouton" type="submit">Sign in</button>
    </form>
    <p style="margin-top:18px"><a href="#" data-vue="oubli">Forgot your password?</a></p>
    <p>No account yet? <a href="#" data-vue="inscription">Create one in a minute</a>.</p>
  </section>

  <section class="carte" id="vue-inscription" hidden style="max-width:520px">
    <h2>Create my account</h2>
    <p>Your account gives you a <strong>14-day free trial</strong> of the full version. If you pay later, use the same address on Ko-fi: that's what links your payment to your account.</p>
    <form class="formulaire" id="form-inscription">
      <label>Email address<input type="email" id="i-email" autocomplete="email" required></label>
      <label>Username (shown in the app)<input id="i-pseudo" maxlength="40" placeholder="Your Twitch name, for example"></label>
      <label>Password (at least 8 characters)<input type="password" id="i-mdp" autocomplete="new-password" minlength="8" required></label>
      <label>One more time<input type="password" id="i-mdp2" autocomplete="new-password" minlength="8" required></label>
      <label style="flex-direction:row;gap:10px;align-items:flex-start"><input type="checkbox" id="i-accord" style="width:18px;height:18px;margin-top:3px"><span>I accept the <a href="cgv.html" target="_blank">terms of sale</a> and the <a href="confidentialite.html" target="_blank">privacy policy</a>.</span></label>
      <p class="msg erreur" id="msg-inscription" hidden></p>
      <button class="bouton" type="submit">Create my account</button>
    </form>
    <p style="margin-top:18px">Already have an account? <a href="#" data-vue="connexion">Sign in</a></p>
  </section>

  <section class="carte" id="vue-verif" hidden style="max-width:520px">
    <h2>Confirm your address</h2>
    <p>We just sent a 6-digit code to <strong id="verif-email"></strong>. Check your spam folder too.</p>
    <form class="formulaire" id="form-verif">
      <label>Code<input id="v-code" class="code-saisie" inputmode="numeric" maxlength="6" autocomplete="one-time-code" required></label>
      <p class="msg" id="msg-verif" hidden></p>
      <button class="bouton" type="submit">Confirm</button>
    </form>
    <p style="margin-top:18px"><button class="lien-bouton" type="button" id="renvoyer">Send a new code</button></p>
  </section>

  <section class="carte" id="vue-oubli" hidden style="max-width:520px">
    <h2>Forgot your password</h2>
    <p>We'll send you a code to choose a new one.</p>
    <form class="formulaire" id="form-oubli">
      <label>Email address<input type="email" id="o-email" autocomplete="email" required></label>
      <p class="msg erreur" id="msg-oubli" hidden></p>
      <button class="bouton" type="submit">Send the code</button>
    </form>
    <p style="margin-top:18px"><a href="#" data-vue="connexion">Back to sign in</a></p>
  </section>

  <section class="carte" id="vue-oubli2" hidden style="max-width:520px">
    <h2>New password</h2>
    <p>If an account exists for <strong id="oubli-email"></strong>, a code is on its way.</p>
    <form class="formulaire" id="form-oubli2">
      <label>Code<input id="o-code" class="code-saisie" inputmode="numeric" maxlength="6" autocomplete="one-time-code" required></label>
      <label>New password<input type="password" id="o-mdp" autocomplete="new-password" minlength="8" required></label>
      <p class="msg erreur" id="msg-oubli2" hidden></p>
      <button class="bouton" type="submit">Change my password</button>
    </form>
  </section>

  <div id="vue-tableau" hidden>
    <h1 style="font-size:clamp(44px,7vw,72px)">Hello <span id="t-nom"></span></h1>
    <p style="color:var(--parchemin)">Signed in as <span id="t-email"></span>.</p>
    <div class="statut-abo" id="t-statut"><span class="point"></span><div><strong id="t-statut-titre"></strong><span id="t-statut-detail"></span></div></div>
    <div class="bandeau-essai" id="t-essai" hidden>
      <div class="prix-essai">€0<small id="t-essai-jours">14 days</small></div>
      <div><h3>Your free trial is waiting</h3><p>Install Taverne Voice, click <strong>Demo: unlock</strong>, <strong>My account</strong> tab, and sign in with this account. The full version unlocks right away, no payment.</p></div>
      <a class="bouton" href="{T}Taverne-Voice-Setup.exe">{DL}Download</a>
    </div>
    <div class="ligne-actions">
      <a class="bouton" id="t-acheter" href="boutique.html">Choose a plan</a>
      <a class="bouton second" id="t-kofi" href="https://ko-fi.com/" target="_blank" rel="noopener" hidden>Manage my subscription on Ko-fi</a>
      <a class="bouton second" href="{T}Taverne-Voice-Setup.exe">{DL}Download</a>
    </div>
    <p class="note-formules">To stop the monthly subscription: on Ko-fi, <em>Account &amp; Billing</em> menu, then <em>Subscriptions</em>. Your access stays until the end of the paid month.</p>

    <div class="colonnes" style="margin-top:26px">
      <section class="carte">
        <h2>My PCs <small style="font:500 15px Rubik,sans-serif;color:var(--parchemin)" id="t-pcs-compte"></small></h2>
        <p>Remove a PC to free its spot (new computer, Windows reinstalled…).</p>
        <ul class="liste-simple" id="t-pcs"></ul>
      </section>
      <section class="carte">
        <h2>My payments</h2>
        <ul class="liste-simple" id="t-paiements"></ul>
      </section>
    </div>

    <div class="colonnes" style="margin-top:18px">
      <section class="carte">
        <h2>My username</h2>
        <form class="formulaire" id="form-pseudo">
          <label>Shown in the app<input id="t-pseudo" maxlength="40"></label>
          <p class="msg" id="msg-pseudo" hidden></p>
          <button class="bouton second petit" type="submit">Save</button>
        </form>
      </section>
      <section class="carte">
        <h2>Password</h2>
        <form class="formulaire" id="form-mdp">
          <label>Current password<input type="password" id="m-ancien" autocomplete="current-password" required></label>
          <label>New password<input type="password" id="m-nouveau" autocomplete="new-password" minlength="8" required></label>
          <p class="msg" id="msg-mdp" hidden></p>
          <button class="bouton second petit" type="submit">Change</button>
        </form>
      </section>
    </div>
    <p class="ligne-actions" style="margin-top:24px">
      <button class="bouton second" type="button" id="t-deconnexion">Sign out</button>
      <button class="lien-bouton" type="button" id="t-supprimer" style="color:var(--braise)">Delete my account</button>
    </p>
  </div>
</div>
""", noindex=True, scripts='<script src="../config.js"></script><script src="../js/api.js"></script><script src="../js/compte.js"></script>')

    # ------------------------------------------------------------------ guide
    def installation():
        return pg("installation.html", "Install", "Install Taverne Voice and the virtual audio cable on Windows.", f"""
<h1>Install</h1>
<p class="chapo">It all happens with a single file. You need Windows 10 or 11 and a mic.</p>

<h2>1. Download</h2>
<p><a class="bouton" href="{T}Taverne-Voice-Setup.exe">{DL}Download Taverne-Voice-Setup.exe</a></p>
<p>Rather not install anything? <a href="{T}Taverne-Voice.exe">Taverne-Voice.exe</a> is the portable version: a single file to run, but without starting with Windows or installing the cable automatically.</p>

<h2>2. Get past the Windows warning</h2>
<p>The first time, Windows may show “Windows protected your PC”. That's normal for a small app that doesn't have a paid certificate yet.</p>
<ol>
  <li>Click <strong>More info</strong>.</li>
  <li>Click <strong>Run anyway</strong>.</li>
</ol>

<h2>3. Pick the options</h2>
<p>The installer offers:</p>
<ul>
  <li><strong>VB-Audio audio cable</strong>: essential, it carries your modified voice into OBS and Discord. Windows asks for your permission, then click <em>Install Driver</em>. Restart your PC afterwards.</li>
  <li><strong>Elgato Stream Deck plugin</strong>, <strong>StreamDock and Ulanzi plugin</strong>: checked automatically if your Stream Deck software is installed.</li>
  <li><strong>Desktop icon</strong> and <strong>Start with Windows</strong>.</li>
</ul>
<p>The app installs in your user folder: no need to be an administrator.</p>

<h2>4. First launch</h2>
<ol>
  <li>Open <strong>Settings</strong> (the gear at the top right).</li>
  <li><strong>Your mic</strong>: your real mic. With SteelSeries Sonar, pick “SteelSeries Sonar - Microphone” to keep your noise reduction.</li>
  <li><strong>Output to OBS and Discord</strong>: <code>CABLE Input</code>.</li>
  <li><strong>Headset</strong>: your headset, to hear yourself with “Hear myself”.</li>
  <li>Click <strong>Apply</strong>.</li>
</ol>
<p>Taverne Voice uses the language of Windows. To change it: <strong>Settings → Language</strong>.</p>
<p>Next, <a href="obs-discord.html">connect your voice to OBS and Discord</a>.</p>

<h2>Updates</h2>
<p>The app checks every 5 minutes for a new version. When one comes out, Windows shows a notification and an <strong>Update</strong> button appears at the top of the window: one click and it replaces itself. Your settings, voices and sounds are kept.</p>

<h2>Uninstall</h2>
<p>Windows Settings → Apps → Installed apps → Taverne Voice → Uninstall. You'll be asked whether to also delete your settings and sounds.</p>
""", guide=True)

    def obs_discord():
        return pg("obs-discord.html", "OBS and Discord", "Connect your Taverne Voice voice to OBS and Discord.", """
<h1>OBS and Discord</h1>
<p class="chapo">Taverne Voice sends your transformed voice into <code>CABLE Input</code>. On the other end of the cable, <code>CABLE Output</code> behaves like a mic: that's what OBS and Discord should listen to.</p>

<h2>OBS Studio</h2>
<ol>
  <li>In <strong>Sources</strong>, click <strong>+</strong> then <strong>Audio Input Capture</strong>.</li>
  <li>Name it “Taverne Voice” and pick the device <code>CABLE Output (VB-Audio Virtual Cable)</code>.</li>
  <li>Mute your old mic source (the speaker icon in the mixer), otherwise people hear you twice: once normal, once with the effect.</li>
</ol>
<div class="encadre"><p>Soundboard sounds go through the same cable: no need for another source for them.</p></div>

<h2>Discord</h2>
<ol>
  <li>User Settings → <strong>Voice &amp; Video</strong>.</li>
  <li><strong>Input Device</strong>: <code>CABLE Output</code>.</li>
  <li>Turn off <strong>noise suppression</strong> (Krisp) and <strong>echo cancellation</strong>: they mistake the effects for noise and ruin them.</li>
  <li>Set input sensitivity manually if your voice cuts out at times.</li>
</ol>

<h2>Hearing yourself</h2>
<p>Turn on <strong>Hear myself</strong> at the bottom of the window to listen to your modified voice in your headset. Keep it off during the stream if the echo bothers you.</p>

<h2>Not working?</h2>
<ul>
  <li>The <strong>Output</strong> light at the top of the window is red: the output isn't <code>CABLE Input</code>, or the cable isn't installed. Open Settings.</li>
  <li>Nobody hears you at all: check the effect is on (<kbd>F8</kbd>) and the right mic is picked in Taverne Voice.</li>
  <li>Run <strong>Settings → Audio diagnostics</strong>: it checks the whole chain and tells you what to do.</li>
  <li>More answers in the <a href="faq.html">FAQ</a>.</li>
</ul>
""", guide=True)

    def voix():
        categories = [("classiques", "Classics"), ("musique", "Music"), ("robots", "Robots"), ("creatures", "Creatures"), ("ambiances", "Ambiences")]
        blocs = ""
        for cid, cnom in categories:
            items = "".join(
                f'<div class="ligne-voix"><span class="bock{" libre" if v["id"] in G.VOIX_DEMO else ""}" style="--c:{v["couleur"]}">{icone(v["icone"])}</span>'
                f'<span><b>{e(nom(v))}{"<span class=\"etiquette\">demo</span>" if v["id"] in G.VOIX_DEMO else ""}</b><small>{e(desc(v))}</small></span></div>'
                for v in G.VOIX if v["cat"] == cid)
            blocs += f"<h2>{cnom}</h2><div class=\"liste-voix\">{items}</div>"
        return pg("voix.html", "The voices", "The 33 Taverne Voice voices: autotune, vocoder, robots, creatures and ambiences.", f"""
<h1>The voices</h1>
<p class="chapo">33 voices in five families. Voices marked “demo” work without a subscription.</p>
<ul>
  <li>Click a voice to use it right away.</li>
  <li><kbd>F8</kbd> turns the effect off or back on, even while you're in game.</li>
  <li>With the full version, sliders adjust pitch, autotune, choir, vibrato, vocoder, robot, echo, cave and grain. <strong>Save my voice</strong> keeps it in “My voices”.</li>
  <li>The star next to the name adds the voice to your favorites.</li>
</ul>
{blocs}
""", guide=True)

    def soundboard():
        return pg("soundboard.html", "Soundboard", "The Taverne Voice soundboard: Myinstants sounds, MP3s, keyboard shortcuts.", """
<h1>Soundboard</h1>
<p class="chapo">Sounds go into OBS and Discord along with your voice. Play them with the mouse, the keyboard or your Stream Deck.</p>

<h2>Add sounds</h2>
<ul>
  <li><strong>Myinstants</strong>: in the Soundboard tab → Myinstants, listen to trending sounds or search for one, then click <strong>Add</strong>.</li>
  <li><strong>Your files</strong>: <strong>Import</strong>, or drop your MP3 and WAV files on the window.</li>
</ul>
<div class="encadre"><p>The demo keeps 3 sounds. The <a href="licence.html">full version</a> has no limit.</p></div>

<h2>Sort into folders</h2>
<p>Click <strong>+ New folder</strong> above your sounds (Memes, Sound effects, Music…). Drag a sound onto a folder's tab to file it, or pick its folder in its panel. Sounds added while a folder is open go straight into it. The star adds a sound to <strong>Favorites</strong>, and <strong>Recent</strong> keeps the last ones you played.</p>

<h2>Lower your voice during sounds</h2>
<p>In the right panel, turn on <strong>Lower my voice during sounds</strong>: while a sound plays, your voice drops to the chosen level, then comes back up smoothly. Handy when you talk over a sound.</p>

<h2>Adjust a sound</h2>
<p>Click a sound to open its panel: volume, name, keyboard shortcut and Stream Deck link. The shortcut works even when Taverne Voice is in the background.</p>
<p>“Stop all” cuts every sound playing; you can give it a shortcut too.</p>

<h2>Copyright</h2>
<div class="encadre alerte"><p>On Twitch, a clip of music, a movie or a show can get flagged and muted in your VODs. Prefer sound effects and short sounds.</p></div>
""", guide=True)

    def interactif():
        return pg("interactif.html", "Roulette and challenges", "The voice roulette, challenges, timer and automations in Taverne Voice.", """
<h1>Roulette and challenges</h1>
<p class="chapo">The <strong>Interactive</strong> tab turns your voice into a game: roulette, challenges, timer and automatic reactions.</p>
<p><img class="capture-guide" src="../img/en/capture-interactif-petit.webp" loading="lazy" width="1360" height="820" alt="The Interactive tab"></p>
<div class="encadre"><p>The roulette, challenges and automations are part of the <a href="boutique.html">subscription</a>. The timer also works in the demo.</p></div>

<h2>The roulette</h2>
<p>Click <strong>Spin</strong> (or <strong>Roulette</strong> at the bottom of the window): the voices scroll by and one lands at random, never the one you already have. You choose:</p>
<ul>
  <li><strong>From</strong>: all voices, your favorites, the Taverne Voice voices or your custom voices.</li>
  <li><strong>The drawn voice lasts</strong>: until the next change, or 15 s to 5 min.</li>
</ul>
<p>The OBS overlay shows the spinning wheel and the winning voice.</p>

<h2>Challenges</h2>
<p>A challenge changes your voice on its own for a few minutes. Choose the interval (10 s to 1 min) and the duration (1 to 10 min), then click a challenge. <strong>Stop</strong> brings your previous voice back.</p>
<div class="tableau"><table>
  <tr><th>Challenge</th><th>What happens</th></tr>
  <tr><td>Chaos</td><td>A new random voice at every interval.</td></tr>
  <tr><td>Escalation</td><td>Your voice goes up a notch at every interval, from the lowest to the highest.</td></tr>
  <tr><td>Pile-up</td><td>An effect is added at every interval: echo, robot, cave, vibrato… all the way to total chaos.</td></tr>
  <tr><td>Trap voice</td><td>At every interval, a one-in-three chance of landing on a trap voice for 10 seconds.</td></tr>
</table></div>

<h2>The effect timer</h2>
<p>Turn it on in the Interactive tab or with the <strong>Timer</strong> button at the bottom of the window: every voice you pick goes back on its own after the set time (5 s to 10 min), to <strong>Normal</strong> or to <strong>the previous voice</strong>. The countdown shows in the app and in the overlay.</p>

<h2>Automations</h2>
<p>Build “When… then…” rules. Examples:</p>
<ul>
  <li>When <strong>I shout into the mic</strong>, then <strong>play the sound</strong> “Crowd going wild”.</li>
  <li>When <strong>I stop talking for</strong> 2 minutes, then <strong>spin the roulette</strong>.</li>
  <li>When <strong>I switch to the voice</strong> Demon, then <strong>play the sound</strong> “Thunder”.</li>
  <li>When <strong>Taverne Voice starts</strong>, then <strong>switch to the voice</strong> of your choice.</li>
</ul>
<p>Each automation has a cooldown (5 s to 5 min) so it doesn't repeat in a loop. <strong>Test</strong> runs it right away so you can try it.</p>

<h2>With Twitch and the Stream Deck</h2>
<ul>
  <li>In the <strong>Twitch &amp; OBS</strong> tab, a reward can <strong>spin the roulette</strong> or <strong>start a challenge</strong>: the viewer's name shows in the overlay.</li>
  <li>On a Stream Deck: <code>taverne://roulette</code>, <code>taverne://defi/chaos</code>… (see <a href="stream-deck.html">Stream Deck</a>).</li>
  <li>On the keyboard: pick a key for the roulette, the challenge, the next voice or the timer in <a href="reglages.html">Settings → Keyboard shortcuts</a>.</li>
</ul>
""", guide=True)

    def atelier():
        return pg("atelier.html", "Workshop and profiles", "Create, edit, duplicate and share your voices in Taverne Voice.", """
<h1>Workshop and profiles</h1>
<p class="chapo">Create your own voices, organize them, and share them with a code.</p>
<p><img class="capture-guide" src="../img/en/capture-atelier-petit.webp" loading="lazy" width="1360" height="820" alt="The creation workshop"></p>
<div class="encadre"><p>The workshop and custom voices are part of the <a href="boutique.html">subscription</a>.</p></div>

<h2>The workshop</h2>
<ol>
  <li>Open the <strong>Workshop</strong> tab. It starts from the voice you're using (change it in <strong>Start from</strong>).</li>
  <li>Turn effects on and set their amount: pitch, autotune, choir, vibrato, vocoder, robot, 8-bit, doubling, echo, cave, grain and filter. Talk: you hear the result live.</li>
  <li>Give it a name, a color and an icon, then <strong>Save as a new voice</strong>.</li>
</ol>
<ul>
  <li><strong>Mix two voices</strong>: choose two voices and slide between them (for example 70% Robot + 30% Demon).</li>
  <li><strong>Random</strong>: a surprise combination of effects, to keep if you like it.</li>
  <li><strong>Reset all</strong>: start again from your normal voice.</li>
</ul>

<h2>Your voices (profiles)</h2>
<p>Your custom voices are in the <strong>My voices</strong> category. Drag them to reorder them. In a voice's panel:</p>
<div class="tableau"><table>
  <tr><th>Button</th><th>What it does</th></tr>
  <tr><td>Duplicate</td><td>Creates an editable copy (also works on the Taverne Voice voices).</td></tr>
  <tr><td>Update</td><td>After moving the sliders, saves the changes into this voice.</td></tr>
  <tr><td>Reset</td><td>Restores the original voice's settings (for a copy of a Taverne Voice voice).</td></tr>
  <tr><td>Rename, icon…</td><td>Changes the name, description, color and icon.</td></tr>
  <tr><td>Share</td><td>Gives you a code to send, or a <code>.tvprofil</code> file.</td></tr>
  <tr><td>Keyboard shortcut</td><td>A key to switch to this voice, even in game.</td></tr>
</table></div>
<p>Your favorites (the star) are also used by the roulette and the “next / previous voice” keys.</p>

<h2>Share a voice</h2>
<ol>
  <li>Pick your voice and click <strong>Share</strong>.</li>
  <li><strong>Copy the code</strong> (it starts with <code>TVP1.</code>) and paste it into Discord, your chat…</li>
  <li>Your friend clicks <strong>Import a voice</strong> in “My voices” and pastes the code, even with text around it.</li>
</ol>
""", guide=True)

    def twitch_obs():
        return pg("twitch-obs.html", "Twitch and overlay", "Twitch channel points and the OBS overlay in Taverne Voice.", """
<h1>Twitch and overlay</h1>
<p class="chapo">Your viewers spend their channel points to change your voice or play a sound, and the overlay shows it on your stream.</p>
<div class="encadre"><p>Channel points and the overlay are part of the <a href="boutique.html">subscription</a>. Channel points require Twitch Affiliate or Partner status.</p></div>

<h2>Link your channel</h2>
<ol>
  <li>In Taverne Voice, open the <strong>Twitch &amp; OBS</strong> tab.</li>
  <li>Click <strong>Link my Twitch channel</strong>. A Twitch page opens with a code.</li>
  <li>Sign in with your channel's account and type the code shown in the app.</li>
</ol>
<p>Taverne Voice never sees your Twitch password. You can unlink your channel anytime; the rewards created by Taverne Voice are then removed.</p>

<h2>Create a reward</h2>
<ol>
  <li>Choose <strong>Change my voice</strong> (with a duration), <strong>Play a sound</strong>, <strong>Roulette</strong> or <strong>Challenge</strong>.</li>
  <li>Choose the voice or the sound, the cost in points and the title shown on Twitch.</li>
  <li>Click <strong>Create on Twitch</strong>. The reward shows up on your channel right away.</li>
</ol>
<p><strong>Test</strong> plays the reward without Twitch, to check how it looks on your stream. <strong>Pause</strong> hides it on Twitch without deleting it.</p>
<ul>
  <li>Voices play one after the other: if two viewers ask for one at the same time, the second waits its turn.</li>
  <li>At the end, your previous voice comes back on its own.</li>
  <li>If the app can't play the reward (sound muted, voice deleted…), the points go back to the viewer.</li>
</ul>

<h2>The OBS overlay</h2>
<ol>
  <li>In OBS, add a <strong>Browser source</strong>.</li>
  <li>Address: <code>http://127.0.0.1:47321/overlay</code>, width <strong>1920</strong>, height <strong>1080</strong>.</li>
  <li>In Taverne Voice, choose what it shows (active voice, sounds playing, channel points, roulette and challenges), the screen corner and the size. Changes apply without touching OBS.</li>
</ol>
<p><img src="../img/en/capture-overlay.webp" width="460" height="106" alt="The overlay during a Twitch reward" style="max-width:100%"></p>
""", guide=True)

    def stream_deck():
        return pg("stream-deck.html", "Stream Deck", "Install the Taverne Voice plugin on Elgato Stream Deck, StreamDock (Mars Gaming, Mirabox, Ajazz) and Ulanzi.", f"""
<h1>Stream Deck</h1>
<p class="chapo">Each brand has its plugin. Once installed, drag a Taverne Voice action onto a key and pick the sound or voice from a list.</p>
<div class="encadre"><p>The Stream Deck plugins are part of the <a href="licence.html">full version</a>.</p></div>

<h2>The actions</h2>
<div class="tableau"><table>
  <tr><th>Action</th><th>What the key does</th></tr>
  <tr><td>Play a sound</td><td>Plays the chosen sound. The key lights up while it plays.</td></tr>
  <tr><td>Change voice</td><td>Switches to the chosen voice. The key lights up when that voice is active.</td></tr>
  <tr><td>Voice changer on/off</td><td>Like <kbd>F8</kbd>: turns the effect on or off.</td></tr>
  <tr><td>Stop all</td><td>Stops every sound playing.</td></tr>
</table></div>
<p>If Taverne Voice is closed, the plugin launches it in the background.</p>

<h2 id="elgato">Elgato Stream Deck</h2>
<ol>
  <li>In Taverne Voice: <strong>Settings → Stream Deck → Elgato Stream Deck → Install the plugin</strong>.</li>
  <li>The Stream Deck app opens and asks you to confirm.</li>
</ol>
<p>Or download the plugin and double-click it: <a class="bouton second petit" href="{T}Taverne-Voice.streamDeckPlugin">{DL}Elgato plugin</a></p>

<h2 id="streamdock">StreamDock: Mars Gaming, Mirabox, Ajazz</h2>
<p>Mars Gaming (MSD-ONE, MSD-PRO…), Mirabox, Ajazz and Soomfon decks use the <strong>StreamDock</strong> software.</p>
<ol>
  <li>Open StreamDock once, so it creates its folder.</li>
  <li>In Taverne Voice: <strong>Settings → Stream Deck → StreamDock → Install the plugin</strong>.</li>
  <li>Fully close StreamDock (right-click its icon next to the clock → Quit) and reopen it. “Taverne Voice” shows up in the list of actions.</li>
</ol>
<details>
  <summary>Install by hand</summary>
  <p><a class="bouton second petit" href="{T}Taverne-Voice-StreamDock.zip">{DL}StreamDock plugin</a></p>
  <ol>
    <li>Open the zip and copy the <code>com.mrtoto.tavernevoice.sdPlugin</code> folder.</li>
    <li>Press <kbd>Windows</kbd> + <kbd>R</kbd>, type <code>%appdata%\\HotSpot\\StreamDock\\plugins</code> and press Enter.</li>
    <li>Paste the folder, then restart StreamDock.</li>
  </ol>
</details>

<h2 id="ulanzi">Ulanzi</h2>
<ol>
  <li>Open Ulanzi Studio once.</li>
  <li>In Taverne Voice: <strong>Settings → Stream Deck → Ulanzi → Install the plugin</strong>.</li>
  <li>Fully close Ulanzi Studio and reopen it.</li>
</ol>
<details>
  <summary>Install by hand</summary>
  <p><a class="bouton second petit" href="{T}Taverne-Voice-Ulanzi.zip">{DL}Ulanzi plugin</a></p>
  <ol>
    <li>Open the zip and copy the <code>com.mrtoto.tavernevoice.ulanziPlugin</code> folder.</li>
    <li>Press <kbd>Windows</kbd> + <kbd>R</kbd>, type <code>%appdata%\\Ulanzi\\UlanziDeck\\Plugins</code> and press Enter.</li>
    <li>Paste the folder, then restart Ulanzi Studio.</li>
  </ol>
</details>

<h2 id="autres">Other brands</h2>
<p>Razer Stream Controller, Loupedeck, Touch Portal or any software that can open a file or a link:</p>
<ol>
  <li>In Taverne Voice: <strong>Settings → Stream Deck → Create Stream Deck shortcuts</strong>.</li>
  <li>The <code>Documents\\Taverne Voice\\Stream Deck</code> folder opens, with one file per sound, per voice and per action.</li>
  <li>In your Stream Deck software, add an “Open” or “Launch file” action and pick the file you want.</li>
</ol>
<p>You can also paste a link into a “Website” or “URL” action:</p>
<div class="tableau"><table>
  <tr><th>Link</th><th>Effect</th></tr>
  <tr><td><code>taverne://son/Applause</code></td><td>plays a sound (by its name)</td></tr>
  <tr><td><code>taverne://voix/robot</code></td><td>switches to a voice</td></tr>
  <tr><td><code>taverne://effet</code>, <code>/on</code>, <code>/off</code></td><td>turns the effect on or off</td></tr>
  <tr><td><code>taverne://stop</code></td><td>stops all sounds</td></tr>
  <tr><td><code>taverne://ouvrir</code></td><td>opens the window</td></tr>
  <tr><td><code>taverne://voix/robot/30</code></td><td>switches to a voice for 30 seconds</td></tr>
  <tr><td><code>taverne://normal</code></td><td>goes back to the Normal voice</td></tr>
  <tr><td><code>taverne://suivante</code>, <code>taverne://precedente</code></td><td>next or previous voice (in your favorites)</td></tr>
  <tr><td><code>taverne://roulette</code>, <code>taverne://roulette/30</code></td><td>spins the roulette (the drawn voice lasts 30 s)</td></tr>
  <tr><td><code>taverne://defi/chaos</code>, <code>/escalade</code>, <code>/cumul</code>, <code>/piege</code>, <code>/stop</code></td><td>starts or stops a challenge (Chaos, Escalation, Pile-up, Trap voice)</td></tr>
</table></div>
<p>Each sound's panel has a <strong>Copy</strong> button for its link. Voice names in links use the voice's id (robot, demon, chipmunk…), the same in every language.</p>
""", guide=True)

    def reglages():
        return pg("reglages.html", "Backups and diagnostics", "Backups, keyboard shortcuts, audio diagnostics, language and statistics in Taverne Voice.", """
<h1>Backups and diagnostics</h1>
<p class="chapo">It's all in <strong>Settings</strong>, the button at the top of the window.</p>

<h2>Language</h2>
<p>Taverne Voice speaks English or French. By default it follows the language of Windows; <strong>Settings → Language</strong> lets you pick one.</p>

<h2>Backups</h2>
<ul>
  <li>Taverne Voice backs up your settings on its own, once a day. The last 10 are kept.</li>
  <li><strong>Back up now</strong>: before changing everything, for example.</li>
  <li><strong>Restore</strong>: brings back the settings from a date. The previous state is kept in a “Before restore” backup.</li>
  <li><strong>Export all</strong>: a .zip file with your voices, sounds, shortcuts and automations. To move to another PC: <strong>Import…</strong> this file on the new one. Your mics and output stay those of the new PC.</li>
  <li>If a power cut damages the settings file, the last backup is restored on its own, and a message tells you.</li>
</ul>

<h2>Keyboard shortcuts</h2>
<p>They work even mid-game. Click an action's box, then press the key you want: voice changer on/off (<kbd>F8</kbd> by default, can be changed), back to Normal, next or previous voice, roulette, challenge, timer, stop sounds. A voice or a sound can also get its own key, from its panel. A key does only one thing: if you give it to another action, it's removed from the old one.</p>
<p>For a letter or a number, add <kbd>Ctrl</kbd>, <kbd>Alt</kbd> or <kbd>Shift</kbd>, otherwise you couldn't type it anymore. If a key shows in red, another program is already using it.</p>

<h2>Audio diagnostics</h2>
<p><strong>Run diagnostics</strong>, then talk normally. It checks:</p>
<ul>
  <li>that the mic is connected and picks up your voice (without clipping);</li>
  <li>that the output is the virtual cable (CABLE Input) and that the cable is installed;</li>
  <li>that audio is running, and how much processing time the effects take;</li>
  <li>shortcuts refused by Windows and available updates.</li>
</ul>
<p>Each problem comes with a button to fix it. <strong>Copy report</strong> gives you a summary to send if you need help.</p>

<h2>Anonymous statistics</h2>
<p>To know which voices and features get used most, Taverne Voice sends anonymous counters every 12 hours. Nothing about you, your custom voices, your sounds or what you say. <strong>See exactly what is sent</strong> shows the content, and the switch turns sending off. Details in the <a href="confidentialite.html">privacy policy</a>.</p>
""", guide=True)

    def licence():
        return pg("licence.html", "Subscription and keys", "Unlock the full version of Taverne Voice with an account or a key.", """
<h1>Subscription and keys</h1>
<p class="chapo">The demo works with no time limit. A subscription unlocks everything else.</p>

<div class="tableau"><table>
  <tr><th></th><th>Demo</th><th>Subscription</th></tr>
  <tr><td>Voices</td><td>5</td><td>33, plus your own</td></tr>
  <tr><td>Fine-tuning sliders</td><td>no</td><td>yes</td></tr>
  <tr><td>Sounds in the soundboard</td><td>3</td><td>unlimited, in folders</td></tr>
  <tr><td>Channel points and OBS overlay</td><td>no</td><td>yes</td></tr>
  <tr><td>Roulette, challenges and automations</td><td>no</td><td>yes</td></tr>
  <tr><td>Workshop, custom voices and sharing</td><td>no</td><td>yes</td></tr>
  <tr><td>Timer, shortcuts, backups, diagnostics</td><td>yes</td><td>yes</td></tr>
  <tr><td>Stream Deck plugins</td><td>no</td><td>every brand</td></tr>
  <tr><td>Number of PCs</td><td>unlimited</td><td>2 per account</td></tr>
</table></div>
<p><a class="bouton" href="boutique.html">See the plans</a></p>

<h2>The 14-day free trial</h2>
<p>Every new account gets 14 days of the full version, with no payment and no credit card. The trial starts the first time you sign in from the app with your account. At the end, the app goes back to demo, unless you've chosen a plan. There's one trial per account and per PC.</p>

<h2>Sign in from the app</h2>
<ol>
  <li>Create your account on <a href="compte.html">My account</a>. To keep going after the trial, pick your plan in the <a href="boutique.html">shop</a>.</li>
  <li>In Taverne Voice, click <strong>Demo: unlock</strong>, <strong>My account</strong> tab.</li>
  <li>Enter your email address and password.</li>
</ol>
<p>Your PC is linked to your account (2 PCs maximum). The license renews on its own as long as your subscription is active. The app also works offline for several weeks.</p>

<h2>Change PC</h2>
<p>In the app: <strong>Settings → License → Sign out of this PC</strong>. Or on the website, in <a href="compte.html">My account</a>, remove the old PC. Then sign in on the new one.</p>

<h2>You received a key</h2>
<p>A key starts with <code>TV1-</code> and was given to you by the creator (giveaway, partner…). In the app: <strong>Demo: unlock</strong>, <strong>I have a key</strong> tab, paste it and click <strong>Activate the key</strong>.</p>
<div class="encadre"><p>A key or an account is personal. If they're shared, the creator can deactivate them: the app then goes back to demo.</p></div>
""", guide=True)

    def faq():
        q = [
            ("Windows says the app is dangerous. Is it a virus?",
             "<p>No. Windows SmartScreen distrusts every app that doesn't have a paid signing certificate yet. Click <strong>More info</strong> then <strong>Run anyway</strong>.</p>"),
            ("Nobody can hear me on Discord.",
             "<p>Check that Discord's input device is <code>CABLE Output</code>, that Taverne Voice's output is <code>CABLE Input</code>, and that Discord's noise suppression is off. The <a href=\"obs-discord.html\">OBS and Discord</a> guide covers each step.</p>"),
            ("I hear a delay in my voice.",
             "<p>The headset adds a delay when “Hear myself” is on. What OBS and Discord receive isn't delayed. Turn off “Hear myself” during the stream.</p>"),
            ("CABLE Input doesn't show up.",
             "<p>The VB-Audio cable needs a PC restart after installing. Otherwise, open <strong>Settings → Virtual audio cable → Install the cable</strong>.</p>"),
            ("Nobody hears me, or the sound crackles.",
             "<p>Open <strong>Settings → Audio diagnostics</strong> and talk during the test: it checks the mic, the output, the cable and the effects load, and tells you what to do. <strong>Copy report</strong> lets you send the result if you need help. See <a href=\"reglages.html\">Backups and diagnostics</a>.</p>"),
            ("The app is in French.",
             "<p>Taverne Voice follows the language of Windows. To switch: <strong>Réglages → Langue</strong> (the gear at the top right), then pick <strong>English</strong>.</p>"),
            ("My key is refused.",
             "<p>Copy all of it, from <code>TV1-</code> to the last character. Spaces and line breaks don't matter. If the message says the key expired or was deactivated, ask the creator for a new key.</p>"),
            ("My Stream Deck doesn't show Taverne Voice.",
             "<p>Fully close your Stream Deck software (right-click its icon next to the clock → Quit), then reopen it. Plugins only load at startup. See the <a href=\"stream-deck.html\">Stream Deck guide</a>.</p>"),
            ("Where are my settings and sounds?",
             "<p>In <code>%APPDATA%\\TaverneVoice</code>. They're kept through updates.</p>"),
            ("I lost my settings or my voices.",
             "<p>Taverne Voice makes a backup every day. In <strong>Settings → Backups</strong>, click <strong>Restore</strong> next to the date you want. If the settings file gets damaged (power cut), the last backup is restored on its own.</p>"),
            ("How do I share a voice with a friend?",
             "<p>Pick your voice, click <strong>Share</strong> and copy the code (it starts with <code>TVP1.</code>). Your friend clicks <strong>Import a voice</strong> in “My voices” and pastes the code.</p>"),
            ("How does the free trial work?",
             "<p>Create your account on <a href=\"compte.html?vue=inscription\">My account</a>, then in the app click <strong>Demo: unlock</strong>, <strong>My account</strong> tab, and sign in. You get 14 days of the full version, no payment. At the end, the app goes back to demo if you haven't chosen a plan: nothing is charged. One trial per account and per PC.</p>"),
            ("How many PCs with a subscription?",
             "<p>2 PCs at a time. To switch, remove the old one in <a href=\"compte.html\">My account</a> or click <strong>Sign out of this PC</strong> in the app's Settings.</p>"),
            ("I paid on Ko-fi but nothing unlocks.",
             "<p>Check that your Taverne Voice account has <strong>the same email address</strong> as on Ko-fi. In the app, Settings → License → <strong>Refresh</strong>. If you paid with another address, email contact@tavernevoice.fr: your payment will be attached to your account.</p>"),
            ("How do I stop my subscription?",
             "<p>On Ko-fi: <em>Account &amp; Billing</em> menu → <em>Subscriptions</em>. Your access stays until the end of the paid month. The 3-month and 1-year passes don't renew.</p>"),
            ("Does it work on Mac or Linux?",
             "<p>No, Taverne Voice is made for Windows 10 and 11.</p>"),
            ("The app stays open when I close the window.",
             "<p>Yes: it stays next to the clock so your voice and shortcuts keep working. Right-click its icon → <strong>Quit</strong> to stop it.</p>"),
        ]
        corps = "".join(f"<details><summary>{e(a)}</summary>{b}</details>" for a, b in q)
        return pg("faq.html", "Questions", "Frequently asked questions about Taverne Voice.", f"""
<h1>Questions</h1>
<p class="chapo">The most common problems, and how to fix them.</p>
{corps}
""", guide=True)

    # ------------------------------------------------------------------ legal
    def bandeau_identite():
        manque = any(v.startswith("[") for v in G.IDENTITE.values())
        return '<div class="encadre alerte"><p>Seller information to be completed before opening the shop.</p></div>' if manque else ""

    def mentions():
        i = G.IDENTITE
        return pg("mentions-legales.html", "Legal notice", "Legal notice for tavernevoice.fr.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Legal notice</h1>
{bandeau_identite()}
{NOTE_TRADUCTION.format("mentions-legales.html")}
<h2>Publisher</h2>
<p>{e(i["nom"])}<br>{e(i["statut"])}<br>{e(i["adresse"])}<br>Contact: <a href="mailto:{e(i["email"])}">{e(i["email"])}</a></p>
<h2>Hosting</h2>
<p>Website: GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr Street, San Francisco, CA 94107, United States.<br>
Account server: Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, United States.</p>
<h2>Ownership</h2>
<p>The Taverne Voice software, its voices, its icons and this website belong to the publisher. Any copy or redistribution without permission is prohibited. Myinstants sounds remain the property of their authors.</p>
</article></div>
""")

    def cgv():
        i = G.IDENTITE
        return pg("cgv.html", "Terms of sale", "Terms of sale for Taverne Voice.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Terms of sale</h1>
{bandeau_identite()}
<p class="chapo">Effective October 27, 2026.</p>
{NOTE_TRADUCTION.format("cgv.html")}
<h2>1. Seller</h2>
<p>{e(i["nom"])}, {e(i["statut"])}, {e(i["adresse"])}. Contact: {e(i["email"])}.</p>
<h2>2. What is sold</h2>
<p>Access to the full version of the Taverne Voice software for Windows: all voices, fine-tuning, the unlimited soundboard, Twitch channel points, the OBS overlay and the Stream Deck plugins. Access is tied to a personal account and can be used on 2 computers at a time. The free demo remains available without purchase.</p>
<h2>3. Prices and plans</h2>
<ul>
  <li><strong>Monthly</strong>: €4.99 per month, renewed automatically every month until stopped.</li>
  <li><strong>3 months</strong>: €14.99, paid once, no renewal.</li>
  <li><strong>1 year</strong>: €59.99, paid once, no renewal.</li>
</ul>
<p>Prices are in euros, all taxes included{"" if "TVA" in i["statut"] else " (VAT not applicable, article 293 B of the French General Tax Code, if the seller is a micro-entrepreneur)"}. Payment is made on Ko-fi, by card or PayPal. Ko-fi and its payment providers process payment data; the seller has no access to it.</p>
<h2>4. Access</h2>
<p>Access activates as soon as Ko-fi confirms the payment, on the account with the same email address. A new purchase is added after the current access.</p>
<h2>4a. Free trial</h2>
<p>Each new account can try the full version for free for 14 days, without a payment method and without commitment. The trial starts the first time the app signs in with the account and ends on its own after 14 days; nothing is charged. Only one trial is granted per person, per account and per computer. A purchase made during the trial is added after the trial ends.</p>
<h2>5. Stopping the monthly subscription</h2>
<p>The customer can stop the monthly subscription at any time, free of charge, from their Ko-fi account (<em>Account &amp; Billing → Subscriptions</em>). Access remains active until the end of the paid period.</p>
<h2>6. Right of withdrawal</h2>
<p>This is digital content supplied immediately. At the time of purchase, the customer expressly requests immediate access and acknowledges losing their 14-day right of withdrawal (article L221-28 13° of the French Consumer Code). If a technical problem prevents using the software, the customer can write to the seller to find a solution or get a refund.</p>
<h2>7. Use</h2>
<p>The account is personal. Account sharing, resale or bypassing the software's protection may lead to suspension of access, without refund. The customer respects the copyright of the sounds they broadcast.</p>
<h2>8. Warranties</h2>
<p>The seller does their best to keep the software working on Windows 10 and 11 and up to date. The legal conformity warranties for digital content apply.</p>
<h2>9. Disputes</h2>
<p>These terms are governed by French law. In case of dispute, the customer can turn free of charge to a consumer mediator, or to the European online dispute resolution platform.</p>
</article></div>
""")

    def confidentialite():
        i = G.IDENTITE
        return pg("confidentialite.html", "Privacy", "What data Taverne Voice keeps, and why.", f"""
<div class="enveloppe page-etroite"><article>
<h1>Privacy</h1>
{bandeau_identite()}
<p class="chapo">What Taverne Voice keeps, why, and how to delete it.</p>
{NOTE_TRADUCTION.format("confidentialite.html")}
<h2>What is kept</h2>
<ul>
  <li><strong>Your account</strong>: email address, username, password (never in plain text, only a hash), and your language (English or French), to send you emails in that language.</li>
  <li><strong>Your PCs</strong>: an 8-character code computed from the Windows identifier (it says nothing about your PC), the computer's name and the last connection.</li>
  <li><strong>Your payments</strong>: plan, amount, date and email address sent by Ko-fi.</li>
  <li><strong>A history</strong> of sign-ins and account changes, for security.</li>
</ul>
<p>The app doesn't listen in: your voice stays on your PC. Your Twitch connection stays encrypted on your PC.</p>
<h2>Website audience measurement</h2>
<p>To know which pages are read and where visitors come from (TikTok, Twitch, Google…), each page sends the server: the page viewed, the site you came from, your country (inferred by Cloudflare) and the device type (computer, phone, tablet). To count visitors without tracking them, the server computes a fingerprint from your IP address, your browser and a secret value that changes <strong>every day</strong>: it's impossible to recognize you from one day to the next or to recover your IP address, which is never stored. No cookies, nothing is stored in your browser. If your browser asks not to be tracked (“Do Not Track” or “Global Privacy Control”), nothing is sent. These detailed visits are erased after 13 months.</p>
<h2>App statistics</h2>
<p>Every 12 hours, Taverne Voice sends anonymous statistics: an identifier drawn at random at install, the version, the license type (demo, trial, subscription, key), the number of custom voices, sounds and automations, and how many times each Taverne Voice voice and each feature (roulette, challenges…) was used. Never the names of your voices or sounds, your devices, or what you say. You can see exactly what is sent, and turn it off, in <strong>Settings → Anonymous statistics</strong>.</p>
<h2>Why</h2>
<p>To run your access (performance of the contract), send verification codes, and meet accounting obligations.</p>
<h2>Who processes it</h2>
<p>{e(i["nom"])}, data controller. Server hosting: Cloudflare. Email delivery: Brevo. Payments: Ko-fi.</p>
<h2>How long</h2>
<p>As long as your account exists. Payments are kept for 10 years for accounting.</p>
<h2>Your rights</h2>
<p>You can delete your account yourself in <a href="compte.html">My account</a>. For any other request (access, correction, erasure): <a href="mailto:{e(i["email"])}">{e(i["email"])}</a>. You can also contact the CNIL (the French data protection authority).</p>
<h2>Cookies</h2>
<p>The site uses no advertising cookies and no audience measurement cookies (the measurement described above doesn't need any). It only keeps your account sign-in and your language choice in your browser. The partners' Twitch player only loads if you click it.</p>
</article></div>
""")

    def page404():
        return pg("404.html", "Page not found", "This page doesn't exist.", """
<div class="enveloppe" style="padding:80px 0"><h1>Page not found</h1><p class="chapo" style="margin-top:16px">This page doesn't exist or has moved.</p><p><a class="bouton" href="index.html">Back to home</a></p></div>
""", noindex=True)

    return {
        "index.html": accueil, "boutique.html": boutique, "compte.html": compte, "partenaires.html": partenaires_page,
        "installation.html": installation, "obs-discord.html": obs_discord, "voix.html": voix, "soundboard.html": soundboard,
        "twitch-obs.html": twitch_obs, "stream-deck.html": stream_deck, "interactif.html": interactif, "atelier.html": atelier,
        "reglages.html": reglages, "licence.html": licence, "faq.html": faq,
        "mentions-legales.html": mentions, "cgv.html": cgv, "confidentialite.html": confidentialite, "404.html": page404,
    }
