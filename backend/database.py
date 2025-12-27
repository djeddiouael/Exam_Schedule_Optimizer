# backend/database.py
import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance
    
    def _init_db(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                cursor_factory=DictCursor
            )
            logger.info("Connexion à la base de données établie")
        except Exception as e:
            logger.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Connexion à la base de données fermée")
    
    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetchone:
                    return cursor.fetchone()
                elif fetchall:
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise
    
    def create_tables(self):
        """Crée toutes les tables de la base de données"""
        try:
            with open('sql/create_tables.sql', 'r') as f:
                sql_script = f.read()
            
            self.execute_query(sql_script)
            logger.info("Tables créées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la création des tables: {e}")
            raise
    
    def insert_sample_data(self):
        """Insère les données d'exemple"""
        try:
            with open('sql/insert_sample_data.sql', 'r') as f:
                sql_script = f.read()
            
            self.execute_query(sql_script)
            logger.info("Données d'exemple insérées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion des données: {e}")
            raise

# Singleton pour accéder à la base de données
db = Database()
