#!/usr/bin/env python3
"""Génère les pages HTML du site (en-tête et pied de page communs à toutes les pages).

Utilisation, depuis la racine du dépôt :
    python3 outils/generer-pages.py

ATTENTION : ce script réécrit les fichiers .html à la racine du dépôt.
Toute modification faite à la main dans ces fichiers est perdue :
modifiez plutôt ce script, puis relancez-le.
"""
import json
import re
from pathlib import Path

# Racine du dépôt (le dossier parent de « outils »)
OUT = Path(__file__).resolve().parent.parent

SITE = "Au Fil de la Reliure"
TEL_DISPLAY = "06 47 60 94 11"
TEL_LINK = "+33647609411"
ADDRESS_L1 = "8 rue du Faubourg Saint-Martin"
ADDRESS_L2 = "55110 Dun-sur-Meuse"
MAPS_QUERY = "8+rue+du+Faubourg+Saint-Martin,+55110+Dun-sur-Meuse"
# E-mail à venir : remplacer EMAIL quand il sera connu (et passer EMAIL_READY à True)
EMAIL = "[email à venir]"
EMAIL_READY = False

NAV = [
    ("index.html", "Accueil"),
    ("savoir-faire.html", "Savoir-faire"),
    ("realisations.html", "Réalisations"),
    ("atelier.html", "L’atelier"),
    ("contact.html", "Contact"),
]

LOGO = """<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
          <rect x="9" y="6" width="30" height="36" rx="2" fill="currentColor"/>
          <rect x="9" y="6" width="6" height="36" rx="1.5" fill="#000" opacity=".18"/>
          <path d="M15 14h20M15 34h20" stroke="#D9B878" stroke-width="1.4"/>
          <path d="M25 20l2 3.5 3.8.6-2.8 2.7.7 3.8-3.7-1.9-3.7 1.9.7-3.8-2.8-2.7 3.8-.6z" fill="#D9B878"/>
        </svg>"""

JSONLD = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": SITE,
    "description": "Artisan relieur à Dun-sur-Meuse : reliure d’art, reliure traditionnelle, "
                   "reliure cartonnée et administrative, dorure artisanale, restauration de livres anciens.",
    "founder": {"@type": "Person", "name": "François Battistini"},
    "telephone": TEL_LINK,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDRESS_L1,
        "postalCode": "55110",
        "addressLocality": "Dun-sur-Meuse",
        "addressRegion": "Grand Est",
        "addressCountry": "FR",
    },
    "areaServed": ["Meuse", "Grand Est"],
    "priceRange": "Sur devis",
}


def email_html(cls=""):
    if EMAIL_READY:
        return f'<a class="{cls}" href="mailto:{EMAIL}?subject=Demande%20de%20devis">{EMAIL}</a>'
    return f'<span class="placeholder">{EMAIL}</span>'


def page(filename, title, description, body, current=None, extra_head=""):
    nav_items = []
    for href, label in NAV:
        aria = ' aria-current="page"' if href == current else ""
        nav_items.append(f'<li><a href="{href}"{aria}>{label}</a></li>')
    nav_html = "\n            ".join(nav_items)
    full_title = f"{title} | {SITE}" if title != SITE else f"{SITE} – Relieur à Dun-sur-Meuse (Meuse)"
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#5E2E15">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:locale" content="fr_FR">
  <link rel="icon" href="images/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="fonts/lora.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/playfair-display.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.classList.add('js');</script>
  <script src="js/main.js" defer></script>{extra_head}
</head>
<body>
  <a class="skip-link" href="#contenu">Aller au contenu</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html">
        {LOGO}
        <span class="brand-text">
          <span class="brand-name">{SITE}</span>
          <span class="brand-tag">François Battistini · Artisan relieur</span>
        </span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-principal">
        <span class="nav-toggle-bars" aria-hidden="true"></span>
        <span class="nav-toggle-label">Menu</span>
      </button>
      <nav class="site-nav" id="menu-principal" aria-label="Navigation principale">
        <ul>
            {nav_html}
        </ul>
      </nav>
    </div>
  </header>

  <main id="contenu">
{body}
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <p class="footer-name">{SITE}</p>
        <p>François Battistini<br>Artisan relieur – doreur – restaurateur</p>
      </div>
      <div>
        <p class="footer-title">Atelier</p>
        <p>{ADDRESS_L1}<br>{ADDRESS_L2}</p>
      </div>
      <div>
        <p class="footer-title">Contact</p>
        <p><a href="tel:{TEL_LINK}">{TEL_DISPLAY}</a><br>{email_html()}</p>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>© <span data-year>2026</span> {SITE} · <a href="mentions-legales.html">Mentions légales</a></p>
    </div>
  </footer>

  <dialog class="lightbox" aria-label="Photo agrandie">
    <button class="lightbox-close" type="button" aria-label="Fermer">×</button>
    <figure>
      <img src="" alt="">
      <figcaption></figcaption>
    </figure>
  </dialog>
</body>
</html>
"""
    # Typographie française : espace insécable avant : ; ! ? » et après «
    html = re.sub(r" ([:;!?»])", "\u00a0\\1", html)
    html = html.replace("« ", "«\u00a0")
    (OUT / filename).write_text(html, encoding="utf-8")


ORNAMENT = '<p class="ornament" aria-hidden="true"><span>❦</span></p>'

CTA = f"""    <section class="section cta">
      <div class="container narrow center">
        <h2>Chaque ouvrage est unique</h2>
        <p>Les tarifs sont établis <strong>sur devis</strong>, gratuitement, selon l’ouvrage, son état et la finition souhaitée.
        N’hésitez pas à passer à l’atelier ou à appeler pour en parler.</p>
        <div class="button-row center">
          <a class="button" href="tel:{TEL_LINK}">Appeler le {TEL_DISPLAY}</a>
          <a class="button button-ghost" href="contact.html">Toutes les coordonnées</a>
        </div>
      </div>
    </section>"""

# Réalisations : (fichier, catégorie, titre, légende)
GALLERY = [
    ("reliure-art-1.svg", "reliure", "Reliure d’art", "Reliure d’art en plein cuir, décor doré"),
    ("restauration-1.svg", "restauration", "Restauration", "Restauration d’un livre ancien : couture et couvrure reprises"),
    ("dorure-1.svg", "dorure", "Dorure", "Titre et filets dorés à la feuille d’or"),
    ("reliure-traditionnelle-1.svg", "reliure", "Reliure traditionnelle", "Demi-reliure cuir à coins, papier marbré"),
    ("reliure-cartonnee-1.svg", "reliure", "Reliure cartonnée", "Reliure cartonnée toilée"),
    ("restauration-2.svg", "restauration", "Restauration", "Consolidation de pages et reprise des coins"),
    ("reliure-administrative-1.svg", "reliure", "Reliure administrative", "Registre relié, titre au dos"),
    ("dorure-2.svg", "dorure", "Dorure", "Décor aux petits fers"),
    ("reliure-document-1.svg", "reliure", "Reliure de document", "Mémoire relié, titre doré"),
]

CAT_LABEL = {"reliure": "Reliure", "dorure": "Dorure", "restauration": "Restauration"}


def gallery_items(items):
    out = []
    for f, cat, title, caption in items:
        out.append(f"""          <li class="gallery-item" data-category="{cat}">
            <a href="images/realisations/{f}" data-lightbox data-caption="{caption}">
              <img src="images/realisations/{f}" alt="{caption}" width="800" height="600" loading="lazy">
            </a>
            <p class="gallery-caption"><span class="tag">{CAT_LABEL[cat]}</span> {caption}</p>
          </li>""")
    return "\n".join(out)


# ---------------------------------------------------------------- Accueil
page("index.html", SITE,
     "Au Fil de la Reliure, atelier de François Battistini, artisan relieur à Dun-sur-Meuse (Meuse) : "
     "reliure d’art, traditionnelle, cartonnée, administrative, dorure et restauration de livres anciens. Sur devis.",
     f"""    <section class="hero">
      <div class="container hero-inner">
        <p class="eyebrow">Artisan relieur à <span class="nowrap">Dun-sur-Meuse</span> · Meuse</p>
        <h1>{SITE}</h1>
        <p class="hero-lead">Reliure, dorure et restauration de livres anciens,<br class="br-wide"> réalisées à la main dans l’atelier de François Battistini.</p>
        <div class="button-row">
          <a class="button button-gold" href="contact.html">Demander un devis</a>
          <a class="button button-light" href="savoir-faire.html">Découvrir le savoir-faire</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow center">
        <h2>Le livre, entre de bonnes mains</h2>
        <p class="lead">Un livre de famille à sauver, un mémoire à relier, un registre à habiller, une collection à mettre en valeur :
        à l’atelier, chaque ouvrage est pris en charge avec soin, selon les gestes et les matériaux de la reliure traditionnelle.</p>
        {ORNAMENT}
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <h2 class="center">Les prestations</h2>
        <div class="cards">
          <article class="card">
            <div class="card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48"><path d="M8 10c6-2 11-1 16 3 5-4 10-5 16-3v28c-6-2-11-1-16 3-5-4-10-5-16-3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M24 13v28" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Reliure</h3>
            <p>Reliure d’art, traditionnelle et artisanale, mais aussi reliure cartonnée, administrative et de documents.</p>
            <a class="card-link" href="savoir-faire.html#reliure">En savoir plus <span aria-hidden="true">→</span></a>
          </article>
          <article class="card">
            <div class="card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48"><path d="M24 6l4.5 9.5 10.5 1.5-7.6 7.3 1.8 10.4L24 29.8l-9.2 4.9 1.8-10.4L9 17l10.5-1.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M10 42h28" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Dorure artisanale</h3>
            <p>Titres, filets et décors dorés à la main, à la feuille d’or, pour signer et sublimer chaque reliure.</p>
            <a class="card-link" href="savoir-faire.html#dorure">En savoir plus <span aria-hidden="true">→</span></a>
          </article>
          <article class="card">
            <div class="card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48"><rect x="11" y="7" width="24" height="34" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M28 30l9-9 4 4-9 9h-4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M16 15h12M16 21h8" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Restauration</h3>
            <p>Restauration de livres anciens : couture, dos, coins, coiffes et pages abîmées, dans le respect de l’ouvrage.</p>
            <a class="card-link" href="savoir-faire.html#restauration">En savoir plus <span aria-hidden="true">→</span></a>
          </article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 class="center">Quelques réalisations</h2>
        <ul class="gallery gallery-preview">
{gallery_items(GALLERY[:3])}
        </ul>
        <p class="center"><a class="button button-ghost" href="realisations.html">Voir toutes les réalisations</a></p>
      </div>
    </section>

{CTA}""",
     current="index.html",
     extra_head='\n  <script type="application/ld+json">' + json.dumps(JSONLD, ensure_ascii=False) + "</script>")

# ---------------------------------------------------------------- Savoir-faire
page("savoir-faire.html", "Savoir-faire et prestations",
     "Reliure d’art, traditionnelle, artisanale, cartonnée, administrative, reliure de documents, dorure artisanale "
     "et restauration de livres anciens à Dun-sur-Meuse. Tarifs sur devis.",
     f"""    <section class="page-head">
      <div class="container narrow center">
        <p class="eyebrow">Savoir-faire</p>
        <h1>Prestations de l’atelier</h1>
        <p class="lead">Un artisan relieur au service de vos livres et de vos documents, du simple registre à la reliure d’art.</p>
      </div>
    </section>

    <section class="section" id="reliure">
      <div class="container">
        <div class="prestation">
          <div class="prestation-intro">
            <h2>La reliure</h2>
            <p>Couture des cahiers, endossure, couvrure : chaque reliure est réalisée à la main, avec des matériaux choisis
            pour durer – cuirs, toiles, papiers marbrés, cartons de qualité.</p>
          </div>
          <dl class="services">
            <div><dt>Reliure d’art</dt><dd>Pièce unique en plein cuir ou demi-cuir, décor et dorure, pour les ouvrages d’exception.</dd></div>
            <div><dt>Reliure traditionnelle</dt><dd>Selon les techniques anciennes : couture sur nerfs, dos à nerfs, coiffes et tranchefiles.</dd></div>
            <div><dt>Reliure artisanale</dt><dd>Une reliure faite main, adaptée à votre livre, à son usage et à vos goûts.</dd></div>
            <div><dt>Reliure cartonnée</dt><dd>Une solution solide et soignée, en toile ou en papier, pour protéger livres, revues et collections.</dd></div>
            <div><dt>Reliure administrative</dt><dd>Registres, actes, délibérations, archives de mairies, d’associations ou d’entreprises.</dd></div>
            <div><dt>Reliure de document</dt><dd>Thèses, mémoires, rapports, partitions, livres de famille ou d’or…</dd></div>
          </dl>
        </div>
      </div>
    </section>

    {ORNAMENT}

    <section class="section" id="dorure">
      <div class="container">
        <div class="prestation">
          <div class="prestation-intro">
            <h2>La dorure artisanale</h2>
            <p>La touche finale qui signe une reliure. Les fers sont chauffés puis appliqués à la main sur la feuille d’or.</p>
          </div>
          <dl class="services">
            <div><dt>Titres et auteurs</dt><dd>Composés en caractères mobiles et dorés au dos ou sur le plat.</dd></div>
            <div><dt>Filets et décors</dt><dd>Filets, fleurons et décors aux petits fers, sobres ou plus riches.</dd></div>
            <div><dt>Personnalisation</dt><dd>Initiales, dates, noms : pour un cadeau, un livre d’or ou un registre.</dd></div>
          </dl>
        </div>
      </div>
    </section>

    {ORNAMENT}

    <section class="section" id="restauration">
      <div class="container">
        <div class="prestation">
          <div class="prestation-intro">
            <h2>La restauration de livres anciens</h2>
            <p>Redonner vie à un ouvrage sans trahir son histoire : l’intervention est toujours mesurée et respectueuse de l’original.</p>
          </div>
          <dl class="services">
            <div><dt>Reliure et couture</dt><dd>Reprise de couture, consolidation ou remplacement du dos, des mors et des coiffes.</dd></div>
            <div><dt>Couvrure</dt><dd>Réparation des coins et des plats, remise en état ou remplacement du cuir et de la toile.</dd></div>
            <div><dt>Corps d’ouvrage</dt><dd>Pages déchirées, cahiers détachés, gardes abîmées.</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <h2 class="center">Comment ça se passe ?</h2>
        <ol class="steps">
          <li><h3>Prise de contact</h3><p>Par téléphone ou directement à l’atelier, vous présentez votre ouvrage et votre projet.</p></li>
          <li><h3>Devis gratuit</h3><p>Après examen du livre, un devis détaillé vous est remis, sans engagement.</p></li>
          <li><h3>Réalisation</h3><p>Le travail est réalisé à la main, à l’atelier, dans les délais convenus.</p></li>
          <li><h3>Remise de l’ouvrage</h3><p>Vous récupérez votre livre, relié ou restauré, prêt à traverser les années.</p></li>
        </ol>
      </div>
    </section>

{CTA}""",
     current="savoir-faire.html")

# ---------------------------------------------------------------- Réalisations
page("realisations.html", "Réalisations",
     "Galerie des réalisations de l’atelier Au Fil de la Reliure : reliures, dorures et restaurations de livres anciens.",
     f"""    <section class="page-head">
      <div class="container narrow center">
        <p class="eyebrow">Galerie</p>
        <h1>Réalisations</h1>
        <p class="lead">Un aperçu des travaux sortis de l’atelier. Touchez une photo pour l’agrandir.</p>
      </div>
    </section>

    <section class="section section-tight">
      <div class="container">
        <div class="filters" role="group" aria-label="Filtrer les réalisations" hidden>
          <button type="button" class="filter" data-filter="all" aria-pressed="true">Tout</button>
          <button type="button" class="filter" data-filter="reliure" aria-pressed="false">Reliure</button>
          <button type="button" class="filter" data-filter="dorure" aria-pressed="false">Dorure</button>
          <button type="button" class="filter" data-filter="restauration" aria-pressed="false">Restauration</button>
        </div>
        <ul class="gallery">
{gallery_items(GALLERY)}
        </ul>
      </div>
    </section>

{CTA}""",
     current="realisations.html")

# ---------------------------------------------------------------- Atelier
page("atelier.html", "L’atelier",
     "François Battistini, artisan relieur à Dun-sur-Meuse : l’atelier Au Fil de la Reliure, ses outils, ses matériaux "
     "et son attachement au travail fait main.",
     f"""    <section class="page-head">
      <div class="container narrow center">
        <p class="eyebrow">À propos</p>
        <h1>L’atelier</h1>
        <p class="lead">Au cœur de Dun-sur-Meuse, un atelier où le temps se prend pour bien faire.</p>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="split-text">
          <h2>François Battistini, artisan relieur</h2>
          <p>Passionné par le livre et par les métiers de la main, François Battistini a fondé <em>{SITE}</em>
          à Dun-sur-Meuse, dans la Meuse.</p>
          <p class="placeholder-block">[Texte à compléter : parcours, formation, années de métier, ce qui l’a amené à la reliure…]</p>
          <p>Relieur, doreur et restaurateur, il travaille aussi bien pour les particuliers que pour les collectivités,
          les associations ou les professionnels : du livre de famille à restaurer au registre municipal à relier.</p>
        </div>
        <figure class="split-media">
          <img src="images/atelier.svg" alt="L’atelier (photo à venir)" width="800" height="1000" loading="lazy">
        </figure>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <h2 class="center">Les outils et les matériaux</h2>
        <div class="cards">
          <article class="card">
            <h3>Les outils</h3>
            <p>Cousoir, presses, plioirs, couteaux à parer, fers et palettes à dorer : des outils traditionnels,
            dont certains ont plusieurs générations d’usage.</p>
          </article>
          <article class="card">
            <h3>Les matériaux</h3>
            <p>Cuirs, toiles, papiers marbrés et cartons sélectionnés pour leur tenue dans le temps,
            colles et fils adaptés aux livres anciens.</p>
          </article>
          <article class="card">
            <h3>L’or</h3>
            <p>Feuille d’or et fers chauffés : la dorure se fait à la main, lettre après lettre, filet après filet.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow center">
        <h2>L’esprit de l’atelier</h2>
        <p class="lead">Prendre le temps, écouter l’histoire de chaque livre, choisir la solution juste plutôt que la plus
        spectaculaire : c’est ainsi que se transmet un savoir-faire.</p>
        {ORNAMENT}
      </div>
    </section>

{CTA}""",
     current="atelier.html")

# ---------------------------------------------------------------- Contact
page("contact.html", "Contact",
     f"Contacter Au Fil de la Reliure, artisan relieur à Dun-sur-Meuse : {TEL_DISPLAY}, {ADDRESS_L1}, {ADDRESS_L2}. Devis gratuit.",
     f"""    <section class="page-head">
      <div class="container narrow center">
        <p class="eyebrow">Contact</p>
        <h1>Passer à l’atelier</h1>
        <p class="lead">Pour un devis ou un simple conseil, le plus simple est d’appeler ou de venir avec votre ouvrage.</p>
      </div>
    </section>

    <section class="section section-tight">
      <div class="container contact-grid">
        <div class="contact-info">
          <div class="contact-block">
            <h2>Téléphone</h2>
            <p><a class="big-link" href="tel:{TEL_LINK}">{TEL_DISPLAY}</a></p>
          </div>
          <div class="contact-block">
            <h2>E-mail</h2>
            <p>{email_html("big-link")}</p>
          </div>
          <div class="contact-block">
            <h2>Adresse</h2>
            <address>{SITE}<br>{ADDRESS_L1}<br>{ADDRESS_L2}</address>
            <p><a href="https://www.openstreetmap.org/search?query={MAPS_QUERY}" target="_blank" rel="noopener">Voir sur OpenStreetMap</a>
            · <a href="https://www.google.com/maps/dir/?api=1&amp;destination={MAPS_QUERY}" target="_blank" rel="noopener">Itinéraire</a></p>
          </div>
          <div class="contact-block">
            <h2>Horaires</h2>
            <p>Horaires à venir.<br>En attendant, l’atelier vous reçoit <strong>sur rendez-vous</strong> : appelez avant de passer.</p>
          </div>
          <div class="contact-block">
            <h2>Tarifs</h2>
            <p>Sur devis, gratuit et sans engagement.</p>
          </div>
          <p class="button-row">
            <a class="button" href="tel:{TEL_LINK}">Appeler l’atelier</a>
          </p>
        </div>
        <div class="map">
          <iframe title="Carte : Dun-sur-Meuse"
            src="https://www.openstreetmap.org/export/embed.html?bbox=5.1650%2C49.3790%2C5.1990%2C49.3930&amp;layer=mapnik"
            loading="lazy" referrerpolicy="no-referrer"></iframe>
          <p class="map-note">Dun-sur-Meuse (55110). <a href="https://www.openstreetmap.org/search?query={MAPS_QUERY}" target="_blank" rel="noopener">Agrandir la carte</a></p>
        </div>
      </div>
    </section>""",
     current="contact.html")

# ---------------------------------------------------------------- Mentions légales
page("mentions-legales.html", "Mentions légales",
     "Mentions légales du site Au Fil de la Reliure.",
     f"""    <section class="page-head">
      <div class="container narrow center">
        <h1>Mentions légales</h1>
      </div>
    </section>

    <section class="section section-tight">
      <div class="container narrow prose">
        <h2>Éditeur du site</h2>
        <p>{SITE}<br>
        François Battistini, entreprise individuelle<br>
        {ADDRESS_L1}, {ADDRESS_L2}<br>
        Téléphone : <a href="tel:{TEL_LINK}">{TEL_DISPLAY}</a><br>
        E-mail : {email_html()}<br>
        SIREN : 919 149 401</p>
        <p>Directeur de la publication : François Battistini.</p>

        <h2>Hébergement</h2>
        <p>GitHub, Inc. (service GitHub Pages)<br>
        88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis<br>
        <a href="https://github.com" target="_blank" rel="noopener">github.com</a></p>

        <h2>Propriété intellectuelle</h2>
        <p>L’ensemble des textes et photographies de ce site est la propriété de {SITE}, sauf mention contraire.
        Toute reproduction sans autorisation préalable est interdite.</p>

        <h2>Données personnelles et cookies</h2>
        <p>Ce site ne comporte aucun formulaire, ne collecte aucune donnée personnelle et ne dépose aucun cookie de mesure d’audience.</p>
        <p>Les polices de caractères sont hébergées sur le site lui-même. Seule la carte de la page Contact fait appel à un service tiers
        (OpenStreetMap), qui peut recevoir votre adresse IP lors de son affichage.</p>

        <h2>Crédits</h2>
        <p>Polices : <em>Playfair Display</em> (Claus Eggers Sørensen) et <em>Lora</em> (Cyreal),
        sous licence SIL Open Font License 1.1. Carte : © les contributeurs d’OpenStreetMap.</p>
      </div>
    </section>""")

# ---------------------------------------------------------------- 404
page("404.html", "Page introuvable",
     "Cette page n’existe pas.",
     """    <section class="page-head">
      <div class="container narrow center">
        <p class="eyebrow">Erreur 404</p>
        <h1>Page introuvable</h1>
        <p class="lead">Cette page semble s’être égarée entre deux cahiers…</p>
        <p class="button-row center"><a class="button" href="index.html">Retour à l’accueil</a></p>
      </div>
    </section>""")

print("Pages générées dans", OUT)
