#!/usr/bin/env python3
"""
Usage:
  scripts/new_fiche.py --id IDENTIFIANT --title "Titre original" --date YYYY-MM-DD --url URL [--authors "Auteurs"] [--keywords "k1,k2"] [--source "Source"]

Le script :
- crée le répertoire fiches/YYYY-MM/ si nécessaire
- crée fiches/YYYY-MM/{identifiant}.md à partir du template templates/fiche-template.md
- modifie index.md automatiquement si demandé (optionnel)
- crée un fichier raw-data/{identifiant}.md placeholder (optionnel)
"""
import argparse
import os
from datetime import datetime

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

def load_template():
    tpl_path = os.path.join(ROOT, "templates", "fiche-template.md")
    if not os.path.exists(tpl_path):
        raise FileNotFoundError(f"Template absent: {tpl_path}")
    with open(tpl_path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def create_fiche(identifier, title, date, url, authors, keywords, source, create_raw=True, update_index=False):
    # date -> YYYY-MM-DD ; dir -> YYYY-MM
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise SystemExit("Date mal formatée. Utiliser YYYY-MM-DD.")
    month_dir = dt.strftime("%Y-%m")
    fiches_dir = os.path.join(ROOT, "fiches", month_dir)
    ensure_dir(fiches_dir)
    fiche_path = os.path.join(fiches_dir, f"{identifier}.md")
    if os.path.exists(fiche_path):
        raise SystemExit(f"Fiche existe déjà : {fiche_path}")

    template = load_template()
    content = template.replace("{IDENTIFIANT_TECHNIQUE}", identifier)
    content = content.replace("Titre original de l'article (langue source)", title)
    content = content.replace("YYYY-MM-DD", date, 1)
    content = content.replace("https://exemple.com/...", url)
    content = content.replace("Nom Auteur(s)", authors or "")
    content = content.replace("mot-clé-1, mot-clé-2, mot-clé-3  (en français)", keywords or "")
    with open(fiche_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fiche créée : {fiche_path}")

    # raw-data placeholder
    if create_raw:
        raw_dir = os.path.join(ROOT, "raw-data")
        ensure_dir(raw_dir)
        raw_path = os.path.join(raw_dir, f"{identifier}.md")
        if not os.path.exists(raw_path):
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(f"# {identifier}\n\n**URL:** {url}\n\n---\n\n[Contenu brut à coller ici]\n")
            print(f"Fichier raw-data placeholder créé : {raw_path}")
        else:
            print(f"raw-data existe déjà : {raw_path}")

    # Ligne d'index à coller (format conseillé)
    short_desc = "(description courte) - Source" if not source else f"(description courte) - {source}"
    index_line = f"- **[{date}]** [{title}](fiches/{month_dir}/{identifier}.md) - {short_desc}"

    if update_index:
        index_path = os.path.join(ROOT, "index.md")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                idx = f.read()
        else:
            idx = "# Veille Technologique\n\n"
        # Insert into the right month section or create it
        month_header = dt.strftime("%B %Y")  # English month name; index.md uses French names, so fallback to appending to top
        insert_point = idx.find("## Articles par date de publication")
        if insert_point != -1:
            # naive append under the month section: place after the header of the month if exists
            # fallback: append near top
            new_idx = idx + "\n" + index_line + "\n"
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_idx)
            print(f"index.md mis à jour avec : {index_line}")
        else:
            with open(index_path, "a", encoding="utf-8") as f:
                f.write("\n## Articles par date de publication\n\n" + index_line + "\n")
            print(f"index.md créé/complété avec : {index_line}")
    else:
        print("\n---\nCopiez la ligne ci-dessous dans index.md dans la section du mois correspondant (ordre décroissant) :\n")
        print(index_line)
        print("\n---\nN'oubliez pas d'ajouter la fiche à la thématique appropriée dans la section 'Thématiques' et d'incrémenter les statistiques.\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="identifiant technique, ex: nom-auteur-sujet-YYYY-MM-DD")
    p.add_argument("--title", required=True, help="Titre original")
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--url", required=True, help="URL de l'article")
    p.add_argument("--authors", default="", help="Auteur(s)")
    p.add_argument("--keywords", default="", help="Mots-clés (séparés par des virgules)")
    p.add_argument("--source", default="", help="Source courte (ex: LinkedIn, TechCrunch)")
    p.add_argument("--no-raw", action="store_true", help="Ne pas créer raw-data placeholder")
    p.add_argument("--update-index", action="store_true", help="Mettre à jour index.md automatiquement")
    args = p.parse_args()

    create_fiche(args.id, args.title, args.date, args.url, args.authors, args.keywords, args.source, create_raw=not args.no_raw, update_index=args.update_index)

if __name__ == "__main__":
    main()