-- sql/insert_sample_data.sql

-- Insertion des départements
INSERT INTO departements (nom) VALUES 
('Informatique'),
('Mathématiques'),
('Physique'),
('Chimie'),
('Biologie'),
('Économie'),
('Droit')
ON CONFLICT (nom) DO NOTHING;

-- Insertion des formations
INSERT INTO formations (nom, dept_id, nb_modules) VALUES
('Licence Informatique', 1, 8),
('Master Data Science', 1, 6),
('Licence Mathématiques', 2, 7),
('Master Physique Quantique', 3, 6),
('Licence Biologie', 5, 7),
('Master Économétrie', 6, 5),
('Licence Droit', 7, 6)  -- Ajout de la formation Droit pour avoir l'ID 7
ON CONFLICT DO NOTHING;

-- Insertion des lieux d'examen
INSERT INTO lieu_examen (nom, capacite, type, batiment, equipement) VALUES
('Amphi A', 300, 'amphi', 'Bâtiment Principal', 'vidéoprojecteur, sonorisation'),
('Amphi B', 250, 'amphi', 'Bâtiment Principal', 'vidéoprojecteur'),
('Salle 101', 20, 'salle', 'Bâtiment Sciences', 'tableaux'),
('Salle 102', 20, 'salle', 'Bâtiment Sciences', 'ordinateurs'),
('Labo Info 1', 25, 'labo', 'Bâtiment Informatique', '25 PC, réseau'),
('Salle 201', 30, 'salle', 'Bâtiment Droit', 'tableaux'),
('Amphi C', 400, 'amphi', 'Bâtiment Nouveau', 'vidéoprojecteur, climatisation')
ON CONFLICT DO NOTHING;

-- Insertion des professeurs
INSERT INTO professeurs (nom, prenom, dept_id, specialite, email) VALUES
('Martin', 'Pierre', 1, 'Base de données', 'pierre.martin@univ.fr'),
('Dubois', 'Marie', 1, 'Algorithmique', 'marie.dubois@univ.fr'),
('Leroy', 'Jean', 2, 'Analyse', 'jean.leroy@univ.fr'),
('Petit', 'Sophie', 3, 'Physique quantique', 'sophie.petit@univ.fr'),
('Garcia', 'Luc', 4, 'Chimie organique', 'luc.garcia@univ.fr'),
('Roux', 'Julie', 5, 'Biologie cellulaire', 'julie.roux@univ.fr'),
('Moreau', 'Thomas', 6, 'Économétrie', 'thomas.moreau@univ.fr')
ON CONFLICT (email) DO NOTHING;

-- Insertion des modules (corrigé - formation_id 7 existe maintenant)
INSERT INTO modules (nom, credits, formation_id, heures_total) VALUES
('Base de données', 6, 1, 45),
('Algorithmique', 6, 1, 45),
('Programmation Python', 4, 1, 30),
('Analyse Mathématique', 8, 3, 60),
('Physique Quantique I', 6, 4, 45),
('Économétrie Avancée', 5, 6, 40),
('Droit des Affaires', 5, 7, 40)  -- Formation 7 existe maintenant
ON CONFLICT DO NOTHING;

-- Insertion d'étudiants (exemple)
INSERT INTO etudiants (nom, prenom, formation_id, promo, email) VALUES
('Durand', 'Alice', 1, 2023, 'alice.durand@etu.univ.fr'),
('Lefevre', 'Paul', 1, 2023, 'paul.lefevre@etu.univ.fr'),
('Bernard', 'Emma', 3, 2023, 'emma.bernard@etu.univ.fr'),
('Thomas', 'Lucas', 4, 2023, 'lucas.thomas@etu.univ.fr')
ON CONFLICT (email) DO NOTHING;

-- Insertion d'inscriptions
INSERT INTO inscriptions (etudiant_id, module_id, note, annee_scolaire, semestre) VALUES
(1, 1, 15.5, 2023, 1),
(1, 2, 14.0, 2023, 1),
(2, 1, 16.0, 2023, 1),
(3, 4, 13.5, 2023, 1)
ON CONFLICT DO NOTHING;

-- Insertion d'examens de test
INSERT INTO examens (module_id, prof_id, salle_id, date_heure, duree_minutes, type_examen) VALUES
(1, 1, 1, '2024-01-15 09:00:00', 180, 'écrit'),
(2, 2, 2, '2024-01-15 14:00:00', 180, 'écrit'),
(4, 3, 3, '2024-01-16 09:00:00', 120, 'oral')
ON CONFLICT DO NOTHING;
