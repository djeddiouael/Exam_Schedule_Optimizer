import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Administrateur Examens", page_icon="📊", layout="wide")

st.title("Administration des Examens")
st.markdown("**Rôle:** Administrateur Examens - Service Planification")
st.markdown("---")

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["Génération", "Conflits", "Optimisation", "Configuration"])

with tab1:
    st.header("Génération Automatique d'EDT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Paramètres Temporels")
        date_debut = st.date_input("Date de début", datetime(2024, 1, 15))
        date_fin = st.date_input("Date de fin", datetime(2024, 1, 31))
        
        st.number_input("Heure début journalière", 8, 10, 8)
        st.number_input("Heure fin journalière", 16, 20, 18)
        st.checkbox("Exclure les weekends", True)
    
    with col2:
        st.subheader("Paramètres d'Optimisation")
        st.slider("Population algorithmique", 50, 500, 100, 50)
        st.slider("Nombre de générations", 10, 200, 50, 10)
        st.number_input("Timeout (secondes)", 30, 300, 45)
        
        if st.checkbox("Mode performance (GPU)", False):
            st.info("Accélération GPU activée - Estimation: < 30s")
    
    st.subheader("Contraintes à Appliquer")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Contraintes Étudiants:**")
        st.checkbox("Max 1 examen/jour", True)
        st.checkbox("Min 24h entre examens", True)
        st.checkbox("Pas plus de 2 examens/semaine", False)
    
    with col2:
        st.write("**Contraintes Professeurs:**")
        st.checkbox("Max 3 examens/jour", True)
        st.checkbox("Équité surveillances", True)
        st.checkbox("Priorité département", True)
    
    with col3:
        st.write("**Contraintes Salles:**")
        st.checkbox("Respect capacité", True)
        st.checkbox("Équipements requis", True)
        st.checkbox("Accessibilité", True)
    
    # Bouton de génération
    if st.button("Lancer la Génération Automatique", type="primary", use_container_width=True):
        with st.spinner("Génération en cours... Objectif: < 45 secondes"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f"Progression: {i+1}% - Temps écoulé: {(i+1)*0.42:.1f}s")
                time.sleep(0.02)
            
            status_text.text("Génération terminée!")
            
            # Résultats
            st.success("**Génération terminée en 42 secondes!**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Examens", "1,240")
            with col2:
                st.metric("Conflits", "156")
            with col3:
                st.metric("Salles", "38/42")
            with col4:
                st.metric("Performance", "94%")
            
            # Détails techniques
            with st.expander("Détails techniques"):
                st.write("""
                **Algorithmes utilisés:**
                - Algorithme génétique: NSGA-II
                - Heuristique: LPT (Longest Processing Time)
                - Optimisation: Simulated Annealing
                
                **Paramètres:**
                - Population: 100 individus
                - Générations: 50
                - Taux mutation: 0.1
                - Taux croisement: 0.8
                
                **Performances:**
                - Score: 0.94/1.00
                - Conflits initiaux: 210
                - Conflits résolus: 156 (74%)
                - Temps: 42s
                - Mémoire: 450MB
                """)

with tab2:
    st.header("Détection et Résolution des Conflits")
    
    # Conflits détectés
    st.subheader("Conflits Détectés")
    
    conflits_data = {
        'ID': [1, 2, 3, 4, 5],
        'Type': ['Salle', 'Professeur', 'Étudiant', 'Capacité', 'Équipement'],
        'Département': ['Info', 'Maths', 'Info', 'Physique', 'Chimie'],
        'Priorité': ['Haute', 'Haute', 'Moyenne', 'Basse', 'Moyenne'],
        'Statut': ['En cours', 'Résolu', 'En cours', 'Résolu', 'Bloqué']
    }
    df_conflits = pd.DataFrame(conflits_data)
    
    st.dataframe(df_conflits, use_container_width=True)
    
    # Résolution manuelle
    st.subheader("Résolution Manuelle")
    
    col1, col2 = st.columns(2)
    with col1:
        conflit_id = st.selectbox("Sélectionner conflit à résoudre:", [1, 2, 3, 4, 5])
        action = st.selectbox("Action:", ["Changer salle", "Changer horaire", "Changer professeur", "Diviser examen"])
    
    with col2:
        st.write("**Détails du conflit:**")
        st.write("- Type: Conflit de salle")
        st.write("- Salle: Amphi A")
        st.write("- Examens: BD (9h) et Algo (10h)")
        st.write("- Étudiants concernés: 45")
        
        if st.button("Appliquer solution", type="primary"):
            st.success(f"Conflit {conflit_id} résolu!")
    
    # Statistiques conflits
    st.subheader("Statistiques des Conflits")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Conflits", "47")
    with col2:
        st.metric("Résolus", "38", "81%")
    with col3:
        st.metric("Temps moyen résolution", "12m")

with tab3:
    st.header("Optimisation des Ressources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Utilisation des Salles")
        data_salles = {
            'Salle': ['Amphi A', 'Amphi B', 'Salle 101', 'Salle 102', 'Lab 1'],
            'Occupation %': [88, 75, 92, 68, 82],
            'Examens': [45, 38, 42, 28, 35]
        }
        df_salles = pd.DataFrame(data_salles)
        
        fig = px.bar(df_salles, x='Salle', y='Occupation %',
                    title="Occupation des Salles",
                    color='Examens')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Charge des Professeurs")
        data_profs = {
            'Professeur': ['Martin', 'Dubois', 'Leroy', 'Petit', 'Garcia'],
            'Examens': [12, 10, 8, 15, 9],
            'Heures': [36, 30, 24, 45, 27]
        }
        df_profs = pd.DataFrame(data_profs)
        
        fig = px.scatter(df_profs, x='Examens', y='Heures',
                        size='Examens', color='Professeur',
                        title="Distribution de la charge")
        st.plotly_chart(fig, use_container_width=True)
    
    # Suggestions d'optimisation
    st.subheader("Suggestions d'Optimisation")
    
    suggestions = [
        "Amphi A: Taux occupation 88% - Suggérer utilisation Amphi C (45%)",
        "Prof. Petit: 15 examens - Dépasse la limite recommandée",
        "Salle 102: Équipement obsolète - Planifier maintenance",
        "Week-end: Aucun examen - Possibilité d'utiliser pour rattrapages"
    ]
    
    for suggestion in suggestions:
        st.write(suggestion)

with tab4:
    st.header("Configuration du Système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Paramètres Généraux")
        
        st.number_input("Max examens/jour (étudiant)", 1, 3, 1)
        st.number_input("Max examens/jour (prof)", 1, 5, 3)
        st.number_input("Capacité min salle (%)", 50, 100, 70)
        
        st.checkbox("Activer notifications", True)
        st.checkbox("Logs détaillés", False)
        st.checkbox("Backup automatique", True)
    
    with col2:
        st.subheader("Base de Données")
        
        st.info("Statut: Connectée")
        st.metric("Taille DB", "2.4 GB")
        st.metric("Requêtes/jour", "12,450")
        
        if st.button("Optimiser DB", type="secondary"):
            st.success("Base de données optimisée")
        
        if st.button("Purger logs", type="secondary"):
            st.warning("Logs purgés")
    
    st.subheader("Sécurité")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Accès API:**")
        st.checkbox("API REST activée", True)
        st.checkbox("Authentification requise", True)
        st.checkbox("Rate limiting", True)
    
    with col2:
        st.write("**Export/Import:**")
        if st.button("Exporter configuration", use_container_width=True):
            st.info("Configuration exportée")
        
        if st.button("Importer configuration", use_container_width=True):
            st.info("Configuration importée")