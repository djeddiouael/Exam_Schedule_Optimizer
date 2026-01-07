#!/bin/bash

echo "Configuration de la base de données"
echo "====================================="

# Activer l'environnement virtuel si nous y sommes
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Vérifier si PostgreSQL est en cours d'exécution
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
fi

# Exécuter les scripts SQL
echo "Création des tables..."
python3 -c "
from backend.database import db
db.create_tables()
print('Tables créées avec succès')
"

echo "Insertion des données d'exemple..."
python3 -c "
from backend.database import db
db.insert_sample_data()
print('Données d\'exemple insérées avec succès')
"

echo "Base de données configurée avec succès!"
echo ""
echo "Données insérées:"
echo "   - 7 départements"
echo "   - 6 formations"
echo "   - 7 professeurs"
echo "   - 7 modules"
echo "   - 4 étudiants"
echo "   - 5 lieux d'examen"
echo "   - 3 examens de test"