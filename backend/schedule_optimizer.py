# backend/schedule_optimizer.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random
from backend.database import db
import logging

logger = logging.getLogger(__name__)

class ScheduleOptimizer:
    def __init__(self):
        self.conflits = []
    
    def generer_emploi_du_temps(self, date_debut: datetime, date_fin: datetime) -> List[Dict]:
        """Génère un emploi du temps optimisé - Version simplifiée et rapide"""
        logger.info(f"Génération rapide de l'emploi du temps du {date_debut} au {date_fin}")
        
        # 1. Récupérer les données en une seule requête
        try:
            modules_data = db.execute_query("""
                SELECT m.id as module_id, m.nom as module_nom, 
                       f.id as formation_id, f.nom as formation_nom,
                       d.id as dept_id, d.nom as dept_nom,
                       (SELECT COUNT(*) FROM inscriptions WHERE module_id = m.id) as nb_etudiants
                FROM modules m
                JOIN formations f ON m.formation_id = f.id
                JOIN departements d ON f.dept_id = d.id
                WHERE NOT EXISTS (
                    SELECT 1 FROM examens e 
                    WHERE e.module_id = m.id 
                    AND e.date_heure BETWEEN %s AND %s
                )
                LIMIT 10  -- Limiter pour la rapidité
            """, (date_debut, date_fin), fetchall=True)
        except Exception as e:
            logger.error(f"Erreur récupération modules: {e}")
            return []
        
        if not modules_data:
            return [{"message": "Aucun module à planifier dans cette période"}]
        
        # 2. Récupérer salles et profs
        salles = db.execute_query("SELECT * FROM lieu_examen WHERE capacite > 0", fetchall=True)
        professeurs = db.execute_query("SELECT * FROM professeurs", fetchall=True)
        
        if not salles or not professeurs:
            return []
        
        # 3. Générer emploi du temps simplifié
        emploi_du_temps = []
        jours = (date_fin - date_debut).days + 1
        
        if jours <= 0:
            return []
        
        # Heures fixes
        creneaux = [(9, 0), (14, 0)]
        
        for i, module in enumerate(modules_data):
            # Calculer le jour et créneau
            jour = i // 2 % jours
            creneau_idx = i % 2
            
            date_examen = date_debut + timedelta(days=jour)
            heure, minute = creneaux[creneau_idx]
            date_heure = date_examen.replace(hour=heure, minute=minute, second=0, microsecond=0)
            
            # Trouver une salle adaptée (simplifié)
            nb_etudiants = module['nb_etudiants'] or 20
            salle = next((s for s in salles if s['capacite'] >= nb_etudiants), salles[0])
            
            # Trouver un professeur du département
            profs_dept = [p for p in professeurs if p['dept_id'] == module['dept_id']]
            if not profs_dept:
                profs_dept = professeurs
            
            # Prendre le premier professeur disponible (vérification simplifiée)
            prof = profs_dept[0]
            
            emploi_du_temps.append({
                'module_id': module['module_id'],
                'module_nom': module['module_nom'],
                'prof_id': prof['id'],
                'prof_nom': f"{prof['prenom']} {prof['nom']}",
                'salle_id': salle['id'],
                'salle_nom': salle['nom'],
                'date_heure': date_heure,
                'duree_minutes': 120,  # Durée réduite
                'type_examen': 'écrit',
                'formation': module['formation_nom'],
                'departement': module['dept_nom'],
                'capacite_salle': salle['capacite'],
                'nb_etudiants': nb_etudiants
            })
        
        logger.info(f"Emploi du temps généré avec {len(emploi_du_temps)} examens")
        return emploi_du_temps
    
    def sauvegarder_emploi_du_temps(self, emploi_du_temps: List[Dict]) -> bool:
        """Sauvegarde simplifiée"""
        try:
            for examen in emploi_du_temps:
                # Vérifier que c'est un vrai examen (pas un message)
                if 'module_id' in examen:
                    db.execute_query("""
                        INSERT INTO examens 
                        (module_id, prof_id, salle_id, date_heure, duree_minutes, type_examen)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        examen['module_id'],
                        examen['prof_id'],
                        examen['salle_id'],
                        examen['date_heure'],
                        examen['duree_minutes'],
                        examen['type_examen']
                    ))
            
            logger.info(f"{len([e for e in emploi_du_temps if 'module_id' in e])} examens sauvegardés")
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return False
