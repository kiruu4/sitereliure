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

## Mettre le site en ligne (GitHub Pages)

1. Sur GitHub, ouvrir le dépôt, puis **Settings → Pages**.
2. Dans *Source*, choisir **Deploy from a branch**, puis la branche **main** et le dossier **/ (root)**.
3. Après une ou deux minutes, le site est visible à l’adresse indiquée, par exemple `https://<compte>.github.io/sitereliure/`.

## Informations restant à compléter

On les retrouve en cherchant dans les fichiers le texte entre crochets `[...]`.

- **E-mail** : remplacer `<span class="placeholder">[email à venir]</span>` par
  `<a href="mailto:adresse@exemple.fr?subject=Demande%20de%20devis">adresse@exemple.fr</a>`.
  Il apparaît dans toutes les pages (pied de page), ainsi que dans `contact.html` et `mentions-legales.html`.
- **Horaires** : dans `contact.html`, bloc « Horaires ».
- **Parcours de François** : dans `atelier.html`, paragraphe `[Texte à compléter : …]`.
- **Photos** : voir ci-dessous.

> L’en-tête et le pied de page sont recopiés dans chaque page. Une modification de ces parties est donc à faire dans **chaque fichier `.html`**.

## Ajouter ou remplacer des photos

1. Déposer les photos dans `images/realisations/`, de préférence en **JPEG**, d’environ 1600 px de large et de moins de 400 Ko.
2. Dans `realisations.html`, chaque photo correspond à un bloc de ce type :

   ```html
   <li class="gallery-item" data-category="reliure">
     <a href="images/realisations/ma-photo.jpg" data-lightbox data-caption="Description de la photo">
       <img src="images/realisations/ma-photo.jpg" alt="Description de la photo" width="800" height="600" loading="lazy">
     </a>
     <p class="gallery-caption"><span class="tag">Reliure</span> Description de la photo</p>
   </li>
   ```

   - `data-category` vaut `reliure`, `dorure` ou `restauration` : c’est ce qui fait fonctionner les filtres.
   - Copier un bloc pour ajouter une photo, en supprimer un pour la retirer.
3. Les 3 premières photos sont aussi présentées sur l’accueil (`index.html`, section « Quelques réalisations »).
4. La photo de l’atelier se remplace en modifiant `images/atelier.svg` dans `atelier.html`.

## Couleurs et polices

Les couleurs se règlent au début de `css/style.css` (`--paper`, `--leather`, `--gold`, etc.).
Les polices *Cormorant Garamond* (titres) et *EB Garamond* (texte) sont chargées depuis Google Fonts.

## Tester sur son ordinateur

Il suffit d’ouvrir `index.html` dans un navigateur. On peut aussi lancer un petit serveur :

```bash
python3 -m http.server 8000
```

puis aller à l’adresse http://localhost:8000.
