import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Plateforme d'Optimisation - Version Simplifiée",
    page_icon="📅",
    layout="wide"
)

st.title("Plateforme d'Optimisation des Examens")
st.markdown("*Version simplifiée - Démonstration*")
st.markdown("---")

# URL de l'API
API_URL = "http://localhost:5000"

def test_api():
    """Teste la connexion à l'API"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "API connectée"
        else:
            return False, f"API erreur: {response.status_code}"
    except Exception as e:
        return False, f"API inaccessible: {str(e)}"

# Vérifier l'API
st.header("État du système")
status_ok, status_msg = test_api()
st.info(status_msg)

if status_ok:
    # Menu principal
    st.subheader("Menu Principal")
    
    option = st.selectbox(
        "Choisissez une action:",
        ["Voir les départements", "Voir les examens", "Générer un emploi du temps"]
    )
    
    if option == "Voir les départements":
        st.subheader("Liste des départements")
        
        try:
            response = requests.get(f"{API_URL}/departements", timeout=10)
            if response.status_code == 200:
                departements = response.json()
                if departements:
                    df = pd.DataFrame(departements)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.metric("Nombre de départements", len(departements))
                else:
                    st.warning("Aucun département trouvé")
            else:
                st.error(f"Erreur: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur: {str(e)}")
    
    elif option == "Voir les examens":
        st.subheader("Examen de démonstration")
        
        # Données de démonstration (simulées)
        examens_demo = [
            {"date": "2024-01-15", "module": "Base de données", "salle": "Amphi A", "prof": "Pierre Martin"},
            {"date": "2024-01-15", "module": "Algorithmique", "salle": "Amphi B", "prof": "Marie Dubois"},
            {"date": "2024-01-16", "module": "Analyse Math", "salle": "Salle 101", "prof": "Jean Leroy"},
        ]
        
        df = pd.DataFrame(examens_demo)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Graphique simple
        st.subheader("Répartition par jour")
        chart_data = pd.DataFrame({
            'Jour': ['15/01', '16/01', '17/01'],
            'Nombre d\'examens': [2, 1, 0]
        })
        st.bar_chart(chart_data.set_index('Jour'))
    
    elif option == "Générer un emploi du temps":
        st.subheader("Génération d'emploi du temps (Démo)")
        
        col1, col2 = st.columns(2)
        with col1:
            date_debut = st.date_input("Date de début", datetime(2024, 1, 15))
        with col2:
            date_fin = st.date_input("Date de fin", datetime(2024, 1, 20))
        
        if st.button("Générer (Démo)", type="primary"):
            st.success(f"Emploi du temps généré du {date_debut} au {date_fin}")
            
            # Résultats simulés
            st.info("**Résultats simulés (démonstration):**")
            
            results = pd.DataFrame({
                'Date': ['2024-01-15', '2024-01-15', '2024-01-16'],
                'Heure': ['09:00', '14:00', '09:00'],
                'Module': ['Base de données', 'Algorithmique', 'Physique'],
                'Salle': ['Amphi A', 'Amphi B', 'Salle 101'],
                'Professeur': ['P. Martin', 'M. Dubois', 'S. Petit']
            })
            
            st.dataframe(results, use_container_width=True, hide_index=True)
            
            st.metric("Examens générés", 3)
            st.metric("Conflits détectés", 0)
            st.metric("Temps de génération", "0.5s")

else:
    st.error("""
    ## L'API n'est pas accessible
    
    **Instructions de dépannage:**
    
    1. **Vérifiez que l'API est démarrée:**
       ```bash
       # Dans un terminal:
       cd ~/Project/Exam_Schedule_Optimizer/backend
       python api_simple.py
       ```
    
    2. **Vérifiez les ports:**
       ```bash
       sudo lsof -i :5000
       ```
    
    3. **Tuez les processus existants:**
       ```bash
       pkill -f "python api"
       ```
    
    4. **Redémarrez l'API:**
       ```bash
       cd ~/Project/Exam_Schedule_Optimizer/backend
       python api_simple.py
       ```
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Plateforme d'Optimisation des Emplois du Temps d'Examens • Version Démo</p>
        <p>Contact: support@exam-optimizer.univ.fr</p>
    </div>
    """,
    unsafe_allow_html=True
)