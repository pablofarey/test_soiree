# Soirées

Site statique d'affiches en plein écran, façon story : un dossier par jour, consultable au téléphone via un QR code. La page ouvre sur l'affiche du jour, on tape pour faire défiler le détail, et un menu déroulant en haut donne accès à l'affiche des autres jours.

## Ajouter une soirée

Un dossier par jour dans `photos/`, nommé `AAAA-MM-JJ_titre` :

```
photos/
  2026-09-15_ouverture/
    00_affiche.jpg      -> le premier ecran
    01_planning.jpg     -> les ecrans suivants, dans l'ordre
    02_bar.jpg
  2026-09-16_concert/
    00_affiche.jpg      -> une affiche seule suffit
```

La première image par ordre alphabétique sert d'affiche : préfixe-la `00_`. Les suivantes forment les écrans de détail, dans l'ordre de leur nom, et ne sont visibles que le jour même. Le titre affiché vient du nom du dossier, date retirée.

Formats acceptés : jpg, png, webp, gif, avif, svg. Le HEIC des iPhone n'est pas affichable par les navigateurs, à convertir en jpg avant.

## Ce que voit un visiteur

La date du jour est celle de son téléphone, donc le site bascule tout seul d'une soirée à l'autre, sans republication. Il voit l'affiche du jour, puis le détail en tapant sur la droite de l'écran, comme une story : tap à gauche pour revenir, glissement du doigt, barres de progression en haut. Par le menu déroulant, il ne voit que l'affiche des autres jours. Si aucune soirée ne tombe aujourd'hui, la page ouvre sur la prochaine à venir.

## Voir le résultat en local

```bash
python3 build.py
python3 -m http.server 8000
```

Puis http://localhost:8000

`build.py` regénère `photos.json`, la liste que lit la page. À relancer après chaque ajout d'images. Les dossiers mal nommés sont signalés et ignorés.

## Publier

Un push sur `main` déclenche le workflow : il relance `build.py` et publie sur GitHub Pages. Les images peuvent aussi être ajoutées directement depuis l'interface web de GitHub, y compris depuis un téléphone, le site se met à jour tout seul.

Le dépôt doit être public (GitHub Pages gratuit) et Pages doit être réglé sur la source « GitHub Actions ».

## QR code

`qr.html` affiche le QR code du site en grand. Ouverte en ligne, la page se pré-remplit avec l'URL du site. Ctrl+P pour l'imprimer.
