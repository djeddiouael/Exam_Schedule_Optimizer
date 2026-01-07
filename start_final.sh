#!/bin/bash

echo "========================================================"
echo "PLATEFORME D'OPTIMISATION DES EXAMENS - VERSION FINALE"
echo "========================================================"

# Arrêter les services existants
echo "Arrêt des services existants..."
pkill -f "python api" 2>/dev/null
pkill -f "streamlit" 2>/dev/null
sleep 2

# Vérifier PostgreSQL
echo "Vérification PostgreSQL..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
    sleep 3
fi

# Aller au projet
cd ~/Project/Exam_Schedule_Optimizer

# Activer environnement
source venv/bin/activate

# Démarrer API simplifiée
echo "Démarrage API Flask..."
cd backend
python api_simple.py &
API_PID=$!
cd ..

sleep 3

# Vérifier API
if curl -s http://localhost:5000/health > /dev/null; then
    echo "API démarrée: http://localhost:5000"
else
    echo "API non démarrée. Démarrage manuel requis."
    echo "Commande: cd backend && python api_simple.py"
    exit 1
fi

# Démarrer Streamlit avec toutes les pages
echo "Démarrage Dashboard Streamlit..."
echo "Pages disponibles:"
echo "   1. Vue Stratégique (Vice-doyen)"
echo "   2. Administrateur Examens"
echo "   3. Chef de Département"
echo "   4. Étudiants/Professeurs"

streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

sleep 3

echo ""
echo "========================================================"
echo "PLATEFORME PRÊTE À L'UTILISATION !"
echo "========================================================"
echo ""
echo "API REST:          http://localhost:5000"
echo "DASHBOARD PRINCIPAL: http://localhost:8501"
echo ""
echo "PAGES SPÉCIFIQUES:"
echo "   - Vice-doyen:        http://localhost:8501/Vue_Stratégique"
echo "   - Administrateur:    http://localhost:8501/Administrateur_Examens"
echo "   - Chef département:  http://localhost:8501/Chef_Département"
echo "   - Étudiants/Profs:   http://localhost:8501/Étudiants_Professeurs"
echo ""
echo "TESTS API:"
echo "   curl http://localhost:5000/"
echo "   curl http://localhost:5000/health"
echo "   curl http://localhost:5000/departements"
echo ""
echo "POUR ARRÊTER: Ctrl+C dans ce terminal"
echo "========================================================"

# Nettoyage
trap "echo ''; echo 'Arrêt...'; kill $API_PID 2>/dev/null; kill $STREAMLIT_PID 2>/dev/null; exit 0" SIGINT SIGTERM

while true; do
    sleep 1
done