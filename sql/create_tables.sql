-- sql/create_tables.sql

-- Table départements
CREATE TABLE IF NOT EXISTS departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table formations
CREATE TABLE IF NOT EXISTS formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    dept_id INTEGER REFERENCES departements(id) ON DELETE CASCADE,
    nb_modules INTEGER DEFAULT 0 CHECK (nb_modules >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table étudiants
CREATE TABLE IF NOT EXISTS etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    formation_id INTEGER REFERENCES formations(id) ON DELETE SET NULL,
    promo INTEGER CHECK (promo >= 2000 AND promo <= 2030),
    email VARCHAR(150) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table modules
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    credits INTEGER DEFAULT 3 CHECK (credits BETWEEN 1 AND 10),
    formation_id INTEGER REFERENCES formations(id) ON DELETE CASCADE,
    pre_req_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    heures_total INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table lieu_examen
CREATE TABLE IF NOT EXISTS lieu_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    capacite INTEGER CHECK (capacite > 0),
    type VARCHAR(50) CHECK (type IN ('amphi', 'salle', 'labo')),
    batiment VARCHAR(50),
    equipement TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table professeurs
CREATE TABLE IF NOT EXISTS professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dept_id INTEGER REFERENCES departements(id) ON DELETE SET NULL,
    specialite VARCHAR(200),
    email VARCHAR(150) UNIQUE,
    heures_surveillance INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table inscriptions
CREATE TABLE IF NOT EXISTS inscriptions (
    etudiant_id INTEGER REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    note DECIMAL(4,2) CHECK (note BETWEEN 0 AND 20),
    annee_scolaire INTEGER,
    semestre INTEGER CHECK (semestre IN (1, 2)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (etudiant_id, module_id, annee_scolaire, semestre)
);

-- Table examens
CREATE TABLE IF NOT EXISTS examens (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    prof_id INTEGER REFERENCES professeurs(id) ON DELETE SET NULL,
    salle_id INTEGER REFERENCES lieu_examen(id) ON DELETE SET NULL,
    date_heure TIMESTAMP NOT NULL,
    duree_minutes INTEGER CHECK (duree_minutes > 0 AND duree_minutes <= 240),
    type_examen VARCHAR(50) DEFAULT 'écrit' CHECK (type_examen IN ('écrit', 'oral', 'pratique')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(salle_id, date_heure)
);

-- Index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_examens_date ON examens(date_heure);
CREATE INDEX IF NOT EXISTS idx_examens_module ON examens(module_id);
CREATE INDEX IF NOT EXISTS idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX IF NOT EXISTS idx_inscriptions_module ON inscriptions(module_id);

-- Table pour les surveillances
CREATE TABLE IF NOT EXISTS surveillances (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER REFERENCES examens(id) ON DELETE CASCADE,
    prof_id INTEGER REFERENCES professeurs(id) ON DELETE CASCADE,
    date_heure TIMESTAMP NOT NULL,
    duree_minutes INTEGER DEFAULT 120,
    role VARCHAR(50) DEFAULT 'surveillant' CHECK (role IN ('surveillant', 'responsable')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(prof_id, date_heure)
);
