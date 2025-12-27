#!/bin/bash

echo "🚀 Lancement de la plateforme d'optimisation"
echo "==========================================="

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Vérifier les dépendances
echo "🔍 Vérification des dépendances..."
python3 -c "
import sys
import pkg_resources

required = {
    'streamlit', 'pandas', 'numpy', 'psycopg2-binary',
    'sqlalchemy', 'python-dotenv', 'plotly', 'flask'
}

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print(f'❌ Dépendances manquantes: {missing}')
    sys.exit(1)
else:
    print('✅ Toutes les dépendances sont installées')
"

# Lancer l'API en arrière-plan
echo "🌐 Démarrage de l'API Flask..."
cd backend
python api.py &
API_PID=$!
cd ..

# Attendre que l'API démarre
sleep 3

# Lancer Streamlit
echo "📊 Démarrage du dashboard Streamlit..."
streamlit run dashboard/app.py

# Nettoyer à la sortie
echo "🛑 Arrêt des processus..."
kill $API_PID 2>/dev/null
