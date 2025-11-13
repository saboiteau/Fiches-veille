# Structure et workflow - Veille Technologique

Ce document décrit la structure recommandée et le workflow minimal pour ajouter une fiche de veille.

Arborescence recommandée :
- fiches/                # fiches analytiques organisées par mois : fiches/YYYY-MM/identifiant.md
- templates/             # modèles (fiche-template.md)
- raw-data/              # contenus bruts convertis en markdown (IGNORÉ par git)
- scripts/               # scripts d'aide (création, initialisation)
- docs/                  # documentation secondaire
- index.md               # index principal (déjà présent)

Workflow pour ajouter une fiche :
1. Initialiser la structure (une seule fois)
   bash scripts/init_structure.sh

2. Créer une nouvelle fiche à partir du template :
   python3 scripts/new_fiche.py --id nom-auteur-sujet-YYYY-MM-DD \
       --title "Titre original de l'article" \
       --date 2025-11-12 \
       --url "https://..." \
       --authors "Prénom Nom" \
       --keywords "mot1,mot2" \
       --source "SourceCourte"
   - Le script crée fiches/YYYY-MM/identifiant.md et un placeholder raw-data/identifiant.md (sauf si --no-raw).
   - Le script affiche la ligne à copier dans index.md (section du mois correspondant).

3. Remplir la fiche (sections `Ton`, `Pense-betes`, `RésuméDe400mots`) en français.

4. Ajouter manuellement la ligne fournie par le script dans `index.md` dans la section du mois (ordre décroissant).

Notes :
- raw-data/ est volontairement ignoré par git pour éviter de versionner des copies d'articles.
- Le script n'édite pas index.md automatiquement pour éviter des conflits manuels ; si vous le souhaitez, je peux proposer une version qui modifie index.md en s'appuyant sur des règles (pré-requis : conventions strictes dans index.md).
- Tous les textes analytiques (RésuméDe400mots, Ton, Pense-betes, Keywords) doivent être rédigés en français.