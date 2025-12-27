import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Planning Personnel", page_icon="👨‍🎓", layout="wide")

st.title("👨‍🎓 Planning Personnel")
st.markdown("---")

# Sélection du type d'utilisateur
user_type = st.radio(
    "Je suis:",
    ["🎓 Étudiant", "👨‍🏫 Professeur"],
    horizontal=True
)

# Formulaire de connexion
col1, col2 = st.columns(2)

with col1:
    if user_type == "🎓 Étudiant":
        identifiant = st.text_input("Numéro étudiant:", "E2023001")
        nom_complet = st.text_input("Nom complet:", "Jean Dupont")
        formation = st.selectbox("Formation:", ["Licence Informatique", "Master Data Science", "Licence Mathématiques"])
    else:
        identifiant = st.text_input("Identifiant professeur:", "P2023001")
        nom_complet = st.text_input("Nom complet:", "Prof. Pierre Martin")
        departement = st.selectbox("Département:", ["Informatique", "Mathématiques", "Physique"])

with col2:
    periode = st.selectbox(
        "Période à afficher:",
        ["Semaine actuelle", "Mois actuel", "Semestre", "Période personnalisée"]
    )
    
    if periode == "Période personnalisée":
        date_debut = st.date_input("Du:", datetime.now())
        date_fin = st.date_input("Au:", datetime.now() + timedelta(days=7))

if st.button("🔍 Charger mon planning", type="primary", use_container_width=True):
    st.success(f"Planning chargé pour {nom_complet}")
    
    # Données de démonstration
    if user_type == "🎓 Étudiant":
        st.markdown(f"### 📚 Planning de {nom_complet} - {formation}")
        
        planning_data = {
            'Date': ['2024-01-15', '2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18'],
            'Jour': ['Lundi', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi'],
            'Heure': ['09:00 - 12:00', '14:00 - 16:00', '09:00 - 12:00', '14:00 - 17:00', '09:00 - 11:00'],
            'Module': ['Base de données', 'Algorithmique', 'Réseaux', 'Systèmes d\'exploitation', 'IA'],
            'Type': ['Écrit', 'Oral', 'Écrit', 'Pratique', 'Écrit'],
            'Salle': ['Amphi A', 'Salle 101', 'Amphi B', 'Lab Info 1', 'Salle 102'],
            'Professeur': ['P. Martin', 'M. Dubois', 'J. Leroy', 'S. Petit', 'L. Garcia']
        }
        
        st.info(f"📊 **Statistiques de la période:** 5 examens • 15h de présence • Moyenne: 3h/jour")
    
    else:  # Professeur
        st.markdown(f"### 👨‍🏫 Planning de {nom_complet} - Département {departement}")
        
        planning_data = {
            'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
            'Jour': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'],
            'Heure': ['09:00 - 12:00', '14:00 - 17:00', 'Toute la journée', '09:00 - 11:00', '14:00 - 16:00'],
            'Activité': ['Examen: Base de données', 'Surveillance: Algorithmique', 'Réunion département', 'Examen: Réseaux', 'Correction copies'],
            'Type': ['Enseignement', 'Surveillance', 'Réunion', 'Enseignement', 'Correction'],
            'Lieu': ['Amphi A', 'Salle 101', 'Bureau 201', 'Amphi B', 'Bureau personnel'],
            'Participants': ['45 étudiants', '38 étudiants', 'Équipe département', '42 étudiants', 'Individuel']
        }
        
        st.info(f"📊 **Statistiques de la période:** 8 activités • 25h de présence • 3 examens à surveiller")
    
    # Affichage du planning
    df_planning = pd.DataFrame(planning_data)
    
    # Version tableau
    st.subheader("📋 Vue Tableau")
    st.dataframe(df_planning, use_container_width=True, hide_index=True)
    
    # Version calendrier
    st.subheader("📅 Vue Calendrier")
    
    for index, row in df_planning.iterrows():
        with st.expander(f"{row['Date']} - {row['Jour']} | {row['Heure']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Activité:** {row['Module' if user_type == '🎓 Étudiant' else 'Activité']}")
                st.write(f"**Type:** {row['Type']}")
                st.write(f"**Lieu:** {row['Salle' if user_type == '🎓 Étudiant' else 'Lieu']}")
            with col2:
                if user_type == "🎓 Étudiant":
                    st.write(f"**Professeur:** {row['Professeur']}")
                    st.write(f"**Durée:** {row['Heure'].split(' - ')[1]}")
                else:
                    st.write(f"**Participants:** {row['Participants']}")
    
    # Options d'export
    st.markdown("---")
    st.subheader("📤 Export du Planning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df_planning.to_csv(index=False)
        st.download_button(
            label="📥 CSV",
            data=csv,
            file_name=f"planning_{identifiant}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Générer un ICS simple
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Examen Test
DTSTART:20240115T090000
DTEND:20240115T120000
LOCATION:Amphi A
END:VEVENT
END:VCALENDAR"""
        
        st.download_button(
            label="📅 iCalendar",
            data=ics_content,
            file_name=f"planning_{identifiant}.ics",
            mime="text/calendar",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            label="📄 PDF",
            data=df_planning.to_json(),
            file_name=f"planning_{identifiant}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    # Fonctionnalités supplémentaires
    st.markdown("---")
    st.subheader("🔔 Notifications et Alertes")
    
    if user_type == "🎓 Étudiant":
        notifications = [
            "📢 **Examen BD:** Rappel pour le 15/01 à 9h en Amphi A",
            "⚠️ **Conflit détecté:** Vérifiez vos examens du 16/01",
            "✅ **Inscription confirmée:** Examen Réseaux du 17/01"
        ]
    else:
        notifications = [
            "📢 **Réunion département:** 17/01 toute la journée",
            "⚠️ **Surveillance supplémentaire:** À attribuer pour le 18/01",
            "✅ **Corrections:** À rendre avant le 22/01"
        ]
    
    for notification in notifications:
        st.write(notification)
    
    # Filtres
    st.markdown("---")
    st.subheader("🔍 Filtres")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox("Afficher seulement les examens", True)
        st.checkbox("Afficher les surveillances", True)
    
    with col2:
        st.checkbox("Afficher les réunions", True)
        st.checkbox("Afficher les corrections", False)
    
    with col3:
        st.checkbox("Alertes par email", True)
        st.checkbox("Notifications push", True)

# Section d'aide
with st.expander("❓ Aide et Support"):
    st.write("""
    **Pour les étudiants:**
    - Vérifiez toujours la salle et l'horaire de vos examens
    - Signalez tout conflit d'horaire immédiatement
    - Consultez régulièrement les mises à jour
    
    **Pour les professeurs:**
    - Confirmez vos disponibilités de surveillance
    - Signalez vos absences au moins 48h à l'avance
    - Vérifiez les équipements nécessaires pour vos examens
    
    **Support technique:**
    - Email: support-etudiants@univ.fr
    - Téléphone: 01 23 45 67 89
    - Bureau: Bâtiment A, Salle 101
    """)
