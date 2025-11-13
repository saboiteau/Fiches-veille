#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Initialisation de la structure de veille dans : $ROOT_DIR"

# Dossiers à créer
dirs=(
  "$ROOT_DIR/fiches"
  "$ROOT_DIR/templates"
  "$ROOT_DIR/raw-data"
  "$ROOT_DIR/scripts"
  "$ROOT_DIR/docs"
)

for d in "${dirs[@]}"; do
  if [ ! -d "$d" ]; then
    mkdir -p "$d"
    echo "Créé : $d"
  else
    echo "Existe déjà : $d"
  fi
done

# Ajouter raw-data/ à .gitignore si absent
GITIGNORE="$ROOT_DIR/.gitignore"
if [ ! -f "$GITIGNORE" ]; then
  touch "$GITIGNORE"
fi

if ! grep -qx "raw-data/" "$GITIGNORE"; then
  echo -e "\n# Raw data non versionnée\nraw-data/" >> "$GITIGNORE"
  echo "Ajouté raw-data/ à .gitignore"
else
  echo "raw-data/ déjà présent dans .gitignore"
fi

echo "Initialisation terminée."