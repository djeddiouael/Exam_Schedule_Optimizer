from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'exam_schedule_db',
    'user': 'exam_user',
    'password': 'exam_password'
}

def get_db_connection():
    """Établit une connexion à la base de données"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Erreur connexion DB: {e}")
        return None

@app.route('/')
def index():
    return jsonify({
        'message': 'API de planification des examens - Version simplifiée',
        'version': '1.0.0',
        'status': 'OK',
        'endpoints': ['/', '/health', '/departements', '/test']
    })

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({'status': 'healthy', 'database': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/departements')
def departements():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, nom FROM departements ORDER BY nom")
            result = cursor.fetchall()
        
        conn.close()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur /departements: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    """Endpoint de test simple"""
    return jsonify({
        'test': 'OK',
        'message': 'L\'API fonctionne correctement',
        'timestamp': '2024-01-01T00:00:00'
    })

if __name__ == '__main__':
    logger.info("Démarrage de l'API simplifiée sur le port 5000")
    print("=" * 50)
    print(" API SIMPLIFIÉE DÉMARRÉE")
    print(" URL: http://localhost:5000")
    print(" Endpoints:")
    print("   - GET /          : Documentation")
    print("   - GET /health    : Santé de l'API")
    print("   - GET /departements : Liste départements")
    print("   - GET /test      : Test simple")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
