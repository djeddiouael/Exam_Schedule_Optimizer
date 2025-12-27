# backend/models.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

@dataclass
class Departement:
    id: int
    nom: str
    created_at: datetime

@dataclass
class Formation:
    id: int
    nom: str
    dept_id: int
    nb_modules: int
    created_at: datetime

@dataclass
class Etudiant:
    id: int
    nom: str
    prenom: str
    formation_id: int
    promo: int
    email: str
    created_at: datetime

@dataclass
class Module:
    id: int
    nom: str
    credits: int
    formation_id: int
    pre_req_id: Optional[int]
    heures_total: int
    created_at: datetime

@dataclass
class LieuExamen:
    id: int
    nom: str
    capacite: int
    type: str
    batiment: str
    equipement: str
    created_at: datetime

@dataclass
class Professeur:
    id: int
    nom: str
    prenom: str
    dept_id: int
    specialite: str
    email: str
    heures_surveillance: int
    created_at: datetime

@dataclass
class Inscription:
    etudiant_id: int
    module_id: int
    note: float
    annee_scolaire: int
    semestre: int
    created_at: datetime

@dataclass
class Examen:
    id: int
    module_id: int
    prof_id: int
    salle_id: int
    date_heure: datetime
    duree_minutes: int
    type_examen: str
    created_at: datetime
    
    @property
    def date_fin(self):
        return self.date_heure + timedelta(minutes=self.duree_minutes)

@dataclass
class Conflit:
    type: str  # 'salle', 'professeur', 'etudiant', 'capacite'
    description: str
    examen1: Examen
    examen2: Optional[Examen] = None
