#!/bin/bash

echo "📦 Initialisation du projet d'optimisation des examens"
echo "====================================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "✅ Python3 est installé"

# Créer l'environnement virtuel
echo "🔧 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Vérifier PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️ PostgreSQL n'est pas installé"
    read -p "Voulez-vous installer PostgreSQL? (o/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        sudo apt update
        sudo apt install -y postgresql postgresql-contrib
    fi
fi

echo "✅ Environnement configuré avec succès!"
echo ""
echo "📋 Étapes suivantes:"
echo "1. Activer l'environnement: source venv/bin/activate"
echo "2. Configurer la base de données: ./scripts/setup_database.sh"
echo "3. Lancer l'API: python backend/api.py"
echo "4. Lancer le dashboard: streamlit run dashboard/app.py"
