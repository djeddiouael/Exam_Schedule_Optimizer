import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Configuration de la page
st.set_page_config(
    page_title="Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    .role-card {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header"> Plateforme d\'Optimisation des Emplois du Temps d\'Examens Universitaires</h1>', unsafe_allow_html=True)
st.markdown("---")

# Configuration
API_URL = "http://localhost:5000"

# Fonction pour vérifier l'API
def check_api():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Sidebar avec sélection de rôle
with st.sidebar:
    # st.image("https://img.icons8.com/color/96/000000/calendar--v1.png", width=80)
    
    st.markdown("###  Sélection du Rôle")
    role = st.selectbox(
        "Choisissez votre rôle:",
        [" Étudiant/Professeur", " Chef de Département", " Administrateur Examens", " Vice-doyen/Doyen"],
        index=3
    )
    
    st.markdown("---")
    st.markdown("###  Navigation")
    
    # Navigation selon le rôle
    if role == " Étudiant/Professeur":
        menu = st.radio("Menu", [" Planning Personnel"])
    elif role == " Chef de Département":
        menu = st.radio("Menu", [" Dashboard Département"])
    elif role == " Administrateur Examens":
        menu = st.radio("Menu", [" Génération Automatique"])
    elif role == " Vice-doyen/Doyen":
        menu = st.radio("Menu", [" Vue Stratégique"])
    
    st.markdown("---")
    
    # Informations système
    if check_api():
        st.success(" API Connectée")
    else:
        st.error(" API Déconnectée")
    
    st.markdown(f"**Rôle actuel:** {role}")
    st.markdown(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
    st.markdown(f"**Version:** 2.0.0")

# Contenu principal selon le rôle et le menu
if role == " Vice-doyen/Doyen" and menu == " Vue Stratégique":
    st.markdown('<h2 class="sub-header"> Vue Stratégique Globale</h2>', unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(" Étudiants", "13,200", "+320")
    with col2:
        st.metric(" Départements", "7", "0")
    with col3:
        st.metric(" Formations", "210", "+5")
    with col4:
        st.metric(" Examens Planifiés", "1,850", "+120")
    
    st.markdown("---")
    
    # Section 1: Occupation des ressources
    st.markdown('<h3 class="sub-header"> Occupation des Salles et Amphis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique occupation salles
        data_salles = {
            'Type': ['Amphis', 'Salles < 20', 'Labos', 'Salles spéciales'],
            'Occupation %': [85, 92, 78, 65],
            'Capacité Moyenne': [300, 18, 25, 30]
        }
        df_salles = pd.DataFrame(data_salles)
        
        fig1 = px.bar(df_salles, x='Type', y='Occupation %',
                     title="Taux d\'Occupation par Type de Salle",
                     color='Occupation %',
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Top 5 salles les plus utilisées
        data_top_salles = {
            'Salle': ['Amphi A', 'Amphi B', 'Salle 101', 'Lab Info 1', 'Salle 201'],
            'Examens': [45, 38, 42, 35, 28],
            'Taux Utilisation': [92, 88, 95, 82, 75]
        }
        df_top = pd.DataFrame(data_top_salles)
        
        fig2 = px.bar(df_top, x='Salle', y='Taux Utilisation',
                     title="Top 5 Salles - Taux d\'Utilisation",
                     color='Examens',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Section 2: Taux de conflits
    st.markdown('<h3 class="sub-header"> Taux de Conflits par Département</h3>', unsafe_allow_html=True)
    
    data_conflits = {
        'Département': ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Économie', 'Droit'],
        'Conflits': [12, 8, 5, 3, 6, 9, 4],
        'Examens': [320, 280, 190, 150, 210, 260, 180],
        'Taux Conflits %': [3.8, 2.9, 2.6, 2.0, 2.9, 3.5, 2.2]
    }
    df_conflits = pd.DataFrame(data_conflits)
    df_conflits['Conflits/100 Examens'] = df_conflits['Conflits'] / df_conflits['Examens'] * 100
    
    fig3 = px.scatter(df_conflits, x='Examens', y='Conflits',
                     size='Taux Conflits %', color='Département',
                     title="Conflits vs Nombre d\'Examens par Département",
                     hover_data=['Taux Conflits %'])
    st.plotly_chart(fig3, use_container_width=True)
    
    # Section 3: KPIs académiques
    st.markdown('<h3 class="sub-header"> KPIs Académiques</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(" Heures Professeurs", "12,850h", "3.2%")
        st.caption("Total heures de surveillance")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(" Taux Salles Utilisées", "78%", "1.5%")
        st.caption("Salles utilisées / Salles disponibles")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(" Satisfaction", "92%", "2.1%")
        st.caption("Enquête satisfaction professeurs")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Calendrier global
    st.markdown('<h3 class="sub-header"> Calendrier Global des Examens</h3>', unsafe_allow_html=True)
    
    dates = pd.date_range(start='2024-01-15', end='2024-02-15', freq='D')
    data_calendar = []
    
    for date in dates:
        day_type = "Weekend" if date.weekday() >= 5 else "Semaine"
        exams = 0
        if date.weekday() < 5:
            exams = random.randint(15, 40)
        
        data_calendar.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Jour': date.strftime('%A'),
            'Examens': exams,
            'Type Jour': day_type
        })
    
    df_calendar = pd.DataFrame(data_calendar)
    
    fig4 = px.line(df_calendar, x='Date', y='Examens',
                  title="Évolution du Nombre d\'Examens par Jour",
                  markers=True)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Section 5: Validation finale
    st.markdown('<h3 class="sub-header"> Validation Finale de l\'Emploi du Temps</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Statut de validation:** En attente")
        st.progress(75)
        
        st.write("**Départements validés:**")
        departements_valides = ['Informatique ✓', 'Mathématiques ✓', 'Physique ✓', 'Chimie ✓']
        for dept in departements_valides:
            st.write(f"- {dept}")
        
        st.write("**Départements en attente:**")
        departements_attente = ['Biologie', 'Économie', 'Droit']
        for dept in departements_attente:
            st.write(f"- {dept}")
    
    with col2:
        if st.button(" Valider l\'Emploi du Temps Global", type="primary"):
            st.success("Emploi du temps validé avec succès!")
            st.balloons()
        
        if st.button(" Renvoyer pour Modification", type="secondary"):
            st.warning("Emploi du temps renvoyé pour modifications")
        
        st.download_button(
            label=" Télécharger le Rapport Complet",
            data=df_calendar.to_csv(index=False),
            file_name="rapport_global_examens.csv",
            mime="text/csv"
        )

elif role == " Administrateur Examens" and menu == "⚡ Génération Automatique":
    st.markdown('<h2 class="sub-header">⚡ Génération Automatique d\'Emploi du Temps</h2>', unsafe_allow_html=True)
    
    # Paramètres de génération
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Période d\'Examens")
        date_debut = st.date_input("Date de début", datetime(2024, 1, 15))
        date_fin = st.date_input("Date de fin", datetime(2024, 1, 31))
        
        jours = (date_fin - date_debut).days
        st.info(f"Période: {jours} jours")
    
    with col2:
        st.markdown("###  Paramètres d\'Optimisation")
        
        st.slider(" Taille de la population", 50, 500, 100, help="Taille de la population pour l\'algorithme génétique")
        st.slider(" Nombre de générations", 10, 200, 50, help="Nombre d\'itérations pour l\'optimisation")
        st.number_input("⏱ Timeout (secondes)", 30, 300, 45, help="Temps maximum d\'exécution")
    
    st.markdown("---")
    
    # Contraintes
    st.markdown('<h3 class="sub-header"> Contraintes à Appliquer</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox(" Étudiants: Max 1 examen/jour", True)
        st.checkbox(" Professeurs: Max 3 examens/jour", True)
        st.checkbox(" Salles: Respect capacité", True)
    
    with col2:
        st.checkbox(" Priorité département", True)
        st.checkbox(" Équité surveillances", True)
        st.checkbox(" Pas d\'examen le weekend", False)
    
    with col3:
        st.checkbox(" Respect pré-requis", True)
        st.checkbox(" Pause déjeuner (12h-14h)", True)
        st.checkbox(" Pas d\'examen après 18h", True)
    
    st.markdown("---")
    
    # Bouton de génération
    if st.button(" Lancer la Génération Automatique", type="primary", use_container_width=True):
        with st.spinner(" Génération en cours... Objectif: < 45 secondes"):
            # Simulation de génération
            import time
            progress_bar = st.progress(0)
            
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.02)
            
            # Résultats simulés
            st.success(" Génération terminée en 42 secondes!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(" Examens planifiés", "1,240")
            with col2:
                st.metric(" Conflits résolus", "156")
            with col3:
                st.metric(" Salles utilisées", "38")
            
            # Détails de la génération
            with st.expander(" Détails de la génération"):
                st.write("""
                **Paramètres utilisés:**
                - Population: 100 individus
                - Générations: 50
                - Taux de mutation: 0.1
                - Taux de croisement: 0.8
                
                **Performances:**
                - Temps total: 42 secondes
                - Score final: 0.94/1.00
                - Conflits initiaux: 210
                - Conflits résolus: 156
                
                **Ressources utilisées:**
                - CPU: 23%
                - Mémoire: 450MB
                - Requêtes DB: 1,240
                """)
            
            # Téléchargement des résultats
            st.download_button(
                label=" Télécharger l\'emploi du temps (CSV)",
                data=pd.DataFrame({'test': [1, 2, 3]}).to_csv(index=False),
                file_name=f"emploi_du_temps_{date_debut}_{date_fin}.csv",
                mime="text/csv"
            )

elif role == " Chef de Département" and menu == " Dashboard Département":
    st.markdown('<h2 class="sub-header"> Dashboard Département - Informatique</h2>', unsafe_allow_html=True)
    
    # Sélection du département
    departement = st.selectbox("Sélectionnez votre département:", 
                              ["Informatique", "Mathématiques", "Physique", "Chimie", "Biologie", "Économie", "Droit"])
    
    # Métriques département
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(" Étudiants", "2,150", "+85")
    with col2:
        st.metric(" Formations", "28", "+2")
    with col3:
        st.metric(" Examens", "320", "+25")
    with col4:
        st.metric(" Conflits", "12", "-3")
    
    st.markdown("---")
    
    # Graphiques département
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition des examens par formation
        data_formations = {
            'Formation': ['Licence Info', 'Master DS', 'Master AI', 'Licence Pro', 'Master SE'],
            'Examens': [85, 64, 52, 48, 71],
            'Étudiants': [450, 180, 120, 90, 210]
        }
        df_formations = pd.DataFrame(data_formations)
        
        fig = px.pie(df_formations, values='Examens', names='Formation',
                    title=f"Répartition des Examens - {departement}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Occupation des salles du département
        data_salles_dept = {
            'Salle': ['Amphi A', 'Salle 101', 'Salle 102', 'Lab Info 1', 'Lab Info 2'],
            'Occupation %': [88, 92, 85, 78, 82],
            'Examens': [45, 38, 32, 28, 24]
        }
        df_salles_dept = pd.DataFrame(data_salles_dept)
        
        fig = px.bar(df_salles_dept, x='Salle', y='Occupation %',
                    title=f"Occupation des Salles - {departement}",
                    color='Examens')
        st.plotly_chart(fig, use_container_width=True)
    
    # Liste des conflits du département
    st.markdown('<h3 class="sub-header"> Conflits à Résoudre</h3>', unsafe_allow_html=True)
    
    conflits_data = {
        'Type': ['Salle', 'Professeur', 'Étudiant', 'Capacité', 'Équipement'],
        'Nombre': [5, 3, 2, 1, 1],
        'Priorité': ['Haute', 'Haute', 'Moyenne', 'Basse', 'Moyenne']
    }
    df_conflits_dept = pd.DataFrame(conflits_data)
    
    st.dataframe(df_conflits_dept, use_container_width=True)
    
    # Validation département
    st.markdown('<h3 class="sub-header">Validation du Département</h3>', unsafe_allow_html=True)
    
    if st.button(f" Valider l\'Emploi du Temps - {departement}", type="primary"):
        st.success(f"Emploi du temps validé pour le département {departement}!")
    
    if st.button(" Demander des Modifications", type="secondary"):
        st.warning("Demande de modifications envoyée à l\'administrateur")

elif role == " Étudiant/Professeur" and menu == " Planning Personnel":
    st.markdown('<h2 class="sub-header"> Planning Personnel</h2>', unsafe_allow_html=True)
    
    # Simulation de connexion
    col1, col2 = st.columns(2)
    
    with col1:
        type_utilisateur = st.radio("Je suis:", ["Étudiant", "Professeur"])
    
    with col2:
        if type_utilisateur == "Étudiant":
            matricule = st.text_input("Numéro d\'étudiant", "E2023001")
        else:
            matricule = st.text_input("Identifiant professeur", "P2023001")
    
    if st.button(" Charger mon planning", type="primary"):
        # Données simulées
        if type_utilisateur == "Étudiant":
            st.success(f"Planning chargé pour l\'étudiant {matricule}")
            
            planning_data = {
                'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
                'Heure': ['09:00', '14:00', '09:00', '14:00', '09:00'],
                'Module': ['Base de données', 'Algorithmique', 'Réseaux', 'Systèmes', 'IA'],
                'Salle': ['Amphi A', 'Salle 101', 'Amphi B', 'Lab Info 1', 'Salle 102'],
                'Durée': ['3h', '2h', '3h', '2h', '3h'],
                'Type': ['Écrit', 'Oral', 'Écrit', 'Pratique', 'Écrit']
            }
        else:
            st.success(f"Planning chargé pour le professeur {matricule}")
            
            planning_data = {
                'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
                'Heure': ['09:00', '14:00', '09:00', 'Toute la journée', '09:00'],
                'Module': ['Base de données', 'Algorithmique', 'Surveillance', 'Réunion', 'IA'],
                'Salle': ['Amphi A', 'Salle 101', 'Amphi B', 'Bureau 201', 'Salle 102'],
                'Durée': ['3h', '2h', '3h', '8h', '3h'],
                'Type': ['Enseignement', 'Enseignement', 'Surveillance', 'Réunion', 'Enseignement']
            }
        
        df_planning = pd.DataFrame(planning_data)
        st.dataframe(df_planning, use_container_width=True)
        
        # Export du planning
        st.download_button(
            label=" Télécharger mon planning (ICS)",
            data="BEGIN:VCALENDAR\nEND:VCALENDAR",
            file_name=f"planning_{matricule}.ics",
            mime="text/calendar"
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p><strong>Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires</strong></p>
        <p> Plus de 13,000 étudiants • 7 départements • 200+ formations • Génération en < 45s</p>
        <p> Contact: support@exam-optimizer.univ.fr • 📞 +33 1 23 45 67 89</p>
    </div>
    """,
    unsafe_allow_html=True
)