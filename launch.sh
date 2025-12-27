#!/bin/bash

echo "========================================================"
echo "🚀 PLATEFORME D'OPTIMISATION DES EXAMENS - DÉMARRAGE"
echo "========================================================"

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "📦 Vérification des dépendances..."
pip install -r requirements.txt flask flask-cors > /dev/null 2>&1

echo "🗄️  Vérification de la base de données..."
python3 -c "
from backend.database import db
try:
    # Vérifier si les tables existent
    result = db.execute_query('SELECT COUNT(*) as count FROM departements', fetchone=True)
    print(f'✅ Base de données OK ({result[\"count\"]} départements)')
except Exception as e:
    print('⚠️  Recréation des tables...')
    db.create_tables()
    db.insert_sample_data()
    print('✅ Base de données initialisée')
"

echo "🌐 Démarrage de l'API Flask..."
cd ~/Project/Exam_Schedule_Optimizer/backend
python api.py &
API_PID=$!
cd ~/Project/Exam_Schedule_Optimizer

echo "⏳ Attente du démarrage de l'API..."
sleep 5

# Vérifier que l'API fonctionne
if curl -s http://localhost:5000/ > /dev/null; then
    echo "✅ API démarrée sur http://localhost:5000"
else
    echo "❌ Échec du démarrage de l'API"
    echo "Démarrage en mode debug..."
    cd backend
    python api.py &
    API_PID=$!
    cd ..
    sleep 3
fi

echo "📊 Démarrage du dashboard Streamlit..."
streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

echo "⏳ Attente du démarrage du dashboard..."
sleep 3

echo ""
echo "========================================================"
echo "🎯 PLATEFORME PRÊTE À L'UTILISATION !"
echo "========================================================"
echo ""
echo "🌐 API REST:     http://localhost:5000"
echo "📊 DASHBOARD:    http://localhost:8501"
echo ""
echo "📋 TESTS RAPIDES:"
echo "   curl http://localhost:5000/departements"
echo "   curl http://localhost:5000/examens"
echo "   curl http://localhost:5000/statistiques"
echo ""
echo "👤 INTERFACE:"
echo "   Ouvrez http://localhost:8501 dans votre navigateur"
echo ""
echo "🛑 POUR ARRÊTER: Appuyez sur Ctrl+C"
echo "========================================================"

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt des processus..."
    kill $API_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    pkill -f "streamlit"
    pkill -f "python api.py"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

# Attendre indéfiniment
while true; do
    sleep 1
done
