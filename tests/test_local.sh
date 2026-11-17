
#!/usr/bin/env bash

# Test local du projet Hadoop MapReduce avec Python

set -euo pipefail

# Se placer automatiquement à la racine du projet
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo " Hadoop MapReduce - Local Test"
echo "=========================================="

# Vérifier la présence des fichiers nécessaires
if [ ! -f "src/mapper.py" ]; then
    echo "ERROR: src/mapper.py not found."
    exit 1
fi

if [ ! -f "src/reducer.py" ]; then
    echo "ERROR: src/reducer.py not found."
    exit 1
fi

if [ ! -f "tests/purchases_sample.txt" ]; then
    echo "ERROR: Sample dataset not found."
    exit 1
fi

# Vérifier Python
if command -v python >/dev/null 2>&1; then
    PYTHON=python
elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    echo "ERROR: Python is not installed or not in PATH."
    exit 1
fi

echo ""
echo "Python version:"
"$PYTHON" --version

# Créer le dossier results s'il n'existe pas
mkdir -p results

echo ""
echo "Running Mapper and Reducer..."

# Exécuter le pipeline MapReduce local
"$PYTHON" src/mapper.py < tests/purchases_sample.txt \
    | sort \
    | "$PYTHON" src/reducer.py \
    | tee results/local_output.txt

echo ""
echo "=========================================="
echo " Local test completed successfully."
echo " Result saved in results/local_output.txt"
echo "=========================================="
