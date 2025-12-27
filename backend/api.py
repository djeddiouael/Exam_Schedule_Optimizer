# backend/api.py
import sys
import os
import logging

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import time

# Import local
try:
    from backend.database import db
    from backend.schedule_optimizer import ScheduleOptimizer
except ImportError:
    # Pour le cas où on exécute directement depuis le répertoire backend
    import sys
    sys.path.append('..')
    from backend.database import db
    from backend.schedule_optimizer import ScheduleOptimizer

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

optimizer = ScheduleOptimizer()

@app.route('/')
def index():
    return jsonify({
        'message': 'API de planification des examens',
        'version': '1.0.0',
        'status': 'OK',
        'endpoints': {
            '/departements': 'Liste des départements',
            '/formations': 'Liste des formations',
            '/examens': 'Liste des examens',
            '/generer': 'Générer un emploi du temps',
            '/conflits': 'Liste des conflits',
            '/statistiques': 'Statistiques'
        }
    })

@app.route('/departements', methods=['GET'])
def get_departements():
    """Récupère la liste des départements - Version rapide"""
    try:
        departements = db.execute_query("SELECT id, nom FROM departements ORDER BY nom", fetchall=True)
        return jsonify(departements)
    except Exception as e:
        logger.error(f"Erreur départements: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/formations', methods=['GET'])
def get_formations():
    """Récupère la liste des formations - Version rapide"""
    try:
        formations = db.execute_query("""
            SELECT f.id, f.nom, d.nom as departement_nom
            FROM formations f
            JOIN departements d ON f.dept_id = d.id
            ORDER BY f.nom
            LIMIT 50
        """, fetchall=True)
        return jsonify(formations)
    except Exception as e:
        logger.error(f"Erreur formations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/examens', methods=['GET'])
def get_examens():
    """Récupère la liste des examens - Version rapide"""
    try:
        start_time = time.time()
        
        # Version simplifiée et limitée
        examens = db.execute_query("""
            SELECT e.id, e.date_heure, e.duree_minutes, e.type_examen,
                   m.nom as module_nom,
                   p.nom as prof_nom, p.prenom as prof_prenom,
                   l.nom as salle_nom,
                   f.nom as formation_nom,
                   d.nom as departement_nom
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            LEFT JOIN professeurs p ON e.prof_id = p.id
            LEFT JOIN lieu_examen l ON e.salle_id = l.id
            JOIN formations f ON m.formation_id = f.id
            JOIN departements d ON f.dept_id = d.id
            ORDER BY e.date_heure DESC
            LIMIT 100
        """, fetchall=True)
        
        elapsed = time.time() - start_time
        logger.info(f"Récupération examens: {len(examens)} examens en {elapsed:.2f}s")
        
        return jsonify(examens)
    except Exception as e:
        logger.error(f"Erreur examens: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generer', methods=['POST'])
def generer_emploi_du_temps():
    """Génère un nouvel emploi du temps - Version optimisée"""
    try:
        start_time = time.time()
        
        data = request.json
        date_debut_str = data.get('date_debut', '2024-01-15')
        date_fin_str = data.get('date_fin', '2024-01-25')
        
        logger.info(f"Début génération EDT: {date_debut_str} -> {date_fin_str}")
        
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d')
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d')
        
        # Limiter la période pour éviter les générations trop longues
        max_jours = 30
        if (date_fin - date_debut).days > max_jours:
            date_fin = date_debut + timedelta(days=max_jours)
            logger.info(f"Période limitée à {max_jours} jours")
        
        # Générer l'emploi du temps
        emploi_du_temps = optimizer.generer_emploi_du_temps(date_debut, date_fin)
        
        # Sauvegarder si ce sont de vrais examens
        if emploi_du_temps and 'message' not in emploi_du_temps[0]:
            success = optimizer.sauvegarder_emploi_du_temps(emploi_du_temps)
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Erreur lors de la sauvegarde'
                }), 500
        
        elapsed = time.time() - start_time
        logger.info(f"Génération terminée en {elapsed:.2f} secondes")
        
        return jsonify({
            'success': True,
            'message': f'Emploi du temps généré avec {len(emploi_du_temps)} examens',
            'temps_execution': f'{elapsed:.2f}s',
            'emploi_du_temps': emploi_du_temps[:10]  # Retourner seulement les 10 premiers pour éviter des réponses trop grandes
        })
        
    except Exception as e:
        logger.error(f"Erreur génération: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de la génération'
        }), 500

@app.route('/statistiques', methods=['GET'])
def get_statistiques():
    """Récupère les statistiques - Version rapide"""
    try:
        # Statistiques simplifiées
        stats = db.execute_query("""
            SELECT 
                COUNT(*) as total_examens,
                COUNT(DISTINCT salle_id) as salles_utilisees,
                COUNT(DISTINCT prof_id) as profs_impliques,
                COUNT(DISTINCT d.id) as departements_concernes
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            JOIN formations f ON m.formation_id = f.id
            JOIN departements d ON f.dept_id = d.id
        """, fetchone=True)
        
        # Occupation des salles (simplifiée)
        occupation = db.execute_query("""
            SELECT 
                l.nom,
                COUNT(e.id) as nb_examens
            FROM lieu_examen l
            LEFT JOIN examens e ON l.id = e.salle_id
            GROUP BY l.id, l.nom
            ORDER BY nb_examens DESC
            LIMIT 10
        """, fetchall=True)
        
        return jsonify({
            'statistiques_generales': stats,
            'occupation_salles': occupation
        })
    except Exception as e:
        logger.error(f"Erreur statistiques: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de santé"""
    try:
        # Vérifier la connexion à la base
        db.execute_query("SELECT 1")
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Démarrage de l'API d'optimisation des examens")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
