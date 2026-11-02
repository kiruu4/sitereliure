# Au Fil de la Reliure

Site vitrine de l’atelier de **François Battistini**, artisan relieur à Dun-sur-Meuse (Meuse).
Reliure, dorure artisanale, restauration de livres anciens.

Le site est fait en HTML et CSS simples, sans framework ni étape de compilation. Il peut être publié tel quel sur GitHub Pages.

## Structure

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil |
| `savoir-faire.html` | Savoir-faire et prestations |
| `realisations.html` | Galerie des réalisations |
| `atelier.html` | L’atelier / À propos |
| `contact.html` | Coordonnées, horaires, carte |
| `mentions-legales.html` | Mentions légales |
| `404.html` | Page « introuvable » |
| `css/style.css` | Toute la mise en forme (couleurs en haut du fichier) |
| `js/main.js` | Menu mobile, filtres de la galerie, agrandissement des photos |
| `images/` | Icône, photos de l’atelier et des réalisations |
| `fonts/` | Polices du site et leurs licences (SIL OFL) |
| `outils/generer-pages.py` | Script qui fabrique toutes les pages `.html` (voir plus bas) |

## Mettre le site en ligne (GitHub Pages)

1. Sur GitHub, ouvrir le dépôt, puis **Settings → Pages**.
2. Dans *Source*, choisir **Deploy from a branch**, puis la branche **main** et le dossier **/ (root)**.
3. Après une ou deux minutes, le site est visible à l’adresse indiquée, par exemple `https://<compte>.github.io/sitereliure/`.

## Modifier les textes : le générateur de pages

Toutes les pages `.html` sont fabriquées par le script **`outils/generer-pages.py`**.
L’en-tête, le menu et le pied de page n’y sont écrits qu’une fois, puis recopiés sur chaque page.

1. Modifier le texte dans `outils/generer-pages.py`. Les coordonnées (téléphone, adresse, e-mail) sont regroupées tout en haut du fichier.
2. Depuis le dossier du site, lancer :

   ```bash
   python3 outils/generer-pages.py
   ```

   Le script n’a besoin que de Python 3, sans aucune installation.
3. Vérifier le résultat dans le navigateur, puis publier les fichiers modifiés.

> ⚠️ Le script **réécrit** les fichiers `.html`. Une modification faite directement dans un fichier `.html` sera perdue au prochain lancement. Il faut donc toujours modifier le script, pas les pages.

## Informations restant à compléter

On les retrouve en cherchant dans `outils/generer-pages.py` le texte entre crochets `[...]`.

- **E-mail** : en haut du script, remplacer `EMAIL = "[email à venir]"` par la vraie adresse, puis mettre `EMAIL_READY = True`. L’adresse apparaîtra alors partout : pied de page, Contact et Mentions légales. Elle sera cliquable, avec l’objet « Demande de devis ».
- **Horaires** : section « Contact », bloc « Horaires ».
- **Parcours de François** : section « Atelier », paragraphe `[Texte à compléter : …]`.
- **Photos** : voir ci-dessous.

## Ajouter ou remplacer des photos

1. Déposer les photos dans `images/realisations/`, de préférence en **JPEG**, d’environ 1600 px de large et de moins de 400 Ko.
2. Dans `outils/generer-pages.py`, la liste `GALLERY` contient une ligne par photo :

   ```python
   ("ma-photo.jpg", "reliure", "Reliure d’art", "Description de la photo"),
   ```

   - Les quatre éléments sont, dans l’ordre : le nom du fichier, la catégorie (`reliure`, `dorure` ou `restauration`, qui fait fonctionner les filtres), un titre et la légende.
   - Ajouter une ligne pour ajouter une photo, en supprimer une pour la retirer.
3. Les 3 premières photos de la liste sont aussi présentées sur l’accueil.
4. Pour la photo de l’atelier, remplacer `images/atelier.svg` par le nom de la photo dans la section « Atelier » du script.
5. Relancer `python3 outils/generer-pages.py`.

## Couleurs et polices

Les couleurs se règlent au début de `css/style.css` (`--paper`, `--leather`, `--gold`, etc.).
Les polices *Playfair Display* (titres) et *Lora* (texte et menus) sont **hébergées sur le site**, dans le dossier `fonts/`. Le site ne fait donc aucun appel à Google : c’est plus rapide et plus respectueux des visiteurs (RGPD). Ces polices sont libres (licence SIL OFL), et leurs licences sont jointes dans `fonts/`.

## Tester sur son ordinateur

Il suffit d’ouvrir `index.html` dans un navigateur. On peut aussi lancer un petit serveur :

```bash
python3 -m http.server 8000
```

puis aller à l’adresse http://localhost:8000.
