#!/bin/bash

clear
echo "========================================================"
echo "🚀 DÉMARRAGE COMPLET - PLATEFORME EXAMENS"
echo "========================================================"

# Arrêter tout
echo "🛑 Arrêt des services existants..."
pkill -f "python api" 2>/dev/null
pkill -f "streamlit" 2>/dev/null
sleep 2

# Vérifier PostgreSQL
echo "🗄️  Vérification de PostgreSQL..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL n'est pas démarré"
    echo "Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
    sleep 3
fi

# Aller au projet
cd ~/Project/Exam_Schedule_Optimizer || exit 1

# Activer l'environnement
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
else
    echo "❌ Environnement virtuel non trouvé"
    exit 1
fi

# Démarrer l'API simplifiée
echo ""
echo "🌐 DÉMARRAGE DE L'API..."
cd backend
python api_simple.py &
API_PID=$!
cd ..

echo "⏳ Attente du démarrage (3 secondes)..."
sleep 3

# Tester l'API
echo ""
echo "🧪 TEST DE L'API..."
if curl -s http://localhost:5000/ > /dev/null; then
    echo "✅ API démarrée sur http://localhost:5000"
    echo "📡 Endpoints disponibles:"
    curl -s http://localhost:5000/ | python3 -m json.tool | grep -A 10 "endpoints"
else
    echo "❌ L'API n'a pas démarré"
    echo "Essayer de la démarrer manuellement:"
    echo "  cd ~/Project/Exam_Schedule_Optimizer/backend"
    echo "  python api_simple.py"
    exit 1
fi

# Démarrer Streamlit
echo ""
echo "📊 DÉMARRAGE DU DASHBOARD..."
streamlit run dashboard/app_simple.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

echo "⏳ Attente du démarrage (3 secondes)..."
sleep 3

echo ""
echo "========================================================"
echo "🎯 PLATEFORME PRÊTE À L'UTILISATION !"
echo "========================================================"
echo ""
echo "🌐 API:        http://localhost:5000"
echo "📊 DASHBOARD:  http://localhost:8501"
echo ""
echo "📋 TESTS RAPIDES:"
echo "   curl http://localhost:5000/"
echo "   curl http://localhost:5000/health"
echo "   curl http://localhost:5000/departements"
echo ""
echo "👤 INTERFACE:"
echo "   Ouvrez http://localhost:8501 dans votre navigateur"
echo ""
echo "🛑 POUR ARRÊTER: Appuyez sur Ctrl+C dans CE terminal"
echo "========================================================"

# Attendre Ctrl+C
trap "echo ''; echo '🛑 Arrêt en cours...'; kill $API_PID 2>/dev/null; kill $STREAMLIT_PID 2>/dev/null; exit 0" SIGINT SIGTERM

while true; do
    sleep 1
done
