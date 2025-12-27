import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chef de Département", page_icon="👨‍🏫", layout="wide")

st.title("👨‍🏫 Dashboard Chef de Département")
st.markdown("---")

# Sélection du département
departement = st.selectbox(
    "Sélectionnez votre département:",
    ["Informatique", "Mathématiques", "Physique", "Chimie", "Biologie", "Économie", "Droit"],
    index=0
)

st.markdown(f"### 📊 Dashboard - Département {departement}")

# Métriques département
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎓 Étudiants", "2,150", "+85")
with col2:
    st.metric("📚 Formations", "28", "+2")
with col3:
    st.metric("📅 Examens", "320", "+25")
with col4:
    st.metric("⚠️ Conflits", "12", "-3")

st.markdown("---")

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["📈 Statistiques", "✅ Validation", "⚠️ Conflits", "👥 Équipe"])

with tab1:
    st.header(f"📈 Statistiques - {departement}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par formation
        data_formations = {
            'Formation': ['Licence Info', 'Master DS', 'Master IA', 'Licence Pro', 'Master SE'],
            'Examens': [85, 64, 52, 48, 71],
            'Étudiants': [450, 180, 120, 90, 210]
        }
        df_formations = pd.DataFrame(data_formations)
        
        fig = px.pie(df_formations, values='Examens', names='Formation',
                    title=f"Répartition des Examens - {departement}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Évolution mensuelle
        data_evolution = {
            'Mois': ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
            'Examens': [120, 150, 180, 210, 280, 320],
            'Conflits': [8, 10, 12, 15, 18, 12]
        }
        df_evolution = pd.DataFrame(data_evolution)
        
        fig = px.line(df_evolution, x='Mois', y=['Examens', 'Conflits'],
                     title=f"Évolution - {departement}",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Détails des formations
    st.subheader("📋 Détails par Formation")
    
    formations_data = {
        'Formation': ['Licence Informatique', 'Master Data Science', 'Master IA', 'Licence Pro Dev Web'],
        'Modules': [8, 6, 6, 7],
        'Étudiants': [450, 180, 120, 90],
        'Examens': [85, 64, 52, 48],
        'Conflits': [4, 2, 3, 1]
    }
    df_formations_det = pd.DataFrame(formations_data)
    st.dataframe(df_formations_det, use_container_width=True)

with tab2:
    st.header(f"✅ Validation - {departement}")
    
    st.info("**Statut de validation du département**")
    
    # Liste des formations à valider
    formations = [
        {"nom": "Licence Informatique", "statut": "✓ Validée", "responsable": "Prof. Martin", "date": "15/01"},
        {"nom": "Master Data Science", "statut": "⏳ En attente", "responsable": "Prof. Dubois", "date": "-"},
        {"nom": "Master IA", "statut": "✓ Validée", "responsable": "Prof. Leroy", "date": "16/01"},
        {"nom": "Licence Pro Dev Web", "statut": "❌ À corriger", "responsable": "Prof. Petit", "date": "14/01"}
    ]
    
    for formation in formations:
        col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
        with col1:
            st.write(f"**{formation['nom']}**")
        with col2:
            st.write(formation['statut'])
        with col3:
            st.write(formation['responsable'])
        with col4:
            st.write(formation['date'])
        st.markdown("---")
    
    # Actions de validation
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"✅ Valider tout {departement}", type="primary", use_container_width=True):
            st.success(f"Département {departement} validé avec succès!")
    
    with col2:
        if st.button("🔄 Demander modifications", type="secondary", use_container_width=True):
            st.warning("Demande de modifications envoyée")

with tab3:
    st.header(f"⚠️ Conflits - {departement}")
    
    st.subheader("Conflits par Formation")
    
    conflits_data = {
        'Formation': ['Licence Info', 'Master DS', 'Master IA', 'Licence Pro'],
        'Conflits Salles': [3, 1, 2, 0],
        'Conflits Profs': [1, 0, 1, 1],
        'Conflits Étudiants': [0, 1, 0, 0],
        'Total': [4, 2, 3, 1]
    }
    df_conflits_form = pd.DataFrame(conflits_data)
    
    fig = px.bar(df_conflits_form, x='Formation', y=['Conflits Salles', 'Conflits Profs', 'Conflits Étudiants'],
                title="Répartition des Conflits par Type",
                barmode='stack')
    st.plotly_chart(fig, use_container_width=True)
    
    # Détails des conflits
    st.subheader("📋 Liste détaillée des Conflits")
    
    details_conflits = {
        'ID': [101, 102, 103, 104],
        'Type': ['Salle', 'Professeur', 'Étudiant', 'Capacité'],
        'Formation': ['Licence Info', 'Master DS', 'Licence Info', 'Master IA'],
        'Description': ['Salle déjà occupée', 'Prof double affectation', 'Étudiant double examen', 'Capacité insuffisante'],
        'Priorité': ['Haute', 'Moyenne', 'Haute', 'Basse'],
        'Statut': ['⏳ En cours', '✅ Résolu', '⏳ En cours', '✅ Résolu']
    }
    df_details = pd.DataFrame(details_conflits)
    st.dataframe(df_details, use_container_width=True)

with tab4:
    st.header(f"👥 Équipe - {departement}")
    
    # Liste des professeurs
    profs_data = {
        'Professeur': ['Pierre Martin', 'Marie Dubois', 'Jean Leroy', 'Sophie Petit', 'Luc Garcia'],
        'Spécialité': ['BDD', 'Algorithmique', 'Analyse', 'Physique', 'Chimie'],
        'Examens': [12, 10, 8, 15, 9],
        'Heures': [36, 30, 24, 45, 27],
        'Disponibilité': ['Disponible', 'Congés', 'Disponible', 'Limitée', 'Disponible']
    }
    df_profs = pd.DataFrame(profs_data)
    
    st.dataframe(df_profs, use_container_width=True)
    
    # Répartition des surveillances
    st.subheader("⏰ Répartition des Surveillances")
    
    fig = px.pie(df_profs, values='Examens', names='Professeur',
                title="Répartition des surveillances")
    st.plotly_chart(fig, use_container_width=True)
    
    # Messagerie interne
    st.subheader("💬 Messagerie Interne")
    
    message = st.text_area("Message à l'équipe:", "Bonjour l'équipe, ...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Envoyer à l'équipe", type="primary"):
            st.success("Message envoyé!")
    with col2:
        if st.button("📅 Planifier réunion", type="secondary"):
            st.info("Réunion planifiée")
