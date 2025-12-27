# config/__init__.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration de la base de données
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'exam_schedule_db')
    DB_USER = os.getenv('DB_USER', 'exam_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'exam_password')
    
    # Constantes du système
    MAX_EXAMS_PER_DAY_STUDENT = int(os.getenv('MAX_EXAMS_PER_DAY_STUDENT', 1))
    MAX_EXAMS_PER_DAY_PROF = int(os.getenv('MAX_EXAMS_PER_DAY_PROF', 3))
    MIN_PROFESSORS_PER_DEPARTMENT = int(os.getenv('MIN_PROFESSORS_PER_DEPARTMENT', 2))
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()
